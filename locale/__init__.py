import importlib
_locales = ['en','us'] # locales here get loaded
locales = {i:importlib.import_module('.'+i,'locale').locale for i in _locales}
def get_locale(locale, string):
    try:
        strings = locales[locale]
        path = string.split('.')
        for i in path:
            strings = strings[i]
        return strings
    except:
        strings = locales['en']
        path = string.split('.')
        for i in path:
            strings = strings[i]
        return strings