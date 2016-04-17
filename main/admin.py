from django.contrib import admin

# Register your models here.

from main.models import *


class ProgrammingLanguageAdmin(admin.ModelAdmin):
	list_display = ['name', 'lang_code', 'extension']
	search_fields = ('name', 'lang_code', 'extension')

admin.site.register(ProgrammingLanguage, ProgrammingLanguageAdmin)


class CodeAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'run_count', 'programming_language', 'public']
	search_fields = ('name', 'slug', 'programming_language', 'code')

admin.site.register(Code, CodeAdmin)
