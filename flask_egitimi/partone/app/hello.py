from flask import (Flask, 
	render_template, session, 
	redirect, url_for, flash
)

#eklentiler
from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.config.update(
	SECRET_KEY = "48fsdfs+dg5!423a-.das/",
	SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite",
	SQLALCHEMY_TRACK_MODIFICATIONS = True,
	DEBUG=True,
)

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)


class UserForm(FlaskForm):
	"""
	- Form sınıflarını tutacak olan moduldür.
	- Bu form sınıfları html formlarına karşılık gelir
	"""
	name = StringField('İsmini gir', validators=[DataRequired(), Length(3,20)])
	submit = SubmitField('Gönder')


class User(db.Model):
	"""
	- SQLAlchemy kütüphanesini kullanarak tablolara karşılık gelecek olan sınıflar
	oluşturulur.
	- Bu sınıflar db.Model sınıfından türetiliyor.
	- Her sınıf bir tabloya karşılık gelir.
	"""
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)


@app.route('/')
def index(name='Yabancı'):
	"""
	name değişkenine değer atanımışsa o kullanılıyor, atanmamışsa bilinmeyen kişi,
	anlamında Yabancı ismini veriyor
	"""
	if session.get('name'):
		name = session.get('name')
	return render_template('index.html', name=name)


@app.route('/kayıt', methods=['GET', 'POST'])
def register():
	"""
	Kayıt işlemlerini yapacak olan sayfanın view fonksiyonu.
	form verileri post metodu ile gelince, form alanı olarak `name` alanımız var,
	bunun içerisindeki verileri almak için `form.name.data` kullanıyoruz.
	form gönderme işleminden sonra `/` index view fonksiyonuna yönlendiriyoruz(redirect).
	"""
	form = UserForm()
	if form.validate_on_submit():
		name = form.name.data
		session["name"] = name
		return redirect(url_for('index'))
	return render_template('register.html', form=form)


@app.route('/veritabanına-kayıt', methods=['GET', 'POST'])
def register_todb():
	"""
	Veritabanına kayıt eden view fonksiyonu
	"""
	form = UserForm()
	if form.validate_on_submit():
		user = User(username=form.name.data)
		db.session.add(user)
		db.session.commit()
		session["name"] = user.username
		flash("Kullanıcı veritabanına kaydedildi.")
		return redirect(url_for('index'))
	return render_template('registertodb.html', form=form)


@app.route('/user/<username>')
def user(username):
	"""
	url de yazılan kullanıcı ismi veri tabanında varsa geriye bilgileri gönderilir
	"""
	# veritabanında eşleşen ilk kaydı geri dönderir
	user = User.query.filter_by(username=username).first()
	return render_template('user.html', user=user)


if __name__ == '__main__':
    manager.run()
