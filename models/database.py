import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# --- Configuración de la Base de Datos ---
DATABASE_URL = "sqlite:///calculator_app.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Modelo de Datos: Cotización (Quote) ---
class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    piece_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    weight_g = Column(Float)
    total_hours = Column(Float)
    filament_type = Column(String)
    material_cost = Column(Float)
    print_time_cost = Column(Float)
    electricity_cost = Column(Float)
    profit_margin_percent = Column(Float)
    final_price = Column(Float)

# --- Gestor de la Base de Datos ---
class DatabaseManager:
    def __init__(self):
        self.engine = engine
        self.SessionLocal = SessionLocal
        Base.metadata.create_all(bind=self.engine)

    def save_quote(self, quote_data):
        db = self.SessionLocal()
        try:
            new_quote = Quote(**quote_data)
            db.add(new_quote)
            db.commit()
            db.refresh(new_quote)
            return new_quote
        finally:
            db.close()

    def get_history(self):
        db = self.SessionLocal()
        try:
            return db.query(Quote).order_by(Quote.created_at.desc()).all()
        finally:
            db.close()
