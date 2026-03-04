from sqlalchemy.orm import Session
import models
import schemas
from fastapi import HTTPException


# Create Employee
def create_employee(db: Session, employee: schemas.EmployeeCreate):
    existing = db.query(models.Employee).filter(
        models.Employee.employee_id == employee.employee_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")

    db_employee = models.Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


# Get All Employees
def get_employees(db: Session):
    return db.query(models.Employee).all()

# Update Employee
def update_employee(db: Session, employee_id: int, employee: schemas.EmployeeUpdate):

    db_employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not db_employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db_employee.employee_id = employee.employee_id
    db_employee.full_name = employee.full_name
    db_employee.email = employee.email
    db_employee.department = employee.department

    db.commit()
    db.refresh(db_employee)

    return db_employee

# Delete Employee
def delete_employee(db: Session, employee_id: int):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}


# Mark Attendance
def mark_attendance(db: Session, attendance: schemas.AttendanceCreate):
    employee = db.query(models.Employee).filter(
        models.Employee.id == attendance.employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db_attendance = models.Attendance(**attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


# Get Attendance by Employee
def get_attendance(db: Session, employee_id: int):
    return db.query(models.Attendance).filter(
        models.Attendance.employee_id == employee_id
    ).all()