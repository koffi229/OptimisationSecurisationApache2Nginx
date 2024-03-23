# coding: utf-8
import os
import subprocess
import yaml

def create_virtualhost(domain_name):
    # Charger les configurations à partir du fichier YAML
    yaml_file_path = f"{domain_name}_config.yaml"
    with open(yaml_file_path, 'r') as yaml_file:
        config_data = yaml.safe_load(yaml_file)

    # Créer le répertoire DocumentRoot s'il n'existe pas
    if not os.path.exists(config_data['DocumentRoot']['value']):
        os.makedirs(config_data['DocumentRoot']['value'])
        print(f"Le répertoire DocumentRoot a été créé : {config_data['DocumentRoot']['value']}")

    # Créer le fichier de log s'il n'existe pas
    access_log_path = os.path.join(config_data['DocumentRoot']['value'], config_data['AccessLog']['value'])
    with open(access_log_path, 'a'):
        os.utime(access_log_path, None)
        print(f"Le fichier de log a été créé : {access_log_path}")

    # Générer le contenu du VirtualHost
    virtualhost_content = f"""
<VirtualHost *:80>
    ServerName {config_data['ServerName']['value']}
    DocumentRoot {config_data['DocumentRoot']['value']}
    AllowOverride {config_data['AllowOverride']['value']}
    mmap {config_data['mmap']['value']}
    Sendfile {config_data['Sendfile']['value']}
    ProcessCreation {config_data['ProcessCreation']['value']}
    {config_data['MPM']['value']}
    MaxRequestWorkers {config_data['MaxRequestWorkers']['value']}
    AtomicOperations {config_data['AtomicOperations']['value']}
    IncreaseChildProcesses {config_data['IncreaseChildProcesses']['value']}
    EnableCaching {config_data['EnableCaching']['value']}
    EnableCompression {config_data['EnableCompression']['value']}
    AccessLog {access_log_path}
</VirtualHost>
"""

    # Enregistrer le contenu dans le fichier du VirtualHost
    virtualhost_file_path = f"/etc/apache2/sites-available/{domain_name}.conf"
    with open(virtualhost_file_path, 'w') as virtualhost_file:
        virtualhost_file.write(virtualhost_content)

    print(f"Le fichier VirtualHost pour {domain_name} a été créé avec succès : {virtualhost_file_path}")

    # Redémarrer Apache2
    try:
        # Tente de redémarrer Apache2
        subprocess.run(['sudo', 'systemctl', 'restart', 'apache2'], check=True)
        print("Apache2 a été redémarré avec succès.")

    except subprocess.CalledProcessError as e:
        # Capture une exception spécifique pour les erreurs de subprocess
        print(f"Erreur lors du redémarrage d'Apache2 : {e}")

    except Exception as e:
        # Capture toute autre exception non spécifique
        print(f"Une erreur s'est produite lors du redémarrage d'Apache2 : {e}")


if __name__ == "__main__":
    domain_name = input("Entrez le nom de domaine de votre site : ")
    create_virtualhost(domain_name)
