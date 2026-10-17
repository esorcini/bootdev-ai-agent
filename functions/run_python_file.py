import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file with optional arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the target file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "Array[string]",
                    "description": "Optional list of arguments to be appended to the file execution",
                },
            },
            "required": ["file_path"]
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        if working_directory is None: raise RuntimeError("invalid working directory")

        absolute_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(absolute_working_dir, file_path))
        valid_target_dir = os.path.commonpath([absolute_working_dir, absolute_file_path]) == absolute_working_dir
        if not valid_target_dir: return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path): return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"): return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args: command.extend(args)

        process_result = subprocess.run(
            command,
            cwd=absolute_working_dir,
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )

        result_string = ""
        if process_result.returncode == 0:
            if not process_result.stdout and not process_result.stderr:
                result_string += "No output produced"
            result_string += f'STDOUT: {process_result.stdout} STDERR: {process_result.stderr}'
        else:
            return f"Process exited with code {process_result.returncode}. STDOUT: {process_result.stdout}. STDERR: {process_result.stderr}."
        return result_string

    except subprocess.CalledProcessError as error:
        return f"Process exited with code {error.returncode}. STDOUT: {error.stdout}. STDERR: {error.stderr}."
    except subprocess.TimeoutExpired as timeout:
        return f"Timeout of {timeout.timeout} expired: {timeout.output}"
    except Exception as e:
        return f"Error: {e}"
