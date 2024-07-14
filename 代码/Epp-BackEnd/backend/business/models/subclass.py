import uuid

from django.db import models


class Subclass(models.Model):
    subclass_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
