import os
from colorama import Fore, Style, init

def display_banner():
    banner = fr'''
{Fore.GREEN}
  ___ ___                                 .__           
 /   |   \   ____  _______   ____   __ __ |  |    ____  
/    ~    \_/ __ \ \_  __ \_/ ___\ |  |  \|  |  _/ __ \ 
\    Y    /\  ___/  |  | \/\  \___ |  |  /|  |__\  ___/ 
 \___|_  /  \___  > |__|    \___  >|____/ |____/ \___  >
       \/       \/              \/                   \/                                        
{Fore.YELLOW}         Outil d'Optimisation et de Sécurisation Apache2 && Nginx
{Style.RESET_ALL}    '''

    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)