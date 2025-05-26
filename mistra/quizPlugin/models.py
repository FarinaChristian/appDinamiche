from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorie"

    def __str__(self):
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=255)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    
    class Meta:
        verbose_name = "Domanda"
        verbose_name_plural = "Domande"

    def __str__(self):
        return self.name


class Answer(models.Model):
    text = models.TextField()
    
    class AnswerScore(models.IntegerChoices):
        SERIOUS_ERROR = -1
        ERROR = 0
        CORRECT = 1
    score = models.IntegerField(choices=AnswerScore)
    
    correction = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    
    class Meta:
        verbose_name = "Risposta"
        verbose_name_plural = "Risposte"

    def __str__(self):
        return self.text


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    min_score = models.IntegerField()
    
    questions = models.ManyToManyField(Question, related_name='tests')
    
    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"

    def __str__(self):
        return self.name


class Sex(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "Sesso"
        verbose_name_plural = "Sesso"

    def __str__(self):
        return self.name


class TestExecution(models.Model):
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
    
    class Meta:
        verbose_name = "Esecuzione Test"
        verbose_name_plural = "Esecuzioni Test"
        ordering = ['-execution_time']
        
    def __str__(self):
        return "{}: {} - score {}".format(self.ip, self.execution_time, self.score)


class GivenAnswer(models.Model):
    test_execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Risposta Data"
        verbose_name_plural = "Risposte Date"
        
    def __str__(self):
        return self.id
