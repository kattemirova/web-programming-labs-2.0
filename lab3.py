from flask import Blueprint, redirect, url_for, render_template, request
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    return render_template ('lab3.html')


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0 
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    return render_template('success.html')


@lab3.route('/lab3/rzd')
def rzd():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
     
   

    viezd = request.args.get('viezd')
    if viezd == '':
        errors['viezd'] = 'Заполните поле!'

    vezd = request.args.get('vezd')
    if vezd == '':
        errors['vezd'] = 'Заполните поле!'

    data = request.args.get('data')
    if data == '':
        errors['data'] = 'Заполните поле!'

    price = 0 
            
    tip = request.args.get('tip')
    if tip == 'Детский':
        price = 500
    else:
        price = 1000

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    elif tip=='Взрослый' and int(age) < 18:
        errors['age'] = 'Перевоз несовершеннолетних без сопровождения взрослых не допустим!'
    elif tip == 'Взрослый' or tip == 'Детский' and int(age) > 120:
        errors['age'] = 'Ошибка'

    polka = request.args.get('polka')
    if polka == 'Нижняя полка':
        price += 1700
    elif polka == 'Верхня полка':
        price += 1400
    elif polka == 'Верхняя боковая полка':
        price +=  1200
    else:
        price += 1500

    bagaz = request.args.get('bagaz')
    if bagaz == 'Да':
        price += 300
    else:
        price += 0

    return render_template('rzd.html', price=price, errors=errors, user=user, age=age, viezd=viezd, vezd=vezd, data=data, tip=tip, polka=polka, bagaz=bagaz)
    
    



