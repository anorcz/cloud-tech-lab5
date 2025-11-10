from flask import Flask, request, redirect, url_for, render_template_string
from pymongo import MongoClient, errors
from bson.objectid import ObjectId

app = Flask(__name__)

MONGO_URI = "mongodb+srv://hwndy9yg5zfcuznqkf9t3lmnw5yhb_db_user:jd306Ikwg0aUpSHY@cluster0.89ni8tj.mongodb.net/taskdb?retryWrites=true&w=majority"

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
except errors.ServerSelectionTimeoutError:
    client = None

if client:
    db = client.get_database()
    tasks = db["tasks"]
else:
    tasks = None

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Task Manager</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 30px auto; }
        h1 { text-align: center; }
        form { margin-bottom: 20px; }
        .task { padding: 10px; border-bottom: 1px solid #ddd; }
        .done { text-decoration: line-through; color: gray; }
        a { margin-left: 10px; }
        .error { color: red; text-align: center; }
    </style>
</head>
<body>

<h1>Task Manager</h1>

{% if tasks is none %}
<div class="error">
    ❌ Не удалось подключиться к базе данных. Проверьте MONGO_URI и доступ к MongoDB Atlas.
</div>
{% else %}
<form method="POST" action="/add">
    <input type="text" name="title" placeholder="Новая задача" required>
    <button type="submit">Добавить</button>
</form>

<h2>Список задач</h2>

{% for task in tasks %}
<div class="task">
    <span class="{{ 'done' if task.done else '' }}">{{ task.title }}</span>
    {% if not task.done %}
        <a href="/done/{{ task._id }}">✅ Выполнить</a>
    {% endif %}
    <a href="/delete/{{ task._id }}">🗑 Удалить</a>
</div>
{% endfor %}
{% endif %}

</body>
</html>
"""

@app.route("/")
def index():
    if tasks is None:
        return render_template_string(HTML, tasks=None)

    all_tasks = list(tasks.find())
    for t in all_tasks:
        t["_id"] = str(t["_id"])
        t["done"] = t.get("done", False)
    return render_template_string(HTML, tasks=all_tasks)


@app.route("/add", methods=["POST"])
def add_task():
    if tasks is None:
        return redirect(url_for("index"))

    title = request.form.get("title")
    if title:
        tasks.insert_one({"title": title, "done": False})
    return redirect(url_for("index"))


@app.route("/done/<id>")
def mark_done(id):
    if tasks is None:
        return redirect(url_for("index"))

    tasks.update_one({"_id": ObjectId(id)}, {"$set": {"done": True}})
    return redirect(url_for("index"))


@app.route("/delete/<id>")
def delete_task(id):
    if tasks is None:
        return redirect(url_for("index"))

    tasks.delete_one({"_id": ObjectId(id)})
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run()
