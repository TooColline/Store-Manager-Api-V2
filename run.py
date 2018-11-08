import os
from app import create_app
from app.api.v2.models.users import UserModels
from app.api.v2.db import initialize_db

app = create_app(os.getenv('FLASK_ENV'))

if __name__ == '__main__':
    app.run()