import secrets
import time
import zlib
from datetime import datetime
from pathlib import Path

import pymysql
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import db
from config import load_config
from stats import draw_sender_chart

NAME_MAX = 100
MESSAGE_MAX = 1000
TOP_SENDERS = 5
CHART_MAX_SENDERS = 15

app = Flask(__name__)
app.config.update(load_config())
db.init_app(app)

STATIC_DIR = Path(app.static_folder)


# ---------- CSRF ----------

def csrf_token():
    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(32)
    return session["_csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


@app.before_request
def check_csrf():
    if request.method == "POST":
        sent = request.form.get("csrf_token", "")
        expected = session.get("_csrf_token", "")
        if not expected or not secrets.compare_digest(sent, expected):
            abort(400, "Phiên làm việc đã hết hạn, hãy tải lại trang và thử lại.")


# ---------- Bộ lọc template ----------

@app.template_filter("timeago")
def timeago(value):
    seconds = int((datetime.now() - value).total_seconds())
    if seconds < 60:
        return "vừa xong"
    for unit_seconds, unit in ((86400 * 365, "năm"), (86400 * 30, "tháng"),
                               (86400, "ngày"), (3600, "giờ"), (60, "phút")):
        if seconds >= unit_seconds:
            return f"{seconds // unit_seconds} {unit} trước"


@app.template_filter("initial")
def initial(name):
    return name.strip()[:1].upper()


@app.template_filter("hue")
def hue(name):
    """Màu ảnh đại diện cố định theo tên."""
    return zlib.crc32(name.lower().encode("utf-8")) % 360


# ---------- Route ----------

@app.route("/")
def index():
    entries = db.get_all_entries()
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        return render_template("add.html", errors={}, form={})

    form = {
        "name": request.form.get("name", "").strip(),
        "message": request.form.get("message", "").strip(),
    }
    errors = {}
    if not form["name"]:
        errors["name"] = "Vui lòng nhập tên."
    elif len(form["name"]) > NAME_MAX:
        errors["name"] = f"Tên tối đa {NAME_MAX} ký tự."
    if not form["message"]:
        errors["message"] = "Vui lòng nhập lời nhắn."
    elif len(form["message"]) > MESSAGE_MAX:
        errors["message"] = f"Lời nhắn tối đa {MESSAGE_MAX} ký tự."

    if errors:
        return render_template("add.html", errors=errors, form=form), 400

    db.add_entry(form["name"], form["message"])
    flash("Cảm ơn bạn! Lời nhắn đã được gửi.", "success")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    if db.delete_entry(id):
        flash("Đã xóa lời nhắn.", "success")
    else:
        flash("Không tìm thấy lời nhắn cần xóa.", "error")
    return redirect(url_for("index"))


@app.route("/stats")
def stats():
    total = db.count_entries()
    senders = db.count_by_sender()
    chart_rows = senders[:CHART_MAX_SENDERS]

    chart_version = None
    if chart_rows:
        draw_sender_chart(chart_rows, STATIC_DIR / "stats.png", theme="light")
        draw_sender_chart(chart_rows, STATIC_DIR / "stats-dark.png", theme="dark")
        chart_version = int(time.time())  # tránh trình duyệt dùng ảnh cũ

    return render_template(
        "stats.html",
        total=total,
        sender_count=len(senders),
        top_senders=senders[:TOP_SENDERS],
        senders=senders,
        chart_limited=len(senders) > CHART_MAX_SENDERS,
        chart_max=CHART_MAX_SENDERS,
        chart_version=chart_version,
    )


# ---------- Xử lý lỗi ----------

@app.errorhandler(400)
def bad_request(err):
    return render_template("error.html", code=400, title="Yêu cầu không hợp lệ",
                           detail=err.description), 400


@app.errorhandler(404)
def not_found(err):
    return render_template("error.html", code=404, title="Không tìm thấy trang",
                           detail="Trang bạn tìm không tồn tại hoặc đã bị di chuyển."), 404


@app.errorhandler(405)
def method_not_allowed(err):
    return render_template("error.html", code=405, title="Phương thức không được hỗ trợ",
                           detail="Thao tác này không thể thực hiện qua đường dẫn trực tiếp."), 405


@app.errorhandler(pymysql.err.OperationalError)
def database_unavailable(err):
    app.logger.exception("Không kết nối được MySQL")
    return render_template("error.html", code=503, title="Không kết nối được cơ sở dữ liệu",
                           detail="Hãy kiểm tra MySQL đã chạy và thông tin trong file .env."), 503


@app.errorhandler(500)
def server_error(err):
    return render_template("error.html", code=500, title="Đã có lỗi xảy ra",
                           detail="Vui lòng thử lại sau."), 500
