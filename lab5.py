from flask import Blueprint, render_template, request, redirect
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
    