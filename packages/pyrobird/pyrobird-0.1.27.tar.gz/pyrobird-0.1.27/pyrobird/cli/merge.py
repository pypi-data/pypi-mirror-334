import json
import os
import click
import logging
import sys

# Configure logging
logger = logging.getLogger(__name__)

@click.command()
@click.option('-r', '--reset-id', is_flag=True, help='Reset entry IDs to sequential numbers (0,1,2...)')
@click.option('-i', '--ignore', is_flag=True, help='Ignore duplicate component names from right files')
@click.option('-o', '--overwrite', is_flag=True, help='Overwrite duplicate component names from left files')
@click.option('-O', '--output', 'output_file', help='Output file name for the merged result')
@click.argument('input_files', nargs=-1, required=True)
def merge(reset_id, ignore, overwrite, output_file, input_files):
    """
    Merge multiple Firebird DEX JSON files.

    This command merges entries from multiple Firebird DEX JSON files based on their IDs.
    Components with the same name in different files are handled according to specified flags.

    By default, the command fails if duplicate component names are found.

    Examples:
      - Merge two files with default behavior (fail on duplicate components):
          pyrobird merge file1.firebird.json file2.firebird.json

      - Merge multiple files, resetting entry IDs to sequential numbers:
          pyrobird merge --reset-id file1.firebird.json file2.firebird.json file3.firebird.json

      - Merge two files, ignoring duplicate components from the second file:
          pyrobird merge --ignore file1.firebird.json file2.firebird.json

      - Merge two files, overwriting duplicate components from the first file:
          pyrobird merge --overwrite file1.firebird.json file2.firebird.json

      - Save merged result to a specific file:
          pyrobird merge --output merged.firebird.json file1.firebird.json file2.firebird.json
    """
    # Check that we have at least two files
    if len(input_files) < 2:
        raise click.UsageError("At least two input files are required for merging.")

    # Check that both ignore and overwrite are not set simultaneously
    if ignore and overwrite:
        raise click.UsageError("--ignore and --overwrite flags cannot be used together.")

    # Initialize with the first file
    try:
        with open(input_files[0], 'r') as f:
            merged_data = json.load(f)
    except FileNotFoundError:
        raise click.FileError(input_files[0], "File not found")
    except json.JSONDecodeError:
        raise click.FileError(input_files[0], "Invalid JSON format")
    except Exception as e:
        raise click.FileError(input_files[0], f"Error opening/parsing: {e}")

    # Verify the first file is a valid Firebird DEX file
    if not _is_valid_dex_file(merged_data):
        raise click.FileError(input_files[0], "Not a valid Firebird DEX file.")

    # Process remaining files
    for file_path in input_files[1:]:
        try:
            with open(file_path, 'r') as f:
                current_data = json.load(f)
        except FileNotFoundError:
            raise click.FileError(file_path, "File not found")
        except json.JSONDecodeError:
            raise click.FileError(file_path, "Invalid JSON format")
        except Exception as e:
            raise click.FileError(file_path, f"Error opening/parsing file: {e}")

        # Verify the current file is a valid Firebird DEX file
        if not _is_valid_dex_file(current_data):
            raise click.FileError(file_path, "Not a valid Firebird DEX file.")

        # Merge the files
        try:
            merged_data = _merge_dex_files(merged_data, current_data, reset_id, ignore, overwrite, file_path)
        except ValueError as e:
            raise click.ClickException(str(e))
        except Exception as e:
            raise click.ClickException(f"Error merging file {file_path}: {e}")

    # Save the merged result
    if output_file:
        try:
            with open(output_file, 'w') as f:
                json.dump(merged_data, f, indent=2)
            logger.info(f"Merged data saved to {output_file}")
        except Exception as e:
            raise click.FileError(output_file, f"Error saving merged data: {e}")
    else:
        # Output to stdout
        print(json.dumps(merged_data, indent=2))

def _is_valid_dex_file(data):
    """Check if the data is a valid Firebird DEX file."""
    # Check for required fields
    if "version" not in data or "entries" not in data:
        return False

    # Check if entries is a list
    if not isinstance(data["entries"], list):
        return False

    # Check each entry
    for entry in data["entries"]:
        if "id" not in entry or "components" not in entry:
            return False

        # Check if components is a list
        if not isinstance(entry["components"], list):
            return False

        # Check each component
        for component in entry["components"]:
            if "name" not in component or "type" not in component:
                return False

    return True

