from . import apache2_config as apache
from . import apache2_optimisation_config as apache_optimisation
import os
from colorama import Fore, Style, init
import subprocess

#Fonction gerant la baniere

def display_banner():
    banner = fr'''
{Fore.GREEN}      █████████                        ██████   ██████                      ███           
  ███░░░░░███                      ░░██████ ██████                      ░░░            
 ░███    ░███  █████ █████  ██████  ░███░█████░███   ██████   ████████  ████   ██████  
 ░███████████ ░░███ ░░███  ███░░███ ░███░░███ ░███  ░░░░░███ ░░███░░███░░███  ░░░░░███ 
 ░███░░░░░███  ░███  ░███ ░███████  ░███ ░░░  ░███   ███████  ░███ ░░░  ░███   ███████ 
 ░███    ░███  ░░███ ███  ░███░░░   ░███      ░███  ███░░███  ░███      ░███  ███░░███ 
 █████   █████  ░░█████   ░░██████  █████     █████░░████████ █████     █████░░████████
░░░░░   ░░░░░    ░░░░░     ░░░░░░  ░░░░░     ░░░░░  ░░░░░░░░ ░░░░░     ░░░░░  ░░░░░░░░ 
                                                                                       
{Fore.YELLOW}         Outil d'Optimisation et de Sécurisation des Services Web
{Style.RESET_ALL}    '''

    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)
    


    
def init():
    display_banner()
    print("Bienvenue")

    try:
        choix = input("Veuillez choisir le service Web à configurer :\n1 - Apache2\n2 - Nginx\n")

        if choix == '1':
            apache.check_installation()
            apache.create_user()
            domain_name = input("Entrez le nom de domaine de votre site : ")
            apache_optimisation.generate_yaml(domain_name)

        elif choix == '2':
            # loogique de configuration de Nginx
            pass

        else:
            print("Choix non valide. Veuillez choisir entre '1' et '2'.")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}. Veuillez réessayer s'il vous plaît.")







    
