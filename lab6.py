from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, redirect
import psycopg2
from Db import db
from sqlalchemy import desc
from flask_login import login_user, login_required, logout_user, current_user
from Db.models import users, articles, favorites, likes
import string

lab6 = Blueprint('lab6', __name__)

@lab6.route("/lab6/check")
def check():
    my_users = users.query.all()
    print(my_users)
    return "result in console!"

@lab6.route("/lab6/checkarticles")
def art():
    my_articles = articles.query.all()
    print(my_articles)
    return "result in console!"

@lab6.route("/lab6/register", methods=["GET", "POST"])
def register():
    errors ={}
    if request.method == "GET":
        return render_template("register_orm.html")
    username_form = request.form.get("username")
    password_form = request.form.get("password")
    isUserExist = users.query.filter_by(username = username_form).first()
    if isUserExist is not None:
        errors = "Пользователь с таким именем уже существует"
        return render_template("register_orm.html", errors=errors)
    if not (username_form or password_form):
        errors = "Пожалуйста, заполните все поля"
        return render_template("register_orm.html", errors=errors)
    if len(password_form) <= 5:
        errors = "Пароль должен содержать больше пяти символов"
        return render_template("register_orm.html", errors=errors)
    hashedPswd = generate_password_hash(password_form, method = "pbkdf2")
    newUser = users(username = username_form, password = hashedPswd)
    db.session.add(newUser)
    db.session.commit()
    return redirect("/lab6/login")

@lab6.route("/lab6/login", methods = ["GET", "POST"])
def login():
    errors = {}
    if request.method == "GET":
        return render_template("login_orm.html")
    username_form = request.form.get("username")
    password_form = request.form.get("password")
    my_user = users.query.filter_by(username = username_form).first()
    if not (username_form or password_form):
        errors = "Пожалуйста, заполните все поля"
        return render_template("login_orm.html", errors=errors)
    if my_user is not None:
        if check_password_hash(my_user.password, password_form):
            login_user(my_user, remember = False)
            return redirect("/lab6/articles")
        else:
            errors = "Неправильный пароль"
            return render_template("login_orm.html", errors=errors)
    else:
        errors = "Пользователя не существует"
        return render_template("login_orm.html", errors=errors)
    

@lab6.route("/lab6/articles")
@login_required
def articles_list():
    my_articles = articles.query.filter_by(user_id = current_user.id).all()
    return render_template("list_articles_orm.html", articles = my_articles, username = current_user.username)

@lab6.route("/lab6/articles/<int:article_id>")
@login_required
def article_details(article_id):
    my_articles = articles.query.get(article_id)
    if my_articles:
        if  my_articles.is_public or (my_articles.user_id == current_user.id):
            return render_template("text_articles_orm.html", article=my_articles, username=current_user.username)
        else:
            return "Автор ограничил доступ к этой статье"
    else:
        return "Not found!"

@lab6.route("/lab6/logout")
@login_required
def logout():
    logout_user()
    return redirect("/lab6")

@lab6.route("/lab6/new_article", methods = ["GET", "POST"])
@login_required
def createArticle():
    errors = {}    
    if request.method == "GET":
        return render_template("new_article_orm.html", username = current_user.username)
    if request.method == "POST":
        text_article = request.form.get("text_article")
        title = request.form.get("title_article")
        is_public = 'is_public' in request.form 
        if len(text_article) == 0:
            errors = 'Заполните текст'
            return render_template("new_article_orm.html", errors=errors, username = current_user.username)

        newArticles = articles(user_id = current_user.id, title = title, article_text = text_article, is_public = is_public)
        db.session.add(newArticles)
        db.session.commit()
        return redirect(f"/lab6/articles/{newArticles.id}")

@lab6.route("/lab6")
def main():
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = "Anon"
    return render_template('glav_orm.html', username=username)

@lab6.route("/lab6/public_articles")
@login_required
def get_public_articles():
    userID = current_user.id
    public_articles = db.session.query(
        articles.id,
        articles.title,
        (favorites.article_id != None).label('favorited_by_current_user'),
        (likes.article_id != None).label('liked_by_current_user'),
        articles.likes.label('like_count')
    ).outerjoin(favorites, ((articles.id == favorites.article_id) & (favorites.user_id == userID))).outerjoin(likes, ((articles.id == likes.article_id) & (likes.user_id == userID))).filter(articles.is_public == True).order_by(desc('favorited_by_current_user'), desc(articles.id)).all()
    return render_template('public_articles_orm.html', public_articles=public_articles, username = current_user.username)

@lab6.route('/lab6/favorite_article/<int:article_id>', methods=['POST'])
@login_required
def favoriteArticle(article_id):
    userID = current_user.id
    favorite_article = favorites.query.filter_by(user_id=userID, article_id=article_id).first()
    if favorite_article is None:  
        favorite_article = favorites(user_id=userID, article_id=article_id)
        db.session.add(favorite_article)
    else:
        db.session.delete(favorite_article)
    db.session.commit()
    return redirect('/lab6/public_articles')

@lab6.route('/lab6/like_article/<int:article_id>', methods=['POST'])
def likeArticle(article_id):
    userID = current_user.id
    like_article = likes.query.filter_by(user_id=userID, article_id=article_id).first()
    if like_article is None:  
        like_article = likes(user_id=userID, article_id=article_id)
        db.session.add(like_article)
        article = articles.query.get(article_id)
        article.likes = db.func.coalesce(articles.likes, 0) + 1
    else:
        db.session.delete(like_article)
        article = articles.query.get(article_id)
        article.likes = db.func.coalesce(articles.likes, 0) - 1
    db.session.commit()
    return redirect('/lab6/public_articles')

    

