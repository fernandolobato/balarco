import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from clients.models import Client, Contact


class WorkType(models.Model):
    """ The model that represents a type of work.

    E.g. Iguala, Graduación, Proyecto.

    Attributes:
    -----------
    name: CharField
        Name of the work type.
    """
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class ArtType(models.Model):
    """ The model that represents a type of art that compose a work.

    Attributes:
    -----------
    work_type: ForeignKey
        Relation to the WorkType that the ArtType is associated with.
    name: CharField
        Name of the art type.
    """
    work_type = models.ForeignKey(WorkType, related_name='art_types', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class Iguala(models.Model):
    """ The model that represents a client's Iguala.

    Attributes:
    -----------
    client: ForeignKey
        Relation to the client that has the Iguala.
    name: CharField
        Name of the Iguala to identify it easily.
    start_date: DateField
        Date when the Iguala starts.
    end_date: DateField
        Date when the Iguala ends.
    """
    client = models.ForeignKey(Client, related_name='igualas', on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)


class ArtIguala(models.Model):
    """ The model that represents the quantity and kind of arts that an Iguala contains.

    Attributes:
    -----------
    iguala: ForeignKey
        Relation that indicates the Iguala of a client.
    art_type: ForeignKey
        Relation that indicates the type of art of the iguala.
    quantity: IntegerField
        The quantity of that specific art type in that iguala.
    """
    iguala = models.ForeignKey(Iguala, related_name='art_iguala', on_delete=models.CASCADE)
    art_type = models.ForeignKey(ArtType, related_name='art_iguala', on_delete=models.CASCADE)

    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.iguala, self.art_type, self.quantity)


class Status(models.Model):
    """ Model that represent all possible status of a project.

    Attributes:
    -----------
    status_id: IntegerField
        Integer that indicates the status id of the STATUS tuple.
    """
    STATUS_PENDIENTE = 0
    STATUS_DISENO = 1
    STATUS_CUENTAS = 2
    STATUS_VALIDACION = 3
    STATUS_PRODUCCION = 4
    STATUS_POR_COBRAR = 5
    STATUS_POR_FACTURAR = 6
    STATUS_TERMINADO = 7
    STATUS = (
        (STATUS_PENDIENTE, 'Pendiente'),
        (STATUS_DISENO, 'Diseño'),
        (STATUS_CUENTAS, 'Cuentas'),
        (STATUS_VALIDACION, 'Validación'),
        (STATUS_PRODUCCION, 'Producción'),
        (STATUS_POR_COBRAR, 'Por cobrar'),
        (STATUS_POR_FACTURAR, 'Por facturar'),
        (STATUS_TERMINADO, 'Terminado'),
    )
    status_id = models.IntegerField(choices=STATUS)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.STATUS[self.status_id][1]


class Work(models.Model):
    """ Model that represents a work.

    Attributes:
    -----------
    executive: ForeignKey
        Relation with the executive that is managing the project.
    contact: ForeignKey
        Relation with the contact that request for the work.
    current_status: ForeignKey
        Relation with the status model to indicate the current status of the work.
    work_type: ForeignKey
        Relation with WorkType model that indicates the type of work the contact asked for.
    iguala: ForeignKey
        Optional relation with Iguala model in case the WorkType is an Iguala.
    creation_date: DateField
        Date that the project was requested for the client.
    name: CharField
        Name of the work to identify it.
    expected_delivery_date: DateField
        Date when the contact wants the product to be delivered.
    brief: TextField
        Description of the project.
    final_link: CharField
        Optional attribute that exists only when a designer finishes a work, it contains
        a url link to the location of the product.
    """
    executive = models.ForeignKey(User, related_name='managed_works', on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, related_name='works', on_delete=models.CASCADE)
    current_status = models.ForeignKey(Status, related_name='works', on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, related_name='works', on_delete=models.CASCADE)
    iguala = models.ForeignKey(Iguala, related_name='works', on_delete=models.CASCADE,
                               blank=True, null=True)

    creation_date = models.DateField(blank=True, null=True)
    name = models.CharField(max_length=100)
    expected_delivery_date = models.DateField()
    brief = models.TextField()
    final_link = models.CharField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.creation_date = datetime.date.today()
        super(Work, self).save(*args, **kwargs)


class ArtWork(models.Model):
    """ Model that represents the relation between a Work and its kind and quantity of arts.

    Attributes:
    -----------
    work: ForeignKey
        Relation with Work model.
    art_type: ForeignKey
        Relation with the art type requested by the work.
    quantity: IntegerField
        The quantity of that specific art type in that work.
    """
    work = models.ForeignKey(Work, related_name='art_works', on_delete=models.CASCADE)
    art_type = models.ForeignKey(ArtType, related_name='art_works', on_delete=models.CASCADE)

    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.work, self.art_type, self.quantity)


class File(models.Model):
    """ Model that represents a file uploaded by a user in a work.

    Attributes:
    -----------
    work: ForeignKey
        Relation with the work that the file belongs to.
    upload: FileField
        File to upload.
    """
    work = models.ForeignKey(Work, related_name='files', on_delete=models.CASCADE)

    upload = models.FileField(upload_to='work_files/')
    is_active = models.BooleanField(default=True)


class WorkDesigner(models.Model):
    """ Model that represents the assignation of a designer to a work.

    Attributes:
    -----------
    designer: ForeignKey
        Relation with User model with the designer that will be assigned to the work.
    work: ForeignKey
        Work in which the designer will be assigned.
    start_date: DateField
        The date when the designer was assigned to the work.
    end_date: DateField
        The date when the designer was unassigned to the work.
    """
    designer = models.ForeignKey(User, related_name='asigned_works', on_delete=models.CASCADE)
    work = models.ForeignKey(Work, related_name='work_designers', on_delete=models.CASCADE)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    active_work = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.designer, self.work)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.start_date = timezone.now()
        if not self.active_work:
            self.end_date = timezone.now()
        super(WorkDesigner, self).save(*args, **kwargs)


class StatusChange(models.Model):
    """ Model that represents the historical change of status of a work.

    Attributes:
    -----------
    work: ForeignKey
        Relation with the work.
    status: ForeignKey
        Relation with the Status model that indicates the status in that date.
    """
    work = models.ForeignKey(Work, related_name='status_changes', on_delete=models.CASCADE)
    status = models.ForeignKey(Status, related_name='status_changes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='status_changes', on_delete=models.CASCADE)

    date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.work, self.status, self.date)

    def save(self, *args, **kwargs):
        self.date = timezone.now()
        super(StatusChange, self).save(*args, **kwargs)
