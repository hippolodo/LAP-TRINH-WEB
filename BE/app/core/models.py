from sqlalchemy import Column, Integer, String, Enum, ForeignKey, TIMESTAMP, Text, Date, Numeric, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

# 1. Users
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    cccd = Column(String(20), unique=True, nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum('male', 'female', 'other'), nullable=False)
    address = Column(Text, nullable=False)
    role = Column(Enum('customer', 'staff', 'admin'), default='customer')
    work_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    dependents = relationship("Dependent", back_populates="user")
    appointments = relationship("Appointment", back_populates="user")

# 2. Dependents (Hồ sơ người tiêm)
class Dependent(Base):
    __tablename__ = "dependents"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(Enum('Nam', 'Nữ', 'Khác'), nullable=False)
    # Đổi tên từ relationship thành relation_type để tránh trùng với hàm relationship() của SQLAlchemy
    relation_type = Column("relationship", String(50), nullable=False) 
    cccd = Column(String(20), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="dependents")
    appointments = relationship("Appointment", back_populates="dependent")
    records = relationship("VaccinationRecord", back_populates="dependent")

# 3. Locations
class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(Text, nullable=False)
    phone = Column(String(20))
    status = Column(Enum('active', 'inactive'), default='active')

    inventory = relationship("Inventory", back_populates="location")
    appointments = relationship("Appointment", back_populates="location")
    schedules = relationship("Schedule", back_populates="location")

# 4. Vaccines
class Vaccine(Base):
    __tablename__ = "vaccines"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    manufacturer = Column(String(100))
    price = Column(Numeric(15, 2), nullable=False)
    description = Column(Text)
    dose_count = Column(Integer, default=1)
    status = Column(Enum('available', 'out_of_stock', 'discontinued'), default='available')

    inventory = relationship("Inventory", back_populates="vaccine")
    appointments = relationship("Appointment", back_populates="vaccine")

# 5. Inventory
class Inventory(Base):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True, autoincrement=True)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    batch_number = Column(String(50), nullable=False)
    stock_quantity = Column(Integer, default=0)
    expiry_date = Column(Date, nullable=False)

    vaccine = relationship("Vaccine", back_populates="inventory")
    location = relationship("Location", back_populates="inventory")

# 6. Schedules
class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    work_date = Column(Date, nullable=False)
    session = Column(Enum('morning', 'afternoon'), nullable=False)
    max_slots = Column(Integer, default=50)
    occupied_slots = Column(Integer, default=0)
    status = Column(Enum('active', 'full', 'closed'), default='active')

    location = relationship("Location", back_populates="schedules")
    appointments = relationship("Appointment", back_populates="schedule")

# 7. Appointments
class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dependent_id = Column(Integer, ForeignKey("dependents.id"), nullable=True)
    patient_name = Column(String(100), nullable=False)
    patient_age = Column(Integer, nullable=False)
    patient_gender = Column(Enum('Nam', 'Nữ', 'Khác'), nullable=False)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("schedules.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    session = Column(Enum('morning', 'afternoon'), nullable=False)
    status = Column(Enum('pending', 'confirmed', 'completed', 'cancelled'), default='pending')
    total_price = Column(Numeric(15, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="appointments")
    dependent = relationship("Dependent", back_populates="appointments")
    vaccine = relationship("Vaccine", back_populates="appointments")
    location = relationship("Location", back_populates="appointments")
    schedule = relationship("Schedule", back_populates="appointments")

# 8. Vaccination Records
class VaccinationRecord(Base):
    __tablename__ = "vaccination_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    dependent_id = Column(Integer, ForeignKey("dependents.id"), nullable=True)
    appointment_id = Column(Integer, unique=True)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id"), nullable=False)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    batch_number = Column(String(50))
    dose_number = Column(String(20))
    date_given = Column(TIMESTAMP, server_default=func.now())
    provider_name = Column(String(100))
    reactions = Column(Text)
    notes = Column(Text)

    dependent = relationship("Dependent", back_populates="records")
    vaccine = relationship("Vaccine")
    location = relationship("Location")