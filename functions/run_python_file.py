import subprocess

import google.genai.types as types

from config import *

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


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = abspath(working_directory)
    absolute_file_path = normpath(abspath(join(working_dir_abs, file_path)))
    output = ""
    # Will be True or False
    valid_target_dir = (
        commonpath([working_dir_abs, absolute_file_path]) == working_dir_abs
    )
    if not valid_target_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'
    command = ["python", absolute_file_path]
    if args:
        command.extend(args)

    try:
        process = subprocess.run(
            command, capture_output=True, text=True, cwd=working_dir_abs, timeout=30
        )
        if process.returncode != 0:
            output = f"Process exited with code {process.returncode}\n"
        if not (process.stderr or process.stdout):
            output = "No output produced\n"
        else:
            output += f"STDOUT: {process.stdout}STDERR: {process.stderr}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
