import os

def split_filename(input_string):
    if '.ann.' in input_string:
        return input_string.split('.ann.')[0]
    else:
        return input_string


def append_to_file(filepath, string_to_append):
    try:
        with open(filepath, 'a') as file:
            file.write(string_to_append)
        print(f"String appended to {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")

def load_log_actions(logfile):
    if not os.path.isfile(logfile):
        return []

    try:
        with open(logfile, 'r') as file:
            lines = file.readlines()

        processed_lines = []
        for line in lines:
            # line = line.split("(")[0]
            processed_lines.append(line.strip())
            # print("entry: ",line.strip())

        return processed_lines
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def find_newest_file(directory):
    """
    Find the newest file in the given directory.
    """
    try:
        # List all files in the directory
        files = [os.path.join(directory, f) for f in os.listdir(directory) if
                 os.path.isfile(os.path.join(directory, f))]

        if not files:
            print("No files found in the directory.")
            return None

        # Find the newest file based on modification time
        #print("FILES ",files)
        #for file in files:
        #    print(os.path.basename(file))
        filtered_files = [file for file in files if os.path.basename(file) != 'log.txt']
        newest_file = max(filtered_files, key=os.path.getmtime)

        print(f"Newest file: {newest_file}")
        return newest_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
