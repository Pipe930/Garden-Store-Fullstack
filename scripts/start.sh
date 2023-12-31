#!/bin/bash

# We move towards the root of the project
cd ..

# Creation of the virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate

# Installation of project dependencies
pip install -r requirements.txt

# Creation of the migrations folders
branch="./apps/branchs/migrations"
country="./apps/countries/migrations"
product="./apps/products/migrations"
sale="./apps/sales/migrations"
user="./apps/users/migrations"

# Condiciones si las carpetas existen
if [ ! -d "$branch" ]; then
    # Create the folder
    mkdir "$branch"
    branchfile="$branch/__init__.py"
    touch "$branchfile"
else
    echo "La carpeta $branch ya existe."
fi

if [ ! -d "$country" ]; then
    # Create the folder
    mkdir "$country"
    countryfile="$country/__init__.py"
    touch "$countryfile"
else
    echo "La carpeta $country ya existe."
fi

if [ ! -d "$product" ]; then
    # Create the folder
    mkdir "$product"
    productfile="$product/__init__.py"
    touch "$productfile"
else
    echo "La carpeta $product ya existe."
fi

if [ ! -d "$sale" ]; then
    # Create the folder
    mkdir "$sale"
    salefile="$sale/__init__.py"
    touch "$salefile"
else
    echo "La carpeta $sale ya existe."
fi

if [ ! -d "$user" ]; then
    # Create the folder
    mkdir "$user"
    userfile="$user/__init__.py"
    touch "$userfile"
else
    echo "La carpeta $user ya existe."
fi

# Creating the environment variable file path
env="./core/.env"

# Creating the environment variables file
touch "$env"

# User assignment of some environment variables
read -p "Ingrese el nombre de la base de datos: " name_database
read -p "Ingrese la contrasena de la base de datos: " password_database
echo "Para conseguir una secret key para el proyecto ingresa en esta pagina web"
echo "https://djecrety.ir"
read -p "Ingrese una secret key para el proyecto: " secret_key

# Create environment variables in the .env file
echo "NAME_DATABASE=$name_database"> "$env"
echo "USER_DATABASE=root">> "$env"
echo "PASSWORD_DATABASE=$password_database">> "$env"
echo "HOST_DATABASE=localhost">> "$env"
echo "PORT_DATABASE=3306">> "$env"
echo "SECRET_KEY=$secret_key">> "$env"
echo "DEBUG=True">> "$env"

# Creation of the files with the models
python manage.py makemigrations

# Creation of database tables
python manage.py migrate

# Creation of the super user
echo \n "Creacion del superusuario"
echo \n "Ingrese una contrasena"

python manage.py createsuperuser --username admin --first_name adminnombre --last_name adminapellido --email admin@gmail.com

# Project execution
python manage.py runserver
