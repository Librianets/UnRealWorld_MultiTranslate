UnReal World 3.89.1 — Translation 0.25 — Russian / Finnish

INSTALLATION
1. Close the game. Download one archive: Standard or Lite.
2. Extract its contents into the folder containing urw.exe, replacing older translation files.
3. Open URW_Launcher.exe and choose the game language.
Standard and Lite provide the same translation. Standard also includes the offline HTML/CSV editor. Console and logging are disabled by default; enable logging in the launcher when collecting a bug report.

UPDATES AND EDITIONS
Open URW_Launcher.exe and click "Check for updates". The updater checks the project's latest public release on GitHub; no account is required. An Internet connection and Windows PowerShell 5.1 are required. PowerShell 5.1 is included with Windows 10/11.
The edition currently installed is selected by default: Standard updates to Standard, Lite updates to Lite. To change editions, select the other edition before checking. You can switch editions even when the version number is unchanged, once that release is available on GitHub.
The updater asks you to confirm installation, downloads the chosen ZIP, checks its SHA-256 checksum and file manifest, then closes and reopens the launcher. The game must be closed. Unknown or incompatible packages are refused. It does not downgrade a newer installed build to an older public release.
Existing URWTrace.ini settings are retained. Translation files are replaced by the release versions. Your previous files, including custom translations and editor files removed during a switch to Lite, are saved in URW_update_backup. This folder holds one backup of the files from before the update; copy important edits elsewhere before the next update overwrites that backup. Unrelated files and saved games are left alone.
If copying fails, the updater attempts to restore the previous files. An interrupted update leaves a recovery record; the next update check attempts recovery before downloading anything. Keep URW_update_backup and URW_update_pending.json until recovery completes. If recovery fails, keep the backup and report the error rather than repeatedly overwriting files.

STEAM LAUNCH
In the launcher's "Launch from Steam" section, choose a language, click "Change game language", then "Enable". The original game is preserved as urw-original.exe; a copy of URWTrace.exe takes the name urw.exe. The original executable's bytes are unchanged. Direct EN/RU/FI launch buttons are disabled while this mode is active. "Restore original" returns to the usual launch method.
Automatic updates refresh the installed Steam loader too. After a manual ZIP update, the launcher detects an outdated loader and offers "Update Steam loader". Click it before playing through Steam. If Steam itself replaces the game EXE, use a translation release compatible with that game version; "Repair after update" restores the Steam integration. An unsupported game version is refused.
Do not copy urw-original.exe or URWSteam.state from another installation or delete them manually.

TRANSLATION EDITING
In Standard, open the desired language's catalog.html, load catalog.json from the same folder, edit and save the JSON back there. Preserve IDs, English source text, variables and control markers. Most message edits reload automatically; encyclopedia index changes may require a restart. For CSV editing, use the import tools in the source repository. Native Finnish proofreading is welcome.
If a message remains in English or a translation seems incorrect, please report it in the project discussion or email librianets@gmail.com. Native Finnish proofreading is welcome.

РУССКИЙ

УСТАНОВКА
1. Закройте игру. Скачайте один архив: обычный или Lite.
2. Распакуйте содержимое в папку с urw.exe с заменой старых файлов перевода.
3. Откройте URW_Launcher.exe и выберите язык игры.
В обоих вариантах одинаковый перевод. Обычный комплект также содержит редактор HTML/CSV. Консоль и журналы по умолчанию выключены; для сбора отчёта включите журнал в лаунчере.

