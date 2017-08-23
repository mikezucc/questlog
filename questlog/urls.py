"""questlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from ingestion import views as ingestionViews
from ingestion import viewswebpages as ingestionPages

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ingest/audio/', ingestionViews.ingestAudio, name='ingestAudio'),
    url(r'^ingest/', ingestionPages.ingestionPage, name='ingestPage'),
    url(r'^$', ingestionPages.ingestionPage, name='ingestPage')
]

"""
Example url regex
    url(r'^aframepage/(?P<pagename>\w+)/', views.aframeDailyPage, name='bufforce8'),
    url(r'^uploadaframepage/', views.aframeUploadPage, name='bufforce9'),
"""
