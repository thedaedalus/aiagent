import os
from os.path import abspath, commonpath, exists, getsize, isdir, isfile, join, normpath

import google.genai.types as types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="It outputs contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to a file from, relative to the working directory and must be provided",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    working_dir_abs = abspath(working_directory)
    file_path = normpath(abspath(join(working_dir_abs, file_path)))
    # Will be True or False
    valid_target_dir = commonpath([working_dir_abs, file_path]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_path, "r") as f:
            content = f.read(MAX_CHARS)
            # After reading the first MAX_CHARS...
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content
    except Exception as e:
        return f"Error: {e}"
