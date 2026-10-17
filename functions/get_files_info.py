from functools import reduce
import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "List files inside a specified directory",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        if working_directory is None: raise RuntimeError("invalid working directory")

        absolute_working_dir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(absolute_working_dir, directory))
        if not os.path.isdir(target_dir): return f'Error: "{directory}" is not a directory'

        valid_target_dir = os.path.commonpath([absolute_working_dir, target_dir]) == absolute_working_dir
        if not valid_target_dir: return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        files_str = ""
        for file in os.listdir(target_dir):
            file_path = f"{target_dir}/{file}"
            files_str = files_str + f"\n- {file}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"

        return files_str.lstrip()
    except Exception as e:
        return f"Error: {e}"
