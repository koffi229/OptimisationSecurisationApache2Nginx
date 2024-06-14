from functions.banner import display_banner
import functions.generate_config
import functions.delete_apache_config
import functions.reinstall_apache2
import functions.virtualhosts_create
import functions.mod_security
import modules.apache
import modules.nginx
import functions.generate_config_nginx
import functions.reinstall_nginx

display_banner()
print("Welcome") 
print("Choose between 1 and 2 for generate system configuration")
print("NB: Choose the server for which you have generated the configuration templates")

try:
    choix = input("\n1 - Apache2\n2 - Nginx\n: ")
    if choix == "1":
        resp = input("Have you ever administered Apache2 before? (yes/no)\nNB:In the event of major changes to the configuration files, this option will enable a complete reinstallation of the web service : ")                   
        if resp.lower() == 'yes':
            functions.reinstall_apache2.processing_reinstalltion()
            functions.delete_apache_config.cleaner()
            functions.generate_config.start_generate()                 
        elif resp.lower() == 'no':
            functions.delete_apache_config.cleaner()
            functions.generate_config.start_generate()
                    
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    elif choix == "2":
        resp = input("Have you ever administered Nginx before? (yes/no)\nNB: In the event of major changes to the configuration files, this option will enable a complete reinstallation of the web service : ")
        if resp.lower() == 'yes':
            functions.reinstall_nginx.start_reinstall()
            functions.generate_config_nginx.start_generate()
        elif resp.lower() == 'no':
            functions.generate_config_nginx.start_generate()
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
    else:
        print("Please choose between 1 and 2")
except Exception as e:
    print(f"Error: {e}")