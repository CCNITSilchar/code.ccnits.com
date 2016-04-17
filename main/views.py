from main.models import *
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
from django.conf import settings
from django.template import loader, Context
from django.http import HttpResponse

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
	def post(self, request, *args, **kwargs):
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

	def get(self, request, *args, **kwargs):
		return JsonResponse({})

	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(SaveCode, self).dispatch(*args, **kwargs)


class ViewCode(TemplateView):
	template_name = "view.html"

	def get_context_data(self, **kwargs):
		context = super(ViewCode, self).get_context_data(**kwargs)
		context['success'] = True
		if "slug" in kwargs:
			try:
				code = Code.objects.get(slug=kwargs["slug"])
				context['success'] = True
				context['code'] = code
			except Code.DoesNotExist:
				context['success'] = False
		else:
			context['success'] = False

		return context


class CompileCode(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(CompileCode, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		context = dict()
		if request.is_ajax() and "slug" in request.POST:
			success = True
			slug = request.POST.get("slug")
			try:
				code = Code.objects.get(slug=slug)
				data = {
						'client_secret': settings.HE_CLIENT_SECRET,
						'async': 0,
						'source': code.code_text,
						'lang': code.programming_language.lang_code,
						'time_limit': 5,
						'memory_limit': 262144,
					}
				r = requests.post(settings.HE_COMPILE_URL, data)
				res = r.json()
				code.he_slug = res['code_id']
				code.save()
				context['output'] = res['compile_status']
			except Code.DoesNotExist:
				success = False
			except Exception:
				success = False
			context['success'] = success
		return JsonResponse(context)

	def get(self, request, *args, **kwargs):
		return JsonResponse({})


class RunCode(View):
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super(RunCode, self).dispatch(*args, **kwargs)

	def post(self, request, *args, **kwargs):
		context = dict()
		if request.is_ajax() and "slug" in request.POST:
			success = True
			slug = request.POST.get("slug")
			try:
				code = Code.objects.get(slug=slug)
				data = {
						'client_secret': settings.HE_CLIENT_SECRET,
						'async': 0,
						'source': code.code_text,
						'lang': code.programming_language.lang_code,
						'input': request.POST.get("custom_input"),
						'time_limit': 5,
						'memory_limit': 262144,
					}
				r = requests.post(settings.HE_RUN_URL, data)
				res = r.json()
				code.he_slug = res['code_id']
				code.run_count += 1
				code.save()
				context['output'] = res['run_status']['output']
				context['time_taken'] = res['run_status']['time_used']
				context['memory_taken'] = res['run_status']['memory_used']
			except Code.DoesNotExist:
				success = False
			except Exception:
				success = False
			context['success'] = success
		return JsonResponse(context)

	def get(self, request, *args, **kwargs):
		return JsonResponse({})


class DownloadCode(View):
	def get(self, request, **kwargs):
		if "slug" in kwargs:
			slug = kwargs["slug"]
			try:
				code = Code.objects.get(slug=slug)
				response = HttpResponse(content_type='text/plain')
				response['Content-Disposition'] = 'attachment; filename="'+code.slug+'.'+code.programming_language.extension+'"'
				t = loader.get_template('code.txt')
				c = Context({'data': code.code_text,})
				response.write(t.render(c))
				return response
			except Code.DoesNotExist:
				return HttpResponse("Invalid Download!")
		else:
			return HttpResponse("Invalid Download!")