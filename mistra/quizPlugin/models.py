from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    score = models.IntegerField()
    correction = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text
    
class Test(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    min_score = models.IntegerField()
    
    questions = models.ManyToManyField(Question, related_name='tests')

    def __str__(self):
        return self.name

class Sex(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TestExecution(models.Model):
    id = models.AutoField(primary_key=True)
    execution_time = models.DateTimeField(auto_now_add=True)
    age = models.IntegerField()
    sex = models.ForeignKey(Sex, related_name='test_executions', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_executions')
    score = models.IntegerField()
    ip = models.GenericIPAddressField()
    duration = models.DurationField()
    revision_date = models.DateTimeField(null=True, blank=True)
    given_answer = models.ManyToManyField(Answer, related_name='test_executions')
    note = models.TextField()
    

