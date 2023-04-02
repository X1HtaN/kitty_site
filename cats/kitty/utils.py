from kitty.models import *
from django.core.cache import cache
from .templatetags.kitty_tags import *
from django.db.models import Count
from .models import *

class DataMixin():
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cache_cats')
        if not cats:
            cats = Category.objects.all()
            cache.set('cache_cats', cats, 60)
        context['cats'] = cats

        if not self.request.user.is_authenticated:
            try:
                main_menu.remove({'title': 'Добавить статью', 'url_name': 'add_page'})
            except:
                pass
        else:
            if main_menu.count({'title': 'Добавить статью', 'url_name': 'add_page'}) == 0:
                main_menu.append({'title': 'Добавить статью', 'url_name': 'add_page'})

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context