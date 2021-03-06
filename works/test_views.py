import datetime

from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse

from . import models, views, serializers
from clients import models as client_models
from balarco import utils


class WorkTypeAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list work types.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.WorkType
        self.serializer_class = serializers.WorkTypeSerializer

        work_type_proyecto = models.WorkType.objects.create(
            work_type_id=0)
        work_type_graduacion = models.WorkType.objects.create(
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

        self.test_objects = [work_type_proyecto, work_type_graduacion, work_type_iguala]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'work_type_id': 2,
            }

        self.data_filtering_test = {
            'name': 'Proyecto',
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'work_type_id': 2,
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
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.ArtType
        self.serializer_class = serializers.ArtTypeSerializer

        work_type_graduacion = models.WorkType.objects.create(
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

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

        self.data_filtering_test = {
            'name': 'Invitación',
        }

        self.number_of_filtered_objects = 1

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
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.Iguala
        self.serializer_class = serializers.IgualaSerializer

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
            work_type_id=2)

        art_type_arte_complejo = models.ArtType.objects.create(
            name='Arte complejo',
            work_type=work_type_iguala)

        art_type_arte_abstracto = models.ArtType.objects.create(
            name='Arte abstracto',
            work_type=work_type_iguala)

        art_iguala1 = {
            'art_type': art_type_arte_complejo.id,
            'quantity': 50
        }

        art_iguala2 = {
            'art_type': art_type_arte_abstracto.id,
            'quantity': 80
        }

        self.test_objects = [iguala_starbucks, iguala_oxxo]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'client': client_oxxo.id,
            'name': 'Iguala Oxxo 2',
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today(),
            'art_iguala': [art_iguala1, art_iguala2]
            }

        self.data_filtering_test = {
            'name': 'Iguala Oxxo',
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'client': client_oxxo.id,
            'name': 'Iguala Oxxo 1',
            'start_date': datetime.date.today(),
            'end_date': datetime.date.today(),
            'art_iguala': [art_iguala1, art_iguala2]
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
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.ArtIguala
        self.serializer_class = serializers.ArtIgualaSerializer

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
            work_type_id=2)

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

        self.data_filtering_test = {
            'quantity': 50,
        }

        self.number_of_filtered_objects = 1

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


class StatusAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list status.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.Status
        self.serializer_class = serializers.StatusSerializer

        status_1 = models.Status.objects.create(
            status_id=0)
        status_2 = models.Status.objects.create(
            status_id=1)
        status_3 = models.Status.objects.create(
            status_id=2)

        self.test_objects = [status_1, status_2, status_3]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'status_id': 3,
            }

        self.data_filtering_test = {
            'status_id': 1,
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'status_id': 4,
            }

        self.edition_obj_idx = 0

        self.view = views.StatusViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:status-list'
        self.url_detail = 'works:status-detail'
        self.factory = APIRequestFactory()


class WorkAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list arts from a work.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.Work
        self.serializer_class = serializers.WorkSerializer

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
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

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

        art_work1 = {
            'art_type': art_type_arte_complejo.id,
            'quantity': 300
            }

        art_work2 = {
            'art_type': art_type_arte_abstracto.id,
            'quantity': 200
            }

        art_work3 = {
            'art_type': art_type_invitacion.id,
            'quantity': 100
            }

        art_work4 = {
            'art_type': art_type_menu.id,
            'quantity': 50
            }

        self.data_creation_test = {
            'executive': self.user.id,
            'contact': contact_instance_julian.id,
            'current_status': status_pendiente.id,
            'work_type': work_type_graduacion.id,
            'name': 'Work graduacion starbucks',
            'expected_delivery_date': '2017-05-18',
            'brief': 'Brief3',
            'art_works': [art_work1, art_work2, art_work3, art_work4]
            }

        self.data_filtering_test = {
            'contact': contact_instance_julian.id,
        }

        self.number_of_filtered_objects = 1

        work_designer1 = {
            'designer': self.user.id,
            'active_work': True
            }

        self.data_edition_test = {
            'name': 'Work graduacion starbucks',
            'expected_delivery_date': '2017-08-20',
            'brief': 'Brief2 edited',
            'work_designers': [work_designer1]
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
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.ArtWork
        self.serializer_class = serializers.ArtWorkSerializer

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
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

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

        self.data_filtering_test = {
            'art_type': art_type_invitacion.id,
        }

        self.number_of_filtered_objects = 1

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


class FileAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list arts from an iguala.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        self.obj_class = models.File
        self.serializer_class = serializers.FileSerializer

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
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

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

        file1 = SimpleUploadedFile("file1.txt", b"file_content")
        file2 = SimpleUploadedFile("file2.txt", b"file_content")
        file_instance_1 = models.File.objects.create(
            work=work_iguala_starbucks,
            filename='File1',
            upload=file1)
        file_instance_2 = models.File.objects.create(
            work=work_graduacion_oxxo,
            filename='File2',
            upload=file2)

        self.test_objects = [file_instance_1, file_instance_2]
        self.number_of_initial_objects = len(self.test_objects)

        file3 = SimpleUploadedFile("file3.txt", b"file_content")
        self.data_creation_test = {
            'work': work_iguala_starbucks.id,
            'filename': 'File3',
            'upload': file3.file,
            }

        self.data_filtering_test = {
            'work': work_iguala_starbucks.id,
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'work': work_graduacion_oxxo.id
            }

        self.edition_obj_idx = 1

        self.view = views.FileViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:files-list'
        self.url_detail = 'works:files-detail'
        self.factory = APIRequestFactory()

    def test_object_creation(self):
        pass


class WorkDesignerAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list work-designer
    relation.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        designer1 = User.objects.create_user(username='designer1',
                                             password='test_password')
        designer2 = User.objects.create_user(username='designer2',
                                             password='test_password')
        self.obj_class = models.WorkDesigner
        self.serializer_class = serializers.WorkDesignerSerializer

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
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

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

        work_designer1 = models.WorkDesigner.objects.create(
            designer=designer1,
            work=work_iguala_starbucks,
            active_work=True)
        work_designer2 = models.WorkDesigner.objects.create(
            designer=designer2,
            work=work_graduacion_oxxo,
            active_work=True)

        self.test_objects = [work_designer1, work_designer2]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'designer': designer1.id,
            'work': work_graduacion_oxxo.id,
            'active_work': True
            }

        self.data_filtering_test = {
            'designer': designer2.id,
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'designer': designer2.id,
            'work': work_graduacion_oxxo.id,
            'active_work': False
            }

        self.edition_obj_idx = 1

        self.view = views.WorkDesignerViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:work_designer-list'
        self.url_detail = 'works:work_designer-detail'
        self.factory = APIRequestFactory()


class StatusChangeAPITest(utils.GenericAPITest):
    """Tests to verify the basic usage of the REST API to create, modify and list status changes.
    It inherits from utils.GenericAPITest and add the necessary class attributes.
    """
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        url = reverse('users:api_login')
        data = {'username': 'test_user', 'password': 'test_password'}
        self.client.post(url, data, format='json')

        designer1 = User.objects.create_user(username='designer1',
                                             password='test_password')
        designer2 = User.objects.create_user(username='designer2',
                                             password='test_password')
        self.obj_class = models.StatusChange
        self.serializer_class = serializers.StatusChangeSerializer

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
            work_type_id=1)
        work_type_iguala = models.WorkType.objects.create(
            work_type_id=2)

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

        status_change1 = models.StatusChange.objects.create(
            work=work_iguala_starbucks,
            status=status_diseno,
            user=designer1)
        status_change2 = models.StatusChange.objects.create(
            work=work_graduacion_oxxo,
            status=status_pendiente,
            user=designer2)

        self.test_objects = [status_change1, status_change2]
        self.number_of_initial_objects = len(self.test_objects)

        self.data_creation_test = {
            'work': work_graduacion_oxxo.id,
            'status': status_diseno.id,
            'user': designer2.id
            }

        self.data_filtering_test = {
            'work': work_iguala_starbucks.id,
        }

        self.number_of_filtered_objects = 1

        self.data_edition_test = {
            'status': status_pendiente.id,
            }

        self.edition_obj_idx = 1

        self.view = views.StatusChangeViewSet.as_view({
                                'get': 'list',
                                'post': 'create',
                                'put': 'update',
                                'patch': 'partial_update',
                                'delete': 'destroy'
                                })

        self.url_list = 'works:status_changes-list'
        self.url_detail = 'works:status_changes-detail'
        self.factory = APIRequestFactory()
