(cd /app/frontend && npm install)
(cd /app/frontend && npm start) &

# start background processing
(cd /app && python manage.py process_tasks) & 

# start serving django app
(cd /app && python manage.py runserver 0.0.0.0:8000)
