rm -rf apps/account/migrations/*_initial.py
rm -rf apps/product/migrations/*_initial.py
rm -rf apps/address/migrations/*_initial.py
rm -rf apps/cart/migrations/*_initial.py

rm -f db.sqlite3
python3 manage.py makemigrations

python3 manage.py migrate