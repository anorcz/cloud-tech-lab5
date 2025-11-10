from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from PythonAnywhere!</h1><p>Версия 2.0: Добавлен новый эндпоинт.</p>'

@app.route('/about')
def about():
    return '<h1>About Page</h1><p>Это обновленная версия в Agile-стиле!</p>'

if __name__ == '__main__':
    app.run(debug=True)
