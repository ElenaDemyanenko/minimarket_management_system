from sqlmodel import create_engine, SQLModel, Session
from urllib.parse import quote_plus

#данные подключения
password = "mis2025!"
encoded_password = quote_plus(password)
DATABASE_URL = f"postgresql://student:{encoded_password}@176.108.247.125:5432/mis2025"

print("подключение к PostgreSQL")
print(f"база: mis2025, схема: Demyanenko")
print(f"пользователь: student")

#создание движка
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    print("использование существующих таблиц с данными")
    
def get_session():
    """создание сессии для работы с бд"""
    with Session(engine) as session:
        yield session


"""
cd "C:\!Методы и ср проектирования\lab3"
python -m uvicorn main:app --reload
 """