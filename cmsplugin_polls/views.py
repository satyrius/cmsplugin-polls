from django import http
from django.db.models import F
from django.views.decorators.http import require_POST

from .models import Poll


@require_POST
def vote(request):
    referer = request.META.get('HTTP_REFERER')

    poll_id = request.POST.get('poll')
    try:
        error = None
        poll = Poll.objects.get(id=poll_id)
    except Poll.DoesNotExist:
        error = 'Poll does not exist'
    except ValueError:
        error = 'Invalid data'
    if error:
        return http.HttpResponseBadRequest(error)

    choice = request.POST.get('choice')
    if choice:
        try:
            choice = int(choice)
        except ValueError:
            rows = 0
        else:
            rows = poll.choice_set.filter(id=choice).update(votes=F('votes') + 1)
        if not rows:
            return http.HttpResponseBadRequest('Invalid choice')

    next_page = request.POST.get('next', referer)
    if next_page:
        return http.HttpResponseRedirect(next_page)
    else:
        return http.HttpResponse('OK')
