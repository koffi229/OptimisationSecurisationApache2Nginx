import modules.apache 

def make_config():
    try:
        choice = input("Veuillez choisir le service Web à configurer :\n1 - Apache2\n2 - Nginx\n")
        while choice not in ['1', '2']:
            choice = input("Choix non valide. Veuillez choisir entre '1' et '2'.\n")
        config = None
        if(choice == '1'):
            modules.apache.start()
        elif(choice == '2'):
            pass

        print("Configuration terminée.")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}. Veuillez réessayer s'il vous plaît.")