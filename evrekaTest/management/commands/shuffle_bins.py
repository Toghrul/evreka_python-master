from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from evrekaTest.models import Bin, BinSensorRecord

from random import random

class Command(BaseCommand):

    def handle(self, *args, **options):
        all_bins = Bin.objects.all()
        today = datetime.now()
        for bin in all_bins:
            if bin.bin_id != 3168:
                records = BinSensorRecord.objects.filter(bin=bin, date__startswith=today.date()).order_by('-date')
                if len(records) > 0:
                    records[0].fullness_rate = random()
                    records[0].save()
                else:
                    records = BinSensorRecord.objects.filter(bin=bin, date__lte=today.date()).order_by('-date')
                    if len(records) > 0:
                        records[0].fullness_rate = random()
                        records[0].save()#


