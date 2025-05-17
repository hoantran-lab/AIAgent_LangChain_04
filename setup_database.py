# setup_database.py
import sqlite3

# Tên file database
DB_FILE = "project_database.db"

def create_connection(db_file):
    """ Tạo kết nối đến SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Đã kết nối tới SQLite phiên bản {sqlite3.version}")
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """ Tạo bảng tasks """
    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        status TEXT,
        deadline TEXT,
        assignee TEXT,
        priority TEXT,
        description TEXT
    );
    """
    try:
        c = conn.cursor()
        c.execute(sql_create_tasks_table)
        print("Đã tạo bảng 'tasks' (hoặc bảng đã tồn tại).")
    except sqlite3.Error as e:
        print(e)

def insert_sample_data(conn):
    """ Chèn dữ liệu mẫu vào bảng tasks """
    tasks_data = [
        ("TASK-001", "Thiết kế giao diện người dùng (UI Design)", "Đang thực hiện", "2024-08-20", "Alice", "Cao", "Thiết kế toàn bộ giao diện cho ứng dụng mobile mới."),
        ("TASK-002", "Phát triển API backend cho user login", "Chưa bắt đầu", "2024-09-05", "Bob", "Cao", "Xây dựng các endpoint API cho chức năng đăng nhập."),
        ("TASK-003", "Kiểm thử tích hợp (Integration Testing)", "Hoàn thành", "2024-07-30", "Charlie", "Trung bình", "Kiểm thử tích hợp frontend và backend."),
        ("TASK-004", "Viết tài liệu hướng dẫn sử dụng", "Đang thực hiện", "2024-09-15", "Alice", "Trung bình", "Biên soạn tài liệu hướng dẫn người dùng."),
        ("TASK-005", "Triển khai lên môi trường Staging", "Chưa bắt đầu", "2024-09-25", "DevOps Team", "Cao", "Triển khai ứng dụng lên staging."),
        ("TASK-006", "Tối ưu hóa hiệu suất database", "Chưa bắt đầu", "2024-10-10", "Bob", "Cao", "Phân tích và tối ưu các truy vấn database chậm."),
        ("TASK-007", "Nghiên cứu công nghệ AI mới", "Đang thực hiện", "2024-11-01", "Alice", "Thấp", "Tìm hiểu về các mô hình LLM mới cho dự án chatbot.")
    ]
    sql_insert_task = "INSERT OR IGNORE INTO tasks (id, name, status, deadline, assignee, priority, description) VALUES (?, ?, ?, ?, ?, ?, ?)"
    try:
        c = conn.cursor()
        c.executemany(sql_insert_task, tasks_data)
        conn.commit()
        print(f"Đã chèn {c.rowcount} dòng dữ liệu mẫu vào bảng 'tasks'.")
    except sqlite3.Error as e:
        print(f"Lỗi khi chèn dữ liệu: {e}")


if __name__ == '__main__':
    conn = create_connection(DB_FILE)
    if conn is not None:
        create_table(conn)
        insert_sample_data(conn)
        conn.close()
        print(f"Đã đóng kết nối tới {DB_FILE}.")
    else:
        print("Lỗi! Không thể tạo kết nối database.")