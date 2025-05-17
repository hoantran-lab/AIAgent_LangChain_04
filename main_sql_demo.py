# main_sql_demo.py
from sql_agent import create_sql_agent_executor

if __name__ == "__main__":
    sql_agent_ex = create_sql_agent_executor()

    if not sql_agent_ex:
        print("Không thể khởi tạo SQL Agent. Kết thúc chương trình.")
        exit()

    print("\n--- DEMO SQL Agent ---")
    print("Đặt câu hỏi cho Agent về dữ liệu dự án (nhập 'thoát' để dừng).")

    # Vòng lặp để người dùng có thể đặt nhiều câu hỏi
    # SQL Agent thường không cần memory ngoài vì mỗi truy vấn là độc lập,
    # nhưng nó sẽ tự động dùng schema và sample rows.
    # Nếu muốn cuộc trò chuyện có ngữ cảnh, bạn có thể thử tích hợp memory
    # vào một custom agent sử dụng SQLDatabaseTool.

    questions = [
        "Có bao nhiêu công việc trong database?",
        "Liệt kê tất cả các công việc đang ở trạng thái 'Đang thực hiện'.",
        "Công việc nào được giao cho Alice và có độ ưu tiên là 'Cao'?",
        "Task 'TASK-002' có deadline khi nào và ai là người thực hiện?",
        "Mô tả của công việc 'Viết tài liệu hướng dẫn sử dụng' là gì?",
        "Có bao nhiêu công việc chưa bắt đầu?",
        "Những công việc nào sẽ đến hạn trong tháng 9 năm 2024?", # Câu hỏi phức tạp hơn về ngày tháng
        "Liệt kê tên và người thực hiện của các task có độ ưu tiên 'Thấp'."
    ]

    for q_text in questions:
        print(f"\n[User] {q_text}")
        try:
            response = sql_agent_ex.invoke({"input": q_text})
            print(f"[Agent] {response['output']}")
        except Exception as e:
            print(f"[Agent Error] Lỗi khi xử lý câu hỏi: {e}")
    
    print("\n--- Thử một câu hỏi mà Agent có thể cần xem schema ---")
    q_schema = "Trong bảng tasks có những cột nào?" # Agent sẽ dùng tool để lấy schema
    print(f"\n[User] {q_schema}")
    try:
        response_schema = sql_agent_ex.invoke({"input": q_schema})
        print(f"[Agent] {response_schema['output']}")
    except Exception as e:
        print(f"[Agent Error] Lỗi khi xử lý câu hỏi schema: {e}")


    # Ví dụ vòng lặp input người dùng (tùy chọn cho video)
    # while True:
    #     user_input = input("\n[User] Câu hỏi của bạn: ")
    #     if user_input.lower() == "thoát":
    #         break
    #     if not user_input.strip():
    #         continue
    #     try:
    #         response = sql_agent_ex.invoke({"input": user_input})
    #         print(f"[Agent] {response['output']}")
    #     except Exception as e:
    #         print(f"[Agent Error] Lỗi khi xử lý câu hỏi: {e}")


    print("\n--- Kết thúc Demo SQL Agent ---")