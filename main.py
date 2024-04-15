import subprocess
import re
import sys

file_path = None

def getfile():
    global file_path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print("Using file:", file_path)
    else:
        file_path = "script.py"
    print("Using file:", file_path)

getfile()

try:
    file = open(file_path, "r+")
except FileNotFoundError:
    print("File not found.")
    exit()
except PermissionError:
    print("No permission to open the file.")
    exit()

lines = file.readlines()
file.seek(0)  # Reset file pointer to the beginning

# Open the Python shell as a subprocess
python_process = subprocess.Popen(['python'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Send input to the Python shell
for line in lines:
    python_process.stdin.write(line)
python_process.stdin.write("exit()\n")  # Exit the Python shell
python_process.stdin.close()  # Close the stdin stream to indicate that no more input will be sent

# Read and print the output of the Python shell
for line in python_process.stdout:
    print(line.strip())

# Check for errors in the error output
error_output = python_process.stderr.read()
if not error_output:
    print("No errors occurred!")
    exit()

# Find all occurrences of "line" followed by a number
matches = re.findall(r'line (\d+)', error_output, re.IGNORECASE)

# Convert the matched numbers to integers
results = [int(match) for match in matches]

# Comment the errors out
def commenterrs():
    for i, line in enumerate(lines, 1):
        if i in results:
            file.write("### " + line)  # Comment out the line containing the error
        else:
            file.write(line)  # Write the line as is

commenterrs()

# Truncate file after writing
file.truncate()

# Wait for the subprocess to exit
python_process.wait()

# Close the file
file.close()

print("Done!")
print("There are now 3 hashtags before every error in the script.")