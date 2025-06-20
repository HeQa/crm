from tortoise import fields, models

class ActionLogs(models.Model):
    log_id = fields.IntField(pk=True)
    employee = fields.ForeignKeyField("app.Employees", related_name="logs")
    action_type = fields.CharField(max_length=100)
    action_time = fields.DatetimeField(auto_now_add=True)
    details = fields.TextField(null=True)

# Справочники
class Universities(models.Model):
    university_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

class Faculties(models.Model):
    faculty_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    university = fields.ForeignKeyField("app.Universities", related_name="faculties")

class Programs(models.Model):
    program_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    faculty = fields.ForeignKeyField("app.Faculties", related_name="programs")

class Cities(models.Model):
    city_id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)