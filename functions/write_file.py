import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or re-write the content of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the target file, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description": "New content to be written inside the target file",
                },
            },
            "required": ["file_path", "content"]
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        if working_directory is None: raise RuntimeError("invalid working directory")

        absolute_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = os.path.commonpath([absolute_working_dir, absolute_file_path]) == absolute_working_dir
        if not valid_target_dir: return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(absolute_file_path): return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_folder = os.path.dirname(file_path)
        if parent_folder: os.makedirs(parent_folder, exist_ok=True)

        with open(absolute_file_path, mode="w") as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
