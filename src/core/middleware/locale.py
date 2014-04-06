from django.conf import settings

_active_languages = tuple(lang[0] for lang in settings.LANGUAGES)


def add_common_template_variables(request):
    return {
        'ACTIVE_LANGUAGE': request.LANGUAGE_CODE,
        'OTHER_LANGUAGES': tuple(filter(lambda x: x != request.LANGUAGE_CODE, _active_languages)),
    }

