import os

def create_virtualhost():
    try:
        nom_domaine = input("Entrez le nom de domaine du site (ex: monsite.com) : ")
        chemin_racine = input("Entrez le chemin complet de la racine du site (ex: /var/www/monsite) : ")
        nom_fichier_conf = input("Entrez le nom du fichier de configuration (sans l'extension .conf) : ")
        utiliser_ssl = input("Voulez-vous utiliser SSL pour ce site ? (oui/non) : ").lower() == "oui"

        port = 443 if utiliser_ssl else 80
        protocol = "https" if utiliser_ssl else "http"

        # Création du répertoire racine s'il n'existe pas
        if not os.path.exists(chemin_racine):
            os.makedirs(chemin_racine)
            print(f"Le répertoire racine {chemin_racine} a été créé.")

        # Création des fichiers de log
        error_log_path = os.path.join("/var/log/apache2/", f"{nom_domaine.split('.')[0]}_error.log")
        access_log_path = os.path.join("/var/log/apache2/", f"{nom_domaine.split('.')[0]}_access.log")

        open(error_log_path, "a").close()
        open(access_log_path, "a").close()

        config = f"""
<VirtualHost *:{port}>
    ServerAdmin webmaster@{nom_domaine}
    ServerName {nom_domaine}
    ServerAlias www.{nom_domaine}
    DocumentRoot {chemin_racine}

    <Directory {chemin_racine}>
        Options Indexes FollowSymLinks MultiViews
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog {error_log_path}
    CustomLog {access_log_path} combined
"""

        if utiliser_ssl:
            try:
                cert_file_path = input("Entrez le chemin complet du fichier de certificat SSL : ")
                key_file_path = input("Entrez le chemin complet du fichier de clé privée SSL : ")

                with open(cert_file_path) as cert_file, open(key_file_path) as key_file:
                    cert_file.read()
                    key_file.read()

                    config += f"""
    SSLEngine on
    SSLCertificateFile    {cert_file_path}
    SSLCertificateKeyFile {key_file_path}
"""
            except FileNotFoundError:
                print("Le fichier spécifié n'a pas été trouvé.")
                return

        config += "\n</VirtualHost>"

        with open(f"/etc/apache2/sites-available/{nom_fichier_conf}.conf", "w") as fichier_conf:
            fichier_conf.write(config)

        # Activation du site et redémarrage d'Apache
        os.system("systemctl start apache2")
        os.system(f"a2ensite {nom_fichier_conf}")
        os.system("systemctl reload apache2")

        print(f"Le fichier de configuration pour {nom_domaine} ({protocol}) a été créé avec succès et le site a été activé.")
        print(f"Les fichiers de logs {error_log_path} et {access_log_path} ont été généré ")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

