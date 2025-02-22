import os
import subprocess

github_repo = "https://github.com/amitz-git/telegram_bot.git"  # Replace with your repo URL
repo_dir = "telegram_bot"  # Replace with your repository folder name
script_name = "script.py"  # Replace with the name of your script

# Clone the repository if it doesn't exist
if not os.path.exists(repo_dir):
    print("Cloning repository...")
    subprocess.run(["git", "clone", github_repo])
else:
    print("Repository already exists. Pulling latest changes...")
    subprocess.run(["git", "-C", repo_dir, "pull"])

# Change directory to the repo
os.chdir(repo_dir)

# Generate requirements.txt
print("Generating requirements.txt...")
subprocess.run(["pip", "freeze", ">", "requirements.txt"], shell=True, check=True)

# Install dependencies (if needed)
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)

# Run the script
print(f"Running {script_name}...")
subprocess.run(["python", script_name])
