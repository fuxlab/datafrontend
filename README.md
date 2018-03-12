Migrate DB:
docker-compose run web python manage.py migrate

Make Migration:
docker-compose run web python manage.py makemigrations results

Run Tests:
docker-compose run web python manage.py test

Docs:
Tuto: https://docs.djangoproject.com/en/1.10/intro/tutorial03/
Static: https://docs.djangoproject.com/en/1.10/howto/static-files/
Auth: https://docs.djangoproject.com/en/1.10/topics/auth/default/
https://docs.djangoproject.com/en/1.10/topics/auth/customizing/

https://hackernoon.com/creating-websites-using-react-and-django-rest-framework-b14c066087c7