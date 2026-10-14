"""Kết nối MySQL (mỗi request một kết nối) và các hàm truy vấn bảng entries."""

import pymysql
from flask import current_app, g
from pymysql.cursors import DictCursor


def get_db():
    if "db" not in g:
        cfg = current_app.config
        g.db = pymysql.connect(
            host=cfg["MYSQL_HOST"],
            port=cfg["MYSQL_PORT"],
            user=cfg["MYSQL_USER"],
            password=cfg["MYSQL_PASSWORD"],
            database=cfg["MYSQL_DATABASE"],
            charset="utf8mb4",
            cursorclass=DictCursor,
            autocommit=True,
            connect_timeout=5,
        )
    return g.db


def close_db(exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)


def get_all_entries():
    with get_db().cursor() as cur:
        cur.execute(
            "SELECT id, name, message, created_at FROM entries"
            " ORDER BY created_at DESC, id DESC"
        )
        return cur.fetchall()


def add_entry(name, message):
    with get_db().cursor() as cur:
        cur.execute(
            "INSERT INTO entries (name, message) VALUES (%s, %s)",
            (name, message),
        )
        return cur.lastrowid


def delete_entry(entry_id):
    """Trả về True nếu có dòng bị xóa."""
    with get_db().cursor() as cur:
        cur.execute("DELETE FROM entries WHERE id = %s", (entry_id,))
        return cur.rowcount > 0


def count_entries():
    with get_db().cursor() as cur:
        cur.execute("SELECT COUNT(*) AS total FROM entries")
        return cur.fetchone()["total"]


def count_by_sender(limit=None):
    """Số lời nhắn theo người gửi, nhiều nhất trước."""
    sql = (
        "SELECT name, COUNT(*) AS total FROM entries"
        " GROUP BY name ORDER BY total DESC, name ASC"
    )
    params = ()
    if limit is not None:
        sql += " LIMIT %s"
        params = (limit,)
    with get_db().cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()
