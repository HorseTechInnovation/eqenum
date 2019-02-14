from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse, FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django import forms
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from languages_plus.utils import associate_countries_and_languages

import tablib
from tablib import Dataset
from import_export import resources
from import_export.formats.base_formats import DEFAULT_FORMATS
from import_export.tmp_storages import TempFolderStorage
from import_export.admin import ImportMixin
from import_export.results import RowResult

from .models import *

TMP_STORAGE_CLASS = getattr(settings, 'IMPORT_EXPORT_TMP_STORAGE_CLASS',
                            TempFolderStorage)


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def update_culture_codes(request):
    associate_countries_and_languages()
    return HttpResponse("Done")



class Home(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = self.request.user

        context['enumtypes'] = EnumType.objects.prefetch_related('enum_set').all()

        return context


class EnumItemImportForm(forms.Form):

    enumtype = forms.ModelChoiceField(queryset=EnumType.objects.all())
    notes = forms.CharField(widget=forms.Textarea)
    import_file = forms.FileField(
        label=_('File to import')
    )
    input_format = forms.ChoiceField(
        label=_('Format'),
        choices=(),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        for i, f in enumerate(DEFAULT_FORMATS):
            choices.append((str(i), f().get_title(),))
        if len(DEFAULT_FORMATS) > 1:
            choices.insert(0, ('', '---'))

        self.fields['input_format'].choices = choices

        if 'enumtype' in kwargs:
            self.fields['enumtype'] = kwargs['enumtype']

class DummyAdminSite:
    name = ''
    def each_context(self, request):
        return {}


class EnumResourceNoEnumtype(resources.ModelResource):

    enumtype_id = None

    class Meta:
        model = Enum
        import_id_fields = ('ref',)
        fields = ('ref','name','emumtype','ordering')

    def __init__(self, *args, **kwargs):
        self.enumtype_id = kwargs['enumtype_id']

    def import_obj(self, obj, data, dry_run):
        """
        store enumtype pk to link the import to
        """
        obj.enumtype_id = self.enumtype_id
        super().import_obj(obj, data, dry_run)

    def before_save_instance(self, instance, using_transactions, dry_run):
        """
        fill in enumtypeid
        """
        instance.enumtype_id = self.enumtype_id



class ImportView(FormView, ImportMixin):

    template_name = "import.html"
    form_class = EnumItemImportForm
    success_url = '/thanks/'


    model = Enum
    resource_class = EnumResourceNoEnumtype
    admin_site = DummyAdminSite()
    import_template_name = 'import.html'

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """

        if 'confirm' in self.request.POST:
            return self.process_import(self.request, enumtype_id=request.POST.get("enumtype"))
        else:
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)

    def process_result(self, result, request):
        self.generate_log_entries(result, request)
        opts = self.model._meta

        success_message = _('Import finished, with {} new and ' \
                            '{} updated {}.').format(result.totals[RowResult.IMPORT_TYPE_NEW],
                                                      result.totals[RowResult.IMPORT_TYPE_UPDATE],
                                                      opts.verbose_name_plural)
        #post_import.send(sender=None, model=self.model)

        return HttpResponse(success_message)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        me = self.request.user

        context['enumtype'] = self.request.POST.get('enumtype', None)

        return context

    def get_resource_kwargs(self, request, *args, **kwargs):
        return {'enumtype_id': kwargs['enumtype_id']}

    def form_valid(self, form):
        # enumtype_resource = resources.modelresource_factory(model=EnumType)()
        #
        #
        # dataset = Dataset()
        # newdata = form.files['import_file']
        #
        # imported_data = dataset.load(newdata.read())
        # result = enumtype_resource.import_data(dataset, dry_run=True)  # Test the data import
        #
        # if not result.has_errors():
        #     enumtype_resource.import_data(dataset, dry_run=False)  # Actually import now
        #
        #
        # return super().form_valid(form)
        # import_formats = DEFAULT_FORMATS
#         # input_format = import_formats[
#         #     int(form.cleaned_data['input_format'])
#         # ]()
#         # tmp_storage = TMP_STORAGE_CLASS()(name=form.cleaned_data['import_file_name'])
#         # data = tmp_storage.read(input_format.get_read_mode())
#         # if not input_format.is_binary() and self.from_encoding:
#         #     data = force_text(data, self.from_encoding)
#         # dataset = input_format.create_dataset(data)
#         #
#         # result = self.process_dataset(dataset, form, request, *args, **kwargs)
#         #
#         # tmp_storage.remove()



        return self.import_action(self.request, enumtype_id=form.cleaned_data['enumtype'].pk)

