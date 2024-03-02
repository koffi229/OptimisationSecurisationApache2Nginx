from functions.banner import display_banner
import functions.generate_config
import functions.delete_apache_config
import functions.reinstall_apache2
import functions.virtualhosts_create
import functions.mod_security
import modules.apache

def main():
    display_banner()
    print("Welcome") 

    try:
        option = input("1 - Generate a template of configuration for the web Server\n2 - Generate a configuration from a YAML template\n3 - Create a virtualhosts\n4 - Install mod_security\n(Please choose between 1 and 4): ")
        
        if option == "1":
            modules.apache.start()
        
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
        elif option == "4":
            print("Before installing mod_security,make sure you've never had to install or configure it before. Continuing can block the web service.")
            ans = input("Do you want to continue??(yes/no)")
            if ans == "yes":
                functions.mod_security.main()
            elif ans == "no":
               pass
            else:
                print("Invalid input. Please enter 'yes' or 'no'. ")
        else:
            print("Invalid option. Please choose between 1 and 4.")

    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()
