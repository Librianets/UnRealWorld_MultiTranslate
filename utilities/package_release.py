"""Package ordinary/Lite translation ZIPs from a standalone translation repo.

Run without arguments; settings are inside this file. No Git/network actions.
Deploy this script as UnRealWorld_MultiTranslate/utilities/package_release.py.
"""
from pathlib import Path
import hashlib,json,shutil,zipfile

REPOSITORY=Path(__file__).resolve().parent.parent
if not (REPOSITORY/'UnRealWorld').is_dir():
    WORKSPACE=next(p for p in Path(__file__).resolve().parents if (p/'Codex/README.md').is_file() and (p/'UnReal_World_RPG').is_dir())
    REPOSITORY=WORKSPACE/'UnReal_World_RPG/git/UnRealWorld_MultiTranslate'
VERSION='0.22'
GAME_VERSION='3.89.1'
OUTPUT=REPOSITORY/'dist'
NATIVE_RUNTIME=REPOSITORY/'runtime'
RUNTIME_FILES=['URW_Launcher.exe','URWTrace.exe','URWTraceHook.dll']
LANGUAGES=['rus_translate','fin_translate']
PLAY_FILES=['catalog.json','legacy_catalog.json','runtime_grammar.json','URW.FNT']
EDIT_FILES=['catalog.html','translations.csv','grammar.json','provenance.json.gz','generated_files.json','README.txt','FONT_NOTES.txt']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def runtime_file(name):
    local=NATIVE_RUNTIME/name
    if local.is_file():return local
    sibling='UnRealWorld_Launcher'if name=='URW_Launcher.exe'else'UnRealWorld_HookTranslate'
    path=REPOSITORY.parent/sibling/name
    if not path.is_file():raise FileNotFoundError('Build/copy the matching runtime first: '+str(local))
    return path
def main():
    source=REPOSITORY/'UnRealWorld'
    binaries={name:runtime_file(name)for name in RUNTIME_FILES}
    for name in ['URWTrace.ini','Translation_README.txt','Translation_HISTORY.txt','THIRD_PARTY_LICENSES.txt','CODE_LICENSE.txt','LICENSE_SCOPE.txt']:
        if not (source/name).is_file():raise FileNotFoundError(source/name)
    for language in LANGUAGES:
        for name in PLAY_FILES+EDIT_FILES:
            if not (source/language/name).is_file():raise FileNotFoundError(source/language/name)
    for name,p in binaries.items():
        if p.read_bytes()[:2]!=b'MZ':raise ValueError('Not a Windows executable: '+name)
    for edition,suffix in [('ordinary',''),('lite','_lite')]:
        dest=OUTPUT/('Hook_'+VERSION+suffix);archive=dest.with_name(dest.name+'.zip')
        if dest.exists()or archive.exists():raise FileExistsError('Preserve existing release: '+str(dest))
    results={}
    for edition,suffix in [('ordinary',''),('lite','_lite')]:
        dest=OUTPUT/('Hook_'+VERSION+suffix);game=dest/'UnRealWorld';game.mkdir(parents=True)
        for name,p in binaries.items():shutil.copy2(p,game/name)
        for name in ['URWTrace.ini','Translation_README.txt','Translation_HISTORY.txt','THIRD_PARTY_LICENSES.txt','CODE_LICENSE.txt','LICENSE_SCOPE.txt']:shutil.copy2(source/name,game/name)
        ini=(game/'URWTrace.ini').read_text(encoding='utf-8-sig')
        if 'ConsoleMode=0'not in ini or'LoggingEnabled=0'not in ini or'GameExe=urw.exe'not in ini:raise ValueError('Public INI must use urw.exe and console/logging0/0')
        names=PLAY_FILES+(EDIT_FILES if edition=='ordinary'else[])
        for language in LANGUAGES:
            folder=game/language;folder.mkdir()
            for name in names:shutil.copy2(source/language/name,folder/name)
        if edition=='ordinary':
            util=dest/'utilities';util.mkdir()
            for p in (REPOSITORY/'utilities').iterdir():
                if p.is_file()and(p.suffix in ['.py','.cmd']or p.name=='PORTABLE_LANGUAGE.txt'):shutil.copy2(p,util/p.name)
            (util/'README.txt').write_text('CSV imports use sibling UnRealWorld language folders.\nSource projects: UnRealWorld_Launcher and UnRealWorld_HookTranslate.\nThe release packager runs from the source repository, not this distribution folder.\n',encoding='utf-8')
            # A release folder is not the complete Git repository used by packager.
            for name in ['package_release.py','package_release.cmd']:(util/name).unlink(missing_ok=True)
        files={p.relative_to(game).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p))for p in game.rglob('*')if p.is_file()}
        archive=dest.with_name(dest.name+'.zip')
        with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9)as z:
            for name in sorted(files):z.write(game/name,arcname=name)
        with zipfile.ZipFile(archive)as z:
            if len(z.namelist())!=len(files)or set(z.namelist())!=set(files):raise ValueError('ZIP layout mismatch')
            for name,v in files.items():
                if hashlib.sha256(z.read(name)).hexdigest()!=v['sha256']:raise ValueError('ZIP SHA mismatch: '+name)
        result=dict(version=VERSION,game=GAME_VERSION,edition=edition,files=files,archive=archive.name,archive_sha256=sha(archive),zip_root='contents of UnRealWorld',binaries={n:sha(p)for n,p in binaries.items()})
        (dest/'MANIFEST.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');results[edition]=result
        print('Verified',archive.name,round(archive.stat().st_size/1048576,2),'MiB',flush=True)
    (OUTPUT/'RELEASES.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
