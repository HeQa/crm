from app.schemas import EmployeeRespone
from app.database.models import Employees

async def employe_respone(employee: Employees) -> EmployeeRespone:
    if employee is None:
        return None
    return EmployeeRespone(id=employee.id,
                    full_name=employee.full_name,
                    email=employee.email,
                    role=employee.role,
                    telegram=employee.telegram)

