import subprocess
import yaml
import os

def check_installation():
    try:
        # Vérifier si Apache est installé en essayant de récupérer la version
        apache_version = subprocess.check_output(['apache2', '-v'], stderr=subprocess.STDOUT, text=True)

        print(f"Apache est déjà installé. Version : {apache_version}")

    except subprocess.CalledProcessError:
        # Si la commande retourne une erreur, cela signifie qu'Apache n'est pas installé
        print("Apache n'est pas installé.")
        
        # Proposer à l'utilisateur de l'installer
        install_choice = input("Voulez-vous installer Apache maintenant ? (oui/non) ").lower()

        if install_choice == 'oui':
            install_apache()
        else:
            print("Installation annulée.")


def install_apache():
    try:
        subprocess.run(['sudo', 'apt', 'install', 'apache2'])

        print("Apache a été installé avec succès.")

    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'installation d'Apache : {e}")


def create_user():
    print("Creation de lutilisateur")







