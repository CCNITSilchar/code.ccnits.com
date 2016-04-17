from main.models import *
from django.views.generic.base import TemplateView

# Create your views here.


class Home(TemplateView):
	template_name = "home.html"

	def get_context_data(self, **kwargs):
		context = super(Home, self).get_context_data(**kwargs)
		programming_languages = ProgrammingLanguage.objects.filter()
		context["languages"] = programming_languages
		return context
