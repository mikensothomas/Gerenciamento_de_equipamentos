from sqlmodel import create_engine, Session
from dotenv import load_dotenv
import os
from sqlalchemy import text

class Database:
    def __init__(self):
        load_dotenv()
        self.database_url = os.getenv("DATABASE_URL")
        self.engine = None

    def connect(self):
        try:
            self.engine = create_engine(self.database_url, echo=True)
            with Session(self.engine) as session:
                session.exec(text("SELECT 1"))
                print("✅ Conexão feita com sucesso!")
            return True
        except Exception as e:
            print("❌ Falha na conexão:", e)
            return False

    def get_session(self):
        if not self.engine:
            self.connect()
        return Session(self.engine)
