import time

def main_test(input_file):
    output_file = '/home/james/Videos/daemon_gitHUB/Daemon_process/files/output.txt'
    with open(input_file, "r") as file:
        content = file.readlines()

    for line in content:
        modified_line = line.strip() + " hi\n"
        app(modified_line, output_file)
        time.sleep(6)

def app(line, output_file):
    with open(output_file, "a") as file:
        file.writelines(line)