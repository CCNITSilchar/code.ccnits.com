from django.db import models
from functions import slug
# Create your models here.


class ProgrammingLanguage(models.Model):
	name = models.CharField(max_length=50)
	lang_code = models.CharField(max_length=50)
	extension = models.CharField(max_length=10)
	sample_code = models.TextField(null=True, blank=True)
	ace_lang_code = models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return '%s' % self.name


class Code(models.Model):
	name = models.CharField(max_length=100, null=True, blank=True)
	slug = models.CharField(max_length=8, null=True, blank=True, unique=True)
	he_slug = models.CharField(max_length=8, null=True, blank=True, unique=True)
	code_text = models.TextField(null=True, blank=True)
	cloned_from = models.ForeignKey("self", blank=True, null=True)
	run_count = models.IntegerField(default=0)
	public = models.BooleanField(default=True)
	programming_language = models.ForeignKey(ProgrammingLanguage)
	custom_input = models.TextField(null=True, blank=True)
	creation_timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
	update_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)

	def __str__(self):
		return '%s' % self.name

	def save(self, *args, **kwargs):
		super(Code, self).save(*args, **kwargs)
		self.slug = slug.encode(self.id)
		super(Code, self).save(*args, **kwargs)
