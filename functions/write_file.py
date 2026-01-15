import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_path, file_path))

    valid_file_path = os.path.commonpath([abs_path, target_file]) == abs_path

    if os.path.isdir(target_file):
        raise Exception(f'Error: Cannot write to "{file_path}" as it is a directory')
    try:
        if not valid_file_path:
            raise Exception(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    except Exception as e:
        return f"Result for '{file_path}' directory: \n{e}"
    
    try:
        os.makedirs(file_path, exist_ok=True)
    except Exception as e:
        return f"Error: could not create parent dirs, {e}"

    with open(target_file, "w") as f:
        try:
            f.write(content)
        except Exception as e:
            return f"Error: could not write to file, {e}"
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text content to a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text content to write to the file"
            )
        },
    ),
)