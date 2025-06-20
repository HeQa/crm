from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Employees(models.Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255, null=False)
    email = fields.CharField(max_length=255, unique=True)
    hashed_password = fields.CharField(max_length=255)
    role = fields.CharField(max_length=50)  # телефонист, менеджер, администратор
    telegram = fields.CharField(max_length=100, null=True)
    is_active = fields.BooleanField(default=True)


class Clients(models.Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=255)
    phone = fields.CharField(max_length=20)
    email = fields.CharField(max_length=255, null=True)
    status = fields.ForeignKeyField("app.ClientStatuses", related_name="clients")
    responsible_employee = fields.ForeignKeyField("app.Employees", related_name="clients")
    source = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "clients"

