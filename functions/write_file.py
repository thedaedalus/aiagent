import os

import google.genai.types as types

from config import *

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Can write to a specified file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="relative path to a file to write. The file can be a new file or an existing file and must be provided",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to write to the file it must be in a string and must be provided",
            ),
        },
        required=["file_path", "content"],
    ),
)


def write_file(working_directory, file_path, content):
    working_dir_abs = abspath(working_directory)
    file_path = normpath(abspath(join(working_dir_abs, file_path)))
    # Will be True or False
    valid_target_dir = commonpath([working_dir_abs, file_path]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if isdir(file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
