from django.test import TestCase
from .models import Machine, Counter, Manifesto, New

class MachineManagersTests(TestCase):

    def test_create_machine(self):
        manifesto = Manifesto.objects.create(
            text="I'm Manifesto"
        )
        machine = Machine.objects.create(
            name='Ayris Machine',
            counter=Counter.objects.create(),
            manifesto=manifesto
        )
        news_list = ["nEw 1 ",
                     "New 2 "]
        for new in news_list:
            New.objects.create(
                machine=machine,
                text=new
            )

        self.assertEqual(machine.name, 'Ayris Machine')
        self.assertEqual(machine.counter.past_counter, 0)
        machine.counter.add_past_counter()
        self.assertEqual(machine.counter.past_counter, 1)
        self.assertEqual(machine.manifesto.text, "I'm Manifesto")
        self.assertEqual(machine.news.first().text, "nEw 1 ")
