from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext as _

from .models import PollPlugin as Plugin


class PollPlugin(CMSPluginBase):
    model = Plugin
    name = _('Poll Plugin')
    render_template = 'cms/plugins/poll_form.html'

    def render(self, context, instance, placeholder):
        context['poll'] = instance.poll
        return context

plugin_pool.register_plugin(PollPlugin)
