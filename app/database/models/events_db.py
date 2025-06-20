from tortoise import fields, models



class Events(models.Model):
    id = fields.IntField(pk=True)
    client = fields.ForeignKeyField("app.Clients", related_name="events")
    employee = fields.ForeignKeyField("app.Employees", related_name="events")
    event_type = fields.CharField(max_length=100)
    event_date = fields.DateField()
    event_time = fields.TimeField()
    description = fields.TextField(null=True)
    status = fields.CharField(max_length=50, null=True)
    mark = fields.CharField(max_length=50, null=True)  # в разработке