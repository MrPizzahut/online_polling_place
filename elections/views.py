from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Candidate, Poll, Choice
import datetime
from django.db.models import Sum

# Create your views here.
def index(request):
    candidates = Candidate.objects.all()
    context = {'candidates': candidates}
    return render(request, 'elections/index.html', context)

def areas(request, area):
    today = datetime.datetime.now()
    try:
        poll = Poll.objects.get(area=area, start_date__lte=today, end_date__gte=today)  # get에 인자로 조건을 전달해줍니다.
        candidates = Candidate.objects.filter(area=area)  # Candidate의 area와 매개변수 area가 같은 객체만 불러오기
    except:
        poll = None
        candidates = None
    context = {'candidates': candidates, 'area': area, 'poll': poll}
    print(context)
    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id=poll.id, candidate_id=selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id=poll.id, candidate_id=selection, votes=1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area=area)
    polls= Poll.objects.filter(area=area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice.objects.filter(poll_id=poll.id).aggregate(Sum('votes'))
        result['total_votes'] = total_votes['votes__sum']
        rates = []
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll_id=poll.id, candidate_id=candidate.id)
                rates.append(round(choice.votes*100/result['total_votes'], 1))
            except:
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates': candidates, 'area': area, 'poll_results': poll_results}
    return render(request, 'elections/result.html', context)

def candidates(request, name):
    try:
        candidate = Candidate.objects.get(name=name)
    except:
        return HttpResponseNotFound("page does not exist  ")
    return HttpResponse(candidate.name)