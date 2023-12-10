from django.db import models

class Status(models.TextChoices):
    PREPARATION = "preparation","preparation"
    ANNOTATION = "annotation","annotation"
    #VALIDATION = "validation","validation"
    FINISHED = "done","done"

class Batch(models.Model):
    class Meta:
        verbose_name_plural = "batches"
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    task = models.CharField(max_length=128)
    priority = models.IntegerField()
    status = models.CharField(max_length=64,choices=Status.choices,default=Status.PREPARATION,db_index=True)
    # how many answers per question to gather
    required_answers = models.IntegerField()

class Question(models.Model):
    batch = models.ForeignKey(Batch,on_delete=models.CASCADE)
    data = models.TextField()
    meta = models.TextField()

class Answers(models.TextChoices):
    ACCEPT = "accept","accept"
    IGNORE = "ignore","ignore"
    REJECT = "reject","reject"

class HateLevel(models.TextChoices):
    NONE = "no hate","no hate"
    LOW = "low hate","low hate"
    HIGH = "high hate","high hate"

class HateCathegory(models.TextChoices):
    RACE = "race","race"
    RELIGION = "religion","religion"
    APPEREANCE = "appereance","appereance"
    DISABILITY = "disability","disability"
    SEXUAL_ORIENTATION = "sexual_orientation", "sexual orientation"
    IDEOLOGY = "ideology","ideology"
    LIFESTYLE = "lifestyle","lifestyle"
    CYBERBULY = "cyberbuly","cyberbuly"


class Annotation(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    hate_level = models.CharField(max_length=64,choices=Status.choices,default=Status.PREPARATION)
    hate_cathegory = models.CharField(max_length=64,choices=Status.choices,default=Status.PREPARATION)
    username = models.CharField(db_index=True,max_length=128)
    answer = models.CharField(max_length=64,choices=Answers.choices)
    created_at = models.DateTimeField(auto_now_add=True,db_index=True)


# Create your models here.
