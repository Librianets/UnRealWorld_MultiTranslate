# UnReal World Multilingual Translation

Russian and Finnish translation data and offline editing tools for
UnReal World 3.89.1 / Hook0.28. This is the player-facing release repository.
Download ordinary or Lite ZIPs from [GitHub Releases](https://github.com/Librianets/UnRealWorld_MultiTranslate/releases/latest) and extract their contents
beside your original `urw.exe`, then run `URW_Launcher.exe`.

Both editions use the same translation and runtime. Ordinary includes the
offline HTML/CSV editor; Lite keeps only files required to play. Native Finnish
proofreading is welcome. Known untranslated messages are being collected;
Hook 0.28 improves quest-journal translation and long entries.

## 0.28 — quest conversations and herbal information

Fixes the chosen dialogue line repeated after selecting an answer, and NPC replies embedded in generated quest conversations. Includes 0.27 improvements to herbal-information cards and effect lists. Russian and Finnish are supported. Use matching 0.28 package components together.

## 0.26 — quest journal

Improves F2 journal translation in Russian and Finnish: herb quantities, animal names, older quest givers, player-name substitutions and compound location descriptions. Longer entries are supported; unknown paragraphs remain in English while known paragraphs can still translate. Use the matching 0.26 DLL and catalogues together.

## Repositories

* **[UnRealWorld_Launcher](https://github.com/Librianets/UnRealWorld_Launcher)** contains the Windows GUI source.
* **[UnRealWorld_HookTranslate](https://github.com/Librianets/UnRealWorld_HookTranslate)** contains the bootstrap and presentation DLL.
* **[UnRealWorld_MultiTranslate](https://github.com/Librianets/UnRealWorld_MultiTranslate)** contains language files, editors and packaging.

Use version 0.28 package components together for3.89.1. The source folders here do not
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
`runtime/`. This local folder is ignored by Git. The prepared0.28 files can
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

The Russian catalogue has16695 entries; Finnish has16694, including313 encyclopedia articles per language. These counts do not prove coverage of every game state.
Both languages pass 570 new item checks; the baseline suite also passed 568 RU,
3711 FI,64 GUI and 18 real menu/font/close checks before publication.
Gameplay and native-speaker review continue.

`LICENSE_SCOPE.txt` separates project code from game text, translations,
fonts and third-party components. Preserve font notes and third-party notices.
Google Drive is no longer used. GitHub Releases is the primary distribution
channel; Yandex Disk is the backup.
See [Russian instructions](README_RU.md).

## Steam launch mode (0.24)

In the launcher, choose the game language under **Launch from Steam**, click
**Change game language**, then **Enable**. Use Steam's Play button afterwards.
The clean game is saved as `urw-original.exe`; a copy of `URWTrace.exe` takes
its place as `urw.exe`. The master `URWTrace.exe` stays beside it.
All three direct launch buttons are disabled while this mode is installed.
Change the game language separately with the game closed, or use **Restore
original**. English runs without loading the translation DLL.

**Repair after update** uses Steam's new original, checks compatibility, then
reinstalls the loader. Unknown game versions are refused. Rollback never
replaces a newer Steam EXE with an older backup. Differing old originals are
preserved under SHA256-based filenames. Do not delete `URWSteam.state` manually.

##0.24 / 26 October2026

Linen, hemp and nettle yarn now belong to the shared item grammar, including
length suffixes and item descriptions. The new entries are editable in each
language catalogue. Game identifiers and crafting logic remain unchanged.
Includes0.23 presentation-only parsing of L inspection and F2 journal blocks.
L was confirmed by a player. Actual F2 quest gameplay needs more feedback.
Unknown spans remain English. No new native hook addresses were added.

## 0.25: updates and editions

The GUI checks the latest stable GitHub release when you click **Check for updates**.
Standard stays Standard and Lite stays Lite by default. Choose the other edition
to switch, including within the same published version. Confirm installation.
Windows PowerShell 5.1 is required (included in Windows 10/11).

`URWUpdater.ps1` verifies SHA-256 and the per-file manifest, preserves INI settings,
backs up replaced files to `URW_update_backup`, and refreshes an installed Steam
loader. Translation edits are replaced by the release files; the backup retains
only the previous update. Keep important edits separately before updating again.
An error triggers rollback; a pending transaction is recovered on the next check.
Only known editor files are removed when switching to Lite. Saves and unrelated
files are untouched. The game must be closed. Unsupported game versions are refused.

For a manual ZIP update, the GUI distinguishes an outdated installed loader from
a missing/mismatched master and offers **Update Steam loader** where appropriate.
The native bootstrap/DLL and translation catalogues remain at 0.24; only the GUI,
updater and player documentation changed in package 0.25.

## Translation coverage

The prepared primary catalogue has all enabled text entries filled: 15,850 enabled entries for Russian and 15,849 for Finnish, including message templates and components. Catalogue completion is 100%; overall coverage of all reachable in-game messages has not been measured. English text can still occur. See [the 0.25 coverage snapshot](docs/COVERAGE_025.txt).
