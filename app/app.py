from functions.banner import display_banner
import functions.generate_config
import functions.delete_apache_config
import functions.reinstall_apache2
import functions.virtualhosts_create
import functions.mod_security
import modules.apache
import modules.nginx
import functions.generate_config_nginx

def main():
    display_banner()
    print("Welcome") 

    try:
        option = input("1 - Generate a template of configuration for the web Server\n2 - Generate a configuration from a YAML template\n3 - Create a virtualhosts\n4 - Restore Apache2 or Nginx configuration\n(Please choose between 1 and 3): ")
        
        if option == "1":
            choix = input("\n1 - Apache2\n2 - Nginx")
            try:
                if choix == "1":
                    modules.apache.start()
                elif choix == "2":
                    modules.nginx.start()
                else:
                    print("Veuiller choisir entre 1 et 2 svp")
            except Exception as e:
                print("Error{e}")
        elif option == "2":
            try:
                choix = input("\n1 - Apache2\n2 - Nginx")
                if choix == "1":
                    resp = input("Have you ever administered Apache2 before? (yes/no): ")                   
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
                    functions.generate_config_nginx.start_generate()
                else:
                    print("Veuiller choisir entre 1 ou 2 svp")
            except Exception as e:
                    print(f"Error: {e}")
        elif option == "3":
            functions.virtualhosts_create.create_virtualhost()    
        else:
            print("Invalid option. Please choose between 1 and 3.")

    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()