ОБНОВЛЕНИЯ И СМЕНА РЕДАКЦИИ
Откройте URW_Launcher.exe и нажмите «Проверить обновления». Проверяется последний опубликованный релиз нашего проекта на GitHub, учётная запись не нужна. Требуются подключение к Интернету и Windows PowerShell 5.1. PowerShell 5.1 входит в Windows 10/11.
По умолчанию выбрана установленная редакция: обычная обновляется на обычную, Lite — на Lite. Для перехода выберите другую редакцию перед проверкой. Перейти можно и в пределах одной версии, когда этот релиз уже доступен на GitHub.
Установщик предложит подтвердить обновление, загрузит выбранный ZIP, проверит контрольную сумму SHA-256 и перечень файлов, затем закроет и снова откроет лаунчер. Игра должна быть закрыта. Неподходящий или повреждённый пакет не устанавливается. Если установленная сборка новее опубликованной, откат к старому релизу не выполняется.
Настройки существующего URWTrace.ini сохраняются. Файлы переводов заменяются версиями из релиза. Предыдущие файлы, включая вашу редактуру и файлы редактора, удаляемые при переходе на Lite, сохраняются в URW_update_backup. В этой папке хранится одна резервная копия файлов до обновления; следующее обновление заменит её. Заранее скопируйте важные правки в другое место. Посторонние файлы и сохранения игры не затрагиваются.
При ошибке копирования установщик пытается вернуть прежние файлы. После прерывания обновления остаётся запись для восстановления; при следующей проверке обновлений сначала выполняется попытка отката. До его завершения не удаляйте URW_update_backup и URW_update_pending.json. Если восстановление не удалось, сохраните резервную копию и сообщите об ошибке.

ЗАПУСК ЧЕРЕЗ STEAM
В блоке «Запуск из Steam» выберите язык, нажмите «Сменить язык игры», затем «Включить». Оригинал сохраняется как urw-original.exe, а имя urw.exe получает копия URWTrace.exe. Байты оригинального EXE не меняются. Прямые кнопки EN/RU/FI в этом режиме отключены. «Вернуть оригинальный запуск» отключает этот режим.
Автоматическое обновление заменяет и установленную копию загрузчика Steam. После ручной распаковки ZIP лаунчер обнаружит старую копию и предложит «Обновить загрузчик Steam». Нажмите эту кнопку перед запуском игры из Steam. Если сам Steam заменил игровой EXE, потребуется совместимый перевод; кнопка «Восстановить после обновления» возвращает интеграцию. Неподдерживаемая версия игры не принимается.
Не переносите urw-original.exe и URWSteam.state из чужой установки и не удаляйте их вручную.

РЕДАКТИРОВАНИЕ ПЕРЕВОДА
В обычной редакции откройте catalog.html нужного языка, загрузите catalog.json из той же папки, внесите правки и сохраните JSON туда же. Не изменяйте ID, английский исходник, параметры и управляющие метки. Большинство текстовых правок подхватывается без перезапуска, но изменение индекса энциклопедии может потребовать перезапуска. Инструменты импорта CSV доступны в репозитории исходников.
Если сообщение осталось английским или перевод кажется неправильным, сообщите об этом в обсуждении проекта или на librianets@gmail.com. Особенно нужна помощь носителей финского языка.

SUOMI
Sulje peli ja pura yksi ZIP urw.exe-tiedoston viereen. Käynnistä URW_Launcher.exe.
Tavallinen ja Lite sisältävät saman käännöksen. Tavallisessa paketissa on myös HTML/CSV-editori.
Paina «Tarkista päivitykset». Oletuksena säilytetään nykyinen paketti. Voit vaihtaa tavallisen ja Lite-paketin välillä myös saman julkaisuversion sisällä. Päivitys käyttää GitHub Releases -palvelua; tiliä ei tarvita. Tarvitaan Internet ja Windows PowerShell 5.1.
Asetukset säilyvät. Korvattavat tiedostot tallennetaan kansioon URW_update_backup, jossa säilytetään vain yksi varmuuskopio päivitystä edeltävistä tiedostoista. Tallenna tärkeät omat muutokset erikseen ennen seuraavaa päivitystä.
Automaattinen päivitys päivittää myös Steam-käynnistimen. Käsin tehdyn ZIP-päivityksen jälkeen paina tarvittaessa «Päivitä Steam-käynnistin». Pelin on oltava suljettu. Pelin alkuperäisen EXE-tiedoston sisältöä ei muuteta.
Jos päivitys keskeytyy, seuraava tarkistus yrittää palauttaa vanhat tiedostot. Älä poista varmuuskopiota tai palautustietuetta ennen palautuksen valmistumista.
