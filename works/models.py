from django.db import models
from django.contrib.auth.models import User

from clients.models import Client, Contact
from balarco import utils


class WorkType(models.Model):
    name = models.CharField(max_length=100)


class ArtType(models.Model):
    work_type = models.ForeignKey(WorkType, related_name='art_types', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)


class Iguala(models.Model):
    client = models.ForeignKey(Client, related_name='igualas', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()


class ArtIguala(models.Model):
    iguala = models.ForeignKey(Iguala, related_name='art_iguala', on_delete=models.CASCADE)
    art_type = models.ForeignKey(ArtType, related_name='art_iguala', on_delete=models.CASCADE)

    quantity = models.IntegerField()


class Status(models.Model):
    status_id = models.IntegerField(choices=utils.STATUS)

    def __str__(self):
        return utils.STATUS[self.status_id][1]


class Work(models.Model):
    executive = models.ForeignKey(User, related_name='managed_works', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='works', on_delete=models.CASCADE)
    current_status = models.ForeignKey(Status, related_name='works', on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, related_name='works', on_delete=models.CASCADE)
    iguala = models.ForeignKey(Iguala, related_name='works', on_delete=models.CASCADE, blank=True)

    creation_date = models.DateField()
    name = models.CharField(max_length=100)
    expected_delivery_date = models.DateField()
    brief = models.TextField()
    final_link = models.CharField(max_length=1000)


class ArtWork(models.Model):
    work = models.ForeignKey(Work, related_name='art_works', on_delete=models.CASCADE)
    art_type = models.ForeignKey(ArtType, related_name='art_works', on_delete=models.CASCADE)

    quantity = models.IntegerField()


class File(models.Model):
    work = models.ForeignKey(Work, related_name='files', on_delete=models.CASCADE)

    upload = models.FileField(upload_to='work_files/')


class WorkDesigner(models.Model):
    designer = models.ForeignKey(User, related_name='asigned_works', on_delete=models.CASCADE)
    work = models.ForeignKey(Work, related_name='work_designers', on_delete=models.CASCADE)

    start_date = models.DateField()
    end_date = models.DateField()


class StatusChange(models.Model):
    work = models.ForeignKey(Work, related_name='status_changes', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, related_name='status_changes', on_delete=models.CASCADE)

    date = models.DateField()
