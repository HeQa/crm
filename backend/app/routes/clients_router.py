from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.fastapi import register_tortoise
from app.database.models import Employees
from app.schemas import EmployeeCreate, EmployeeLogin, ClientCreate, CallCreate, EventCreate, ClientResponse, SyncRequest
from typing import List
from app.services.client_service import get_clients_all, create_client_service
from app.auth.dependencies import get_current_user
from app.database.models import Clients

router = APIRouter(prefix="/clients", tags=["Clients"])

# Эндпоинты для клиентов
@router.get("/", response_model=List[ClientResponse])
async def get_clients(
    user=Depends(get_current_user)
):
    client_list = await get_clients_all()
    return client_list

@router.post("/create")
async def create_client(client: ClientCreate,
                        user=Depends(get_current_user)
                        ):
    if client.status_id is None:
            raise HTTPException(
                status_code=422,
                detail="status_id is required"
            )
    return await create_client_service(client)

@router.post("/sync_clients")
async def sync_clients(
    request: SyncRequest,
    user=Depends(get_current_user)
):
    results = {
        "total_received": len(request.clients),
        "created": 0,
        "skipped": 0,
        "details": []
    }
    
    for client_data in request.clients:
        try:
            # Проверяем существование клиента по телефону
            # client_list = await get_clients_all()
            existing_client = await Clients.get_or_none(phone=client_data.phone)
            # existing_client = next(
            #     (client for client in client_list if client.phone == client_data.phone), 
            #     None
            # )
            # print("Client list: ", client_list)
            print("Existing client: ", existing_client)
            if existing_client:
                results["skipped"] += 1
                results["details"].append({
                    "phone": client_data.phone,
                    "status": "skipped",
                    "reason": "Client already exists",
                    "client_id": existing_client.id
                })
                continue
            
            # Создаем нового клиента
            #print("Client data: ", client_data)
     
            new_client = {
                'full_name': client_data.full_name,
                'phone': client_data.phone,
                'email': client_data.email,
                'status_id': client_data.status_id,
                'responsible_employee_id': client_data.responsible_employee_id,
                'source': client_data.source
            }

            new_client_data = client_data.model_dump()
            created_client = await create_client_service(new_client_data)
            print("Abpoba_created: ", created_client)
            results["created"] += 1
            results["details"].append({
                "phone": client_data.phone,
                "status": "created",
                "client_id": created_client.id
            })
            
        except Exception as e:
            results["details"].append({
                "phone": client_data.phone,
                "status": "error",
                "error": str(e)
            })
    
    return {
        "message": "Sync completed",
        "results": results
    }