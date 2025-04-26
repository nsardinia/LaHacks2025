 # Change to the directory where this script is located
cd "$(dirname "$0")" || { echo "Failed to change directory. Exiting."; exit 1; }

echo "Now in the script's directory: $(pwd)"

# Install Dependencies
sudo apt update -y && sudo apt upgrade -y
sudo apt install ffmpeg -y

pip install -r ../requirements.txt --break

