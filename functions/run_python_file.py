import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):

    abs_path = os.path.abspath(working_directory)

    target_file = os.path.normpath(os.path.join(abs_path, file_path))

    valid_file_path = os.path.commonpath([abs_path, target_file]) == abs_path
    try:

        if not os.path.isfile(target_file):
            raise Exception(f'Error: "{file_path}" does not exist or is not a regular file')
    except Exception as e:
        return e 
    try:
        if not valid_file_path:
            raise Exception(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    except Exception as e:
        return f"Result for '{file_path}' directory: \n{e}"
    
    try:
        if file_path[-3:] != ".py":
            raise Exception(f'Error: "{file_path}" is not a Python file')
    except Exception as e:
        return e
    
    command = ["python", target_file]

    if args:
        command.extend(args)

    try:
        process = subprocess.run(command, cwd=abs_path, text=True, timeout=30, capture_output=True)  
    except Exception as e:
        return f"Error: executing Python file: {e}"
      
    return_code = process.returncode
    stdout = process.stdout
    stderr = process.stderr
    
    output_string = ""

    if return_code != 0:
        output_string += f"Process exited with with code {return_code}\n"

    if not stdout or not stderr:
        output_string += "No output produced\n"
    
    if stdout:
        output_string += f"STDOUT: {stdout}\n"

    if stderr:
        output_string += f"STDERR: {stderr}"

    return output_string

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)