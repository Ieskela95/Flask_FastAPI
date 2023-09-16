from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from forms_ex_1 import LoginForm, RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY'] = b'9b15f576d3fe61bd4b0dffd9230689db54cdbe38de825044d52a966eeee75d7f'
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'Hello'


# @app.route('/form', methods=['GET', 'POST'])
# @csrf.exempt
# def my_form():
#     return 'No csrf protection !'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        print(request.form.get('username'))
        print(request.form.get('password'))

    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        email = form.email.data
        password = form.password.data
        print(email, password)
    ...
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
