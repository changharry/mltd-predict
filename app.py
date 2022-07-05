from flask import Flask

app = Flask(__name__)
from view import views

if __name__ == '__main__':
    app.run()
