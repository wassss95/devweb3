from urllib import request
from flask import Flask, render_template
from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
#db.init_app(app)

class Data(db.Model):
    __tabname = "data"

    id           = db.Column(db.Integer, primary_key=True)
    rna_id       = db.Column(db.String(30), nullable=True)
    rna_id_ex_id = db.Column(db.String(30), nullable=True)
    gestion      = db.Column(db.String(20), nullable=True)

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/edit/<id>' ,methods=['GET','POST'])
def edit(id):
  data = Data.query.get(id)

  if request.method == 'POST':
    data.rna_id = request.form['rna_id']
    data.rna_id_ex_id = request.form['rna_id_ex_id']
    data.gestion = request.form['gestion']
    db.session.commit()
    return redirect(url_for('assos'))
  return render_template('edit.html', data=data)

@app.route('/add', methods=['GET','POST'])
def add():
  if request.method == 'POST':
        rna_id = request.form['rna_id']
        rna_id_ex_id = request.form['rna_id_ex_id']
        gestion = request.form['gestion']
        new_data = Data(rna_id=rna_id, rna_id_ex_id=rna_id_ex_id, gestion=gestion)
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('assos'))
  return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
  data=Data.query.get(id)
  db.session.delete(data)
  db.session.commit()
  return redirect(url_for('assos'))

@app.route('/assos')
def assos():
  datas = Data.query.limit(10).all()
  for data in datas:
    print(f"{data.rna_id}")
  
  #stmt = select(Data)
  #result = db.session.execute(stmt)
  #for data in result.scalars():
    #print(f"{data.rna_id}")

  return render_template('assos.html', datas=datas)  

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)

if __name__ == '__main__':
  app.run()