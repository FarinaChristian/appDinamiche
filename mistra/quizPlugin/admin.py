from django.contrib import admin
from .models import *
from django.utils.html import format_html

admin.site.register(GivenAnswer)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ('text', 'score', 'correction')


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


@admin.register(Sex)
class SexAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'text_preview')
    list_filter = ('category',)
    search_fields = ('name', 'text', 'category__name')
    
    inlines = [AnswerInline]

    def text_preview(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    text_preview.short_description = 'Anteprima Testo'
    
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description_preview', 'min_score')
    search_fields = ('name', 'description')
    
    filter_horizontal = ('questions',)

    def description_preview(self, obj):
        return (obj.description[:75] + '...') if len(obj.description) > 75 else obj.description
    description_preview.short_description = 'Anteprima Descrizione'    

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'question_name', 'score', 'correction_preview')
    list_filter = ('score', 'question__category')
    search_fields = ('text', 'question__name', 'correction')
    list_select_related = ('question', 'question__category')

    def text_preview(self, obj):
        return (obj.text[:75] + '...') if len(obj.text) > 75 else obj.text
    text_preview.short_description = 'Anteprima Risposta'

    def correction_preview(self, obj):
        return (obj.correction[:75] + '...') if len(obj.correction) > 75 else obj.correction
    correction_preview.short_description = 'Anteprima Correzione'

    def question_name(self, obj):
        return obj.question.name
    question_name.short_description = 'Domanda'
    question_name.admin_order_field = 'question__name'

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