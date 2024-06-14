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

def main():
    display_banner()
    print("Welcome") 

    try:
        option = input("Would you wanna create a virtualhosts Apache2(y/n): ")
        if option == "n":
            pass
        
        # if option == "1":
        #     choix = input("\n1 - Apache2\n2 - Nginx\n: ")
        #     try:
        #         if choix == "1":
        #             modules.apache.start()
        #         elif choix == "2":
        #             modules.nginx.start()
        #         else:
        #             print("Veuiller choisir entre 1 et 2 svp")
        #     except Exception as e:
        #         print("Error{e}")
        # elif option == "2":
        #     try:
        #         choix = input("\n1 - Apache2\n2 - Nginx\n: ")
        #         if choix == "1":
        #             resp = input("Have you ever administered Apache2 before? (yes/no): ")                   
        #             if resp.lower() == 'yes':
        #                 functions.reinstall_apache2.processing_reinstalltion()
        #                 functions.delete_apache_config.cleaner()
        #                 functions.generate_config.start_generate()                 
        #             elif resp.lower() == 'no':
        #                 functions.delete_apache_config.cleaner()
        #                 functions.generate_config.start_generate()
                    
        #             else:
        #                 print("Invalid input. Please enter 'yes' or 'no'.")
        #         elif choix == "2":
        #             resp = input("Have you ever administered Nginx before? (yes/no): ")
        #             if resp.lower() == 'yes':
        #                 functions.reinstall_nginx.start_reinstall()
        #                 functions.generate_config_nginx.start_generate()
        #             elif resp.lower() == 'no':
        #                 functions.generate_config_nginx.start_generate()
        #             else:
        #                 print("Invalid input. Please enter 'yes' or 'no'.")
        #         else:
        #             print("Veuiller choisir entre 1 ou 2 svp")
        #     except Exception as e:
        #             print(f"Error: {e}")
        elif option == "y":
            functions.virtualhosts_create.create_virtualhost()    
        else:
            print("Invalid option. Please choose between 1 and 3.")

    except Exception as e:
        print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()
