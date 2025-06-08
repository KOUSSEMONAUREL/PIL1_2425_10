from django.db import models

class Articles(models.Model):
    titre = models.CharField(max_length=200)
    contenue = models.TextField()
    prix = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to= 'images', blank=True)
    slug = models.SlugField(null=True)
    actif = models.BooleanField(default= True)

    class Meta:
        verbose_name = ("Article")
        verbose_name_plural = ("Articles")
        
    def __str__(self):
        return self.titre   