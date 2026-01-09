import os

def get_files_info(working_directory, directory="."):
    abs_path = os.path.abspath(working_directory)

    target_dir = os.path.normpath(os.path.join(abs_path, directory))

    valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path

    try:
        if not valid_target_dir:
            raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    except Exception as e:
        return f"Result for '{directory}' directory: \n{e}"
    
    try:
        if os.path.isdir(target_dir) == False:
            raise Exception(f'Error: "{directory}" is not a directory')
    except Exception as e:
        return f"Result for '{directory}' directory: \n{e}"
    
    items_in_dir = os.listdir(target_dir)
    output = ""
    for item in items_in_dir:
        item_path = os.path.join(target_dir, item)
        output += f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
        output += "\n"
    return f"Result for '{directory}' directory: \n{output[:-1]}"