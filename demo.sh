python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask create_dummy_user
flask run
