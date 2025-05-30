from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Question, Answer, TestExecution, GivenAnswer, Sex
from django.utils import timezone
from datetime import timedelta


def home(request):
    tests = Test.objects.all()
    return render(request, 'home.html', {'tests': tests})


def start_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)

    question_list = list(test.questions.all())
    total_questions = len(question_list)

    # inizializza l'esecuzione se non c'è già
    if 'execution_id' not in request.session:
        sex = Sex.objects.first()  # per semplicità
        execution = TestExecution.objects.create(
            age=25,
            ip=request.META.get('REMOTE_ADDR'),
            test=test,
            sex=sex,
            duration=timedelta(0)
        )
        request.session['execution_id'] = execution.id
        request.session['question_index'] = 0
        request.session['start_time'] = timezone.now().isoformat()
    else:
        execution = get_object_or_404(TestExecution, id=request.session['execution_id'])

    index = request.session.get('question_index', 0)

    # tutte le domande sono state risposte
    if index >= total_questions:
        # calcola punteggio
        score = sum([ga.answer.score for ga in execution.given_answers_through.all()])
        execution.score = score

        execution.duration = timezone.now() - timezone.datetime.fromisoformat(request.session['start_time'])

        execution.save()

        # reset sessione
        for k in ['execution_id', 'question_index', 'start_time']:
            request.session.pop(k, None)

        return render(request, 'test_completed.html', {'execution': execution})

    current_question = question_list[index]
    context = {
        'question': current_question,
        'answers': current_question.answers.all(),
        'progress': f"{index + 1} / {total_questions}"
    }

    return render(request, 'question.html', context)


def submit_answer(request, test_id):
    if request.method == 'POST':
        execution = get_object_or_404(TestExecution, id=request.session.get('execution_id'))
        answer_id = request.POST.get('answer')
        answer = get_object_or_404(Answer, id=answer_id)
        GivenAnswer.objects.create(test_execution=execution, answer=answer)

        request.session['question_index'] += 1
        return redirect('quiz-question', test_id=test_id)
