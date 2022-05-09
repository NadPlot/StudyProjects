from django import template

register = template.Library()

# set возможных нецензурных слов:
words = {'СЛОВО', 'СЛОВО1', 'СЛОВО2', 'СЛОВО3'}


@register.filter(
    name='censor')
def censor(value):
    if isinstance(value, str):
        text = set(value.split())
        for word in words:
            if word in text:
                value = str(''.join(value.split(word)))
        return value
    else:
        raise ValueError(f'Введенный текст {type(value)} не содержит слова')
