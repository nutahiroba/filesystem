from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import wc
import pathlib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.todo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# class ToDo(db.Model):
# 	id = db.Column(db.Integer, primary_key=True)
# 	todo = db.Column(db.String(128), nullable=False)

class File(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  path = db.Column(db.String(128), nullable = False)
  cutwords = db.Column(db.JSON)


# @app.route('/')
# def index():
# 	data = ToDo.query.all()
# 	print(data)
# 	return render_template('todo.html',data=data)

@app.route('/')
def index():
	p = pathlib.Path(r"C:\Users\nutta\OneDrive\ドキュメント\授業資料")
	file_list = list(p.glob("*.docx"))
	#for line in file_list:


# @app.route('/add', methods=['POST'])
# def add():
# 	todo = request.form['todo']
# 	new_todo = ToDo(todo=todo)
# 	db.session.add(new_todo)
# 	db.session.commit()
# 	return redirect(url_for('index'))
	
# @app.route('/del_todo/<int:id>')
# def del_todo(id):
# 	del_data = ToDo.query.filter_by(id=id).first()
# 	db.session.delete(del_data)
# 	db.session.commit()
# 	return redirect(url_for('index'))
	

if __name__ == '__main__':
	#db.create_all()
	app.run()