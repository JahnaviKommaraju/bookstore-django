from tabnanny import verbose
from tkinter import CASCADE
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify #transforms string to slug format

# Create your models here.
class Country(models.Model): #many-to-many example
    #a book can be published in many countries, a country can publish many books
    name=models.CharField(max_length=50)
    code=models.CharField(max_length=2)

    def __str__(self): #to display the name instead of country objects
        return self.name

    class Meta:  #to avoid extra "s" in admin panel
        verbose_name_plural ="Countries"


class Address(models.Model): #one-to-one example
    #one author has one address, one address belongs to one author
    street=models.CharField(max_length=80)
    postal_code=models.CharField(max_length=5)
    city=models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"
    
    class Meta:
        verbose_name_plural = "Address Entries" #to find out address model shld be output when plural is needed

class Author(models.Model):#one-to-many example
    #one book has one author,one author writes multiple books
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address=models.OneToOneField(Address,on_delete=models.CASCADE,null=True)
    def full_name(self):
        # return self.first_name+self.last_name
        #   or
        return f"{self.first_name} {self.last_name}"

    def __str__(self):  #how objects of this class are printed when we return a string
        # return f"{self.first_name}{self.last_name}"
        #   or
        return self.full_name()

class Book(models.Model):
    # id=models.AutoField()  -> no need to mention explicity, django will provide auto increment
    title=models.CharField(max_length=50)
    rating=models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    #author=models.CharField(null=True,max_length=100) #can have null value and will be null if not inserted
    author=models.ForeignKey(Author,on_delete=models.CASCADE,null=True,related_name="books") #Foerign Key -> one-to-many
        #on_delete should be used to say that if any of model gets deleted then what the class should do
        #CASCADE -> if any Author is deleted then all the related books should also be deleted 
        #null=True -> says that if any value is not there then we can have 'NULL' value
         #here related_name="books" -> it is for naming the inverse of relation
    is_bestselling=models.BooleanField(default=False)
    slug=models.SlugField(default="",blank=True,editable=True,null=False,db_index=True) #it automaticaaly converts the string Harry Potter 1-> harry-potter-1
                        #here,we have to use slug for every book , so its used more frequently and to improve its performance we
                        # have to use db_index=True  to access quickly so that db will save columns efficiently
                        #but adding db_index to each and every field will reduce the overall perfromance. 
                    #here, blank="True" says dajango that slug is not mandatory and can be blank/empty in admin panel
    published_countries=models.ManyToManyField(Country,null=False,related_name="books")
    #here, we can't use on_delete option 
    #bcoz in other relationships like one-to-one and one-to-many there are always 2 tables involved and then info about related table
    #is stored in one of the 2 tables but in many-to-many bcoz book have mutilple tables and we can't delete all of the tables
    #for many-to-many,
    #  django automatically creates a 3rd table for mapping behind the scenes n some mapping table holds 
    # 1 row per connection between country and book
    #i.e if 1 book is in 2 countries then 2 rows would be added to in between mapping table 
    #hence, when we delete a country djnago will go to mapping table and delete the connection here.So, thats why we don't setup on_delete
                   
    def get_absolute_url(self):
        # return reverse("book-detail", args=[self.id])
        return reverse("book-detail", args=[self.slug])

    ###no need of this as we have prepopulated slug in admin panel
    # def save(self,*args, **kwargs): #to override built in save()
    #     #before the db gets saved i want to update the db
    #     self.slug=slugify(self.title)
    #     super().save(*args, **kwargs )  #to make sure that django still calls the save method
    
    #utility methods
    def __str__(self):  #how objects of this class are printed when we return a string
        return f"{self.title}({self.rating})"

    #output all books and each book is clickable that gives more info
    