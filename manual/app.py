import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "data.json"
CHART_FILE = Path(__file__).parent / "static" / "stats.png"


def load_entries():
    if DATA_FILE.exists():
        with DATA_FILE.open(encoding="utf-8") as file:
            return json.load(file)
    return []


def save_entries():
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(entries, file, ensure_ascii=False, indent=4)


entries = load_entries()
next_id = max((entry["id"] for entry in entries), default=0) + 1


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
    save_entries()
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    for entry in entries:
        if entry["id"] == id:
            entries.remove(entry)
            save_entries()
            break
    return redirect(url_for("index"))


@app.route("/stats")
def stats():
    counts = Counter(entry["name"] for entry in entries)
    top_senders = counts.most_common(5)

    CHART_FILE.parent.mkdir(exist_ok=True)

    all_senders = counts.most_common()
    names = [name for name, count in all_senders]
    totals = [count for name, count in all_senders]

    plt.figure(figsize=(8, 4))
    if names:
        plt.bar(names, totals, color="#5b6cff")
        plt.ylabel("Số lời nhắn")
        plt.title("Lời nhắn theo người gửi")
    else:
        plt.text(0.5, 0.5, "Chưa có lời nhắn", ha="center", va="center")
        plt.axis("off")
    plt.tight_layout()
    plt.savefig(CHART_FILE)
    plt.close()

    return render_template(
        "stats.html",
        total=len(entries),
        top_senders=top_senders,
        chart_url=url_for(
            "static", filename="stats.png", v=int(CHART_FILE.stat().st_mtime)
        ),
    )
