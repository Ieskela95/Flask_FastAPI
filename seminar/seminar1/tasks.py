from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('hello.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/contact/')
def contacts():
    return render_template('contact.html')


@app.route('/add-nums/<int:num>/<int:num2>')
def add_nums(num, num2):
    return str(num+num2)


@app.route('/str-len/<str_inp>')
def str_len(str_inp):
    return str(len(str_inp))


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/students/')
def students():
    _students = [
        {
            "name": "John",
            "surname": "Doe",
            "age": 20,
            "average": 85
        },
        {
            "name": "Jane",
            "surname": "Smith",
            "age": 22,
            "average": 92
        },
    ]
    context = {'students': _students}
    return render_template('students.html', **context)


@app.route('/news/')
def news():
    _news = [
        {
            "title": "article 1",
            "descr": "Text",
            "date": 2010
        },
        {
            "title": "article 2",
            "descr": "Text",
            "date": 2020
        },
        {
            "title": "article 3",
            "descr": "Text",
            "date": 2030
        },
    ]
    context = {'news': _news}
    return render_template('news.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
