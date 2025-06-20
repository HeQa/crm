import asyncio
from tortoise.transactions import in_transaction
from app.database.models import Clients, ClientStatuses, Employees
from app.schemas import ClientResponse, EmployeeRespone, ClientCreate

from app.services.employees_service import employe_respone
from typing import List

async def client_response_create(client: Clients) -> ClientResponse:
    try:
        #await client.refresh_from_db(fields=['email'])
        # Fetch related data in parallel
        print("Client: ", client)
        status, employee = await asyncio.gather(
            ClientStatuses.get_or_none(id=client.status_id),
            Employees.get_or_none(id=client.responsible_employee_id)
        )

        if status is None:
            raise ValueError(f"Status with ID {client.status_id} not found")
        if employee is None:
            raise ValueError(f"Employee with ID {client.responsible_employee_id} not found")
        
        response_employee = await employe_respone(employee)
        # print(client.id, client.full_name, client.phone, client.email)
        return ClientResponse(
            id=client.id,
            full_name=client.full_name,
            phone=client.phone,
            email=client.email,
            status=status.name,
            responsible_employee=response_employee,  # Use the converted employee
            source=client.source,
        )
    except Exception as e:
        print(f"Error creating client response: {str(e)}")
        raise


async def get_clients_all() -> List[ClientResponse]:
    clients = await Clients.all()

    respone = []
    for client in clients:
        repone_obj = await client_response_create(client)
        respone.append(repone_obj)
    return respone


async def create_client_service(data: ClientCreate) -> ClientResponse:
    if data['full_name'] == None:
        raise ValueError("full_name is required") # status_id
    # statuses = await ClientStatuses.all()
    # print([s.name for s in statuses])
    client = await Clients.create(
                                    full_name=data['full_name'],
                                    phone=data['phone'],
                                    email=data['email'],
                                    status_id=data['status_id'],
                                    responsible_employee_id=data['responsible_employee_id'],
                                    source=data['source']
                                )
    respone = await client_response_create(client)
    return respone


