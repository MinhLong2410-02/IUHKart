rm -rf apps/customers/migrations/0001_initial.py
rm -rf apps/vendor/migrations/0001_initial.py
rm -rf apps/product/migrations/0001_initial.py
rm -rf apps/address/migrations/0001_initial.py

rm -f db.sqlite3
python3 manage.py makemigrations

python3 manage.py migrate