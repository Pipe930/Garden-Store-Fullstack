@REM Project Creation

@echo off

@REM Virtual environment name
set "nombre_entorno=env"

@REM We move towards the root of the project
cd ..

@REM Creation of the virtual environment
python -m venv %nombre_entorno%

@REM Activate the virtual environment
call %nombre_entorno%\Scripts\activate.bat

@REM Installation of project dependencies
pip install -r requirements.txt

@REM Folder path assignment
set "branch=.\apps\branchs\migrations"
set "country=.\apps\countries\migrations"
set "product=.\apps\products\migrations"
set "voucher=.\apps\sales\migrations"
set "user=.\apps\users\migrations"

@REM Creation of the migrations folders
if exist "%branch%" (
    echo La carpeta "migrations" ya existe.
) else (
    mkdir .\apps\branchs\migrations
)

if exist "%country%" (
    echo La carpeta "migrations" ya existe.
) else (
    mkdir .\apps\countries\migrations
)

if exist "%product%" (
    echo La carpeta "migrations" ya existe.
) else (
    mkdir .\apps\products\migrations
)

if exist "%voucher%" (
    echo La carpeta "migrations" ya existe.
) else (
    mkdir .\apps\sales\migrations
)

if exist "%user%" (
    echo La carpeta "migrations" ya existe.
) else (
    mkdir .\apps\users\migrations
)

@REM Designation of variables of the paths of the __init__.py files
set "init_branch=%branch%\__init__.py"
set "init_country=%country%\__init__.py"
set "init_product=%product%\__init__.py"
set "init_voucher=%voucher%\__init__.py"
set "init_user=%user%\__init__.py"

@REM Creation of the __init__.py files inside the migrations folders
echo. > "%init_branch%"
echo. > "%init_country%"
echo. > "%init_product%"
echo. > "%init_voucher%"
echo. > "%init_user%"

@REM Creating the environment variables
set "archivoenv=.\core\.env"

@REM Enter information for environment variables
set /p "name_database=Ingrese el nombre de la base de datos: "
set /p "password_database=Ingrese la contrsena de la base de datos: "
echo "Para conseguir una secret key para el proyecto ingresa en esta pagina web"
echo "https://djecrety.ir"
set /p "secretkey=Ingrese la secret key del proyecto: "

@REM Create environment variables in the .env file
echo NAME_DATABASE='%name_database%'> "%archivoenv%"
echo USER_DATABASE=root>> "%archivoenv%"
echo PASSWORD_DATABASE='%password_database%'>> "%archivoenv%"
echo HOST_DATABASE=localhost>> "%archivoenv%"
echo PORT_DATABASE=3306>> "%archivoenv%"
echo SECRET_KEY=%secretkey%>> "%archivoenv%"
echo DEBUG=True>> "%archivoenv%"

@REM Creation of the files with the models
python manage.py makemigrations

@REM Creation of database tables
python manage.py migrate

@REM Creation of the super user

echo "Creacion del superusuario"
echo "Ingrese una contrasena"
python manage.py createsuperuser --username admin --first_name adminnombre --last_name adminapellido --email admin@gmail.com

@REM Project execution
python manage.py runserver
