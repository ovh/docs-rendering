from jinja2 import contextfilter

DEFAULT_LOCALE = 'en'

@contextfilter
def doorbell(ctx, entity):
    locale = entity.locale if hasattr(entity, 'locale') and entity.locale else DEFAULT_LOCALE
    available_langs = ctx.get('DOORBELL_API')
    result = available_langs.get(locale)
    return {} if not result else result
