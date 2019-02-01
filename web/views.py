from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from languages_plus.utils import associate_countries_and_languages


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def update_culture_codes(request):
    associate_countries_and_languages()
    return HttpResponse("Done")