from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = 'works'

router = routers.DefaultRouter()
router.register(r'work_types', views.WorkTypeViewSet, base_name='work_types')
router.register(r'art_types', views.ArtTypeViewSet, base_name='art_types')
router.register(r'igualas', views.IgualaViewSet, base_name='igualas')
router.register(r'art_igualas', views.ArtIgualaViewSet, base_name='art_igualas')
router.register(r'works', views.WorkViewSet, base_name='works')
router.register(r'art_works', views.ArtWorkViewSet, base_name='art_works')
router.register(r'files', views.FileViewSet, base_name='files')
router.register(r'work_designer', views.WorkDesignerViewSet, base_name='work_designer')
router.register(r'status_changes', views.StatusChangeViewSet, base_name='status_changes')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
