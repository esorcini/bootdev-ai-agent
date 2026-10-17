from functions.get_files_info import get_files_info

print(f"Result for the current directory:\n{get_files_info("calculator", ".")}")
print(f"Result for the 'pkg' directory:\n{get_files_info("calculator", "pkg")}")
print(f"Result for the '/bin' directory:\n{get_files_info("calculator", "/bin")}")
print(f"Result for the '../' directory:\n{get_files_info("calculator", "../")}")
