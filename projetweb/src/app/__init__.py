from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
import json
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

@app.route('/edit/<int:id>' ,methods=['GET','POST'])
def edit(id):
  data = Data.query.get(id)
  if request.method == 'POST':
    data.rna_id = request.form['rna_id']
    data.rna_id_ex_id = request.form['rna_id_ex_id']
    data.gestion = request.form['gestion']
    db.session.commit()
    return redirect(url_for('assos'))
  
  return render_template('edit.html', data=data)


@app.route('/add' ,methods=['GET','POST'])
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

@app.route('/delete/<id>',methods=['GET','POST'])
def delete(id):
  data = Data.query.get(id)
  db.session.delete(data)
  db.session.commit()
  return redirect(url_for('assos'))



@app.route('/assos')
def assos():
  datas = Data.query.limit(20).all()
  for data in datas:
    print(f"{data.rna_id}")

  return render_template('assos.html', datas=datas)  

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
  return render_template('hello.html', name=name)


@app.route('/tableau')
def tableau():
  return render_template('tableau.html')


@app.route('/gestion')
def gestion():
  return render_template('gestion.html')



@app.route('/cercle')
def cercle():
    datas = Data.query.all()
    gestion_count = {}
    for d in datas:
        if d.gestion in gestion_count:
            gestion_count[d.gestion] += 1
        else:
            gestion_count[d.gestion] = 1

    gestion_values = list(gestion_count.values())
    gestion_labels = list(gestion_count.keys())
    data = {
        'values': gestion_values,
        'labels': gestion_labels
    }
    return render_template('cercle.html', graph_data=json.dumps(data))



if __name__ == '_main_':
    app.run()