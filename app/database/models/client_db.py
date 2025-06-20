from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class ClientStatuses(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    source = fields.CharField(max_length=255, null=True)

class ClientCard(models.Model):
    client = fields.OneToOneField("app.Clients", related_name="card", pk=True)
    academic_year = fields.CharField(max_length=10, null=True)  # 25/26
    call_ai = fields.TextField(null=True)  # рекомендации из звонка


