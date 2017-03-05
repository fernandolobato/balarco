import datetime

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory

from . import models
from . import views
from clients import models as client_models
from balarco import utils


class WorkTypeAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list work types.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = models.WorkType

        work_type_proyecto = models.WorkType.objects.create(
            name='Proyecto')
        work_type_graduacion = models.WorkType.objects.create(
            name='Graduación')
        work_type_iguala = models.WorkType.objects.create(
            name='Iguala')

        self.test_objects = [work_type_proyecto, work_type_graduacion, work_type_iguala]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'name': 'Work type 4',
            }

        self.data_edition_test = {
            'name': 'Proyectos',
            }

        self.edition_obj_idx = 0

        self.view = views.WorkTypeViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:work_types-list'
        self.url_detail = 'works:work_types-detail'
        self.factory = APIRequestFactory()


class ArtTypeAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list art types.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = models.ArtType

        work_type_graduacion = models.WorkType.objects.create(
            name='Graduación')
        work_type_iguala = models.WorkType.objects.create(
            name='Iguala')

        art_type_arte_complejo = models.ArtType.objects.create(
            name='Arte complejo',
            work_type=work_type_iguala)

        art_type_arte_abstracto = models.ArtType.objects.create(
            name='Arte abstracto',
            work_type=work_type_iguala)

        art_type_invitacion = models.ArtType.objects.create(
            name='Invitación',
            work_type=work_type_graduacion)

        self.test_objects = [art_type_arte_complejo, art_type_arte_abstracto, art_type_invitacion]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'name': 'Work type 4',
            'work_type': work_type_graduacion.id
            }

        self.data_edition_test = {
            'name': 'Arte complejo 2',
            'work_type': work_type_iguala.id
            }

        self.edition_obj_idx = 0

        self.view = views.ArtTypeViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:art_types-list'
        self.url_detail = 'works:art_types-detail'
        self.factory = APIRequestFactory()


class IgualaAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list igualas.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = models.Iguala

        client_starbucks = client_models.Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)

        client_oxxo = client_models.Client.objects.create(
            name='Test Oxxo',
            address='Epigmenio González 100',
            is_active=True)

        iguala_starbucks = models.Iguala.objects.create(
            client=client_starbucks,
            name='Iguala Starbucks',
            start_date=datetime.date.today(),
            end_date=datetime.date.today())

        iguala_oxxo = models.Iguala.objects.create(
            client=client_oxxo,
            name='Iguala Oxxo',
            start_date=datetime.date.today(),
            end_date=datetime.date.today())

        self.test_objects = [iguala_starbucks, iguala_oxxo]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'client': client_oxxo.id,
            'name': 'Iguala Oxxo 2',
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today()
            }

        self.data_edition_test = {
            'client': client_oxxo.id,
            'name': 'Iguala Oxxo 1',
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today()
            }

        self.edition_obj_idx = 1

        self.view = views.IgualaViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:igualas-list'
        self.url_detail = 'works:igualas-detail'
        self.factory = APIRequestFactory()


class ArtIgualaAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list arts from an iguala.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = models.ArtIguala

        client_starbucks = client_models.Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)

        client_oxxo = client_models.Client.objects.create(
            name='Test Oxxo',
            address='Epigmenio González 100',
            is_active=True)

        iguala_starbucks = models.Iguala.objects.create(
            client=client_starbucks,
            name='Iguala Starbucks',
            start_date=datetime.date.today(),
            end_date=datetime.date.today())

        iguala_oxxo = models.Iguala.objects.create(
            client=client_oxxo,
            name='Iguala Oxxo',
            start_date=datetime.date.today(),
            end_date=datetime.date.today())

        work_type_iguala = models.WorkType.objects.create(
            name='Iguala')

        art_type_arte_complejo = models.ArtType.objects.create(
            name='Arte complejo',
            work_type=work_type_iguala)

        art_type_arte_abstracto = models.ArtType.objects.create(
            name='Arte abstracto',
            work_type=work_type_iguala)

        art_iguala1 = models.ArtIguala.objects.create(
            iguala=iguala_starbucks,
            art_type=art_type_arte_complejo,
            quantity=50)

        art_iguala2 = models.ArtIguala.objects.create(
            iguala=iguala_oxxo,
            art_type=art_type_arte_abstracto,
            quantity=80)

        self.test_objects = [art_iguala1, art_iguala2]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'iguala': iguala_starbucks.id,
            'art_type': art_type_arte_abstracto.id,
            'quantity': 20
            }

        self.data_edition_test = {
            'iguala': iguala_oxxo.id,
            'art_type': art_type_arte_abstracto.id,
            'quantity': 30
            }

        self.edition_obj_idx = 1

        self.view = views.ArtIgualaViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:art_igualas-list'
        self.url_detail = 'works:art_igualas-detail'
        self.factory = APIRequestFactory()
