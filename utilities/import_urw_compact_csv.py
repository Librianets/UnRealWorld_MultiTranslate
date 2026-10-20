"""Import edited translations.csv into its catalog.json. No arguments.
Only editable fields are accepted; IDs, source and source contracts stay fixed.
"""
from pathlib import Path
import csv,gzip,hashlib,json,os
from urw_compact_catalog import validate_units,canonical
from urw_compact_editor import build_editor

ROOT=Path(__file__).resolve().parents[2]
FOLDER=ROOT/'UnReal_World_RPG/work2/3.88/compact_catalog'
if Path(__file__).with_name('PORTABLE_COMPACT.txt').exists():FOLDER=Path(__file__).resolve().parent.parent/'catalog'
if Path(__file__).with_name('PORTABLE_RUNTIME.txt').exists():FOLDER=Path(__file__).resolve().parent.parent/'UnRealWorld/rus_translate'
EDITABLE=['translation','forms','plural','argument_forms','agreement','gender','apply_translation','context']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def main(folder=None,validator=None):
    folder=Path(folder or FOLDER);path=folder/'catalog.json';table=folder/'translations.csv'
    catalog=read(path);by_id={u['id']:u for u in catalog['units']};seen=set();changed=0
    with table.open(encoding='utf-8-sig',newline='')as f:
        reader=csv.DictReader(f,delimiter=';')
        if not set(['id','source']+EDITABLE)<=set(reader.fieldnames or[]):raise ValueError('CSV fields missing')
        for row in reader:
            uid=row['id']
            if uid not in by_id or uid in seen:raise ValueError('Unknown or repeated ID '+uid)
            seen.add(uid);u=by_id[uid]
            if row['source']!=u['source']:raise ValueError('Source changed: '+uid)
            if row.get('variables')and canonical(json.loads(row['variables']))!=canonical(u['variables']):raise ValueError('Source contract changed: '+uid)
            values={k:row[k]for k in EDITABLE}
            values['apply_translation']=int(values['apply_translation'])
            for k in ['forms','plural','argument_forms','agreement']:
                values[k]=json.loads(values[k])if values[k]else{}
                if not isinstance(values[k],dict):raise ValueError('Expected JSON object: '+uid+' '+k)
            for field in ['gender_by_form','literal_values','argument_translations']:
                if field in row:
                    values[field]=json.loads(row[field])if row[field]else{}
                    if not isinstance(values[field],dict):raise ValueError('Expected JSON object: '+field)
            if 'head'in row:values['head']=row['head']
            if 'binding_rules'in row:
                values['binding_rules']=json.loads(row['binding_rules'])if row['binding_rules']else{}
                if not isinstance(values['binding_rules'],dict):raise ValueError('Expected binding rules object')
            object_fields={'forms','plural','argument_forms','agreement','binding_rules','gender_by_form','literal_values','argument_translations'}
            def existing(field):
                value=u.get(field)
                return ({}if field in object_fields else'')if value is None else value
            if any(canonical(existing(k))!=canonical(v)for k,v in values.items()):
                u.update(values);u.update(user_edited=True,status='user_edit');changed+=1
    if seen!=set(by_id):raise ValueError('Incomplete CSV: missing '+str(len(set(by_id)-seen))+' rows')
    errors=validate_units(catalog['units'])
    if errors:raise ValueError(json.dumps(errors[:10],ensure_ascii=False))
    if validator:validator(catalog)
    # No output is written until the complete edited table has passed validation.
    temp=path.with_suffix('.json.tmp');temp.write_text(json.dumps(catalog,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8',newline='\n');os.replace(temp,path)
    stamp=read(folder/'generated_files.json')if(folder/'generated_files.json').exists()else{}
    stamp['translations.csv']=hashlib.sha256(table.read_bytes()).hexdigest()
    (folder/'generated_files.json').write_text(canonical(stamp)+'\n',encoding='utf-8',newline='\n')
    grammar=read(folder/'grammar.json');provenance=json.loads(gzip.decompress((folder/'provenance.json.gz').read_bytes()))
    (folder/'catalog.html').write_text(build_editor(catalog,grammar,provenance),encoding='utf-8',newline='\n')
    print('Imported edited rows:',changed)
    return changed
if __name__=='__main__':main()
