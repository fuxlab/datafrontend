cd /app/frontend
yarn install
yarn start &

cd /app

# start background processing
python manage.py process_tasks & 

# start serving
python manage.py runserver 0.0.0.0:8000