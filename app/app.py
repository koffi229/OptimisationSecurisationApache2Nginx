from modules.nginx import Nginx
from functions.banner import display_banner
import functions.generate_config
import functions.startup_config 
import functions.delete_apache_config
import functions.reinstall_apache2
import functions.virtualhosts_create

def main():
    display_banner()
    print("Welcome") 

    try:
        option = input("1 - Generate a template of configuration for the web Server\n2 - Generate a configuration from a YAML template\n3 - Create a virtualhosts\n(Please choose between 1 and 3): ")
        
        if option == "1":
            functions.startup_config.make_config()
        
        elif option == "2":
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
        elif option == "3":
            functions.virtualhosts_create.create_virtualhost()
        
        else:
            print("Invalid option. Please choose between 1 and 3.")

    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()
