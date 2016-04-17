from main.models import *
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.


class Home(TemplateView):
	template_name = "home.html"

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		programming_languages = ProgrammingLanguage.objects.order_by('name').filter()
		context["languages"] = programming_languages
		context["sample_code"] = programming_languages[0].sample_code
		return context


class Sample(View):

	def get(self, request):
		context = dict()
		if request.is_ajax() and "lang_id" in request.GET:
			success = True
			try:
				lang_id = int(request.GET.get('lang_id'))
				language = ProgrammingLanguage.objects.get(id=lang_id)
			except ProgrammingLanguage.DoesNotExist:
				success = False
			except ValueError:
				success = False

			if success:
				context['success'] = True
				context['sample'] = language.sample_code
				context['ace_mode'] = language.ace_lang_code
			else:
				context['success'] = False
		return JsonResponse(context)


class SaveCode(View):

	def post(self, request):
		context = dict()
		if request.is_ajax() and "lang_id" in request.POST:
			success = True
			slug = None
			try:
				lang_id = int(request.POST.get('lang_id'))
				language = ProgrammingLanguage.objects.get(id=lang_id)
				slug = (request.POST.get('slug'))
				user_code = (request.POST.get('code'))
				code = Code.objects.get(slug=slug)
				code.code_text = user_code
				code.programming_language = language
				code.save()
			except Code.DoesNotExist:
				lang_id = int(request.POST.get('lang_id'))
				language = ProgrammingLanguage.objects.get(id=lang_id)
				user_code = (request.POST.get('code'))
				code = Code()
				code.code_text = user_code
				code.programming_language = language
				code.save()
				slug = code.slug
			except Exception:
				success = False

			if success:
				context['success'] = True
				context['slug'] = slug
			else:
				context['success'] = False
		return JsonResponse(context)

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(SaveCode, self).dispatch(*args, **kwargs)





