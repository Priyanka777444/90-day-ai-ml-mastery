from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

#Create SQLite database
engine = create_engine('sqlite:///tickets.db', echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

#Tickect model
class TicketRecord(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    ticket = Column(String, nullable=False)
    category = Column(String)
    priority = Column(String)
    emotion = Column(String)
    action = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

#create tables
def init_db():
    Base.metadata.create_all(bind=engine)

#save tickets
def save_ticket(ticket_data: dict):
    db = SessionLocal()
    record = TicketRecord(
        ticket = ticket_data.get('ticket', ''),
        category = ticket_data.get('category', ''),
        priority = ticket_data.get('priority', ''),
        emotion = ticket_data.get('emoiton', ''),
        action = ticket_data.get('action', '')
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    db.close()
    return record.id

# Get all tickets from database
def get_all_tickets():
    db = SessionLocal()
    tickets = db.query(TicketRecord).order_by(TicketRecord.created_at.desc()).all()
    db.close()
    return tickets

#get all tickets by priority
def get_by_priority(priority: str):
    db = SessionLocal()
    ticket = db.query(TicketRecord).filter(
        TicketRecord.priority == priority
    ).all()
    db.close()
    return ticket

def get_stats():
    db = SessionLocal()
    total = db.query(TicketRecord).count()
    high = db.query(TicketRecord).filter(TicketRecord.priority == 'HIGH').count()
    billing = db.query(TicketRecord).filter(TicketRecord.category =="BILLING").count()
    angry = db.query(TicketRecord).filter(TicketRecord.emotion.in_ == (['ANGRY', 'FRUSTRATED'])).count()
    db.close()
    return {
        'total': total,
        'high_priority': high,
        'billing_issue': billing,
        'unhappy_customers': angry
    }


    

