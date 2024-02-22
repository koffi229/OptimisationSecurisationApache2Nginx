import modules.apache 

def make_config():
    try:
        choice = input("Please select the web service to be configured :\n1 - Apache2\n2 - Nginx\n")
        while choice not in ['1', '2']:
            choice = input("Invalid choice. Please choose between '1' and '2.\n")
        config = None
        if(choice == '1'):
            modules.apache.start()
        elif(choice == '2'):
            pass

        print("Configuration complete.")

    except Exception as e:
        print(f"An error has occurred: {e}. Please try again.")