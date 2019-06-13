cd /app/frontend
yarn install
yarn build
yarn start &

cd /app
python manage.py runserver 0.0.0.0:8000