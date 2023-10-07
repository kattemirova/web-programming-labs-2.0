from flask import Flask, redirect, url_for, render_template
from lab1 import lab1

app = Flask(__name__)
app.register_blueprint(lab1)

@app.route('/lab2/example')
def example():
    name, number,  group, kurs = 'Темирова Екатерина, Пахомова Валерия', 2, 'ФБИ-11', '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    
    books = [
        {'avtor': 'Кирилл Кутузов', 'name': 'Бесобой', 'zanr': 'Фантастика', 'str': 240},
        {'avtor': 'Борис Акунин', 'name': 'Азазель', 'zanr': 'Детектив', 'str': 272},
        {'avtor': 'Борис Акунин', 'name': 'Турецкий гамбит', 'zanr': 'Военный/Приключения', 'str': 208},
        {'avtor': 'Борис Акунин', 'name': 'Левиафан', 'zanr': 'Детектив', 'str': 624},
        {'avtor': 'Дженнифер Линн Барнс', 'name': 'Последний гамбит', 'zanr': 'Триллер', 'str': 416},
        {'avtor': 'Николай Калиниченко', 'name': 'Королевский гамбит', 'zanr': 'Спорт/Самооборона', 'str': 416},
        {'avtor': 'Элизабет Фримантл', 'name': 'Гамбит королевы', 'zanr': 'Исторические романы', 'str': 480},
        {'avtor': 'Мамлеев Юрий', 'name': 'Московский гамбит', 'zanr': 'Роман', 'str': 296},
        {'avtor': 'Евгений Руднев', 'name': 'Сибирский гамбит', 'zanr': 'Биография', 'str': 288},
        {'avtor': 'Ерофей Трофимов', 'name': 'Лесной гамбит', 'zanr': 'Роман', 'str': 310},
    ]

    return render_template('example.html', name=name, number=number, group=group, kurs=kurs, fruits=fruits, books=books)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/vina')
def vina():
    return render_template('vina.html')

@app.route('/lab2/zac')
def zac():
    a=9.2
    b=1.8
    c=2.9
    K=5
    N=5
    return render_template('zac.html', a=a, b=b, c=c, K=K, N=N)