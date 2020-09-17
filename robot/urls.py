from django.conf.urls import url
from robot import views


urlpatterns = [
    url(r'^exam$', views.show_exam_handle_index_controller)
]