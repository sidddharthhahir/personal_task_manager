# Personal Task Manager - Setup Guide

## Quick Start

1. **Extract the ZIP file** to your desired location
2. **Open terminal/command prompt** and navigate to the project folder:
   ```bash
   cd personal_task_manager/task_manager
   ```

3. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate it
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create admin user (optional):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server:**
   ```bash
   python manage.py runserver
   ```

8. **Open your browser** and go to: `http://localhost:8000`

## Features Included

✅ User Registration & Login  
✅ Create, Edit, Delete Tasks  
✅ Mark Tasks as Complete  
✅ Task Filtering (All, Pending, Completed)  
✅ Due Date Support  
✅ Daily Motivational Quotes  
✅ Bootstrap UI with Responsive Design  
✅ AJAX Task Toggle (no page refresh)  
✅ Task Statistics Dashboard  

## Project Structure

```
personal_task_manager/
├── README.md
├── SETUP_GUIDE.md
└── task_manager/
    ├── manage.py
    ├── requirements.txt
    ├── task_manager/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── tasks/
        ├── models.py
        ├── views.py
        ├── urls.py
        ├── admin.py
        ├── templates/tasks/
        └── static/tasks/
```

## Troubleshooting

**Issue: ModuleNotFoundError**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt`

**Issue: Database errors**
- Delete `db.sqlite3` file
- Run migrations again: `python manage.py migrate`

**Issue: Static files not loading**
- Run: `python manage.py collectstatic`
- Check STATIC_URL in settings.py

## Next Steps

- Customize the CSS in `tasks/static/tasks/css/style.css`
- Add more features like task categories
- Deploy to a cloud platform like Heroku
- Add email notifications for due dates
