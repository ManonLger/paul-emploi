from django.db import models

from api.models.fields import Degree, Skill, Location, Language


class Formation(models.Model):
    name = models.CharField(max_length=255)
    required_skills = models.ManyToManyField(Skill, related_name='required_skills')
    acquired_skills = models.ManyToManyField(Skill, related_name='acquired_skills')
    required_degrees = models.ManyToManyField(Degree, related_name='required_degrees')
    acquired_degree = models.ForeignKey(Degree, null=True)
    duration = models.CharField(max_length=255, null=True)
    location = models.ForeignKey(Location, null=True)
    language = models.ForeignKey(Language, null=True)
