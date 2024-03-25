import yaml
import subprocess
import os
import shutil

class NginxConfigGenerator:
    def __init__(self, yaml_file_path):
        self.yaml_file_path = yaml_file_path
        self.config_data = self.read_config()

    def read_config(self):
        try:
            with open(self.yaml_file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Le fichier YAML n'a pas été trouvé à l'emplacement spécifié : {self.yaml_file_path}")
            return None
        except yaml.YAMLError as e:
            print(f"Erreur de syntaxe YAML dans le fichier : {e}")
            return None
        
    def disable_other_services(self):
        try:
            # Arrêter Apache si activé
            subprocess.run(['sudo', 'systemctl', 'stop', 'apache2'])
            print("Apache arrêté avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'arrêt d'Apache : {e}")


    ########################################################
    def modify_config_options(self):
        print("Options de configuration actuelles :")
        for section, options in self.config_data.items():
            print(f"\nSection: {section}")
            for key, value in options.items():
                print(f"{key}: {value}")

            modify = input(f"\nWould you want to modify the option of this section {section} ? (y/n) : ").lower()
            if modify == 'o' or modify == 'y':
                for key in options.keys():
                    new_value = input(f"Nouvelle valeur pour {key} : ")
                    self.config_data[section][key] = new_value

        print("\nOptions de configuration mises à jour avec succès.")

    ########################################################

    def generate_nginx_config(self, modify_options=False, disable_other_services=True):
        if disable_other_services:
            self.disable_other_services()
            
        if modify_options:
            self.modify_config_options()
            print("New configuration options applied.")

        if self.config_data:
            nginx_conf_backup_path = '/etc/nginx/nginx.conf.backup'
            nginx_conf_path = '/etc/nginx/nginx.conf'

            # Sauvegarde de nginx.conf existant
            try:
                shutil.copy(nginx_conf_path, nginx_conf_backup_path)
                print("Sauvegarde de nginx.conf create with success.")
            except Exception as e:
                print(f"Erreur lors de la création de la sauvegarde de nginx.conf : {e}")
                return

            nginx_conf_content = self.format_nginx_config()
            with open(nginx_conf_path, 'w') as nginx_conf:
                nginx_conf.write(nginx_conf_content)
                print("Configuration Nginx mise à jour avec succès.")

            self.parse_nginx_conf(nginx_conf_path)
            self.restart_nginx()

    def format_nginx_config(self):
        nginx_conf_template = """
user www-data;
worker_processes {Worker[worker_processes]};
worker_rlimit_nofile {Worker[worker_rlimit_nofile]};
pid /run/nginx.pid;
error_log /var/log/nginx/error.log;

events {{
    worker_connections {events[worker_connections]};
}}

http {{
    include       mime.types;
    default_type  application/octet-stream;

    # Buffer settings
    client_body_buffer_size      {Buffers[client_body_buffer_size]};
    client_header_buffer_size    {Buffers[client_header_buffer_size]};
    large_client_header_buffers  {Buffers[large_client_header_buffers]};
    client_max_body_size         {Buffers[client_max_body_size]};

    # Proxy settings
    proxy_buffering      {Proxy[proxy_buffering]};
    proxy_buffer_size    {Proxy[proxy_buffer_size]};
    proxy_buffers        {Proxy[proxy_buffers]};

    # Timeout settings
    client_body_timeout   {Timeout[client_body_timeout]};
    client_header_timeout {Timeout[client_header_timeout]};
    keepalive_timeout     {Timeout[keepalive_timeout]};
    send_timeout          {Timeout[send_timeout]};
    keepalive_requests    {Timeout[keepalive_requests]};

    # Compression settings
    gzip            {Compression[gzip]};
    gzip_types      {Compression[gzip_types]};

    # TCP settings
    sendfile        {TCP[sendfile]};
    tcp_nodelay     {TCP[tcp_nodelay]};
    tcp_nopush      {TCP[tcp_nopush]};

    # SSL settings
    ssl_session_cache          {SSL[ssl_session_cache]};
    ssl_session_timeout        {SSL[ssl_session_timeout]};
    ssl_buffer_size            {SSL[ssl_buffer_size]};
    ssl_stapling               {SSL[ssl_stapling]};
    ssl_stapling_verify        {SSL[ssl_stapling_verify]};
    resolver                   {SSL[resolver]};
    resolver_timeout           {SSL[resolver_timeout]};

    # Security headers
    server_tokens {http[server_tokens]};
    add_header X-Frame-Options SAMEORIGIN always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header default-src "'self' https: data: 'unsafe-inline' 'unsafe-eval'" always;
    add_header X-Content-Type-Options nosniff always;
    proxy_hide_header X-Powered-By;
    add_header Referrer-Policy origin-when-cross-origin always;



    server {{
        #proxy_cache {server[proxy_cache]};
        proxy_cache_valid {server[proxy_cache_valid]};
        listen            {server[listen_ipv6_80]} default_server deferred;
        listen            {server[listen_ipv4_80]} default_server deferred;
        #listen            {server[listen_ipv6_443]};
        #listen            {server[listen_ipv4_443]};
    }}
}}


#mail {{
#	# See sample authentication script at:
#	# http://wiki.nginx.org/ImapAuthenticateWithApachePhpScript
#
#	server {{
#		listen     localhost:110;
#		protocol   pop3;
#		proxy      on;
#	}}
#
#	server {{
#		listen     localhost:143;
#		protocol   imap;
#		proxy      on;
#	}}
#}}

include /etc/nginx/generated_configs//*.conf;
"""

        # Format security headers
        add_headers = ""
        if 'add_headers' in self.config_data['http']:
            for header in self.config_data['http']['add_headers']:
                name = header['name']
                value = header['value']
                always = header.get('always', False)
                add_headers += f"    add_header {name} {value}{' always' if always else ''};\n"

        return nginx_conf_template.format(**self.config_data)
        #return nginx_conf_template.format(add_headers=add_headers, **self.config_data)

    def parse_nginx_conf(self, nginx_conf_path):
        try:
            with open(nginx_conf_path, 'r') as nginx_conf_file:
                nginx_conf_content = nginx_conf_file.read()

            # Remplacer True par on
            nginx_conf_content = nginx_conf_content.replace('True', 'on')
            # Remplacer False par off
            nginx_conf_content = nginx_conf_content.replace('False', 'off')

            with open(nginx_conf_path, 'w') as nginx_conf_file:
                nginx_conf_file.write(nginx_conf_content)

            print("Fichier nginx.conf analysé et modifié avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'analyse et de la modification du fichier nginx.conf : {e}")

    def restart_nginx(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'])
            print("Nginx redémarré avec succès.")
        except Exception as e:
            print(f"Erreur lors du redémarrage de Nginx : {e}")

def start_generate():
    path_yaml = input("Please enter the name of the yaml file: ")
    modify_options = input("Voulez-vous modifier les options de configuration avant de générer les configurations ? (y/n) : ").lower()
    modify_options = modify_options == 'o' or modify_options == 'y'
    generator = NginxConfigGenerator(path_yaml)
    generator.generate_nginx_config(modify_options)