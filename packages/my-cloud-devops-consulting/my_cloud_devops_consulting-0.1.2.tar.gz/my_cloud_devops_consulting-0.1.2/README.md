# Cloud & DevOps Consulting

This project is a website for Cloud & DevOps consulting services. It is built with **Flask** for the backend, **MongoDB** for the database, and **Docker** for containerization.

## Features

- Cloud consulting services
- DevOps solutions
- Security & Compliance consulting

## Prerequisites

Before getting started, make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/products/docker-desktop)
- [Git](https://git-scm.com/)
- [MongoDB](https://www.mongodb.com/try/download/community) (if you're not using MongoDB Atlas)
- [pip](https://pip.pypa.io/en/stable/)
- [twine](https://twine.readthedocs.io/en/stable/) (for uploading to PyPI)

## Installation

### 1. Clone the Repository

Clone this repository to your local machine using Git:
```bash
git clone https://github.com/Betrand1999/project-root.git
cd project-root
,,,
####
Setup Python Environment
python3 -m venv venv
source venv/bin/activate  # For Windows use `venv\Scripts\activate`
#####

####
Install Dependencies
pip install -r requirements.txt
###


###
 Set Up Python Package Build Tools
 The setup.py file is where you define the details of your package, including its dependencies, description, version, and more.
###

###
MANIFEST.in
he MANIFEST.in file ensures that the necessary files are included when you build your package.
###

###
Build the Package
python setup.py sdist bdist_wheel
###

###
Upload to PyPI (Optional)
If you want to distribute your package on PyPI, you'll need a PyPI account. After registering and logging in to PyPI, use twine to upload the distribution files.
Install Twine: pip install twine
Upload the Package:
twine upload dist/*
###

##################################################################
pip install wheel
#################################################################
To  see packages OutPUT
ls dist/
project-root-0.1.0.tar.gz  
project_root-0.1.0-py3-none-any.whl
###################################################################

pip install dist/project_root-0.1.0-py3-none-any.whl
####################################################################

pip install twine
what is twine: Twine is a utility for publishing Python packages on the Python Package Index (PyPI)
#####################################################################
twine upload dist/my_cloud_devops_consulting-0.1.1-py3-none-any.whl

#############################################################################
How route are configure in apache2
sudo vi /etc/apache2/sites-available/000-default.conf



<VirtualHost *:80>
    ServerAdmin webmaster@localhost

    # Default application
    ProxyPreserveHost On
    ProxyPass / http://localhost:8080/
    ProxyPassReverse / http://localhost:8080/

    # Application running on port 9090
    ProxyPass /app2 http://localhost:9090/
    ProxyPassReverse /app2 http://localhost:9090/

    # Logging
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


# Enable both configurations and restart Apache:

bash
Copy code
sudo a2ensite app1.conf
sudo a2ensite app2.conf
sudo systemctl restart apache2


 # sudo systemctl restart apache2

####################################################
https://www.youtube.com/watch?v=3j33lNzMZlM&t=308s
####################################################