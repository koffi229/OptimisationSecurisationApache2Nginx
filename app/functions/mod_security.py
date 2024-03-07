import os
import subprocess
import fileinput

# Fonction pour mettre à jour les dépôts du système
def update_repos():
    try:
        subprocess.run(["sudo", "apt", "update", "-y"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la mise à jour des dépôts :", e)
        exit(1)

# Fonction pour installer le module ModSecurity pour Apache2
def install_mod_security():
    try:
        subprocess.run(["sudo", "apt", "install", "libapache2-mod-security2", "-y"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur lors de l'installation du module ModSecurity :", e)
        exit(1)

# Fonction pour redémarrer le service Apache2
def restart_apache():
    try:
        subprocess.run(["sudo", "systemctl", "restart", "apache2"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur lors du redémarrage d'Apache2 :", e)
        exit(1)

# Fonction pour configurer ModSecurity
def configure_mod_security():
    try:
        subprocess.run(["sudo", "cp", "/etc/modsecurity/modsecurity.conf-recommended", "/etc/modsecurity/modsecurity.conf"], check=True)
        subprocess.run(["sudo", "sed", "-i", "s/SecRuleEngine DetectionOnly/SecRuleEngine On/", "/etc/modsecurity/modsecurity.conf"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la configuration de ModSecurity :", e)
        exit(1)

# Fonction pour télécharger et installer les règles OWASP CRS
def download_owasp_crs():
    try:
        subprocess.run(["wget", "https://github.com/coreruleset/coreruleset/archive/v3.3.0.zip"], check=True)
        subprocess.run(["unzip", "v3.3.0.zip"], check=True)
        subprocess.run(["mv", "coreruleset-3.3.0/crs-setup.conf.example", "/etc/modsecurity/crs-setup.conf"], check=True)
        subprocess.run(["mv", "coreruleset-3.3.0/rules/", "/etc/modsecurity/"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur lors du téléchargement et de l'installation des règles OWASP CRS :", e)
        exit(1)

# Fonction pour éditer le fichier de configuration de sécurité d'Apache2
def edit_security_conf():
    try:
        subprocess.run(["sudo", "sed", "-i", "/IncludeOptional \/etc\/modsecurity\/\*\.conf/d", "/etc/apache2/mods-enabled/security2.conf"], check=True)
        subprocess.run(["sudo", "sed", "-i", "/Include \/etc\/modsecurity\/rules\/\*\.conf/d", "/etc/apache2/mods-enabled/security2.conf"], check=True)
        subprocess.run(["sudo", "sed", "-i", "1s/^/IncludeOptional \/etc\/modsecurity\/\*\.conf\n/", "/etc/apache2/mods-enabled/security2.conf"], check=True)
        subprocess.run(["sudo", "sed", "-i", "1s/^/Include \/etc\/modsecurity\/rules\/\*\.conf\n/", "/etc/apache2/mods-enabled/security2.conf"], check=True)
    except subprocess.CalledProcessError as e:
        print("Erreur lors de la configuration des fichiers de sécurité d'Apache2 :", e)
        exit(1)

# Fonction pour éditer le fichier de configuration security2.conf
def edit_security2_conf():
    try:
        security_conf_path = "/etc/apache2/mods-enabled/security2.conf"
        with fileinput.FileInput(security_conf_path, inplace=True, backup='.bak') as f:
            for line in f:
                if "IncludeOptional /usr/share/modsecurity-crs/*.load" in line:
                    line = "#" + line
                print(line, end='')
    except Exception as e:
        print("Erreur lors de la configuration des fichiers de sécurité d'Apache2 :", e)
        exit(1)

# Fonction principale
def main():
    try:
        update_repos()
        install_mod_security()
        restart_apache()
        configure_mod_security()
        download_owasp_crs()
        edit_security_conf()
        edit_security2_conf()
        restart_apache()
    except Exception as e:
        print("Une erreur s'est produite lors de l'exécution du script :", e)
        exit(1)


