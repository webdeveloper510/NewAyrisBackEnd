from rest_framework import viewsets

import machine.models as machine_model
from .serializers import (
MachineSerializer,

)

from buildx.models import (
ObjectName
)
from buildx.serializers import (
ObjectNameSerializer
)


class MachineViewSet(viewsets.ModelViewSet):
    queryset = machine_model.Machine.objects.all()
    serializer_class = MachineSerializer

class MyObjectsNameViewSet(viewsets.ModelViewSet):
    queryset = ObjectName.objects.all()
    serializer_class = ObjectNameSerializer

class MyMachineViewSet(viewsets.ModelViewSet):
    serializer_class = MachineSerializer

    def get_queryset(self):
        print(self.kwargs)

        if "pk" in self.kwargs:
            machine_id = self.kwargs['pk']

            #TODO avoid pk OR add CHECK

            # print("machine_id", machine_id)
            # print("machine_id", type(machine_id))
            # print("machine :", machine_model.Machine.objects.filter(pk=machine_id))
            machine = machine_model.Machine.objects.filter(pk=machine_id)
            return machine
        else:
            try:
                machines = machine_model.Machine.objects.all()
            except Exception as Error:
                raise Exception("Error", Error)
            else:
                if machines.count() == 1:
                    return machines
                else:
                    raise Exception("They are more then One machine")
