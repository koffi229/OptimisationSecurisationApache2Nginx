import os

class ApacheConfigCleaner:
    def __init__(self, config_directory='/etc/apache2/conf-available/', apache2_conf_path='/etc/apache2/apache2.conf'):
        self.config_directory = config_directory
        self.apache2_conf_path = apache2_conf_path

    def remove_configs(self):
        config_files = ['mpm_config.conf', 'security_config.conf', 'general_config.conf']
        for config_file in config_files:
            file_path = os.path.join(self.config_directory, config_file)
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    print(f"The files {config_file} was delete with success.")
                except Exception as e:
                    print(f"Error during the suppresion of file {config_file} : {e}")
            #else:
                #print(f"Le fichier {config_file} n'existe pas.")

    def remove_inclusions(self):
        try:
            with open(self.apache2_conf_path, 'r') as apache2_conf:
                lines = apache2_conf.readlines()

            new_lines = [line for line in lines if not any(file_name in line for file_name in ['mpm_config.conf', 'security_config.conf', 'general_config.conf'])]

            with open(self.apache2_conf_path, 'w') as apache2_conf:
                apache2_conf.writelines(new_lines)

            print("Inclusions was deleted with success in apache2.conf.")
        except Exception as e:
            print(f"An error occurred while deleting inclusions in apache2.conf : {e}")

#if __name__ == "__main__":
def cleaner():
    cleaner = ApacheConfigCleaner()
    cleaner.remove_configs()
    cleaner.remove_inclusions()
