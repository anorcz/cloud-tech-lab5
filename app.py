from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

# В памяти храним список задач
tasks = []

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
    </style>
</head>
<body>

<h1>Task Manager</h1>

<form method="POST" action="/add">
    <input type="text" name="title" placeholder="Новая задача" required>
    <button type="submit">Добавить</button>
</form>

<h2>Список задач</h2>

{% for task in tasks %}
<div class="task">
    <span class="{{ 'done' if task['done'] else '' }}">{{ task['title'] }}</span>
    {% if not task['done'] %}
        <a href="/done/{{ loop.index0 }}">✅ Выполнить</a>
    {% endif %}
    <a href="/delete/{{ loop.index0 }}">🗑 Удалить</a>
</div>
{% else %}
<p>Список пуст</p>
{% endfor %}

</body>
</html>
"""

# ================= ROUTES =================

@app.route("/")
def index():
    return render_template_string(HTML, tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    if title:
        tasks.append({"title": title, "done": False})
    return redirect(url_for("index"))

@app.route("/done/<int:task_id>")
def mark_done(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = True
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for("index"))

# ================ RUN ====================

if __name__ == "__main__":
    app.run(debug=True)
