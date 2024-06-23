import subprocess
import paramiko
import warnings

warnings.filterwarnings(action='ignore', module='.*paramiko.*')

def run_local_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("Error:", result.stderr)

def run_remote_command(host, username, password, command):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    output = stdout.read()
    error = stderr.read()
    if output:
        print(output.decode())
    if error:
        print("Error:", error.decode())
    ssh_client.close()

def main():
    while True:
        print("1. List files")
        print("2. Create a directory")
        print("3. Display running processes")
        print("4. Show current directory")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            command = "ls -l"
        elif choice == "2":
            dir_name = input("Enter directory name to create: ")
            command = f"mkdir {dir_name}"
        elif choice == "3":
            command = "ps -aux"
        elif choice == "4":
            command = "pwd"
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice")
            continue

        location = input("Run command locally or remotely? (local/remote): ")

        if location == "local":
            run_local_command(command)
        elif location == "remote":
            host = input("Enter remote host: ")
            username = input("Enter remote username: ")
            password = input("Enter remote password: ")
            run_remote_command(host, username, password, command)
        else:
            print("Invalid location")

if __name__ == "__main__":
    main()
