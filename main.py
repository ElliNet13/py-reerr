import traceback
import os

def edit_error_line(script_path):
    print("Editing line 1 in:", script_path)
    with open(script_path, "r") as file:
        lines = file.readlines()

    if lines:
        lines[0] = "### " + lines[0]

    with open(script_path, "w") as file:
        file.writelines(lines)

def run_script(script_path):
    if not os.path.exists(script_path):
        print("Error: Script file does not exist.")
        return

    try:
        exec(open(script_path).read())
    except Exception as e:
        print("Error occurred:")
        print(e)
        traceback.print_exc()
        edit_error_line(script_path)
        print("Added three hashtags before line 1 in:", script_path)

# Example usage:
script_path = "script.py"
run_script(script_path)