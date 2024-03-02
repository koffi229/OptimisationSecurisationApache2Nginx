import yaml
import os

#repertoire de travail
rep = r"templates"
os.chdir(rep)

#creation de la classe

class ConfigGenerator:
    def __init__(self):
        self.base_template = """
Profil: {profile}
Options: {Options}
HostnameLookups: {HostnameLookups}
AllowOverride: {AllowOverride}
EnableMMAP: {EnableMMAP}
EnableSendfile: {EnableSendfile}
Modules:
  mpm: {modules_mpm}
  mod_cache: {mod_cache}
  mod_reqtimeout: {mod_reqtimeout}
  mod_atomic: {mod_atomic}
  mod_deflate: {mod_compression}
MPM_Modules:
  StartServers: {StartServers}
  MinSpareThreads: {MinSpareThreads}
  MaxSpareThreads: {MaxSpareThreads}
  ThreadLimit: {ThreadLimit}
  ThreadsPerChild: {ThreadsPerChild}
  MaxConnectionsPerChild: {MaxConnectionsPerChild}
  MaxRequestWorkers: {MaxRequestWorkers}
  ServerLimit: {ServerLimit}
KeepAlive:
  enabled: {KeepAlive}
  timeout: {KeepAliveTimeout}
  max_requests: {MaxKeepAliveRequests}
Server:
  ServerSignature: {ServerSignature}
  ServerTokens: {ServerTokens}
  TraceEnable: {TraceEnable}
Security:
  SSLProtocol: {SSLProtocol}
  SSLCipherSuite: {SSLCipherSuite}
  SSLHonorCipherOrder: {SSLHonorCipherOrder}
  StrictTransportSecurity: {StrictTransportSecurity}
  expose_php: {expose_php}
Rules: 
  XFrameOptions: {XFrameOptions}
  XContentTypeOptions: {XContentTypeOptions}
"""

    def generate_config(self, profile):
        mpm_module = self.get_profile_values(profile)
        specific_module = f"{mpm_module[0]}"

        mpm_module_values = self.get_mpm_module(profile)


        # Valeur du template à revoir
        self.base_template = self.base_template.format(
            profile=profile,
            Options=f"{self.get_options(profile)}",
            HostnameLookups=f"{self.get_hostname_lookups(profile)}",
            AllowOverride=f"{self.get_allow_override(profile)}",
            EnableMMAP=f"{self.get_enable_mmap(profile)}",
            EnableSendfile=f"{self.get_enable_sendfile(profile)}",
            modules_mpm=specific_module,
            mod_cache=f"{self.get_enable_mod_cache(profile)}",
            mod_reqtimeout=f"{self.get_enable_mod_reqtimeout(profile)}",
            mod_atomic=f"{self.get_enable_mod_atomic(profile)}",
            mod_compression=f"{self.get_enable_mod_compression(profile)}",
            StartServers=mpm_module_values.get('start_servers', ''),
            MinSpareThreads=mpm_module_values.get('min_spare_threads', ''),
            MaxSpareThreads=mpm_module_values.get('max_spare_threads', ''),
            ThreadLimit=mpm_module_values.get('thread_limit', ''),
            ThreadsPerChild=mpm_module_values.get('threads_per_child', ''),
            MaxConnectionsPerChild=mpm_module_values.get('max_connections_per_child', ''),
            MaxRequestWorkers=mpm_module_values.get('max_request_workers', ''),
            ServerLimit=mpm_module_values.get('server_limit', ''),
            KeepAlive=f"{self.get_keep_alive(profile)}",
            KeepAliveTimeout=f"{self.get_keep_alive_timeout(profile)}",
            MaxKeepAliveRequests=f"{self.get_max_keep_alive_requests(profile)}",
            ServerSignature=f"{self.get_server_signature(profile)}",
            ServerTokens=f"{self.get_server_tokens(profile)}",
            #Timeout=f"{self.get_timeout(profile)}",
            TraceEnable=f"{self.get_trace_enable(profile)}",
            #################################################
            SSLProtocol=f"{self.get_ssl_protocol(profile)}",
            SSLCipherSuite=f"{self.get_ssl_cipher_suite(profile)}",
            SSLHonorCipherOrder=f"{self.get_ssl_honor_cipher_order(profile)}",
            StrictTransportSecurity=f"{self.get_strict_transport_security(profile)}",
            XFrameOptions=f"{self.get_x_frame_options(profile)}",
            XContentTypeOptions=f"{self.get_x_content_type_options(profile)}",
            expose_php=f"{self.get_expose_php(profile)}",
        )

