import os
import fileinput


# Fonction pour mettre à jour les dépôts du système
def update_repos():
    try:
        # Exécute la commande 'apt update' pour mettre à jour les dépôts
        os.system("sudo apt update -y")
    except Exception as e:
        # En cas d'erreur, affiche un message d'erreur et quitte le script
        print("Erreur lors de la mise à jour des dépôts :", e)
        exit(1)

# Fonction pour installer le module ModSecurity pour Apache2
def install_mod_security():
    try:
        # Exécute la commande 'apt install' pour installer le module ModSecurity
        os.system("sudo apt install libapache2-mod-security2 -y")
    except Exception as e:
        # En cas d'erreur, affiche un message d'erreur et quitte le script
        print("Erreur lors de l'installation du module ModSecurity :", e)
        exit(1)

# Fonction pour redémarrer le service Apache2
def restart_apache():
    try:
        # Exécute la commande 'systemctl restart' pour redémarrer Apache2
        os.system("sudo systemctl restart apache2")
    except Exception as e:
        # En cas d'erreur, affiche un message d'erreur et quitte le script
        print("Erreur lors du redémarrage d'Apache2 :", e)
        exit(1)

# Fonction pour configurer ModSecurity
def configure_mod_security():
    try:
        # Copie le fichier de configuration recommandé de ModSecurity et active le moteur de règles
        os.system("sudo cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf")
        os.system("sudo sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf")
    except Exception as e:
        # En cas d'erreur, affiche un message d'erreur et quitte le script
        print("Erreur lors de la configuration de ModSecurity :", e)
        exit(1)

# Fonction pour télécharger et installer les règles OWASP CRS
def download_owasp_crs():
    try:
        # Télécharge et extrait les règles OWASP CRS
        os.system("wget https://github.com/coreruleset/coreruleset/archive/v3.3.0.zip")
        os.system("unzip v3.3.0.zip")
        os.system("mv coreruleset-3.3.0/crs-setup.conf.example /etc/modsecurity/crs-setup.conf")
        os.system("mv coreruleset-3.3.0/rules/ /etc/modsecurity/")
    except Exception as e:
        # En cas d'erreur, affiche un message d'erreur et quitte le script
        print("Erreur lors du téléchargement et de l'installation des règles OWASP CRS :", e)
        exit(1)

# Fonction pour éditer le fichier de configuration de sécurité d'Apache2
def edit_security_conf():
    try:
        # Modifie le fichier de configuration d'Apache2 pour inclure les fichiers de configuration ModSecurity
        os.system("sudo sed -i '/IncludeOptional \/etc\/modsecurity\/\*\.conf/d' /etc/apache2/mods-enabled/security2.conf")
        os.system("sudo sed -i '/Include \/etc\/modsecurity\/rules\/\*\.conf/d' /etc/apache2/mods-enabled/security2.conf")
        os.system("sudo sh -c 'echo \"IncludeOptional /etc/modsecurity/*.conf\" >> /etc/apache2/mods-enabled/security2.conf'")
        os.system("sudo sh -c 'echo \"Include /etc/modsecurity/rules/*.conf\" >> /etc/apache2/mods-enabled/security2.conf'")
    except Exception as e:
        # En cas d'erreur, affiche un message d'erreur et quitte le script
        print("Erreur lors de la configuration des fichiers de sécurité d'Apache2 :", e)
        exit(1)


def edit_security2_conf():
    try:
        # Chemin du fichier de configuration de sécurité d'Apache2
        security_conf_path = "/etc/apache2/mods-enabled/security2.conf"

        # Modifier le fichier security2.conf
        with fileinput.FileInput(security_conf_path, inplace=True, backup='.bak') as f:
            for line in f:
                if "IncludeOptional /usr/share/modsecurity-crs/*.load" in line:
                    # Commenter la ligne
                    line = "#" + line
                print(line, end='')
    
    except Exception as e:
        print("Erreur lors de la configuration des fichiers de sécurité d'Apache2 :", e)
        exit(1)


# Fonction principale
def main():
    try:
        # Appelle les différentes fonctions pour effectuer les étapes de configuration
        update_repos()
        install_mod_security()
        restart_apache()
        configure_mod_security()
        download_owasp_crs()
        edit_security_conf()
        edit_security2_conf()
        restart_apache()
    except Exception as e:
        # En cas d'erreur inattendue, affiche un message d'erreur général et quitte le script
        print("Une erreur s'est produite lors de l'exécution du script :", e)
        exit(1)

# Point d'entrée du script
if __name__ == "__main__":
    main()
