import os
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required

from ydcommon.settings import IGNORE_QUNIT_HTML_FILES


class QunitTestsView(TemplateView):
    template_name = 'js-tests/index.html'

    def get_context_data(self, **kwargs):
        context = super(QunitTestsView, self).get_context_data(**kwargs)
        if kwargs['path'] == 'index':
            for template_dir in settings.TEMPLATE_DIRS:
                path = os.path.join(template_dir, 'js-tests')
                files = [f.replace('.html', '') for f in os.listdir(path)
                         if os.path.isfile(os.path.join(path, f))]
                for ignore_file in IGNORE_QUNIT_HTML_FILES:
                    if ignore_file in files:
                        files.remove(ignore_file)
            context['files'] = files
        return context

    def get(self, request, *args, **kwargs):
        if not kwargs['path']:
            kwargs['path'] = 'index'
        self.template_name = 'js-tests/%s.html' % kwargs['path']
        return super(QunitTestsView, self).get(request, *args, **kwargs)

qunit_view = staff_member_required(QunitTestsView.as_view())
