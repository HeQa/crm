from tortoise import fields, models


class Scripts(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)

class ScriptsText(models.Model):
    id = fields.IntField(pk=True)
    script = fields.ForeignKeyField("app.Scripts", related_name="texts")
    parent = fields.IntField(null=True)  # родительский уровень
    head = fields.CharField(max_length=255, null=True)  # заголовок уровня
    text = fields.TextField()  # текст ответа