import os

def delete_files(file_paths):
    """
    Deletes multiple files at the specified file paths.

    Args:
        file_paths (list): A list of file paths to be deleted.

    Returns:
        dict: A dictionary with file paths as keys and results as values.
    """
    results = {}
    
    for file_path in file_paths:
        try:
            os.remove(file_path)
            results[file_path] = "Deleted successfully."
        except FileNotFoundError:
            results[file_path] = "File does not exist."
        except PermissionError:
            results[file_path] = "Permission denied."
        except Exception as e:
            results[file_path] = f"Error: {e}"

    for file, result in results.items():
        print(f"{file}: {result}")
    
    return results