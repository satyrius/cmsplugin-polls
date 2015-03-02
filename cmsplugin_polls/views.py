from django import http
from django.views.decorators.http import require_POST

from .models import Poll


@require_POST
def vote(request):
    referer = request.META.get('HTTP_REFERER')
    next_page = request.POST.get('next', referer)

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

    if not poll.can_vote(request):
        if next_page:
            return http.HttpResponseRedirect(next_page)
        else:
            return http.HttpResponseForbidden('You had voted')

    choice = request.POST.get('choice')
    if choice:
        if not poll.vote(choice, request):
            return http.HttpResponseBadRequest('Invalid choice')

    if next_page:
        return http.HttpResponseRedirect(next_page)
    elif not choice:
        return http.HttpResponseBadRequest('There is no choice')
    else:
        return http.HttpResponse('OK')
