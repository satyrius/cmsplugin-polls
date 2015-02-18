from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST

from .models import Poll


@require_POST
def vote(request):
    poll_id = request.POST.get('poll')
    Poll.object.get(poll_id)

    next_page = request.POST.get('next')
    if not next_page:
        next_page = request.META.get('HTTP_REFERER')

    return HttpResponseRedirect(next_page)
