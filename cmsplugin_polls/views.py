from django.http import HttpResponseRedirect
from .models import Poll


def vote(request):
    poll_id = request.POST.get('poll')
    Poll.object.get(poll_id)

    next_page = request.POST.get('next')
    if not next_page:
        next_page = request.META.get('HTTP_REFERER')

    return HttpResponseRedirect(next_page)
