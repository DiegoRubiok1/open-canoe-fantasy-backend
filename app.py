from flask import Flask, render_template
from extensions import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://fantasy:fantasy1223@localhost/fantasy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host="localhost", port= 3000, debug=True)