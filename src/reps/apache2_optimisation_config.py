# coding: utf-8


import subprocess
import yaml
import os

def generate_yaml(domain_name):
    # Créer un dictionnaire avec des commentaires pour guider l'utilisateur
    config_data = {
        
        
        'DocumentRoot': {
            'value': '/chemin/vers/le/repertoire',
            'comment': 'Le chemin du répertoire racine du site (DocumentRoot).'
        },
        'AllowOverride': {
            'value': 'All',
            'comment': 'Le paramètre AllowOverride (All/None).Il est conseille de le mettre a None si vous ne compter pas utiliser un fichier .htaccess'
        },
        'mmap': {
            'value': True,
            'comment': 'Activer mmap (true/false). Il est conseille de le desactiver'
        },
        'Sendfile': {
            'value': True,
            'comment': 'Activer Sendfile (true/false). Il est conseiller de le desactiver'
        },
        'ProcessCreation': {
            'value': 'posix',
            'comment': 'Process Creation (posix/simple).'
        },
        'MPM': {
            'value': 'event',
            'comment': 'Choisir un Module Multi-Processus (MPM).'
        },
        'MaxRequestWorkers': {
            'value': '150',
            'comment': 'Le nombre maximal de travailleurs simultanés.'
        },
        'AtomicOperations': {
            'value': True,
            'comment': 'Activer les opérations atomiques (true/false).'
        },
        'IncreaseChildProcesses': {
            'value': True,
            'comment': 'Augmenter le nombre de processus/threads enfants (true/false).'
        },
        'EnableCaching': {
            'value': True,
            'comment': 'Activer la mise en cache (true/false).'
        },
        'EnableCompression': {
            'value': True,
            'comment': 'Activer la compression (true/false).'
        },
        'AccessLog': {
            'value': '/chemin/vers/le/fichier/access.log',
            'comment': 'Le chemin du fichier de logs d\'accès (AccessLog).'
        }
    }

    # Enregistrer les informations dans un fichier YAML
    yaml_file_path = f"{domain_name.split('.')[0]}_config.yaml"
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(config_data, yaml_file, default_flow_style=False)

    print(f"Les informations ont été enregistrées dans {yaml_file_path}.")
