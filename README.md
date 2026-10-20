# UnReal World Multilingual Translation

Russian and Finnish translation data and offline editing tools for
UnReal World 3.89 / Hook0.20. This is the player-facing release repository.
Download ordinary or Lite ZIPs from [GitHub Releases](https://github.com/Librianets/UnRealWorld_MultiTranslate/releases/latest) and extract their contents
beside your original `urw.exe`, then run `URW_Launcher.exe`.

Both editions use the same translation and runtime. Ordinary includes the
offline HTML/CSV editor; Lite keeps only files required to play. Native Finnish
proofreading is welcome. Known untranslated messages are being collected;
0.21 has not been released.

## Repositories

* **[UnRealWorld_Launcher](https://github.com/Librianets/UnRealWorld_Launcher)** contains the Windows GUI source.
* **[UnRealWorld_HookTranslate](https://github.com/Librianets/UnRealWorld_HookTranslate)** contains the bootstrap and presentation DLL.
* **[UnRealWorld_MultiTranslate](https://github.com/Librianets/UnRealWorld_MultiTranslate)** contains language files, editors and packaging.

Use version 0.20 components together for3.89. The source folders here do not
contain an original game executable. Built runtime files and release ZIPs
are intentionally outside Git history.

## Edit translations

Open `UnRealWorld/rus_translate/catalog.html` or
`UnRealWorld/fin_translate/catalog.html` in a browser, then load the current
`catalog.json` from the same folder. Change target text/forms and save the
JSON back to that folder. Keep IDs, source text, parameters and controls intact.
The game normally reloads message edits; encyclopedia index changes may need
a restart. Some older fallback entries are separate in `legacy_catalog.json`.

For CSV edits run `utilities/import_russian.cmd` or `import_finnish.cmd` with
Python3.11+. These commands validate and import only the selected language's
CSV; they do not alter English source contracts or the other language.

The188 hook profiles and function identifiers belong to the runtime model.
Do not edit addresses to fix a translation. See `docs/COMPATIBILITY.json`.

## Package releases

Place matching `URW_Launcher.exe`, `URWTrace.exe` and `URWTraceHook.dll` in
`runtime/`. This local folder is ignored by Git. The prepared0.20 files can
be compared with `docs/BINARY_SHA256.json`. If runtime files are absent,
the packaging script can use builds in the two sibling source repositories.

Run `utilities/package_release.cmd`. It creates ordinary and Lite directories
and ZIPs under `dist/`. ZIP roots contain only the contents of `UnRealWorld`,
never an extra parent directory or utilities. Licenses accompany both editions.
The packager refuses to overwrite an existing release directory or ZIP.

Upload the resulting ZIPs as GitHub Release assets; do not commit ZIPs or
EXE/DLL files to Git. The default settings disable console and logging.
For feedback enable LoggingEnabled1 in the launcher before playing, then send
the relevant session folder under `logs`. Lite supports logging too.

## Content and licensing

Each language has 16301 catalogue entries, 15801 enabled, including 313
encyclopedia articles. These counts do not prove coverage of every game state.
Both languages pass 570 new item checks; the baseline suite also passed 568 RU,
3711 FI,64 GUI and 18 real menu/font/close checks before publication.
Gameplay and native-speaker review continue.

`LICENSE_SCOPE.txt` separates project code from game text, translations,
fonts and third-party components. Preserve font notes and third-party notices.
Google Drive is no longer used. GitHub Releases is the primary distribution
channel; Yandex Disk is the backup.
See [Russian instructions](README_RU.md).
