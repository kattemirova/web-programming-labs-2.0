from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, redirect, session
from flask_session import Session
import psycopg2

lab5 = Blueprint('lab5', __name__)

def dbConnect():
    conn = psycopg2.connect(
        host = "127.0.0.1",
        database = "knowledge_base_temirova_pakhomova",
        user = "temirova_pakhomova_knowledge_base",
        password = "123"
    )
    return conn;

def dbClose(cursor, connection):
    cursor.close()
    connection.close()

@lab5.route("/lab5")
def main():
    username = "Anon"
    return render_template ('glav.html', username=username)

@lab5.route('/lab5/users')
def users():
    conn = dbConnect()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    users = [row[0] for row in cur.fetchall()]
    dbClose(cur, conn)


    return render_template('users.html', users=users)

@lab5.route('/lab5/register', methods=["GET", "POST"])
def registerPage():
    errors = []

    if request.method == "GET":
        return render_template("register.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append("Пожалуйста, заполните все поля")
        print(errors)
        return render_template("register.html", errors=errors)

    hashPassword = generate_password_hash(password)
    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT username FROM users WHERE username = %s", (username,))

    if cur.fetchone() is not None:
        errors.append("Пользователь с данным именем уже существует")

        conn.close()
        cur.close()
        
        return render_template("register.html", errors=errors)

    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashPassword))

    conn.commit()
    conn.close()
    cur.close()

    return redirect("/lab5/login")

@lab5.route('/lab5/login', methods = ["GET", "POST"])
def login():
    errors = []

    if request.method == "GET":
        return render_template("login.html", errors=errors)

    username = request.form.get("username")
    password = request.form.get("password")

    if not (username or password):
        errors.append('Пожалуйста, заполните все поля')
        return render_template("login.html", errors=errors)

    conn = dbConnect()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))

    result = cur.fetchone()

    if result is None:
        errors.append("Неправильный логин или пароль")
        dbClose(cur, conn)
        return render_template("login.html", errors=errors)

    userID, hashPassword = result

    if check_password_hash(hashPassword, password):
        session['id'] = userID
        session['username'] = username
        dbClose(cur, conn)
        return render_template("glav.html", username=username)

    else:
        errors.append("Неправильный логин или пароль")
        return render_template("login.html", errors=errors)

@lab5.route("/lab5/new_article", methods = ["GET", "POST"])
def createArticle():
    errors =[]

    userID = session.get("id")
    is_public = request.form.get("is_public")
    if is_public == "public":
        is_public = True
    else:
        is_public = False


    if userID is not None:
        if request.method == "GET":
            return render_template("new_article.html", username=session.get("username"))
        
        if request.method == "POST":
            text_article = request.form.get("text_article")
            title = request.form.get("title_article")
            is_public = request.form.get("is_public")

            if len(text_article) == 0:
                errors.append('Заполните текст')
                return render_template("new_article.html", errors=errors, username=session.get("username"))

            conn = dbConnect()
            cur = conn.cursor()

            cur.execute("INSERT INTO articles(user_id, title, article_text, is_public) VALUES (%s, %s, %s, %s) RETURNING id", (userID, title, text_article, is_public))

            new_article_id = cur.fetchone()[0]
            conn.commit()

            dbClose(cur, conn)

            return redirect(f"/lab5/articles/{new_article_id}")

    return redirect("/lab5/login")

@lab5.route("/lab5/articles/<int:article_id>")
def getArticle(article_id):
    userID = session.get("id")

    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute("SELECT title, article_text FROM articles WHERE id = %s", (article_id,))


        articleBody = cur.fetchone()

        dbClose(cur, conn)

        if articleBody is None:
            return "Not found!"

        text = articleBody[1].splitlines()

        return render_template("articles.html", article_text=text, article_title=articleBody[0], username=session.get("username"))

@lab5.route("/lab5/show")
def showZam():
    userID = session.get("id")

    if userID is not None:
        
        conn = dbConnect()
        cur = conn.cursor()

        cur.execute("SELECT id, title FROM articles WHERE user_id = %s", (userID,))

        articles = cur.fetchall()

        conn.commit()
      
        dbClose(cur, conn)

        return render_template("show.html", articles=articles, username=session.get("username"))
      

    return redirect("/lab5/login")  

@lab5.route("/lab5/logout")
def Razlog():
    session.clear()
    return redirect("/lab5/login")

@lab5.route('/lab5/public_articles')
def publicArticles():
    userID = session.get("id")
    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                articles.id, 
                articles.title, 
                CASE WHEN favorites.article_id IS NOT NULL THEN true ELSE false END as is_favorite, 
                CASE WHEN likess.article_id IS NOT NULL THEN true ELSE false END as is_liked, 
                articles.likes as like_count
            FROM 
                articles 
                LEFT JOIN favorites ON articles.id = favorites.article_id AND favorites.user_id = %s
                LEFT JOIN likess ON articles.id = likess.article_id AND likess.user_id = %s
            WHERE articles.is_public = true
            ORDER BY is_favorite DESC, articles.id DESC""", (userID, userID))
        public_articles = cur.fetchall()

        dbClose(cur, conn)
        return render_template('public_articles.html', public_articles=public_articles, username=session.get("username"))
    return redirect("/lab5/login")  

@lab5.route('/lab5/favorite_article/<int:article_id>', methods=['POST'])
def favoriteArticle(article_id):
    userID = session.get("id")
    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()  
        cur.execute("SELECT id FROM favorites WHERE user_id = %s AND article_id = %s", (userID, article_id))
        favorite_entry = cur.fetchone()

        if favorite_entry is None:  
            cur.execute("INSERT INTO favorites (user_id, article_id, is_favorite) VALUES (%s, %s, true)", (userID, article_id))
            conn.commit() 

        else:
            cur.execute("DELETE FROM favorites WHERE user_id = %s AND article_id = %s", (userID, article_id))
            conn.commit()

        dbClose(cur, conn)

        return redirect('/lab5/public_articles')
  
    return redirect("/lab5/login")



@lab5.route('/lab5/like_article/<int:article_id>', methods=['POST'])
def likeArticle(article_id):
    userID = session.get("id")
    if userID is not None:
        conn = dbConnect()
        cur = conn.cursor()  
        cur.execute("SELECT id FROM likess WHERE user_id = %s AND article_id = %s", (userID, article_id))
        like_entry = cur.fetchone()

        if like_entry is None:  
            cur.execute("INSERT INTO likess (user_id, article_id) VALUES (%s, %s)", (userID, article_id))
            conn.commit()  
           
            cur.execute("UPDATE articles SET likes = COALESCE(likes, 0) + 1 WHERE id = %s", (article_id,))
        else:
            cur.execute("DELETE FROM likess WHERE user_id = %s AND article_id = %s", (userID, article_id))
            conn.commit()
        
            cur.execute("UPDATE articles SET likes = COALESCE(likes, 0) - 1 WHERE id = %s", (article_id,))

        conn.commit()

        dbClose(cur, conn)

        return redirect('/lab5/public_articles')
  
    return redirect("/lab5/login")


