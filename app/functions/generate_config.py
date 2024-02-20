import yaml
import subprocess
import os


class ApacheConfigGenerator:
    def __init__(self, yaml_file_path, config_directory='/etc/apache2/conf-available/'):
        self.yaml_file_path = yaml_file_path
        self.config_directory = config_directory
        self.config_data = self.read_config()

    def read_config(self):
        try:
            with open(self.yaml_file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"YAML file not found at specified location: {self.yaml_file_path}")
            return None
        except yaml.YAMLError as e:
            print(f"YAML syntax error in the file: {e}")
            return None

    def generate_apache_config(self):
        if self.config_data:
            self.create_config_directory()
            self.generate_general_config()
            self.generate_module_config()
            #self.generate_php_config()
            self.generate_security_config()
            self.restart_apache()
            self.include_general_config()

    def create_config_directory(self):
        try:
            os.makedirs(self.config_directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating configuration directory: {e}")

    def generate_general_config(self):
        general_config_template = """
<Directory /var/www/>
    Options {OPTIONS}
    HostnameLookups {HOSTNAMELOOKUPS}
    AllowOverride {ALLOWOVERRIDE}
</Directory>

EnableMMAP {ENABLEMMAP}
EnableSendfile {ENABLESENDFILE}

<IfModule mod_rewrite.c>
    RewriteEngine On
</IfModule>

KeepAlive {KEEPALIVE_ENABLED}
KeepAliveTimeout {KEEPALIVE_TIMEOUT}
MaxKeepAliveRequests {KEEPALIVE_MAX_REQUESTS}

ServerSignature {SERVER_SIGNATURE}
ServerTokens {SERVER_TOKENS}
Timeout {TIMEOUT}
TraceEnable {TRACE_ENABLE}
"""

        # Replace placeholders in the template with the retrieved values from the YAML file
        general_config = general_config_template.format(
            OPTIONS=self.config_data.get('Options', 'DEFAULT_VALUE'),
            HOSTNAMELOOKUPS=self.config_data.get('HostnameLookups', 'DEFAULT_VALUE'),
            ALLOWOVERRIDE=self.config_data.get('AllowOverride', 'DEFAULT_VALUE'),
            ENABLEMMAP=self.config_data.get('EnableMMAP', 'DEFAULT_VALUE'),
            ENABLESENDFILE=self.config_data.get('EnableSendfile', 'DEFAULT_VALUE'),
            KEEPALIVE_ENABLED=self.config_data.get('KeepAlive', {}).get('enabled', 'DEFAULT_VALUE'),
            KEEPALIVE_TIMEOUT=self.config_data.get('KeepAlive', {}).get('timeout', 'DEFAULT_VALUE'),
            KEEPALIVE_MAX_REQUESTS=self.config_data.get('KeepAlive', {}).get('max_requests', 'DEFAULT_VALUE'),
            SERVER_SIGNATURE=self.config_data.get('Server', {}).get('ServerSignature', 'DEFAULT_VALUE'),
            SERVER_TOKENS=self.config_data.get('Server', {}).get('ServerTokens', 'DEFAULT_VALUE'),
            TIMEOUT=self.config_data.get('KeepAlive', {}).get('timeout', 'DEFAULT_VALUE'),
            TRACE_ENABLE=self.config_data.get('Server', {}).get('TraceEnable', 'DEFAULT_VALUE')
        )

        with open(os.path.join(self.config_directory, 'general_config.conf'), 'w') as file:
            file.write(general_config)
            print("Fichier general_config.conf généré")

    def generate_module_config(self):
        modules = self.config_data.get('Modules', {})
        
        for module, value in modules.items():
            if module.startswith('mod_') and isinstance(value, bool):
                if value:
                    activation_function = getattr(self, f'activate_{module}', None)
                    if activation_function:
                        activation_function()
                    else:
                        print(f"The activation function for the module {module} is not implemented.")
                else:
                    deactivation_function = getattr(self, f'deactivate_{module}', None)
                    if deactivation_function:
                        deactivation_function()
                    else:
                        print(f"The deactivation function for the module {module} is not implemented")

        mpm_module = self.config_data.get('Modules', {}).get('mpm')
        if mpm_module:
            active_mpm_module = self.get_active_mpm_module()
            if active_mpm_module and active_mpm_module != mpm_module:
                print(f"Deactivation of the current MPM module ({active_mpm_module}) and activation of {mpm_module}")
                self.deactivate_activate_mpm_module(active_mpm_module, mpm_module)
        else:
            print("No MPM module specified in YAML file.")

        self.install_required_modules()

        mpm_config = """
<IfModule {mpm_module}_module>
    StartServers {StartServers}
    MinSpareThreads {MinSpareThreads}
    MaxSpareThreads {MaxSpareThreads}
    ThreadLimit {ThreadLimit}
    ThreadsPerChild {ThreadsPerChild}
    MaxConnectionsPerChild {MaxConnectionsPerChild}
    MaxRequestWorkers {MaxRequestWorkers}
    ServerLimit {ServerLimit}
</IfModule>
""".format(
    mpm_module=mpm_module,
    **self.config_data.get('MPM_Modules', {})
)

        self.write_config_to_file(mpm_config, 'mpm_config.conf')
        print("Fichier mpm_config.conf généré")

    #def generate_php_config(self):
        #php_config_template = """
#expose_php {expose_php}
#"""

 #       php_config = php_config_template.format(expose_php=self.config_data.get('PHP', {}).get('expose_php', 'Off'))

 #       with open(os.path.join(self.config_directory, 'php_config.conf'), 'w') as file:
 #           file.write(php_config)

 #       print("Fichier php_config.conf généré")

    def generate_security_config(self):
        security_config = """
<IfModule mod_ssl.c>
    SSLProtocol {SSLProtocol}
    SSLCipherSuite {SSLCipherSuite}
    SSLHonorCipherOrder {SSLHonorCipherOrder}
    StrictTransportSecurity {StrictTransportSecurity}
</IfModule>

<IfModule mod_headers.c>
    {XFrameOptions}
    {XContentTypeOptions}
</IfModule>
        """.format(
            **self.config_data['Security'],
            **self.config_data['Rules']
        )

        self.write_config_to_file(security_config, 'security_config.conf')
        print("File security_config.conf generate")

    def write_config_to_file(self, config_content, file_name):
        file_path = os.path.join(self.config_directory, file_name)
        with open(file_path, 'w') as file:
            file.write(config_content)
        self.include_config_in_main(file_path)

    def include_config_in_main(self, file_path):
        apache2_conf_path = '/etc/apache2/apache2.conf'
        try:
            with open(apache2_conf_path, 'a') as apache2_conf:
                apache2_conf.write(f"Include {file_path}\n")
            print(f"Inclusion of {file_path} in {apache2_conf_path}")
        except Exception as e:
            print(f"Inclusion error in {apache2_conf_path}: {e}")

    def include_general_config(self):
        self.include_config_in_main(os.path.join(self.config_directory, 'general_config.conf'))

    def restart_apache(self):
        try:
            subprocess.run(['sudo', 'systemctl', 'restart', 'apache2'])
            print("Apache2 successfully restarted.")
        except Exception as e:
            print(f"Apache2 restart error : {e}")

    def get_active_mpm_module(self):
        try:
            result = subprocess.run(['apache2ctl', '-V'], capture_output=True, text=True)
            active_mpm_module = next((line.split()[2] for line in result.stdout.splitlines() if line.startswith('Server MPM')), None)
            return active_mpm_module
        except Exception as e:
            print(f"Error determining active MPM module: {e}")
            return None

    def deactivate_activate_mpm_module(self, active_mpm_module, new_mpm_module):
        try:
            subprocess.run(['sudo', 'a2dismod', f'mpm_{active_mpm_module}'])
            subprocess.run(['sudo', 'a2enmod', f'mpm_{new_mpm_module}'])
            subprocess.run(['sudo', 'systemctl', 'restart', 'apache2'])
        except Exception as e:
            print(f"Error when deactivating/activating MPM modules : {e}")

    # Fonctions d'activation et de désactivation des modules
    def activate_mod_cache(self):
        self.activate_module('cache')

    def deactivate_mod_cache(self):
        self.deactivate_module('cache')

    def activate_mod_reqtimeout(self):
        self.activate_module('reqtimeout')

    def deactivate_mod_reqtimeout(self):
        self.deactivate_module('reqtimeout')

    def activate_mod_atomic(self):
        self.activate_module('atomic')

    def deactivate_mod_atomic(self):
        self.deactivate_module('atomic')

    def activate_mod_deflate(self):
        self.activate_module('deflate')

    def deactivate_mod_deflate(self):
        self.deactivate_module('deflate')

    # Fonctions d'activation et de désactivation des modules génériques
    def activate_module(self, module):
        try:
            subprocess.run(['sudo', 'a2enmod', module])
            print(f"Module {module} activé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'activation du module {module} : {e}")

    def deactivate_module(self, module):
        try:
            subprocess.run(['sudo', 'a2dismod', module])
            print(f"Module {module} désactivé avec succès.")
        except Exception as e:
            print(f"Erreur lors de la désactivation du module {module} : {e}")

    def install_module(self, module):
        try:
            subprocess.run(['sudo', 'a2enmod', module])
            print(f"Module {module} activé avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'activation du module {module} : {e}")

    def install_required_modules(self):
        required_modules = self.config_data.get('Required_Modules', [])
        for module in required_modules:
            self.install_module(module)

    # Fonctions d'installation des modules MPM
    def install_mpm_worker(self):
        if not self.is_module_installed('mpm_worker'):
            self.install_module('mpm_worker')

    def deactivate_mpm_worker(self):
        self.deactivate_module('mpm_worker')

    def install_mpm_event(self):
        if not self.is_module_installed('mpm_event'):
            self.install_module('mpm_event')

    def deactivate_mpm_event(self):
        self.deactivate_module('mpm_event')

    def install_mpm_prefork(self):
        if not self.is_module_installed('mpm_prefork'):
            subprocess.run(['sudo', 'a2enmod', 'php8.5'])
            self.install_module('mpm_prefork')
            

    def deactivate_mpm_prefork(self):
        subprocess.run(['sudo', 'a2dismod', 'php8.5'])
        self.deactivate_module('mpm_prefork')

    def is_module_installed(self, module):
        try:
            result = subprocess.run(['apache2ctl', '-t', '-D', 'DUMP_MODULES'], capture_output=True, text=True)
            return module in result.stdout
        except Exception as e:
            print(f"Error checking module installation {module} : {e}")
            return False


#if __name__ == "__main__":

def start_generate():
    path_yaml = input("Please enter the YAML file name: ")
    generator = ApacheConfigGenerator(path_yaml)
    generator.generate_apache_config()
