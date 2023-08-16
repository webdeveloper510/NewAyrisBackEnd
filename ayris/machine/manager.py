from django.db import models


class MachineManager(models.Manager):
    pass


class MachineQuerySet(models.QuerySet):

    # TO REMOVE counter with machine.all().delete()
    def delete(self):
        for machine in self:
            print("REMOVE Counter : ",  machine.counter)
            machine.counter.delete()
        return super().delete()
