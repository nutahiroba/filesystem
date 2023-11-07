from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('testdb.config')

db = SQLAlchemy(app)

from .models import employee  # 追加

import testdb.views