##############################################
          #Creation du YAML File
        with open(f"{profile}_config.yaml", "w") as file:
            file.write(self.base_template)


##############################################            

    # Methodes pour recuperer les valeurs specifiques du profil
    def get_profile_values(self, profile):
        profiles = {
            "high": ("event", "800"),
            "low": ("prefork", "200"),
            "moderate": ("worker", "100"),
        }
        return profiles[profile]
    
    def get_enable_mod_cache(self, profile):
        enable_mod_cache_profiles = {
            "high" : "True",
            "low" : "False",
            "moderate" : "True",
        }
        return enable_mod_cache_profiles.get(profile, "")
    
    def get_enable_mod_reqtimeout(self, profile):
        enable_mod_reqtimeout_profiles = {
            "high" : "True",
            "low" : "True",
            "moderate" : "True",
        }
        return enable_mod_reqtimeout_profiles.get(profile, "")
    
    def get_enable_mod_atomic(self, profile):
        enable_mod_atomic_profiles = {
            "high" : "False",
            "low" : "False",
            "moderate" : "True",

        }
        return enable_mod_atomic_profiles.get(profile, "")
    

    def get_enable_mod_compression(self, profile):
        enable_mod_compression_profiles = {
            "high" : "True",
            "low" : "True",
            "moderate" : "True",

        }
        return enable_mod_compression_profiles.get(profile, "")



    def get_options(self, profile):
        options_profiles = {
            "high": "-FollowSymLinks +SymLinksIfOwnerMatch -Indexes",
            "low": "+FollowSymLinks -Indexes",
            "moderate": "-FollowSymLinks +SymLinksIfOwnerMatch -Indexes",
        }
        return options_profiles.get(profile, "")

    def get_hostname_lookups(self, profile):
        hostname_profiles = {
            "high": "On",
            "low": "Off",
            "moderate": "Off",
        }
        return hostname_profiles.get(profile, "")

    def get_allow_override(self, profile):
        override_profiles = {
            "high": "all",
            "low": "None",
            "moderate": "None",
        }
        return override_profiles.get(profile, "")

    def get_enable_mmap(self, profile):
        mmap_profiles = {
            "high": "On",
            "low": "Off",
            "moderate": "Off",
        }
        return mmap_profiles.get(profile, "")

    def get_enable_sendfile(self, profile):
        sendfile_profiles = {
            "high": "Off",
            "low": "On",
            "moderate": "On",
        }
        return sendfile_profiles.get(profile, "")

    def get_keep_alive(self, profile):
        keep_alive_profiles = {
            "high": "On",
            "low": "Off",
            "moderate": "On",
        }
        return keep_alive_profiles.get(profile, "")

    def get_keep_alive_timeout(self, profile):
        timeout_profiles = {
            "high": "5",
            "low": "15",
            "moderate": "10",
        }
        return timeout_profiles.get(profile, "")

    def get_max_keep_alive_requests(self, profile):
        max_requests_profiles = {
            "high": "150",
            "low": "50",
            "moderate": "75",
        }
        return max_requests_profiles.get(profile, "")

    def get_server_signature(self, profile):
        return "Off"

    def get_server_tokens(self, profile):
        return "Prod"

    #def get_timeout(self, profile):
     #   timeout_profiles = {
      #      "high": "60",
       #     "low": "60",
        #    "moderate": "45",
        #}
        return timeout_profiles.get(profile, "")

    def get_trace_enable(self, profile):
        trace_profiles = {
            "high": "Off",
            "low": "On",
            "moderate": "Off",
        }
        return trace_profiles.get(profile, "")

    def get_mpm_module(self, profile):
        profiles = {
            "high": {"module": "event", "start_servers": 4, "min_spare_threads": 25, "max_spare_threads": 75, "thread_limit": 64, "threads_per_child": 25, "max_request_workers": 800, "server_limit": 32, "max_connections_per_child": 10000},
            "low": {"module": "prefork", "start_servers": 4, "min_spare_threads": 20, "max_spare_threads": 40, "max_request_workers": 200, "max_connections_per_child": 4500},
            "moderate": {"module": "worker", "start_servers": 4, "min_spare_threads": 25, "max_spare_threads": 75, "thread_limit": 64, "threads_per_child": 25, "max_request_workers": 100, "server_limit": 32, "max_connections_per_child": 1000}
        }
        return profiles.get(profile, {})
    

    ###########################################Security######################################################

    def get_ssl_protocol(self, profile):
        ssl_protocol_profiles = {
            "high": "all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1",
            "low": "all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1",
            "moderate": "all -SSLv2 -SSLv3 -TLSv1 -TLSv1.1",
        }
        return ssl_protocol_profiles.get(profile, "")

    def get_ssl_cipher_suite(self, profile):
        ssl_cipher_suite_profiles = {
            "high": "hIGH:3DES:!aNULL:!MD5:!SEED:!IDEA",
            "low": "hIGH:3DES:!aNULL:!MD5:!SEED:!IDEA",
            "moderate": "hIGH:3DES:!aNULL:!MD5:!SEED:!IDEA",
        }
        return ssl_cipher_suite_profiles.get(profile, "")
    
    def get_ssl_honor_cipher_order(self, profile):
        ssl_honor_cipher_order_profiles = {
            "high": "on",
            "low": "on",
            "moderate": "on",
        }
        return ssl_honor_cipher_order_profiles.get(profile, "")
    
    def get_strict_transport_security(self, profile):
        strict_transport_security_profiles = {
            "high": "Header always set Strict-Transport-Security max-age=15552000; includeSubDomains",
            "low": "Header always set Strict-Transport-Security max-age=15552000; includeSubDomains",
            "moderate": "Header always set Strict-Transport-Security max-age=15552000; includeSubDomains",
        }
        return strict_transport_security_profiles.get(profile, "")
    
    def get_x_frame_options(self, profile):
        x_frame_options_profiles = {
            "high": "Header always set X-Frame-Options DENY",
            "low": "Header always set X-Frame-Options DENY",
            "moderate": "Header always set X-Frame-Options DENY",
        }
        return x_frame_options_profiles.get(profile, "")
    
    def get_x_content_type_options(self, profile):
        x_content_type_options_profiles = {
            "high": "Header always set X-Content-Type-Options nosniff",
            "low": "Header always set X-Content-Type-Options nosniff",
            "moderate": "Header always set X-Content-Type-Options nosniff",
        }
        return x_content_type_options_profiles.get(profile, "")
    def get_expose_php(self, profile):
        expose_php_profiles = {
            "high": "Off",
            "low": "Off",
            "moderate": "Off",
        }
        return expose_php_profiles.get(profile, "")

    

# Exemple d'utilisation
def start():
    generator = ConfigGenerator()
    def choix_config():
        print("\nThree types of profiles exist: high, low, moderate\n \n1 - high: Concerns servers with good hardware configuration \n2 - low: Concerns servers with low hardware configuration \n3 - moderate: It's a moderatee of configuration between the first option and the second \n")
        profile_var = input("Choose your configuration profil ( 1 - 3): ")
        if profile_var == "1":
            chx = "high"
        elif profile_var == "2":
            chx = "low"
        elif profile_var == "3":
            chx = "moderate"
        else:
            print("Please choose between 1 and 3")
        return generator.generate_config(chx)
    choix_config()
    print(f"Configuration generate in folder: {rep}")
    