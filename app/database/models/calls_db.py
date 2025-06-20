from tortoise import fields, models

class Calls(models.Model):
    call_id = fields.IntField(pk=True)
    client = fields.ForeignKeyField("app.Clients", related_name="calls")
    employee = fields.ForeignKeyField("app.Employees", related_name="calls")
    start_time = fields.DatetimeField()
    duration = fields.IntField()  # в секундах
    transcript = fields.TextField(null=True)
    summary = fields.TextField(null=True)  # краткое содержание от ИИ
    file_link = fields.CharField(max_length=255, null=True)
    rating = fields.IntField(null=True)  # рейтинг соответствия скрипту