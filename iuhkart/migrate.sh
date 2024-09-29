rm -rf apps/account/migrations/*_initial.py
rm -rf apps/product/migrations/*_initial.py
rm -rf apps/address/migrations/*_initial.py
rm -rf apps/cart/migrations/*_initial.py
rm -rf apps/review/migrations/*_initial.py
rm -rf apps/discount/migrations/*_initial.py
rm -rf apps/order/migrations/*_initial.py
rm -rf apps/dashboard/migrations/*_initial.py

python3 manage.py makemigrations

python3 manage.py migrate