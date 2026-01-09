import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from constants import MAX_CHARS

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_path, file_path))

    valid_file_path = os.path.commonpath([abs_path, target_file]) == abs_path

    try:
        if not valid_file_path:
            raise Exception(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    except Exception as e:
        return f"Result for '{file_path}' directory: \n{e}"
    
    try:
        if os.path.isfile(target_file) == False:
            raise Exception(f'Error: File not found or is not a regular file: "{file_path}"')
    except Exception as e:
        return f"Result for '{file_path}' directory: \n{e}"
    
    with open(target_file, "r") as f:
        file_content_string = f.read(MAX_CHARS)

        if f.read(1):
            file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        print(file_content_string)

    return file_content_string

