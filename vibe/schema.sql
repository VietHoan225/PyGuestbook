-- Tạo database và bảng cho PyGuestbook (bản Vibe).
-- Chạy được nhiều lần: sudo mysql < schema.sql
-- Tài khoản MySQL tạo riêng theo hướng dẫn trong README (không để mật khẩu ở đây).

CREATE DATABASE IF NOT EXISTS guestbook
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;

USE guestbook;

CREATE TABLE IF NOT EXISTS entries (
    id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    -- as_ci: phân biệt dấu (An ≠ Ân) nhưng không phân biệt hoa thường khi thống kê
    name       VARCHAR(100) COLLATE utf8mb4_0900_as_ci NOT NULL,
    message    TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_entries_name (name),
    INDEX idx_entries_created_at (created_at)
) ENGINE = InnoDB;
