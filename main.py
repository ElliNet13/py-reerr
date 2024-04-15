import subprocess
import re

with open('script.py', 'r') as file:
    # Read the file and split it into lines
    lines = file.read().splitlines()

# Open the Python shell as a subprocess
python_process = subprocess.Popen(['python'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Send input to the Python shell
for line in lines:
  python_process.stdin.write(line + '\n')
python_process.stdin.write("exit()\n")  # Exit the Python shell

# Close the stdin stream to indicate that no more input will be sent
python_process.stdin.close()

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
for result in results:
    with open('script.py', 'w') as file:
        for i, line in enumerate(lines, 1):
            if i == result:
                file.write("### " + line + "\n")  # Comment out the line containing the error
            else:
                file.write(line + '\n')  # Write the line as is

# Wait for the subprocess to exit
python_process.wait()

print("Done!")
print("There are now 3 hashtags before every error in the script.")