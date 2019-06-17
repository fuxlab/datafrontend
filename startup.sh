cd /app/frontend
yarn install
yarn start &

cd /app
python manage.py runserver 0.0.0.0:8000