from django.db import models
from django.utils import timezone
import random
import string


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
        return "{} - {}".format(self.name, self.category.name) 


class Answer(models.Model):
    text = models.TextField()
    
    class AnswerScore(models.IntegerChoices):
        SERIOUS_ERROR = -1, "Errore Grave"
        ERROR = 0, "Errore"
        CORRECT = 1, "Corretto"
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
    age = models.IntegerField(verbose_name="Età utente")
    ip = models.GenericIPAddressField(verbose_name="Indirizzo IP utente")
    execution_time = models.DateTimeField(auto_now_add=True, verbose_name="Data d'esecuzione")
    score = models.IntegerField(verbose_name="Punteggio", default=0)
    duration = models.DurationField(verbose_name="Durata")
    revision_date = models.DateTimeField(null=True, blank=True, verbose_name="Data di revisione")
    note = models.TextField(verbose_name="Note di revisione")
    
    sex = models.ForeignKey(Sex, related_name='test_executions', on_delete=models.CASCADE, verbose_name="Sesso utente")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='test_executions', verbose_name="Test relativo")
    
    revision_code = models.CharField(max_length=12, unique=True, editable=False, blank=True, verbose_name="Codice di revisione")
    
    class Meta:
        verbose_name = "Esecuzione Test"
        verbose_name_plural = "Esecuzioni Test"
        ordering = ['-execution_time']
        
    def __str__(self):
        return self.revision_code
    
    def _generate_unique_revision_code(self):
        """Generates a unique revision code"""
        if not self.execution_time:
            exec_time = timezone.now().date()
        else:
            exec_time = self.execution_time
            
        date_str = exec_time.strftime("%Y%m%d")
        
        while True:
            random_chars = "".join(random.choices(string.ascii_uppercase, k=3))
            potential_code = f"{date_str}-{random_chars}"
            
            # check if it already exists
            if not TestExecution.objects.filter(revision_code=potential_code).exists():
                return potential_code
            
    def save(self, *args, **kwargs):
        if not self.revision_code:
            self.revision_code = self._generate_unique_revision_code()
        
        super().save(*args, **kwargs)


class GivenAnswer(models.Model):
    test_execution = models.ForeignKey(TestExecution, on_delete=models.CASCADE, related_name='given_answers_through')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Risposta Data"
        verbose_name_plural = "Risposte Date"

    def __str__(self):
        if self.pk:
            return f"Esecuzione: {self.test_execution.revision_code} - Domanda: {self.answer.question.name[:30]}... - Risposta: {self.answer.text[:30]}..."
        return f"Nuova Risposta Data (ID: {self.id})"


    # Proprietà per facilitare l'accesso nell'admin inline
    @property
    def question_text(self):
        return self.answer.question.text

    @property
    def answer_text(self):
        return self.answer.text

    @property
    def answer_score_value(self):
        return self.answer.score

    @property
    def answer_score_display(self):
        return self.answer.get_score_display()

    @property
    def answer_correction(self):
        return self.answer.correction
