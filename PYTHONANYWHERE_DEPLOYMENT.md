# PythonAnywhere Deployment Guide

This guide will help you fix all the issues and successfully deploy your Django project on PythonAnywhere.

## 📋 Current Issues Identified

Based on your error logs, here are the issues that need to be fixed:

1. ❌ WSGI file has incorrect placeholder paths (`YOUR_USERNAME`)
2. ❌ Missing `python-decouple` package
3. ❌ `ALLOWED_HOSTS` not configured (now fixed locally)
4. ❌ `STATIC_ROOT` not configured (now fixed locally)
5. ❌ Missing database migrations (`cart_feedback` table)

## 🔧 Step-by-Step Fix Instructions

### Step 1: Push Updated Code to GitHub

First, commit and push your updated `settings.py`:

```powershell
git add moviesstore/settings.py pythonanywhere_wsgi.py PYTHONANYWHERE_DEPLOYMENT.md
git commit -m "Fix PythonAnywhere deployment settings"
git push origin main
```

### Step 2: Pull Latest Code on PythonAnywhere

On PythonAnywhere, open a **Bash console** and run:

```bash
cd /home/UjaanRakshit/ujaan-moviesstore
git pull origin main
```

### Step 3: Install Missing Dependencies

In the same Bash console, install the required package:

```bash
pip3.10 install --user python-decouple
```

Or if you have a `requirements.txt`:

```bash
pip3.10 install --user -r requirements.txt
```

### Step 4: Set Up Environment Variables

Create a `.env` file in your project root:

```bash
cd /home/UjaanRakshit/ujaan-moviesstore
nano .env
```

Add these variables (update with your actual values):

```env
SECRET_KEY=your-secret-key-here
DEBUG=False
GOOGLE_MAPS_API_KEY=your-google-maps-api-key-here
```

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 5: Run Database Migrations

```bash
cd /home/UjaanRakshit/ujaan-moviesstore
python3.10 manage.py migrate
```

### Step 6: Collect Static Files

```bash
python3.10 manage.py collectstatic --noinput
```

### Step 7: Fix WSGI Configuration

1. Go to your **Web** tab on PythonAnywhere
2. Click on the **WSGI configuration file** link (should be `/var/www/ujaanrakshit_pythonanywhere_com_wsgi.py`)
3. **Delete ALL the contents** of that file
4. Copy and paste the contents from `pythonanywhere_wsgi.py` (the file I just created in your project)
5. Click **Save**

The correct WSGI configuration should look like this:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/UjaanRakshit/ujaan-moviesstore'
if path not in sys.path:
    sys.path.insert(0, path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'moviesstore.settings'

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 8: Configure Static Files Mapping

In the **Web** tab:

1. Scroll to the **Static files** section
2. Add a new entry:
   - **URL**: `/static/`
   - **Directory**: `/home/UjaanRakshit/ujaan-moviesstore/staticfiles`

3. Add another entry for media files:
   - **URL**: `/media/`
   - **Directory**: `/home/UjaanRakshit/ujaan-moviesstore/media`

### Step 9: Set Up Virtual Environment (If Using One)

If you're using a virtual environment:

1. In the **Web** tab, find the **Virtualenv** section
2. Enter the path: `/home/UjaanRakshit/.virtualenvs/your-venv-name`
   
   OR create a new one:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 moviesstore-venv
   pip install -r /home/UjaanRakshit/ujaan-moviesstore/requirements.txt
   ```

### Step 10: Reload Your Web App

1. Go to the **Web** tab
2. Click the big green **Reload** button
3. Wait for the reload to complete

### Step 11: Test Your Application

Visit: `https://ujaanrakshit.pythonanywhere.com`

## 🐛 Troubleshooting

### Check Error Logs

If something goes wrong, check the logs:

1. Go to the **Web** tab
2. Click on **Error log** or **Server log**
3. Look for the most recent errors

### Common Issues

**Issue: ModuleNotFoundError**
- Solution: Make sure all packages are installed with `pip3.10 install --user package-name`

**Issue: Database errors**
- Solution: Run migrations again: `python3.10 manage.py migrate`

**Issue: Static files not loading**
- Solution: 
  1. Run `python3.10 manage.py collectstatic --noinput`
  2. Check static files mapping in Web tab
  3. Reload the web app

**Issue: DisallowedHost errors**
- Solution: Your `settings.py` already has this fixed with `ALLOWED_HOSTS`

## 📝 Checklist

- [ ] Updated code pushed to GitHub
- [ ] Latest code pulled on PythonAnywhere
- [ ] `python-decouple` installed
- [ ] `.env` file created with proper values
- [ ] Database migrations run
- [ ] Static files collected
- [ ] WSGI file updated correctly
- [ ] Static files mapping configured
- [ ] Virtual environment set up (if using)
- [ ] Web app reloaded
- [ ] Website tested and working

## 🎉 Success!

Once all steps are complete, your Django application should be running successfully on PythonAnywhere!

## 📚 Additional Resources

- [PythonAnywhere Django Help](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
