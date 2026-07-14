#Placement Portal

Run the backend:

```bash
cd backend
venv/bin/python app.py
```

Run Redis, Celery worker, and Celery beat for background jobs:

```bash
redis-server
cd backend
venv/bin/celery -A controllers.tasks.celery worker --loglevel=info
venv/bin/celery -A controllers.tasks.celery beat --loglevel=info
```

Run the frontend:

```bash
cd frontend
npm run dev
```

