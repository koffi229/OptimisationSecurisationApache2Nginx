import yaml
import os

#repertoire de travail
#rep = r"templates"
#os.chdir(rep)

class ConfigGenerator:
    def __init__(self):
        self.base_template = """
Worker:
    worker_processes: {worker_processes}
    worker_rlimit_nofile: {worker_rlimit_nofile}
Buffers:
    client_body_buffer_size: {client_body_buffer_size}
    client_header_buffer_size: {client_header_buffer_size}
    client_max_body_size: {client_max_body_size}
    large_client_header_buffers: {large_client_header_buffers}
Proxy:
    proxy_buffering: {proxy_buffering}
    proxy_buffer_size: {proxy_buffer_size}
    proxy_buffers: {proxy_buffers}
Timeout:
    client_body_timeout: {client_body_timeout}
    client_header_timeout: {client_header_timeout}
    keepalive_timeout: {keepalive_timeout}
    send_timeout: {send_timeout} 
    keepalive_requests: {keepalive_requests}
Compression:
    gzip: {gzip}
    gzip_types: {gzip_types}
TCP:
    sendfile: {sendfile}
    tcp_nodelay: {tcp_nodelay}
    tcp_nopush: {tcp_nopush}
events:
    worker_connections: {worker_connections}
ProxyCache:
    proxy_cache_path: {proxy_cache_path}
server: 
    proxy_cache: {proxy_cache}
    proxy_cache_valid: {proxy_cache_valid}
    listen_ipv6_80: "[::]:80"
    listen_ipv4_80: "80"
    listen_ipv6_443: "[::]:443 ssl http2"
    listen_ipv4_443: "443 ssl http2"
SSL:
    ssl_session_cache: {ssl_session_cache}
    ssl_session_timeout: {ssl_session_timeout}
    ssl_buffer_size: {ssl_buffer_size}
    ssl_stapling: {ssl_stapling}
    ssl_stapling_verify: {ssl_stapling_verify}
    resolver: {resolver}
    resolver_timeout: {resolver_timeout}
http:
    server_tokens: "off"
    add_headers:
        - name: "X-Frame-Options"
          value: "SAMEORIGIN"
          always: true
        - name: "Strict-Transport-Security"
          value: "max-age=31536000"
        - name: "X-XSS-Protection"
          value: "1; mode=block"
        - name: "default-src"
          value: "'self' https: data: 'unsafe-inline' 'unsafe-eval' always"
        - name: "X-Content-Type-Options"
          value: "nosniff always"
          always: true
        - name: "proxy_hide_header"
          value: "X-Powered-By"
        - name: "more_clear_headers"
          value: "X-Powered-By"
        - name: "Referrer-Policy"
          value: "origin-when-cross-origin always"
          always: true
Security:
    ssl_protocols: {ssl_protocols}
    ssl_prefer_server_ciphers: {ssl_prefer_server_ciphers}
"""

    def generate_config(self, profile):
        self.base_template = self.base_template.format(
            worker_processes=self.get_worker_processes(profile),
            worker_rlimit_nofile=self.get_worker_rlimit_nofile(profile),
            client_body_buffer_size=self.get_client_body_buffer_size(profile),
            client_header_buffer_size=self.get_client_header_buffer_size(profile),
            client_max_body_size=self.get_client_max_body_size(profile),
            large_client_header_buffers=self.get_large_client_header_buffers(profile),
            proxy_buffering=self.get_proxy_buffering(profile),
            proxy_buffer_size=self.get_proxy_buffer_size(profile),
            proxy_buffers=self.get_proxy_buffers(profile),
            client_body_timeout=self.get_client_body_timeout(profile),
            client_header_timeout=self.get_client_header_timeout(profile),
            keepalive_timeout=self.get_keepalive_timeout(profile),
            send_timeout=self.get_send_timeout(profile),
            keepalive_requests=self.get_keepalive_requests(profile),
            gzip=self.get_gzip(profile),
            gzip_types=self.get_gzip_types(profile),
            sendfile=self.get_sendfile(profile),
            tcp_nodelay=self.get_tcp_nodelay(profile),
            tcp_nopush=self.get_tcp_nopush(profile),
            worker_connections=self.get_worker_connections(profile),
            proxy_cache_path=self.get_proxy_cache_path(profile),
            proxy_cache=self.get_proxy_cache(profile),
            proxy_cache_valid=self.get_proxy_cache_valid(profile),
            ssl_session_cache=self.get_ssl_session_cache(profile),
            ssl_session_timeout=self.get_ssl_session_timeout(profile),
            ssl_buffer_size=self.get_ssl_buffer_size(profile),
            ssl_stapling=self.get_ssl_stapling(profile),
            ssl_stapling_verify=self.get_ssl_stapling_verify(profile),
            resolver=self.get_resolver(profile),
            resolver_timeout=self.get_resolver_timeout(profile),
            server_tokens=self.get_server_tokens(profile),
            ssl_protocols=self.get_ssl_protocols(profile),
            ssl_prefer_server_ciphers=self.get_ssl_prefer_server_ciphers(profile),
        )

        with open(f"Nginx_{profile}_config.yaml", "w") as file:
            file.write(self.base_template)

    def get_worker_processes(self, profile):
        worker_processes_profiles = {
            "high": "auto",
            "moderate": "auto",
        }
        return worker_processes_profiles.get(profile, "")

    def get_worker_rlimit_nofile(self, profile):
        worker_rlimit_nofile_profiles = {
            "high": "100000",
            "moderate": "50000",
        }
        return worker_rlimit_nofile_profiles.get(profile, "")

    def get_client_body_buffer_size(self, profile):
        client_body_buffer_size_profiles = {
            "high": "16k",
            "moderate": "10k",
        }
        return client_body_buffer_size_profiles.get(profile, "")

    def get_client_header_buffer_size(self, profile):
        client_header_buffer_size_profiles = {
            "high": "3k",
            "moderate": "1k",
        }
        return client_header_buffer_size_profiles.get(profile, "")

    def get_client_max_body_size(self, profile):
        client_max_body_size_profiles = {
            "high": "20m",
            "moderate": "10m",
        }
        return client_max_body_size_profiles.get(profile, "")

    def get_large_client_header_buffers(self, profile):
        large_client_header_buffers_profiles = {
            "high": "2 3k",
            "moderate": "1 2k",
        }
        return large_client_header_buffers_profiles.get(profile, "")

    def get_proxy_buffering(self, profile):
        proxy_buffering_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return proxy_buffering_profiles.get(profile, "")

    def get_proxy_buffer_size(self, profile):
        proxy_buffer_size_profiles = {
            "high": "8k",
            "moderate": "4k",
        }
        return proxy_buffer_size_profiles.get(profile, "")

    def get_proxy_buffers(self, profile):
        proxy_buffers_profiles = {
            "high": "12 4k",
            "moderate": "6 2k",
        }
        return proxy_buffers_profiles.get(profile, "")

    def get_client_body_timeout(self, profile):
        client_body_timeout_profiles = {
            "high": "30s",
            "moderate": "15s",
        }
        return client_body_timeout_profiles.get(profile, "")

    def get_client_header_timeout(self, profile):
        client_header_timeout_profiles = {
            "high": "10",
            "moderate": "7",
        }
        return client_header_timeout_profiles.get(profile, "")

    def get_keepalive_timeout(self, profile):
        keepalive_timeout_profiles = {
            "high": "30",
            "moderate": "15",
        }
        return keepalive_timeout_profiles.get(profile, "")

    def get_send_timeout(self, profile):
        send_timeout_profiles = {
            "high": "60",
            "moderate": "30",
        }
        return send_timeout_profiles.get(profile, "")

    def get_keepalive_requests(self, profile):
        keepalive_requests_profiles = {
            "high": "100",
            "moderate": "75",
        }
        return keepalive_requests_profiles.get(profile, "")

    def get_gzip(self, profile):
        gzip_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return gzip_profiles.get(profile, "")

    def get_gzip_types(self, profile):
        gzip_types_profiles = {
            "high": " application/atom+xml application/javascript application/json application/ld+json application/manifest+json application/rss+xml application/vnd.geo+json application/vnd.ms-fontobject application/x-font-ttf application/x-web-app-manifest+json application/xhtml+xml application/xml font/opentype image/bmp image/svg+xml image/x-icon text/cache-manifest text/css text/plain text/vcard text/vnd.rim.location.xloc text/vtt text/x-component text/x-cross-domain-policy",
            "moderate": "text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript",}
        return gzip_types_profiles.get(profile, "")

    def get_sendfile(self, profile):
        sendfile_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return sendfile_profiles.get(profile, "")

    def get_tcp_nodelay(self, profile):
        tcp_nodelay_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return tcp_nodelay_profiles.get(profile, "")

    def get_tcp_nopush(self, profile):
        tcp_nopush_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return tcp_nopush_profiles.get(profile, "")

    def get_worker_connections(self, profile):
        worker_connections_profiles = {
            "high": "100000",
            "moderate": "50000",
        }
        return worker_connections_profiles.get(profile, "")

    def get_proxy_cache_path(self, profile):
        proxy_cache_path_profiles = {
            "high": "/var/cache/nginx levels=1:2 keys_zone=my_cache:10m inactive=60m;",
            "moderate": "/var/cache/nginx levels=1:2 keys_zone=my_cache:10m inactive=60m;",
        }
        return proxy_cache_path_profiles.get(profile, "")

    def get_proxy_cache(self, profile):
        proxy_cache_profiles = {
            "high": "my_cache",
            "moderate": "my_cache",
        }
        return proxy_cache_profiles.get(profile, "")

    def get_proxy_cache_valid(self, profile):
        proxy_cache_valid_profiles = {
            "high": "200 60m",
            "moderate": "200 60m",
        }
        return proxy_cache_valid_profiles.get(profile, "")

    def get_ssl_session_cache(self, profile):
        ssl_session_cache_profiles = {
            "high": "shared:SSL:10m",
            "moderate": "shared:SSL:10m",
        }
        return ssl_session_cache_profiles.get(profile, "")

    def get_ssl_session_timeout(self, profile):
        ssl_session_timeout_profiles = {
            "high": "24h",
            "moderate": "12h",
        }
        return ssl_session_timeout_profiles.get(profile, "")

    def get_ssl_buffer_size(self, profile):
        ssl_buffer_size_profiles = {
            "high": "1400",
            "moderate": "700",
        }
        return ssl_buffer_size_profiles.get(profile, "")

    def get_ssl_stapling(self, profile):
        ssl_stapling_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return ssl_stapling_profiles.get(profile, "")

    def get_ssl_stapling_verify(self, profile):
        ssl_stapling_verify_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return ssl_stapling_verify_profiles.get(profile, "")

    def get_resolver(self, profile):
        resolver_profiles = {
            "high": "8.8.8.8 8.8.4.4 216.146.35.35 216.146.36.36 valid=60s",
            "moderate": "8.8.8.8 8.8.4.4 216.146.35.35 216.146.36.36 valid=60s",
        }
        return resolver_profiles.get(profile, "")

    def get_resolver_timeout(self, profile):
        resolver_timeout_profiles = {
            "high": "2s",
            "moderate": "1s",
        }
        return resolver_timeout_profiles.get(profile, "")

    def get_server_tokens(self, profile):
        server_tokens_profiles = {
            "high": "off",
            "moderate": "off",
        }
        return server_tokens_profiles.get(profile, "")

    def get_ssl_protocols(self, profile):
        ssl_protocols_profiles = {
            "high": "TLSv1.2 TLSv1.3",
            "moderate": "TLSv1.2 TLSv1.3",
        }
        return ssl_protocols_profiles.get(profile, "")

    def get_ssl_prefer_server_ciphers(self, profile):
        ssl_prefer_server_ciphers_profiles = {
            "high": "on",
            "moderate": "on",
        }
        return ssl_prefer_server_ciphers_profiles.get(profile, "")
  
def start():
    generator = ConfigGenerator()
    def sortie(choice):
        print(f"Configuration generate in folder templates with name : Nginx_{choice}_config.yaml")
    def choix_config():
        print("\nTwo types of profiles exist: high, moderate\n \n1 - high: (>=8 GB ram ; Octa-Core)) \n2 - moderate: (>=4 GB Ram ; Quad-Core))\n")
        profile_var = input("Choose your configuration profil (1 - 2): ")
        if profile_var == "1":
            chx = "high"
            sortie(chx)
        elif profile_var == "2":
            chx = "moderate"
            sortie(chx)
        else:
            print("Please choose between 1 and 3")
        return generator.generate_config(chx)
    choix_config()
