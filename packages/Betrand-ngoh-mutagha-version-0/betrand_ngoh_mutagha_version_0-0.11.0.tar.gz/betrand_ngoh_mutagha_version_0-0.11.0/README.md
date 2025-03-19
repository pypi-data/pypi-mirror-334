###
git clone https://github.com/yourusername/your-repo.git
###
cd your-repo

####
Go to steup.py edit the version
Go to setup edit the user name
with python cannot rebuild artifact project with same name
######




####
Build the Project
python3 -m venv venv
source venv/bin/activate


 ####
 It downloads and installs the package from PyPI into your local Python environment.
 pip install <setup_project_name> same name in pypi
#####

#####
to run it locally
python -m <the_root_directory_name_that_contain_your_application_with.app> 
example python -m hello_world_app.app

#####
In cloud 

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt



###### Here is a README.md file that documents the process of setting up and managing your self-hosted GitHub Actions runner on Ubuntu. ##
# GitHub Actions Self-Hosted Runner on Ubuntu

This repository contains instructions and automation for setting up a **self-hosted GitHub Actions runner** on an Ubuntu instance. The setup ensures that the runner **automatically starts** on reboot and remains **persistently registered** with GitHub.

## **1. Setup Instructions**
### **1.1 Install the GitHub Actions Runner**
Run the following commands to install and configure the self-hosted runner:

```bash
# Create a working directory
mkdir actions-runner && cd actions-runner

# Download the latest GitHub Actions Runner
curl -o actions-runner-linux-x64-2.322.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.322.0/actions-runner-linux-x64-2.322.0.tar.gz

# Verify checksum
echo "b13b784808359f31bc79b08a191f5f83757852957dd8fe3dbfcc38202ccf5768  actions-runner-linux-x64-2.322.0.tar.gz" | shasum -a 256 -c

# Extract the runner files
tar xzf ./actions-runner-linux-x64-2.322.0.tar.gz

 Register the Runner with GitHub
 ./config.sh --url https://github.com/Betrand1999/cicd --token YOUR_NEW_GITHUB_TOKEN
./run.sh

### Automating the Runner with systemd ###
sudo nano /etc/systemd/system/github-runner.service
[Unit]
Description=GitHub Actions Runner Auto Start
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/actions-runner
ExecStartPre=/bin/bash -c 'if [ ! -f /home/ubuntu/actions-runner/.credentials ]; then /home/ubuntu/actions-runner/config.sh --url https://github.com/Betrand1999/cicd --token YOUR_NEW_GITHUB_TOKEN; fi'
ExecStart=/home/ubuntu/actions-runner/run.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
###
sudo systemctl daemon-reload
sudo systemctl enable github-runner.service
sudo systemctl start github-runner.service
sudo systemctl status github-runner.service
stop and start instance