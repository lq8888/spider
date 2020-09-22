from django.conf.urls import url
from robot import views


urlpatterns = [
    url(r'^exam$', views.show_exam_handle_index_controller),
    url(r'^exam/all$', views.get_exam_all_controller),
    url(r'^exam/(\d+)$', views.get_exam_new_controller),
]