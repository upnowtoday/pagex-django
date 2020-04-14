# PageX-Django

## Prerequisites
1. [Python 3.x](https://www.python.org/) (recommended Python 3.6)
2. [MongoDB 3.6](https://www.mongodb.com/) (or higher)

## How to?
1. clone the project
```
git clone git@gitlab.com:page-x/pagex-django.git
```

2. create a virtual environment and install requirements
```
virtualenv pagex-venv
source pagex-venv/bin/activate
pip install -r requirements.txt
```

3. edit the `.env-dev` file and update the environment values accordingly

4. run migrations
```bash
python manage.py migrate
```

5. create a superuser
```bash
python manage.py createsuperuser
```
this command will prompt for input from user, provide necessary value 

6. start the development server
```bash
python manage.py runserver
```

## API documentation
As of now, we are using the documentation tool provided by the [**Postman**](https://www.postman.com/)
.
You can find the doc [**here**](https://documenter.getpostman.com/view/8096111/SzS4R7ET?version=latest)