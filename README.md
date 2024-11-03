# Purpose
The purpose and the goal of this project is to
- extract information from KIT Campus Management system
- set up a database for further automatic processing of information
- provide a platform/an app that notifies user if something changes, after subscribing to relevant notifications
- provide a platform/an app where you can easily find relevant WhatsApp and Signal groups for lectures and laboratories
- provide a platform/an app where you can easily find and share ilias passwords and other relevant information
- provide a platform/an app where you can set up a shared community calendar where changes can be made by all users to update information of events as soon as possible with notification option if someone changed an event
  - background 1: responsible people for lectures are not able to set up a flexible schedule for their lectures so they write their schedule on the homepage of their institute
  - background 2: responsible people for lectures are not able to notifiy people through Campus if a lecture room or time or anything changes
  - background 3: users can't merge their private or work calendar into Campus calendar so selecting lectures at the start of the semester is cumbersome
- provide a platform/an app that integrates a mailing system for xxxxx@student.kit.edu addresses with notification feature

# set up build system
```
# Install dependencies
conda env create --prefix .conda -f install_environment/environment.yml

# Clone pdf2htmlEX repository
TEMP_DIR=$(mktemp -d)
git clone https://github.com/telmop/pdf2htmlEX.git $TEMP_DIR/pdf2htmlEX
cd $TEMP_DIR/pdf2htmlEX
./buildScripts/buildInstallLocallyApt

# Install Google Chrome
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Install Docker using apt
install_docker() {
  # Set up Docker's apt repository.
  # Add Docker's official GPG key:
  sudo apt-get update
  sudo apt-get install -y ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
  sudo chmod a+r /etc/apt/keyrings/docker.asc

  # Add the repository to Apt sources:
  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo \"$VERSION_CODENAME\") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update

  # To install the latest version, run:
  sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

  # enable and start docker service
  sudo systemctl enable docker
  sudo systemctl start docker
  sudo systemctl status docker

  # Verify that the installation is successful by running the hello-world image:
  sudo docker run hello-world
}

set_up_postgres() {
  docker pull postgres
  docker run --name my-postgres -e POSTGRES_PASSWORD=my_password -d -p 5432:5432 postgres
}

install_docker
set_up_postgres

# see also .github/workflows/python-app.yml
```

# recommended build environment
- debian based os
- VSCode

# update environment.yml
```
python install_environment/clean_yml.py
```

# remove conda environment
```
conda env remove -p .conda
```

# update conda environment
```
conda env update --file install_environment/environment.yml -p ./.conda
```

# How to convert pip packages into conda packages
Try to not use pip together with conda!
Instead convert pip packages into conda packages.
- pip2conda
- grayskull