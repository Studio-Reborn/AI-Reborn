from flask import Flask
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
    app.run(
        host="0.0.0.0",
        port=int(os.getenv('FLASK_RUN_PORT', 5000)), 
        debug=os.getenv('DEBUG', 'False') == 'True'  
    )
