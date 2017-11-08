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
# keep login out the API, its honestly just a bandaid for the lack
# of intimacy that our current mediums can provide
from ingestion import views as ingestionAPI
from ingestion import viewswebpages as ingestionPages
from ingestion import quanty as quanty

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ingest/(?P<usernameInput>\w+)/', ingestionAPI.ingestFiles, name='ingestFiles'),
    url(r'^process/(?P<usernameInput>\w+)/', quanty.processMind, name='processBOnk'),
    url(r'^mymind/', ingestionPages.mindPageCurrentUser, name='mindPageCurrentUser'),
    url(r'^mind/(?P<usernameInput>\w+)/', ingestionPages.mindPage, name='mindPage'),
    url(r'^api/mind-post/', ingestionPages.mindPageAPIPOST, name='mindPageAPIPOST'),
    url(r'^api/mind/(?P<usernameInput>\w+)/', ingestionPages.mindPageAPI, name='mindPageAPI'),
    url(r'^auth/', ingestionPages.loginRequest, name='loginRequest'),
    url(r'^login/', ingestionPages.loginPage, name='loginPage'),
    url(r'^downlink/(?P<frameid>\w+)/(?P<filename>.*)/', ingestionPages.downlinkFrameData, name='downlinkFrameData'),
    url(r'^$', ingestionPages.loginPage, name='rootpage'),#downlinkFrameData
]

"""
Example url regex
    url(r'^aframepage/(?P<pagename>\w+)/', views.aframeDailyPage, name='bufforce8'),
    url(r'^uploadaframepage/', views.aframeUploadPage, name='bufforce9'),
"""
