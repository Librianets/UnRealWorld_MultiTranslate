# Многоязычный перевод UnReal World

Каталоги RU/FI и офлайн-редактор для3.89.1 / Hook0.24. Это основной репозиторий
для игроков: готовые обычный/Lite-архивы выкладываются в GitHub Releases.
Резерв — Яндекс Диск. Google Drive больше не используем.

Исходники GUI — UnRealWorld_Launcher; загрузчик/DLL — UnRealWorld_HookTranslate.
Во всех трёх проектах используйте совместимую0.24 для чистой английской3.89.1.
Работающие бинарники положены в локальную runtime, которая исключена из Git.
Папку игры и оригинальный urw.exe добавлять не нужно.

Для правки откройте `UnRealWorld/rus_translate/catalog.html` или
`UnRealWorld/fin_translate/catalog.html` и загрузите актуальный catalog.json.
Сохраняйте JSON обратно в папку соответствующего языка. Исходники, ID,
параметры и управляющие символы не менять. Резерв legacy_catalog.json
содержит отдельные старые записи; основной CSV его не заменяет.

После CSV запускайте `utilities/import_russian.cmd` / `import_finnish.cmd`.
Нужен Python3.11+ без дополнительных пакетов. Исходные тексты/контракты
защищены от случайной замены. Личный Context оставляем владельцу проекта.

`utilities/package_release.cmd` собирает обычный и Lite в dist. В ZIP только
содержимое UnRealWorld, без внешней папки и utilities. Настройки публичного
INI0/0. MinHook/HDE-уведомление добавляется в оба архива. Существующие dist
скрипт не перезаписывает. Для следующего выпуска измените VERSION в
utilities/package_release.py после подготовки и проверки новых компонентов.

Выпуск0.24 исправляет названия пряжи с длиной и включает исправления L/F2 из0.23.
Русский:16345 карточек,15845 включены; финский:16344/15844; по313 статей энциклопедии;
это не доказательство100% игровых состояний. Носители финского нужны для вычитки.
Статус лицензий — LICENSE_SCOPE.txt; шрифты и игровые тексты не переходят
автоматически под лицензию нашего C++/Python-кода.

## Запуск из Steam (0.24)

В блоке «Запуск из Steam» выберите язык, нажмите «Сменить язык игры», затем
«Включить». Запускайте кнопкой Steam. Оригинал — urw-original.exe, на месте
urw.exe — копия загрузчика; отдельный URWTrace.exe остаётся рядом. Все три
прямые кнопки запуска блокируются. Язык меняется отдельно при закрытой игре;
English запускается без DLL. Отключение режима: «Вернуть оригинальный запуск».

«Восстановить после обновления» сохраняет новый EXE Steam и снова ставит
загрузчик. Неизвестная версия отклоняется. Откат не заменяет новый EXE старым.
Отличающаяся старая копия сохраняется с SHA в имени. URWSteam.state вручную
не удаляйте. Проверяется блокировка файлов/запущенная игра.

##0.24 / 26 October2026

Linen, hemp and nettle yarn now belong to the shared item grammar, including
length suffixes and item descriptions. The new entries are editable in each
language catalogue. Game identifiers and crafting logic remain unchanged.
Includes0.23 presentation-only parsing of L inspection and F2 journal blocks.
L was confirmed by a player. Actual F2 quest gameplay needs more feedback.
Unknown spans remain English. No new native hook addresses were added.
