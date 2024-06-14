import os
from colorama import Fore, Style, init

def display_banner():
    banner = fr'''
{Fore.RED}
__________         .__                   .__                 
\______   \_____   |  |    ____  _______ |__|  ____    ____  
 |    |  _/\__  \  |  |  _/ __ \ \_  __ \|  | /  _ \  /    \ 
 |    |   \ / __ \_|  |__\  ___/  |  | \/|  |(  <_> )|   |  \
 |______  /(____  /|____/ \___  > |__|   |__| \____/ |___|  /
        \/      \/            \/                          \/ 

                                      
{Fore.YELLOW}                  Apache2 && Nginx Optimization and Security Tool
{Style.RESET_ALL}    '''

    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)