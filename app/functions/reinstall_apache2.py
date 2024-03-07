import os
import time
import itertools

def display_phase(phase):
    print(f"\nPhase {phase}: ", end="", flush=True)

def continuous_animation(animation_chars, duration):
    start_time = time.time()
    for char in itertools.cycle(animation_chars):
        if time.time() - start_time > duration:
            break
        print(f"\r{char} Processing", end="", flush=True)
        time.sleep(0.1)

def execute_command(command):
    start_time = time.time()
    os.system(command)
    end_time = time.time()
    return end_time - start_time

def stop_apache2():
    display_phase("Stopping Apache2")
    duration = execute_command("sudo systemctl stop apache2 > /dev/null 2>&1")
    continuous_animation(["⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"], duration)

def uninstall_apache2():
    display_phase("Uninstalling Apache2")
    duration = execute_command("sudo apt-get purge apache2 -y > /dev/null 2>&1")
    execute_command("sudo apt-get autoremove -y > /dev/null 2>&1")
    
    # Removing remaining directories related to Apache2
    output = os.popen("whereis apache2").read()
    directories = output.split(':')[1].split()
    for directory in directories:
        if os.path.exists(directory):
            print(f"Removing directory: {directory}")
            os.system(f"sudo rm -rf {directory}")

    continuous_animation(["□", "■"], duration)

def install_apache2():
    display_phase("Reinstalling Apache2")
    duration = execute_command("sudo apt-get update > /dev/null 2>&1")
    execute_command("sudo apt-get install apache2 -y > /dev/null 2>&1")
    execute_command("sudo dpkg -S /usr/sbin/apache2 > /dev/null 2>&1")
    execute_command("sudo apt install --reinstall apache2-bin -y > /dev/null 2>&1")
    duration += execute_command("sudo systemctl start apache2 > /dev/null 2>&1")
    continuous_animation(["□", "■"], duration)

def processing_reinstalltion():
    try:
        print("Starting the uninstallation and reinstallation of Apache2...")
        stop_apache2()
        uninstall_apache2()
        install_apache2()
        print("\nApache2 has been uninstalled and reinstalled successfully.")
    except Exception as e:
        print("An error occurred:", e)
