from flask import Blueprint, render_template, request, redirect

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    return render_template('lab9/index.html')

@lab9.app_errorhandler(404)
def not_found(e):
    return render_template('lab9/404.html'), 404

@lab9.app_errorhandler(500)
def error(e):
    return render_template('lab9/500.html'), 500

@lab9.route('/lab9/500')
def server_error():
    return render_template('lab9/500.html'), 500


@lab9.route('/lab9/form')
def form():
    user = request.args.get('user')
    user1 = request.args.get('user1')
    sex = request.args.get('sex')
    return render_template('lab9/form.html', user=user, user1=user1, sex=sex)

@lab9.route('/lab9/form_show')
def form_show():
    user = request.args.get('user')
    user1 = request.args.get('user1')
    sex = request.args.get('sex')
    return render_template('lab9/form_show.html', user=user, user1=user1, sex=sex)