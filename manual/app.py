from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

entries = []
next_id = 1


@app.route("/")
def index():
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["GET", "POST"])
def add():
    global next_id

    if request.method == "GET":
        return render_template("add.html")

    name = request.form.get("name", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not message:
        return render_template(
            "add.html",
            error="Vui lòng nhập đầy đủ tên và lời nhắn.",
            name=name,
            message=message,
        )

    entries.append({"id": next_id, "name": name, "message": message})
    next_id += 1
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    for entry in entries:
        if entry["id"] == id:
            entries.remove(entry)
            break
    return redirect(url_for("index"))
