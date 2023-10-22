from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Prozorro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t = db.Column(db.String(120))
    tl = db.Column(db.String(120))
    cpv = db.Column(db.String(120))
    v = db.Column(db.String(20))
    a = db.Column(db.String(20))
    s = db.Column(db.String(120))
    t_id = db.Column(db.String(21))
    cdb = db.Column(db.String(50))
    t_method = db.Column(db.String(50))
    
    def to_dict(self):
        
        return {
            "id": self.id,
            "t": self.t,
            "tl": self.tl,
            "cpv": self.cpv,
            "v": self.v,
            "a": self.a,
            "s": self.s,
            "t_id": self.t_id,
            "cdb": self.cdb,
            "t_method": self.t_method 
        }


db.create_all()


@app.route('/')
def index():
    return render_template('pro_table.html')


@app.route('/api/data')
def data():
    return {'data': [user.to_dict() for user in Prozorro.query]}


if __name__ == '__main__':
    app.run()