def _merge_dex_files(left_data, right_data, reset_id, ignore, overwrite, right_file_path):
    """
    Merge two Firebird DEX files.

    Args:
        left_data: The first file's data (will be modified in-place)
        right_data: The second file's data
        reset_id: Whether to reset entry IDs to sequential numbers
        ignore: Whether to ignore duplicate components from the right file
        overwrite: Whether to overwrite duplicate components in the left file
        right_file_path: Path to the right file (for error messages)

    Returns:
        The merged data

    Raises:
        ValueError: If duplicate component names are found and neither ignore nor overwrite is set
    """
    if reset_id:
        # Reset entry IDs in both data structures
        for i, entry in enumerate(left_data["entries"]):
            entry["id"] = i

        for i, entry in enumerate(right_data["entries"]):
            entry["id"] = i

    # Create dictionaries of entries by ID for efficient lookup
    left_entries_by_id = {entry["id"]: entry for entry in left_data["entries"]}
    right_entries_by_id = {entry["id"]: entry for entry in right_data["entries"]}

    # Collect all entry IDs from both files
    all_entry_ids = set(left_entries_by_id.keys()) | set(right_entries_by_id.keys())

    # Create a new entries list for the merged result
    merged_entries = []

    # Process each entry ID
    for entry_id in sorted(all_entry_ids, key=lambda x: (isinstance(x, (int, float)), x)):
        left_entry = left_entries_by_id.get(entry_id)
        right_entry = right_entries_by_id.get(entry_id)

        # Cases:
        # 1. Entry exists only in left file: add it to merged result
        # 2. Entry exists only in right file: add it to merged result
        # 3. Entry exists in both files: merge components

        if left_entry and not right_entry:
            merged_entries.append(left_entry)
        elif right_entry and not left_entry:
            merged_entries.append(right_entry)
        else:  # Entry exists in both files
            # Create a new entry with the same ID
            merged_entry = {"id": entry_id, "components": []}

            # Get components from both entries
            left_components_by_name = {comp["name"]: comp for comp in left_entry["components"]}
            right_components_by_name = {comp["name"]: comp for comp in right_entry["components"]}

            # Check for duplicate component names
            duplicate_names = set(left_components_by_name.keys()) & set(right_components_by_name.keys())

            if duplicate_names and not (ignore or overwrite):
                # Default behavior: fail with detailed error
                error_msg = f"Duplicate component names found in entry ID '{entry_id}': {list(duplicate_names)}. "
                error_msg += f"File: {right_file_path}. "
                error_msg += "Use --ignore (-i) or --overwrite (-o) flags to handle duplicates."
                raise ValueError(error_msg)

            # Handle components based on flags
            all_component_names = set(left_components_by_name.keys()) | set(right_components_by_name.keys())

            for comp_name in all_component_names:
                left_comp = left_components_by_name.get(comp_name)
                right_comp = right_components_by_name.get(comp_name)

                if left_comp and not right_comp:
                    # Component only in left file
                    merged_entry["components"].append(left_comp)
                elif right_comp and not left_comp:
                    # Component only in right file
                    merged_entry["components"].append(right_comp)
                else:  # Component in both files
                    if ignore:
                        # Ignore right component, use left
                        merged_entry["components"].append(left_comp)
                        logger.warning(f"Ignoring component '{comp_name}' in entry ID '{entry_id}' from {right_file_path}")
                    elif overwrite:
                        # Overwrite left component with right
                        merged_entry["components"].append(right_comp)
                        logger.warning(f"Overwriting component '{comp_name}' in entry ID '{entry_id}' with component from {right_file_path}")
                    else:
                        # Should not reach here due to earlier check, but just in case
                        merged_entry["components"].append(left_comp)

            # Copy any additional fields from the left entry
            for key, value in left_entry.items():
                if key not in ["id", "components"]:
                    merged_entry[key] = value

            merged_entries.append(merged_entry)

    # Update the merged data
    left_data["entries"] = merged_entries

    # Return the merged data
    return left_data