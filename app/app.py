from modules.nginx import Nginx
from functions.banner import display_banner
import functions.generate_config
import functions.startup_config 
import functions.delete_apache_config


display_banner()
print("Bienvenue")

try:
    option = input("1 - Genererate a template of configuration for the web Server \n2 - Genererate a configuration from yaml template\n(Please choose between (1 et 2)) ")
    if option == "1" :
        functions.startup_config.make_config()
    if option == "2" :
        #resp = input("Aviez vous déjà appliqué un template auparavent ? (oui/non)")
        #if resp == 'oui':
            functions.delete_apache_config.cleaner()
            functions.generate_config.start_generate()
        #if resp == 'non':
            #functions.generate_config.start_generate()
except Exception as e:
    print(f"Une erreur s'est produite {e}")





