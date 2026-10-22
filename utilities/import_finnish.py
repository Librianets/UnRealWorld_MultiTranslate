"""Import one language's compact CSV. No arguments; set LANGUAGE below."""
from pathlib import Path
import re
from import_urw_compact_csv import main as import_table

LANGUAGE='fi'  # fi or ru; editing labels in the launcher is independent.
ROOT=next((p for p in Path(__file__).resolve().parents if (p/'Codex/README.md').is_file() and (p/'UnReal_World_RPG').is_dir()),Path(__file__).resolve().parents[2])
FOLDER=ROOT/'UnReal_World_RPG/work2/hook/3.89.1/fin_translate'
if Path(__file__).with_name('PORTABLE_LANGUAGE.txt').exists():
    FOLDER=Path(__file__).resolve().parent.parent/'UnRealWorld'/('fin_translate'if LANGUAGE=='fi'else'rus_translate')
elif LANGUAGE=='ru':FOLDER=FOLDER.with_name('rus_translate')

def validate(catalog):
    if catalog.get('language')!=LANGUAGE:raise ValueError('Wrong language catalogue')
    codepage='cp1252'if LANGUAGE=='fi'else'cp1251'
    for u in catalog['units']:
        if u['apply_translation']!=1:continue
        for value in [u['translation'],*u.get('forms',{}).values(),*u.get('agreement',{}).values()]:
            value.encode(codepage,errors='strict')
            if LANGUAGE=='fi'and re.search('[А-Яа-яЁё]',value):raise ValueError('Russian target in Finnish: '+u['id'])

if __name__=='__main__':import_table(FOLDER,validate)
