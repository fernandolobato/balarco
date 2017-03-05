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


class WorkAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list arts from a work.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = models.Work

        client_starbucks = client_models.Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)
        client_oxxo = client_models.Client.objects.create(
            name='Test Oxxo',
            address='Epigmenio González 100',
            is_active=True)

        contact_instance_julian = client_models.Contact.objects.create(
            name='Julian',
            last_name='Niebieskikiwat',
            charge='Manager',
            landline='4471172395',
            mobile_phone_1='26416231',
            email='julian@elguandul.com',
            alternate_email='julio@hotmail.com',
            client=client_starbucks,
            is_active=True)
        contact_instance_hector = client_models.Contact.objects.create(
            name='Hector',
            last_name='Sanchez',
            charge='Developer',
            landline='4426683012',
            mobile_phone_1='5555555',
            email='hector@eldominio.com',
            client=client_oxxo,
            is_active=True)

        iguala_starbucks = models.Iguala.objects.create(
            client=client_starbucks,
            name='Iguala Starbucks',
            start_date=datetime.date.today(),
            end_date=datetime.date.today())

        work_type_graduacion = models.WorkType.objects.create(
            name='Graduación')
        work_type_iguala = models.WorkType.objects.create(
            name='Iguala')

        status_pendiente = models.Status.objects.create(
            status_id=models.Status.STATUS_PENDIENTE)
        status_diseno = models.Status.objects.create(
            status_id=models.Status.STATUS_DISENO)

        work_iguala_starbucks = models.Work.objects.create(
            executive=self.user,
            contact=contact_instance_julian,
            current_status=status_diseno,
            work_type=work_type_iguala,
            iguala=iguala_starbucks,
            name='Work iguala starbucks',
            expected_delivery_date=datetime.date.today(),
            brief='Brief1')
        work_graduacion_oxxo = models.Work.objects.create(
            executive=self.user,
            contact=contact_instance_hector,
            current_status=status_pendiente,
            work_type=work_type_graduacion,
            name='Work graduación oxxo',
            expected_delivery_date=datetime.date.today(),
            brief='Brief2')

        self.test_objects = [work_iguala_starbucks, work_graduacion_oxxo]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'executive': self.user.id,
            'contact': contact_instance_julian.id,
            'current_status': status_pendiente.id,
            'work_type': work_type_graduacion.id,
            'name': 'Work graduacion starbucks',
            'expected_delivery_date': '2017-05-18',
            'brief': 'Brief3'
            }

        self.data_edition_test = {
            'name': 'Work graduacion starbucks',
            'expected_delivery_date': '2017-08-20',
            'brief': 'Brief2 edited'
            }

        self.edition_obj_idx = 1

        self.view = views.WorkViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:works-list'
        self.url_detail = 'works:works-detail'
        self.factory = APIRequestFactory()


class ArtWorkAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list arts from an iguala.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.obj_class = models.ArtWork

        client_starbucks = client_models.Client.objects.create(
            name='Test Starbucks',
            address='Felipe Ángeles 225',
            is_active=True)
        client_oxxo = client_models.Client.objects.create(
            name='Test Oxxo',
            address='Epigmenio González 100',
            is_active=True)

        contact_instance_julian = client_models.Contact.objects.create(
            name='Julian',
            last_name='Niebieskikiwat',
            charge='Manager',
            landline='4471172395',
            mobile_phone_1='26416231',
            email='julian@elguandul.com',
            alternate_email='julio@hotmail.com',
            client=client_starbucks,
            is_active=True)
        contact_instance_hector = client_models.Contact.objects.create(
            name='Hector',
            last_name='Sanchez',
            charge='Developer',
            landline='4426683012',
            mobile_phone_1='5555555',
            email='hector@eldominio.com',
            client=client_oxxo,
            is_active=True)

        iguala_starbucks = models.Iguala.objects.create(
            client=client_starbucks,
            name='Iguala Starbucks',
            start_date=datetime.date.today(),
            end_date=datetime.date.today())

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
        art_type_menu = models.ArtType.objects.create(
            name='Menú',
            work_type=work_type_graduacion)

        status_pendiente = models.Status.objects.create(
            status_id=models.Status.STATUS_PENDIENTE)
        status_diseno = models.Status.objects.create(
            status_id=models.Status.STATUS_DISENO)

        work_iguala_starbucks = models.Work.objects.create(
            executive=self.user,
            contact=contact_instance_julian,
            current_status=status_diseno,
            work_type=work_type_iguala,
            iguala=iguala_starbucks,
            name='Work iguala starbucks',
            expected_delivery_date=datetime.date.today(),
            brief='Brief1')
        work_graduacion_oxxo = models.Work.objects.create(
            executive=self.user,
            contact=contact_instance_hector,
            current_status=status_pendiente,
            work_type=work_type_graduacion,
            name='Work graduación oxxo',
            expected_delivery_date=datetime.date.today(),
            brief='Brief2')

        art_work1 = models.ArtWork.objects.create(
            work=work_iguala_starbucks,
            art_type=art_type_arte_complejo,
            quantity=50)
        art_work2 = models.ArtWork.objects.create(
            work=work_iguala_starbucks,
            art_type=art_type_arte_abstracto,
            quantity=65)
        art_work3 = models.ArtWork.objects.create(
            work=work_graduacion_oxxo,
            art_type=art_type_invitacion,
            quantity=300)

        self.test_objects = [art_work1, art_work2, art_work3]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'work': work_graduacion_oxxo.id,
            'art_type': art_type_menu.id,
            'quantity': 300
            }

        self.data_edition_test = {
            'quantity': 300
            }

        self.edition_obj_idx = 1

        self.view = views.ArtWorkViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:art_works-list'
        self.url_detail = 'works:art_works-detail'
        self.factory = APIRequestFactory()
