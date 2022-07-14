from flask import Flask

app = Flask(__name__)

app.secret_key = "your password better not be pa55word"