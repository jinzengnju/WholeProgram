from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add-db$', views.add_data),
    url(r'addIdAndFilename$', views.write_filenameTo_db)

]