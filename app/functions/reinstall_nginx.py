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
        print(f"Une erreur est survenue lors de l'exécution de {command}: {e.stderr.decode('utf-8')}")
        sys.exit(1)

def print_status(message):
    print(f"\n{message}")

def start_reinstall():
    print_status("Arrêt du service Nginx...")
    run_command(['sudo', 'systemctl', 'stop', 'nginx'])
    print_status("Service Nginx arrêté.")

    print_status("Désinstallation de Nginx en cours...")
    run_command(['sudo', 'apt-get', 'purge', 'nginx', '-y'])
    print_status("Désinstallation terminée.")

    print_status("Mise à jour du système...")
    run_command(['sudo', 'apt-get', 'update'])
    print_status("Mise à jour terminée.")

    print_status("Suppression des dépendances non utilisées...")
    run_command(['sudo', 'apt-get', 'autoremove', '-y'])
    print_status("Suppression terminée.")

    print_status("Réinstallation de Nginx en cours...")
    run_command(['sudo', 'apt-get', 'install', 'nginx', '-y'])
    print_status("Réinstallation terminée.")

    print("Nginx a été réinstallé avec succès!")


