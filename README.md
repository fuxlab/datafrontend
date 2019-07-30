# Datafrontend

Datafrontend is a holistic solution to manage data for your machine learning products.


Migrate DB:

    docker-compose run datafrontend python manage.py migrate

Make Migration:

    docker-compose run datafrontend python manage.py makemigrations results

Run Tests:

    docker-compose run datafrontend python manage.py test

Show All Routes:

    docker-compose run datafrontend python manage.py show_urls

Recreate JS-Files (and keep watching):

    docker-compose up datafrontend
    docker-compose exec datafrontend bash > cd frontend && yarn build

Run Tasks:

    docker-compose run datafrontend python manage.py process_tasks



Docs:
Tuto: https://docs.djangoproject.com/en/1.10/intro/tutorial03/
Static: https://docs.djangoproject.com/en/1.10/howto/static-files/
Auth: https://docs.djangoproject.com/en/1.10/topics/auth/default/
https://docs.djangoproject.com/en/1.10/topics/auth/customizing/

Webpack
https://medium.com/@biswashirok/blending-django-with-react-front-end-739cad2e3d30
https://medium.com/code-oil/burning-questions-with-answers-to-why-webpack-dev-server-live-reload-does-not-work-6d6390277920

React:
http://v1k45.com/blog/modern-django-part-1-setting-up-django-and-react/
http://v1k45.com/blog/modern-django-part-2-redux-and-react-router-setup/
http://v1k45.com/blog/modern-django-part-3-creating-an-api-and-integrating-with-react/