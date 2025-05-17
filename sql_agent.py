# sql_agent.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase # Wrapper cho DB
from langchain.agents import create_sql_agent # Hàm tạo SQL Agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit # Bộ tools cho SQL
# from sqlalchemy import create_engine # Nếu cần kết nối phức tạp hơn

load_dotenv()

DB_FILE = "project_database.db" # Đường dẫn tới file SQLite đã tạo
DB_URI = f"sqlite:///{DB_FILE}" # URI kết nối cho SQLAlchemy

def create_sql_agent_executor():
    print(f"Đang khởi tạo SQL Agent cho database: {DB_URI}...")

    # 1. Khởi tạo LLM
    llm = ChatOpenAI(model="gpt-4", temperature=0) # GPT-4 thường làm việc tốt với SQL

    # 2. Kết nối tới Database
    # LangChain sử dụng SQLAlchemy để tương tác với DB
    # SQLDatabase.from_uri sẽ tự tạo engine
    try:
        db = SQLDatabase.from_uri(DB_URI, sample_rows_in_table_info=3) # sample_rows giúp LLM hiểu dữ liệu hơn
        print(f"Kết nối thành công tới database. Các bảng mẫu: {db.get_usable_table_names()}")
    except Exception as e:
        print(f"Lỗi kết nối database: {e}")
        return None

    # 3. Tạo SQLDatabaseToolkit
    # Toolkit này chứa các tools cần thiết để Agent tương tác với DB
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    tools = toolkit.get_tools() # Lấy danh sách các tools từ toolkit

    # 4. Tạo SQL Agent
    # create_sql_agent sẽ tự động xử lý prompt và các cấu hình cần thiết
    # Nó sử dụng một loại Agent đặc biệt (thường là dựa trên OpenAI Functions/Tools nếu LLM hỗ trợ)
    # để tương tác với các tools trong toolkit.
    # Chúng ta không cần truyền prompt riêng như các Agent trước,
    # trừ khi muốn tùy chỉnh sâu.
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit, # Hoặc có thể truyền trực tiếp tools=tools
        verbose=True,
        agent_type="openai-tools", # Khuyến nghị nếu dùng model OpenAI mới
                                  # Có thể là "openai-functions" hoặc bỏ qua để LangChain tự chọn
        handle_parsing_errors=True
    )

    print("SQL Agent đã sẵn sàng!")
    return agent_executor