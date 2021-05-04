from django.db import models

# Create your models here.

class Movie(models.Model):
	movie_title = models.CharField(max_length=150)
	geners = models.IntegerField()
	director = models.CharField(max_length=100)
	movie_plot = models.TextField()


	def __str__(self):
		return self.movie_title
