@echo off
del /s /q apps\account\migrations\0001_initial.py
del /s /q apps\product\migrations\0001_initial.py
del /s /q apps\address\migrations\0001_initial.py

del db.sqlite3
python manage.py makemigrations
python manage.py migrate