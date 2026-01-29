import os
from os.path import abspath, commonpath, exists, getsize, isdir, isfile, join, normpath

import google.genai.types as types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    working_dir_abs = abspath(working_directory)
    target_dir = normpath(join(working_dir_abs, directory))
    # Will be True or False
    valid_target_dir = commonpath([working_dir_abs, target_dir]) == working_dir_abs
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        files = os.listdir(target_dir)
        results = []
        for file in files:
            file_path = join(target_dir, file)
            if isdir(file_path):
                is_dir = True
            elif isfile(file_path):
                is_dir = False
                file_size = getsize(file_path)
            else:
                is_dir = False
                file_size = 0
            results.append(f"- {file}: file_size={file_size}, is_dir={is_dir}")
        return "\n".join(results)
    except Exception as e:
        return f"Error: {e}"
