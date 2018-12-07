

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

React:
http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/
http://v1k45.com/blog/modern-django-part-2-redux-and-react-router-setup/