from flask import Flask, redirect
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)

@app.route("/menu")
def menu():
    return """
<!doctype html>
<html>
    <head>
        <title>Темирова Екатерина, Пахомова Валерия, Лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программирование, часть 2, Список лабораторных
        </header>

        <h1>web-сервер на flask</h1>

        <main>
            <a href="/lab1">Первая лабораторая работа</a>
        </main>

        <footer>
            &copy; Темирова, Пахомова, ФБИ-11, 3 курс, 2023
        </footer>
    </body>
</html>
"""

@app.route("/lab1")
def lab1():
    return """
<!doctype html>
<html>
    <head>
        <title>Темирова Екатерина, Пахомова Валерия, Лабораторная 1</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>web-сервер на flask</h1>

        <main>
            Flask — фреймворк для создания веб-приложений на языке программирования 
            Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
            Относится к категории так называемых микрофреймворков — минималистичных каркасов 
            веб-приложений, сознательно предоставляющих лишь самые ба- зовые возможности.
        </main>

        <footer>
            &copy; Темирова, Пахомова, ФБИ-11, 3 курс, 2023
        </footer>
    </body>
</html>
"""