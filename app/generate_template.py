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

choix = input("Generate template for Apache or Nginx(1/2):\n1 - Apache2\n2 - Nginx\n:")
try:
    if choix == "1":
        modules.apache.start()
    elif choix == "2":
        modules.nginx.start()
    else:
        print("Please choose between 1 and 2")
except Exception as e:
        print("Error{e}")