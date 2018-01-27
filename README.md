this is a blog webapp with basic blog functionalities
#for trying it on your system

Use a directory & inside directory you can type following commands:

# to initialize
1. git init

#to clone project
2. git clone https://github.com/robin-rawat/blog_advanced.git

#use virtualenv to use separate environment with selected or required dependability(packages)
#virtualenv install link=https://virtualenv.pypa.io/en/stable/installation/
#remember virtualenv is optional

#to create vitualenv 
3.virtualenv -p python3.6.2 env_name  //-p represents python version to use inside virualenv

#to activate virtualenv
4. source env_name/bin/activate 

#browse to siteb directory and type to install required packages in virtualenv
5. pip install -r requirements.txt

#run the site using
6. python manage.py runserver

#oOh!getting errors
#remember no database file is in the appdata. it means no data is being stored and so no data will be shown
#so you need to make migrations on data models in order to create and store posts data

#to do that
7. python manage.py makemigrations
8. python manage.py migrate

!all set!
  >..<


