from flask import Flask, render_template,redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db=SQLAlchemy(app)
#db.init_app(app)

class Data(db.Model):
    __tablename__ = "data"

    id = db.Column(db.Integer, primary_key=True)
    rna_id = db.Column(db.String(30), nullable=True) 
    rna_id_ex = db.Column(db.String(30), nullable=True)
    gestion = db.Column(db.String(20), nullable=True)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/assos')
def assos():
    #stmt = select(Data)
    #datas = Data.query.limit(10).all()
    datas = Data.query.limit(10).all()
  
    return render_template('assos.html', datas=datas)
    #result = db.session.execute(stmt)
    #for data in datas:
     #   print(f"{data.rna_id}")
    #return render_template('assos.html')


@app.route('/delete_data/<int:id>', methods=['POST'])
def delete_data(id):
    data = Data.query.get_or_404(id)

    if request.method == 'POST':
        # Supprimer la ligne et rediriger vers la page principale
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('assos'))

    # Sinon, afficher un formulaire pour confirmer la suppression
    return render_template('delete_data.html', data=data)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
if __name__ == '__main__':
    app.run()  


@app.route('/liste')
def liste():
    return render_template('liste.html') 


if __name__ == '-_main_-':
    app.run()
