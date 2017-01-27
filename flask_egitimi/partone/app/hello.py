from flask import Flask, render_template, session, redirect, url_for

#eklentiler
from flask_bootstrap import Bootstrap
from flask_moment import Moment 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length 

app = Flask(__name__)
app.config.update(
	SECRET_KEY = "48fsdfs+dg5!423a-.das/",
	)

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
	name = StringField('İsmini gir', validators=[DataRequired(), Length(3,20)])
	submit = SubmitField('Gönder')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kayıt', methods=['GET', 'POST'])
def register():
	"""
	Kayıt işlemlerini yapacak olan sayfanın view fonksiyonu.
	form verileri post metodu ile gelince, form alanı olarak `name` alanımız var,
	bunun içerisindeki verileri almak için `form.name.data` kullanıyoruz.
	form gönderme işleminden sonra `/` index view fonksiyonuna yönlendiriyoruz(redirect).
	"""
	form = NameForm()
	if form.validate_on_submit():
		name = form.name.data
		session["name"] = name
		return redirect(url_for('index'))
	return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

