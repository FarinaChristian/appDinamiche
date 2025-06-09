from django.apps import AppConfig


class QuizpluginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quizPlugin'

    def ready(self):
        import quizPlugin.cms_app  # forza l'import
