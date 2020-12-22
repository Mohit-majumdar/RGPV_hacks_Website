from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Semseter(models.Model):
    sem = models.IntegerField(null=True)
    def __str__(self):
        return str(self.sem)



class Branch(models.Model):
    branch = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.branch


class Book(models.Model):
    sem = models.ForeignKey(Semseter,on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    book =  models.CharField(max_length=100,null=True)

    def __str__(self):
        return self.book + '--' + 'sem:'+str(self.sem)

class User_contect(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    mobile = models.IntegerField(null=True)
    def __str__(self):
        return self.user.username +'--'+ str(self.mobile)

class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    moblie = models.ForeignKey(User_contect,on_delete=models.CASCADE,null=True)
    book = models.ForeignKey(Book,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return 'order no.' + '--' + str(self.id)


class Notes(models.Model): #for Notes
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    sem = models.ForeignKey(Semseter,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50,null=True)
    note = models.FileField(null=True)
    date = models.DateField(null=True)

    def __str__(self):
        return self.name
class Previous_year_question(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True)
    sem = models.ForeignKey(Semseter,on_delete=models.CASCADE,null=True)
    year = models.IntegerField(null=True)
    file = models.FileField(null=True)

    def __str__(self):
        return self.name + '  ' + str(self.year)




class Suggetion_Comment(models.Model):
    name = models.CharField(max_length=20,null=True)
    email = models.EmailField(null=True)
    massege = models.TextField(max_length = 400, null= True)

    def __str__(self):
        return self.massege

class No_downloads(models.Model):
    note = models.ForeignKey(Notes,on_delete=models.CASCADE,null=True)
    downloads = models.IntegerField(null=True)

    def __str__(self):
        return self.note.name + "--" + str(self.downloads)






