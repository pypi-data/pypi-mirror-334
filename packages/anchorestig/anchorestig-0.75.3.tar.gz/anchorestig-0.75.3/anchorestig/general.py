import shutil
import importlib.util
import os
import tarfile
import subprocess as sp

def sync_policies():
    package_name = "anchorestig"
    spec = importlib.util.find_spec(package_name)
    package_root_directory = os.path.dirname(spec.origin)
    try:
        sp.run(["docker", "run", "--rm", "-d", "--name=policies", "anchore/combined-stig:latest", "sleep", "1000"])
        sp.run(["docker", "cp", "policies:policies/.", f"{package_root_directory}/policies"])
        sp.run(["docker", "kill", "policies"])
        directories = [d for d in os.listdir(f'{package_root_directory}/policies') if os.path.isdir(os.path.join(f'{package_root_directory}/policies', d))]
        print("\nAvailable profiles are:")
        for directory in directories:
            if directory != "input_templates":
                print(directory)
        print("\n")
    except Exception:
        print("Unauthorized to pull Anchore policies. Please login with the provided Docker credentials and try again.")
        exit()

def sync_profiles_from_tar(tar_path):
    package_name = "anchorestig"
    spec = importlib.util.find_spec(package_name)
    package_root_directory = os.path.dirname(spec.origin)
    try:
        file = tarfile.open(tar_path)
        file.extractall(f"{package_root_directory}")
        directories = [d for d in os.listdir(f'{package_root_directory}/policies') if os.path.isdir(os.path.join(f'{package_root_directory}/policies', d))]
        print("\nAvailable profiles are:")
        for directory in directories:
            if directory != "input_templates":
                print(directory)
        print("\n")
    except Exception:
        print("Unable to extract tarred policies. Please try again.")
        exit()

def check_saf_installed():
    # Check if 'saf' binary is available in PATH
    saf_path = shutil.which('saf')
    
    if saf_path:
        print(f"'saf' is installed at: {saf_path}")
    else:
        print("'saf' is not installed. If running this tool in a disconnected environment, please cancel this run with CTRL+C and manually install before proceeding.")
        
        # Prompt user to install via Homebrew or npm
        choice = input("Do you want to install 'saf' via Homebrew (1) or npm (2)? Enter 1 or 2: ")
        
        if choice == '1':
            install_command = "HOMEBREW_NO_AUTO_UPDATE=1 brew install mitre/saf/saf-cli"
        elif choice == '2':
            install_command = "npm install -g @mitre/saf"
        else:
            print("Invalid choice. Please enter 1 for Homebrew or 2 for npm.")
            return
        
        try:
            # Run the chosen installation command
            sp.run(install_command, shell=True, check=True)
            print(f"'saf' has been installed successfully using {install_command}.")
        except sp.CalledProcessError as e:
            print(f"Installation failed: {e}")

def check_cinc_installed():
    # Check if 'saf' binary is available in PATH
    cinc_path = shutil.which('cinc-auditor')
    
    if cinc_path:
        print(f"'CINC' is installed at: {cinc_path}")
    else:
        print("'CINC Auditor' is not installed. Please install this using `anchorestig provision --install`.")