

from django.urls import path, include, re_path
from django.conf.urls import url
from django.contrib.auth import views
from django.conf import settings

from importlib import import_module



from allauth.socialaccount import providers
from django.conf.urls.static import static

from django.contrib import admin

from django.contrib.auth import views as auth_views


from django.contrib.auth.decorators import login_required, user_passes_test


from rest_framework import routers, serializers, viewsets

#from registration.backends.simple.views import RegistrationView
#from web.forms import CustomUserForm
import os

challenge_dir = os.path.join(settings.BASE_DIR,".well-known/acme-challenge")

admin.autodiscover()

#
# from tastypie.api import Api

from web.views import *
# from web.api import *


#from web.importexport import ImportEntries,upload_entries, event_starttimes_export, event_results_export, \


# router = routers.DefaultRouter()
# router.register(r'tests', TestSheetViewSet)
#


def can_organise(user):
    if user and user.is_authenticated:
        return user.is_superuser or user.is_organiser
    else:
        return False


urlpatterns = [
    # path('api/v2/', include(router.urls)),
    # path('api/v2/check/', last_update_check, name="last_update_check"),
    # path('api/v2/publish_comp/', publish_comp, name="publish_comp"),
    #path('api/v2/score/', quick_save_score, name="quick_save_score"),


    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('update_culture_codes/', update_culture_codes, name='update_culture_codes'),



    path('account/', include('django.contrib.auth.urls')),

    path('accounts/', include('allauth.urls')),

    path('js_error_hook/', include('django_js_error_hook.urls')),

    path('admin/doc/',include('django.contrib.admindocs.urls')),



    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]





if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)

