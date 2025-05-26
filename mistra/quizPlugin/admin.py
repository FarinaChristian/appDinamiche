from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Test)
admin.site.register(Sex)
admin.site.register(GivenAnswer)

class GivenAnswerInline(admin.TabularInline):
    model = GivenAnswer
    
    # Campi da mostrare nell'inline
    fields = ('get_question_name', 'question_text_display', 'answer_text_display', 'formatted_score', 'answer_correction_display')
    readonly_fields = fields

    extra = 0
    can_delete = False

    verbose_name = "Risposta data"
    verbose_name_plural = "Dettaglio Risposte Date e Punteggi"
    
    classes = ('collapse',)

    # Metodi per mostrare i campi personalizzati
    def get_question_name(self, obj):
        return obj.answer.question.name
    get_question_name.short_description = "Nome Domanda"

    def question_text_display(self, obj):
        text = obj.question_text
        return (text[:100] + '...') if len(text) > 100 else text
    question_text_display.short_description = "Testo Domanda"

    def answer_text_display(self, obj):
        text = obj.answer_text
        return (text[:75] + '...') if len(text) > 75 else text
    answer_text_display.short_description = "Testo Risposta Data"

    def formatted_score(self, obj):
        score_value = obj.answer_score_value
        score_display = obj.answer_score_display
        
        color = "green"
        if score_value == Answer.AnswerScore.ERROR:
            color = "orange"
        elif score_value == Answer.AnswerScore.SERIOUS_ERROR:
            color = "red"
        
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, score_display)
    
    formatted_score.short_description = "Punteggio Risposta"
    
    def answer_correction_display(self, obj):
        text = obj.answer_correction
        if not text:
            return "-"
        return (text[:75] + '...') if len(text) > 75 else text
    answer_correction_display.short_description = "Correzione"


    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
    

@admin.register(TestExecution)
class TestExecutionAdmin(admin.ModelAdmin):
    
    list_display = (
        'revision_code',
        'age',
        'sex',
        'ip',
        'execution_time',
        'score',
        'duration',
        'revision_date',
        'note',
    )
    
    search_fields = ('revision_code', 'ip')
    
    list_filter = ('execution_time', 'revision_date')
    
    readonly_fields = ('revision_code', 'execution_time')
    
    fieldsets = (
        ('Informazioni Utente', {
            'fields': ('age', 'sex', 'ip'),
            'classes': ('collapse',),
        }),
        ('Informazioni Esecuzione', {
            'fields': ('execution_time', 'score', 'duration'),
            'classes': ('collapse',),
        }),
        ('Revisione', {
            'fields': ('revision_code', 'revision_date', 'note'),
            'classes': ('collapse',),
        })
    )
    
    inlines = [GivenAnswerInline]

    def get_queryset(self, request):
        # Ottimizza le query per caricare i dati correlati
        return super().get_queryset(request).prefetch_related(
            'given_answers_through__answer__question', 
            'test'
        )