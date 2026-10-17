import os

from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read a file and return its content as a str value. Results can be limited to a max amount of characters on specific contexts.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the target file, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"]
        },
    },
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        if working_directory is None: raise RuntimeError("invalid working directory")

        absolute_working_dir = os.path.abspath(working_directory)

        target_dir = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        if not os.path.isfile(target_dir): return f'Error: File not found or is not a regular file: "{file_path}"'

        valid_target_dir = os.path.commonpath([absolute_working_dir, target_dir]) == absolute_working_dir
        if not valid_target_dir: return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(target_dir) as file:
            file_contents = file.read(MAX_CHARS)
            if file.read(1):
                file_contents += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_contents
    except Exception as e:
        return f"Error: {e}"
