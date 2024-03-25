import shutil
import os

def restore_nginx_conf():
    # Check if backup file exists
    if os.path.exists('nginx.conf.backup'):
        # Check if current configuration file exists
        if os.path.exists('nginx.conf'):
            # Remove current configuration file
            os.remove('nginx.conf')
        # Restore from backup
        shutil.copy('nginx.conf.example', 'nginx.conf')
        print("nginx.conf has been successfully restored.")
    else:
        print("nginx.conf.backup file does not exist.")

def main():
    print("This program will restore nginx.conf from nginx.conf.backup.")
    confirmation = input("Are you sure you want to continue? (yes/no): ")
    if confirmation.lower() == "yes":
        restore_nginx_conf()
    else:
        print("Operation cancelled.")

#if __name__ == "__main__":
 #   main()
