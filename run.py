import os
from app import create_app
from app.api.v2.models.users import UserModels
from app.api.v2.db import initialize_db

app = create_app(os.getenv('FLASK_ENV'))

admin = {
    'email': 'defaultadmin@gmail.com',
    'password': '123456'
}


if __name__ == '__main__':
    initialize_db()

    if not UserModels.checkifuserexists(admin):
        UserModels.create_admin(admin)
        
    app.run()