import os

PORT = int(os.environ.get('PORT', 8080))
DB_URL = os.environ.get('DB_URL')
DB_NAME = os.environ.get('DB_NAME', "GoExplore")
