import subprocess
import sys
import time

# Fonction pour l'animation cool
def spinner(proc):
    chars = "/—\|"
    while proc.poll() is None:
        for char in chars:
            sys.stdout.write('\b' + char)
            sys.stdout.flush()
            time.sleep(0.1)
def start_reinstall():
    try:
        # Arrêt du service Nginx
        print("Arrêt du service Nginx...")
        stop_proc = subprocess.Popen(['sudo', 'systemctl', 'stop', 'nginx'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        spinner(stop_proc)
        print("\nService Nginx arrêté.")

        # Désinstallation de Nginx
        print("Désinstallation de Nginx en cours...")
        uninstall_proc = subprocess.Popen(['sudo', 'apt-get', 'purge', 'nginx', '-y'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        spinner(uninstall_proc)
        print("\nDésinstallation terminée.")

        # Suppression des dépendances non utilisées
        print("Suppression des dépendances non utilisées...")
        autoremove_proc = subprocess.Popen(['sudo', 'apt-get', 'autoremove', '-y'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        spinner(autoremove_proc)
        print("\nSuppression terminée.")

        # Réinstallation de Nginx
        print("Réinstallation de Nginx en cours...")
        install_proc = subprocess.Popen(['sudo', 'apt-get', 'install', 'nginx', '-y'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        spinner(install_proc)
        print("\nRéinstallation terminée.")

        print("Nginx a été réinstallé avec succès!")
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est survenue: {e}")
