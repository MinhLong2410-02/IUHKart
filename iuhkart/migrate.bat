@echo off
del /s /q apps\account\migrations\*_initial.py
del /s /q apps\product\migrations\*_initial.py
del /s /q apps\address\migrations\*_initial.py
del /s /q apps\cart\migrations\*_initial.py
del /s /q apps\review\migrations\*_initial.py


del db.sqlite3
python manage.py makemigrations
python manage.py migrate