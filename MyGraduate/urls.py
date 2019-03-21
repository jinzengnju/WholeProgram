"""MyGraduate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from . import search,get_12fact
from django.conf.urls import include
from WenShuModel import urls as wenshu_urls

urlpatterns = [
    url(r'^search-form$', search.search_form),
    url(r'^wenshu', include(wenshu_urls)),

    url(r'^resultcalculate/$', search.search),
    url(r'^result_law/$', search.get_lawresult),

    url(r'^resultFactCalculate/$',get_12fact.search_wenshu),
    url(r'^result_fact/$', get_12fact.get_factresult),

    url(r'^analysis_content/$',get_12fact.get_content),
    url(r'^result_fact/case_content/$', get_12fact.show_content),


]
