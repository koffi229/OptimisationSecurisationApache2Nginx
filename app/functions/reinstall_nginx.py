import subprocess
import sys
import time

def spinner(proc):
    chars = "/—\\|"
    while proc.poll() is None:
        for char in chars:
            sys.stdout.write(f'\b{char}')
            sys.stdout.flush()
            time.sleep(0.1)

def run_command(command):
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        spinner(proc)
        stdout, stderr = proc.communicate()
        if proc.returncode != 0:
            raise subprocess.CalledProcessError(proc.returncode, command, output=stdout, stderr=stderr)
        return stdout.decode('utf-8'), stderr.decode('utf-8')
    except subprocess.CalledProcessError as e:
        print(f"An error has occurred while running {command}: {e.stderr.decode('utf-8')}")
        sys.exit(1)

def print_status(message):
    print(f"\n{message}")

def start_reinstall():
    print_status("Nginx service stopped...")
    run_command(['sudo', 'systemctl', 'stop', 'nginx'])
    print_status("Nginx service stopped.")

    print_status("Uninstalling Nginx in progress...")
    run_command(['sudo', 'apt-get', 'purge', 'nginx', '-y'])
    print_status("Uninstall complete.")

    print_status("System update...")
    run_command(['sudo', 'apt-get', 'update'])
    print_status("Update complete.")

    print_status("Remove unused dependencies...")
    run_command(['sudo', 'apt-get', 'autoremove', '-y'])
    print_status("Deletion complete.")

    print_status("Nginx reinstallation in progress...")
    run_command(['sudo', 'apt-get', 'install', 'nginx', '-y'])
    print_status("Reinstallation complete.")

    print("Nginx has been successfully reinstalled!")


