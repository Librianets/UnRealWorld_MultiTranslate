"""English interface for the Finnish catalogue; embedded source data is never touched."""

# Applied only to the static HTML/JavaScript template, before catalogue JSON is embedded.
UI_TEXT = {
    'каталог сообщений 0.05': 'message catalogue 0.05',
    'сообщения и перевод': 'messages and translation',
    'Исследование 0.05 · исходная грамматика сохранена · подключение к игре ещё не выполнено':
        'Study 0.05 · source grammar preserved · not connected to the game yet',
    'Открыть catalog.json': 'Open catalog.json',
    'Сохранить catalog.json': 'Save catalog.json',
    'Выгрузить CSV': 'Export CSV',
    'Нет несохранённых правок': 'No unsaved changes',
    'Есть несохранённые правки': 'Unsaved changes',
    'Словари и компоненты': 'Dictionaries and components',
    'Проверка и отключённые': 'Review and disabled',
    'Семейства и маршруты': 'Families and routes',
    'Все': 'All',
    'Сообщения': 'Messages',
    'Шаблоны': 'Templates',
    'Сборка': 'Assembly',
    'Поиск EN, RU, ID, функция': 'Search EN, FI, ID, function',
    'Назад': 'Previous',
    'Далее': 'Next',
    'Текст EN, условия выбора и связи с кодом доступны только для чтения. «Контекст» заполняет пользователь. Формы и согласование задаются явно; английские функции изменения слов к русскому тексту не применяются. Правки JSON/CSV нужно сохранить в соответствующий файл каталога. Игра и хук этим документом не изменяются.':
        'English source text, selection conditions and code references are read-only. Context is supplied by the user. Word forms and agreement are explicit; English inflection functions are not applied to Finnish text. Save JSON/CSV changes to the corresponding catalogue file. This document does not change the game or hook.',
    'Список из редактируемых компонентов · ': 'List of editable components · ',
    ' исходных вариантов': ' source variants',
    'Бит ': 'Bit ',
    'Связка: ': 'Conjunction: ',
    "g.ru_conjunction||'и'": "g.ru_conjunction||'ja'",
    '. Все английские варианты сохранены в grammar.json.': '. All English variants are preserved in grammar.json.',
    'Выбор ': 'Choice ',
    ' ветвей': ' branches',
    'Все ветви сохранены в grammar.json': 'All branches are preserved in grammar.json',
    'Список до ': 'List of up to ',
    ' элементов: ': ' items: ',
    ' семейств': ' families',
    ' единиц': ' entries',
    'Перевод': 'Translation',
    'Включение ': 'Enabled ',
    '0 — отключено': '0 — disabled',
    '1 — включено': '1 — enabled',
    '2 — проверить': '2 — review',
    '3 — нет применения': '3 — no applicable use',
    '4 — исключено': '4 — excluded',
    'Формы, параметры и связи с исходником': 'Forms, parameters and source references',
    'Формы слова (JSON)': 'Word forms (JSON)',
    'Согласование аргументов (JSON)': 'Argument forms and agreement (JSON)',
    'Числовые варианты шаблона (JSON)': 'Counted template variants (JSON)',
    'Родовые формы (JSON)': 'Agreement forms (JSON)',
    'Род по числовым формам (JSON)': 'Grammatical class by number (JSON)',
    'Подстановки аргументов (JSON)': 'Argument translations (JSON)',
    'Буквальные значения (JSON)': 'Literal values (JSON)',
    'Правила конкретных связей (JSON)': 'Rules for specific bindings (JSON)',
    'Контекст': 'Context',
    'Параметры сохранены': 'Placeholders preserved',
    'Проверьте параметры {v1}, {v2}': 'Check placeholders {v1}, {v2}',
    'Изменение с потерей параметров не принято. Исправьте поле до сохранения.':
        'A change that removes placeholders was not accepted. Correct the field before saving.',
    'Нужен объект': 'Expected a JSON object',
    'JSON не принят: ': 'JSON rejected: ',
    'Неверный формат': 'Invalid format',
    'Другой состав каталога': 'Catalogue entries do not match',
    'Исходник/ID отличается': 'Source text or ID differs',
    'Параметры отличаются: ': 'Placeholders differ: ',
    'Каталог открыт': 'Catalogue opened',
    'Исправьте неверные параметры или JSON перед сохранением': 'Correct invalid placeholders or JSON before saving',
    'Каталог JSON': 'JSON catalogue',
    'Файл сохранён / подготовлен к скачиванию': 'File saved / ready to download',
    'Сохраните файл в папке каталога. В подключённой сборке игра подхватит JSON автоматически. Для CSV сначала выполните его импорт.':
        'Save the file in the catalogue folder. The connected game reloads JSON automatically. Import CSV changes first.',
    'Исправьте неверные поля перед выгрузкой': 'Correct invalid fields before exporting',
}


def localize_template(template, *, version='0.05', runtime_integration=False):
    """Return the Finnish catalogue UI in English, without processing embedded data."""
    template = template.replace('<html lang="ru">', '<html lang="en">')
    for source in sorted(UI_TEXT, key=len, reverse=True):
        template = template.replace(source, UI_TEXT[source])
    if runtime_integration:
        template = template.replace('message catalogue 0.05', 'message catalogue ' + str(version))
        template = template.replace(
            'Study 0.05 · source grammar preserved · not connected to the game yet',
            'Runtime hook ' + str(version) + ' · catalogue connected · saved catalog.json is reloaded automatically by the game',
        )
    return template
