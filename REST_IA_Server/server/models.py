from django.db import models


# Create your models here.
class Owner(models.Model):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'owner'


class Application(models.Model):
    name = models.CharField(max_length=50, blank=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="expediteur")

    class Meta:
        db_table = 'application'


class TypePage(models.Model):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'typepage'


class Page(models.Model):
    url = models.CharField(max_length=100, blank=False)
    pge_estimated_time = models.IntegerField()  #Temps estimé sur la page en millisecondes.
    type_page = models.ForeignKey(TypePage, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'page'


class User(models.Model):
    class Meta:
        db_table = 'user'


class Visite(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    time = models.IntegerField(blank=True, null=True)  #En millisecondes
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)

    class Meta:
        db_table = 'visite'


class TypeElement(models.Model):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'typeelement'


class Element(models.Model):
    name = models.CharField(max_length=50, blank=False)
    type_element = models.ForeignKey(TypeElement, on_delete=models.CASCADE)

    class Meta:
        db_table = 'element'


class TypeAction(models.Model):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        db_table = 'typeaction'


class Action(models.Model):
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    typeaction = models.ForeignKey(TypeAction, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'action'
