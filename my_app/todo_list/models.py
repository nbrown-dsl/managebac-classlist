from django.db import models

# create databse table with attributes.
class List(models.Model):
    item =  models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=50, default="")
    #managebac fields
    className =  models.CharField(max_length=200,default="")
    program =  models.CharField(max_length=50,default="")

    def __str__(self):
        return self.item + ' completed: ' + str(self.completed) + ' priority: ' +self.priority

