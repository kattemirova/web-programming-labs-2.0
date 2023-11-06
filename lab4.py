from flask import Blueprint, render_template, request
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4.html')


@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    if username == '':
        error = 'Введите имя пользователя!'
        return render_template('login.html', error=error, username=username, password=password)
    if password == '':
        error = 'Введите пароль!'
        return render_template('login.html', error=error, username=username, password=password)

    if username == 'alex' and password == '123':
        return render_template('success1.html', username=username)
    
    
    error = 'Неверный логин и/или пароль!'
    return render_template('login.html', error=error, username=username, password=password)

@lab4.route('/lab4/cold', methods = ['GET', 'POST'])
def cold():
    if request.method == 'GET':
        return render_template('cold.html')
    temperature = request.form.get('temperature')
    if temperature == '':
        error = 'Ошибка: не задана температура'
        return render_template('cold.html', error=error, temperature=temperature)

    if int(temperature) < -12:
        error = 'Не удалось установить температуру - слишком низкое значение'
        return render_template('cold.html', error=error, temperature=temperature)
    if int(temperature) > -1:
        error = 'Не удалось установить температуру - слишком высокое значение'
        return render_template('cold.html', error=error, temperature=temperature)
    if int(temperature) >= -12 and int(temperature) <= -9:
        return render_template('coldsuc1.html', temperature=temperature)
    if int(temperature) >= -8 and int(temperature) <= -5:
        return render_template('coldsuc2.html', temperature=temperature)
    if int(temperature) >= -4 and int(temperature) <= -1:
        return render_template('coldsuc3.html', temperature=temperature)
    error = 'Задайте температуру'
    return render_template('cold.html', error=error, temperature=temperature)

@lab4.route('/lab4/zerno', methods = ['GET', 'POST'])
def zerno():
    if request.method == 'GET':
        return render_template('zerno.html')
    price = 0 
    sk = 0
    weight = request.form.get('weight')
    zerno = request.form.get('zerno')
    if weight == '':
        error = 'Введите вес'
        return render_template('zerno.html', error=error, weight=weight)

    if zerno == 'Ячмень':
        price = 12000 * int(weight)
    elif zerno == 'Овес':
        price = 8500 * int(weight)
    elif zerno == 'Пшеница':
        price = 8700 * int(weight)
    else:
        price = 14000 * int(weight)

    if int(weight) > 50:
        price = price * 0.9
        sk = 10
    if int(weight) > 500:
        error = 'Извините, в данный момент такого количества нет в наличии'
        return render_template('zerno.html', error=error, weight=weight)
    if int(weight) <= 0:
        error = 'Неверное значение веса'
        return render_template('zerno.html', error=error, weight=weight)

    return render_template('zerno.html', sk=sk, price=price, zerno=zerno, weight=weight)
