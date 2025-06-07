from django.shortcuts import render, redirect, get_object_or_404
from .models import Test, Question, Answer, TestExecution, GivenAnswer, Sex
from django.utils import timezone
from datetime import timedelta


def home(request):
    tests = Test.objects.all()
    sex = Sex.objects.all()

    context = {
        'tests': tests,
        'sex': sex,
    }

    return render(request, 'home.html', context)


def start_test(request, test_id):
    # Recupera il test e le domande associate
    test = get_object_or_404(Test, id=test_id)

    question_list = list(test.questions.all())
    total_questions = len(question_list)

    if 'execution_id' not in request.session:
        # Se non esiste un'esecuzione del test nella sessione, creane una nuova
        age = request.POST.get('age')
        sex = request.POST.get('sex')

        execution = TestExecution.objects.create(
            age=age,
            sex=Sex.objects.get(name=sex),
            ip=request.META.get('REMOTE_ADDR'),
            test=test,
            duration=timedelta(0)
        )

        request.session['execution_id'] = execution.id
        request.session['question_index'] = 0
        request.session['start_time'] = timezone.now().isoformat()
    else:
        # Se esiste già un'esecuzione, recuperala
        execution = get_object_or_404(TestExecution, id=request.session['execution_id'])

    index = request.session.get('question_index', 0)

    previous_answer = None
    if index < total_questions:
        current_question = question_list[index]
        previous_answer = execution.given_answers_through.filter(answer__question=current_question).last()

    if index >= total_questions:
        score = sum([ga.answer.score for ga in execution.given_answers_through.all()])
        execution.score = score
        execution.duration = timezone.now() - timezone.datetime.fromisoformat(request.session['start_time'])
        execution.save()

        given_answers = execution.given_answers_through.select_related('answer__question')

        for k in ['execution_id', 'question_index', 'start_time']:
            request.session.pop(k, None)

        return redirect('quiz-completed', revision_code=execution.revision_code)

    answered_question_ids = set(execution.given_answers_through.values_list('answer__question_id', flat=True))

    current_question = question_list[index]
    context = {
        'question': current_question,
        'answers': current_question.answers.all(),
        'progress': f"{index + 1} / {total_questions}",
        'execution': execution,
        'selected_answer_id': previous_answer.answer.id if previous_answer else None,
        'answered_question_ids': answered_question_ids,
        'question_list': question_list,
        'current_index': index,
    }

    return render(request, 'question.html', context)


def test_completed_view(request, revision_code):
    execution = get_object_or_404(TestExecution, revision_code=revision_code)
    given_answers = execution.given_answers_through.select_related('answer__question')

    context = {
        'execution': execution,
        'given_answers': given_answers,
    }

    return render(request, 'test_completed.html', context)


def submit_answer(request, test_id):
    if request.method == 'POST':
        execution = get_object_or_404(TestExecution, id=request.session.get('execution_id'))
        action = request.POST.get('action')

        jump_to = request.POST.get('jump_to')

        if jump_to and jump_to.isdigit():
            request.session['question_index'] = int(jump_to)
        elif action == 'back':
            if request.session['question_index'] > 0:
                request.session['question_index'] -= 1
        else:  # avanti
            answer_id = request.POST.get('answer')
            if answer_id:
                answer = get_object_or_404(Answer, id=answer_id)
                # Sovrascrivi risposta precedente, se esiste
                GivenAnswer.objects.update_or_create(
                    test_execution=execution,
                    answer__question=answer.question,
                    defaults={'answer': answer}
                )
                request.session['question_index'] += 1

        return redirect('quiz-question', test_id=test_id)