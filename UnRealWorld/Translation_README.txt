UnReal World 3.89.1 — Hook 0.22 — RU / FI / EN
Выпуск0.22. Готовые архивы доступны в GitHub Releases.

УСТАНОВКА
Закройте игру. Распакуйте один ZIP рядом с оригинальным urw.exe.
Не копируйте из чужой установки urw-original.exe и URWSteam.state.
До включения режима Steam работают обычные кнопки запуска ENG/RUS/FIN.

ЗАПУСК ЧЕРЕЗ STEAM
1. Откройте URW_Launcher.exe.
2. В блоке «Запуск из Steam» выберите Русский, Suomi или English и
   нажмите «Сменить язык игры».
3. Нажмите «Включить». Теперь запускайте игру кнопкой «Играть» в Steam.
Оригинал сохраняется как urw-original.exe, а на место urw.exe копируется
загрузчик. Отдельная копия загрузчика URWTrace.exe остаётся рядом.
Содержимое оригинального EXE не меняется. Папки переводов прежние.

В режиме Steam все три кнопки прямого запуска блокируются, включая ENG.
Чтобы сменить язык: закройте игру, выберите язык в блоке Steam и нажмите
«Сменить язык игры». Следующий запуск из Steam использует этот язык.
English запускает оригинал без подключения библиотеки перевода.
Чтобы вернуть обычные кнопки запуска: «Вернуть оригинальный запуск».

ПОСЛЕ ОБНОВЛЕНИЯ / ПРОВЕРКИ ФАЙЛОВ STEAM
Steam может восстановить оригинальный urw.exe. Закройте игру, установите
совместимую версию перевода, откройте наш лаунчер и нажмите
«Восстановить после обновления». Новый оригинал сохраняется, загрузчик
снова копируется на urw.exe. Старый отличный оригинал сохраняется отдельно
с SHA256 в имени; новый EXE не заменяется старой резервной копией.
Неизвестная версия игры блокирует восстановление до адаптации перевода.
Кнопка «Вернуть оригинальный запуск» оставляет обновлённый EXE Steam на
месте, даже если перевод пока не поддерживает эту версию.
URWSteam.state — запись установки; не удаляйте её вручную.
URWSteam.lock — временная блокировка на время запуска/настройки, удаляется
автоматически. Постоянные журналы по умолчанию выключены.

ПРОВЕРКИ И ОГРАНИЧЕНИЯ
Проверены установка, повторное восстановление, отказ на неизвестном EXE,
откат, блокировка на время игры и реальные EN/RU/FI запуски переименованного
оригинала. Запуск кнопкой Steam, оверлей, учёт времени и Steam Cloud требуют
проверки пользователем. Сам клиент Steam в автоматическом тесте не запускался.
Это обновление загрузчика/лаунчера. Переводы и URWTraceHook.dll сохранены
из0.21; внутренний диагностический номер DLL остаётся0.21.
Пакет0.22 рассчитан только на3.89.1. Накопленные пропуски текста пока без правок.

Обычный набор содержит редактор catalog.html и translations.csv.
Lite даёт тот же перевод без редактора. ConsoleMode=0 / LoggingEnabled=0.
Для отчётов включите журнал через лаунчер; результаты находятся в logs.

ENGLISH
Close the game and extract one ZIP beside urw.exe. In URW_Launcher.exe,
select English launcher captions if needed. Under "Launch from Steam",
select a game language and click "Change game language", then "Enable".
Use Steam's Play button. All three direct launch buttons are disabled in
Steam mode. English runs without the translation DLL. Change the language
with the game closed, or click "Restore original" to disable Steam mode.
After Steam replaces urw.exe, install a compatible translation package and
click "Repair after update". Unsupported game versions are refused.
The current original is preserved as urw-original.exe; URWTrace.exe is the
master loader. Rollback never overwrites a newer Steam EXE with an older one.
Release0.22 is available in GitHub Releases. Actual Steam integration
(overlay, playtime, Cloud) still needs a user test.

SUOMI
Sulje peli ja pura ZIP urw.exe-tiedoston viereen. Valitse käynnistimen kieleksi
Suomi. Valitse kohdassa "Käynnistys Steamista" pelin kieli, paina "Vaihda pelin
kieli" ja sitten "Ota käyttöön". Käynnistä peli Steamin Pelaa-painikkeella.
Suoran käynnistyksen painikkeet ovat silloin pois käytöstä. Vaihda kieli pelin
ollessa suljettuna. "Palauta alkuperäinen" poistaa Steam-käynnistyksen käytöstä.
Steamin päivityksen jälkeen asenna yhteensopiva käännöspaketti ja paina
"Korjaa päivityksen jälkeen". Tuntematonta peliversiota ei korvata.
Versio0.22 on saatavilla GitHub Releases -sivulla.
