from django.urls import include, path
from . import views
from .views import open_flask
from rest_framework import routers

# The basic router URLs for interacting with our models
router = routers.DefaultRouter()
router.register(r'users', views.APIUserViewSet)
router.register(r'module', views.ModuleViewSet)
router.register(r'lecture', views.LectureViewSet)
router.register(r'lecturerecord', views.LectureRecordViewSet)

# Urls for our system, all the API links for our frontend to interact with + the link for running the flask app
urlpatterns = [
   path('api/', include(router.urls)),
   path('apiregister/', views.UserRegistrationAPIView.as_view(), name="api_register"),
   path('apilecture/', views.AddLectureAPIView.as_view(), name="api_lecture"),
   path('apimodule/', views.AddModuleAPIView.as_view(), name="api_module"),
   path('apiremove/module/', views.RemoveModuleAPIView.as_view(), name="api_remove_module"),
   path('apiremove/lecture/', views.RemoveLectureAPIView.as_view(), name="api_remove_lecture"),
   path('apirecord/', views.AddLectureRecordAPIView.as_view(), name="api_record"),
   path('flask/<str:mcode>/<str:lecture_id>/<str:date>/<str:time>/<str:attendance>/<str:day>', views.open_flask, name="start_flask")
]