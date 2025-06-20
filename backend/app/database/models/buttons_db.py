from tortoise import fields, models


class Button(models.Model):
    id = fields.IntField(pk=True)
    parent_script_id = fields.IntField(fk=True)
    text = fields.CharField(max_length=1000)
    description = fields.TextField(null=True)