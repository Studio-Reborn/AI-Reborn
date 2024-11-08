from flask import Flask, request
from dotenv import load_dotenv
import os
from app.api.swagger import api

load_dotenv()
app = Flask(__name__)

@app.route('/')
def Reborn():
    return 'Reborn'

api.init_app(app)

if __name__ == '__main__':
    app.run(port=os.getenv('FLASK_RUN_PORT'), debug=os.getenv('DEBUG'))
