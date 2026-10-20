"""Small offline Doxygen-style catalogue. No external libraries or network."""
import json,re

def build_editor(catalog,grammar,provenance):
    locations={};evidence_locations={}
    def collect(value,out):
        if isinstance(value,list):
            for v in value:collect(v,out)
        elif isinstance(value,dict):
            if value.get('resource'):out.add(str(value['resource'])+(':'+str(value['line'])if value.get('line')else''))
            for key in ['string_va','source_va']:
                if isinstance(value.get(key),(str,int))and value.get(key):out.add('urw.exe · '+str(value[key]))
            for key in ['function','function_va','source_function','caller']:
                if isinstance(value.get(key),str)and re.fullmatch(r'0x[0-9a-fA-F]+',value[key]):out.add('func '+value[key])
            if isinstance(value.get('call_va'),str):out.add('CALL '+value['call_va'])
            for v in value.values():
                if isinstance(v,(dict,list)):collect(v,out)
    for gid,roles in grammar['unit_bindings'].items():
        found=set()
        for origin in provenance['origins'].get(gid,[]):
            for eid in origin.get('evidence',[]):
                if eid not in evidence_locations:
                    evidence_locations[eid]=set();collect(provenance['evidence'].get(eid,{}),evidence_locations[eid])
                found.update(evidence_locations[eid])
        for binding in roles.values():locations.setdefault(binding['unit'],set()).update(found)
    data=json.dumps(dict(catalog=catalog,grammar=grammar,unit_families=provenance['unit_families'],locations={u:sorted(v,key=lambda s:(not(s.startswith('urw.exe')or'.txt'in s.lower()or'.nfo'in s.lower()),s))for u,v in locations.items()}),ensure_ascii=False,sort_keys=True,separators=(',',':')).replace('<','\\u003c')
    template=HTML
    if catalog.get('language')=='fi':
        from urw_compact_editor_fi import localize_template
        template=localize_template(template,version=catalog.get('version','0.05'),runtime_integration=catalog.get('runtime_integration',False))
    html=template.replace('/*CATALOG_DATA*/',data)
    if catalog.get('language')=='fi':
        return html
    if catalog.get('runtime_integration'):
        html=html.replace('каталог сообщений 0.05','каталог сообщений '+catalog['version']).replace('Исследование 0.05 · исходная грамматика сохранена · подключение к игре ещё не выполнено','Runtime hook '+catalog['version']+' · каталог подключён · сохранённый catalog.json подхватывается игрой автоматически')
    return html

HTML=r'''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width">
<title>UnReal World — каталог сообщений 0.05</title>
<style>
:root{font:15px system-ui,sans-serif;color:#263548;background:#fff}*{box-sizing:border-box}body{margin:0}header{padding:18px 24px;background:linear-gradient(#fbfdff,#dce7f3);border-bottom:1px solid #99aac0}h1{font-size:23px;margin:0 0 8px}h2{font-size:18px}small,.muted{color:#536a81}.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;padding:10px 24px;background:#edf2f8;border-bottom:1px solid #bbc9d9}button,input,select,textarea{font:inherit}button{cursor:pointer;background:#f2f6fb;border:1px solid #96adc4;border-radius:4px;padding:6px 10px}button.active{background:#345e87;color:white}input[type=search]{min-width:260px;padding:7px}#content{max-width:1250px;margin:18px auto;padding:0 20px}.card{border:1px solid #becddd;border-radius:4px;margin:14px 0;padding:14px}.meta{float:right;font-size:12px;max-width:48%;overflow-wrap:anywhere}.source{white-space:pre-wrap;overflow-wrap:anywhere;margin:10px 0;line-height:1.45}.target{width:100%;min-height:65px;padding:8px;color:#1d3954;border:1px solid #a0b3c6}.field{margin-top:8px}label{display:block}.forms{width:100%;min-height:75px;font-family:monospace}.context{width:100%;min-height:45px}.inline{display:flex;gap:12px;align-items:center}.inline label{display:inline}details{margin-top:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f5f7fa;padding:8px}a{color:#235982}.nav{display:flex;gap:15px;align-items:center}#notice{min-height:24px;padding:6px 24px;color:#7a4300}#file{display:none}#footer{padding:16px 24px;border-top:1px solid #ccc}.bad{color:#a12620}.good{color:#1e6831}#examples{white-space:pre-wrap}
</style>
<header><h1>UnReal World · сообщения и перевод</h1><small>Исследование 0.05 · исходная грамматика сохранена · подключение к игре ещё не выполнено</small></header>
<div class="bar"><button id="open">Открыть catalog.json</button><button id="save">Сохранить catalog.json</button><button id="csv">Выгрузить CSV</button><input id="file" type="file" accept=".json"><span id="dirty">Нет несохранённых правок</span></div>
<nav class="bar" id="tabs"><button data-tab="all" class="active">Все</button><button data-tab="messages">Сообщения</button><button data-tab="templates">Шаблоны</button><button data-tab="components">Словари и компоненты</button><button data-tab="assembly">Сборка</button><button data-tab="review">Проверка и отключённые</button><button data-tab="families">Семейства и маршруты</button></nav>
<div class="bar"><input id="search" type="search" placeholder="Поиск EN, RU, ID, функция"><span id="count"></span><span class="nav"><button id="prev">Назад</button><span id="page"></span><button id="next">Далее</button></span></div>
<div id="notice" role="status"></div><main id="content"></main>
<footer id="footer">Текст EN, условия выбора и связи с кодом доступны только для чтения. «Контекст» заполняет пользователь. Формы и согласование задаются явно; английские функции изменения слов к русскому тексту не применяются. Правки JSON/CSV нужно сохранить в соответствующий файл каталога. Игра и хук этим документом не изменяются.</footer>
<script id="data" type="application/json">/*CATALOG_DATA*/</script><script>
'use strict';
const embedded=JSON.parse(document.getElementById('data').textContent),grammar=embedded.grammar;
let catalog=embedded.catalog, tab='all',page=0,dirty=false,handle=null;const draftErrors=new Set();
const $=s=>document.querySelector(s), units=()=>new Map(catalog.units.map(u=>[u.id,u]));
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const families=new Map(grammar.families.map(f=>[f.id,f]));
const holders=s=>{const found=[];let at=0;while(at<s.length){if(s.startsWith('{{',at)||s.startsWith('}}',at)){at+=2;continue;}const m=s[at]==='{'?s.slice(at).match(/^\{([a-zA-Z_][a-zA-Z_0-9]*)(?::([^{}]+))?\}/):null;if(m){found.push(m[1]+':'+(m[2]||''));at+=m[0].length;}else ++at;}return Array.from(new Set(found)).sort().join('|')};
function notice(s){$('#notice').textContent=s}
function changed(u){u.user_edited=true;u.status='user_edit';dirty=true;$('#dirty').textContent='Есть несохранённые правки'}
function related(u){return (embedded.unit_families[u.id]||[]).map(id=>families.get(id)).filter(Boolean)}
function info(u){return (embedded.locations[u.id]||[]).join('\n')+'\n'+related(u).map(f=>[f.title,f.root_va,(f.covered_call_sites||[]).join(', ')].filter(Boolean).join(' · ')).join('\n')}
function select(){const q=$('#search').value.toLocaleLowerCase();return catalog.units.filter(u=>{
 const roles=u.roles||[u.role];
 if(tab==='messages'&&!roles.includes('message'))return false;
 if(tab==='templates'&&u.kind!=='template')return false;
 if(tab==='components'&&!roles.includes('component'))return false;
 if(tab==='assembly'&&u.kind!=='assembly')return false;
 if(tab==='review'&&u.apply_translation===1)return false;
 return !q||[u.id,u.source,u.translation,info(u)].join('\n').toLocaleLowerCase().includes(q)
})}
function sourceChain(gid,depth=0,seen=new Set()){
 if(depth>4||seen.has(gid))return esc(gid)+' …';seen=new Set(seen);seen.add(gid);
 const n=grammar.nodes[gid];if(!n)return esc(gid);
 const bs=grammar.unit_bindings[gid];if(bs){const b=bs.component||bs.message;return '<a href="#'+esc(b.unit)+'" data-unit="'+esc(b.unit)+'">'+esc(units().get(b.unit)?.source||b.unit)+'</a>'}
 if(n.op==='literal')return esc(n.text);
 if(n.op==='parameter')return esc(n.name+' ['+n.type+']');
 if(grammar.generators?.[gid]){const g=grammar.generators[gid];return '<details><summary>Список из редактируемых компонентов · '+n.options.length+' исходных вариантов</summary>'+g.items.map(item=>'<div>Бит '+esc(item.bit)+': '+sourceChain(item.graph,depth+1,seen)+'</div>').join('')+'<small>Связка: '+esc(g.ru_conjunction||'и')+'. Все английские варианты сохранены в grammar.json.</small></details>';}
 if(n.op==='choice')return '<details><summary>Выбор '+esc(n.key)+' · '+n.options.length+' ветвей</summary>'+n.options.slice(0,24).map(o=>'<div>'+esc(o.id)+': '+sourceChain(o.value.name,depth+1,seen)+(o.conditions?.length?' <small>'+esc(JSON.stringify(o.conditions))+'</small>':'')+'</div>').join('')+(n.options.length>24?'<small>Все ветви сохранены в grammar.json</small>':'')+'</details>';
 if(n.op==='bounded_list')return 'Список до '+esc(n.maximum)+' элементов: '+sourceChain(n.item.name,depth+1,seen);
 if(n.value)return esc(n.op+': '+(n.name||''))+' → '+sourceChain(n.value.name,depth+1,seen);
 const refs=n.parts||n.args||[];return esc(n.op)+' → '+refs.map(r=>sourceChain(r.name,depth+1,seen)).join(' + ')
}
function bindings(u){let html='';for(const [gid,roles]of Object.entries(grammar.unit_bindings))for(const [role,b]of Object.entries(roles))if(b.unit===u.id){html+='<details><summary>'+esc(role+' · '+gid)+'</summary>';for(const[name,arg]of Object.entries(b.arguments))html+='<div><b>'+esc(name)+'</b> ['+esc(arg.type)+'] '+esc(arg.source_binding||arg.domain||'')+' → '+sourceChain(arg.graph)+'</div>';html+='</details>'}return html}
function render(){
 const host=$('#content');host.replaceChildren();
 if(tab==='families'){
 const q=$('#search').value.toLocaleLowerCase(),rows=grammar.families.filter(f=>JSON.stringify(f).toLocaleLowerCase().includes(q));$('#count').textContent=rows.length+' семейств';$('#page').textContent='';
 for(const f of rows.slice(page*40,page*40+40)){const d=document.createElement('section');d.className='card';d.innerHTML='<h2>'+esc(f.title)+'</h2><pre>'+esc(JSON.stringify(f,null,2))+'</pre>'+sourceChain(grammar.aliases[f.node]);host.append(d)}return}
 const rows=select();page=Math.min(page,Math.max(0,Math.ceil(rows.length/40)-1));$('#count').textContent=rows.length+' единиц';$('#page').textContent=(page+1)+' / '+Math.max(1,Math.ceil(rows.length/40));
 for(const u of rows.slice(page*40,page*40+40)){
 const d=document.createElement('section');d.className='card';d.id=u.id;
 d.innerHTML='<div class="meta" title="'+esc(info(u))+'">'+esc(u.id)+'<br>'+esc((embedded.locations[u.id]||[]).slice(0,2).join(' · ')||related(u).map(f=>f.root_va).filter(Boolean).slice(0,3).join(' · '))+'</div><small>'+esc((u.roles||[u.role]).join(', ')+' · '+u.kind+' · '+u.status)+'</small><div class="source"></div><label>Перевод<textarea class="target"></textarea></label><div class="inline field"><label>Включение <select class="apply"><option value="0">0 — отключено</option><option value="1">1 — включено</option><option value="2">2 — проверить</option><option value="3">3 — нет применения</option><option value="4">4 — исключено</option></select></label><span class="valid"></span></div><details><summary>Формы, параметры и связи с исходником</summary><label>Формы слова (JSON)<textarea class="forms lexical"></textarea></label><label>Согласование аргументов (JSON)<textarea class="forms arguments"></textarea></label><label>Числовые варианты шаблона (JSON)<textarea class="forms plural"></textarea></label><label>Родовые формы (JSON)<textarea class="forms agreement"></textarea></label><label>Род по числовым формам (JSON)<textarea class="forms genderforms"></textarea></label><label>Подстановки аргументов (JSON)<textarea class="forms argtranslations"></textarea></label><label>Буквальные значения (JSON)<textarea class="forms literalvalues"></textarea></label><label>Правила конкретных связей (JSON)<textarea class="forms bindingrules"></textarea></label><pre class="contract"></pre><div class="bindings"></div><pre class="origin"></pre></details><label class="field">Контекст<textarea class="context" placeholder=""></textarea></label>';
 d.querySelector('.source').textContent=u.source;const target=d.querySelector('.target');target.value=u.translation;const validation=()=>{const ok=holders(u.source)===holders(target.value);const el=d.querySelector('.valid');el.textContent=ok?'Параметры сохранены':'Проверьте параметры {v1}, {v2}';el.className='valid '+(ok?'good':'bad');return ok};validation();target.addEventListener('input',()=>{if(validation()){draftErrors.delete(u.id);u.translation=target.value;changed(u)}else {draftErrors.add(u.id);notice('Изменение с потерей параметров не принято. Исправьте поле до сохранения.')}});
 const apply=d.querySelector('.apply');apply.value=u.apply_translation;apply.onchange=()=>{u.apply_translation=Number(apply.value);changed(u)};
 const ctx=d.querySelector('.context');ctx.value=u.context||'';ctx.oninput=()=>{u.context=ctx.value;changed(u)};
 for(const[cls,key]of [['.lexical','forms'],['.arguments','argument_forms'],['.plural','plural'],['.agreement','agreement'],['.genderforms','gender_by_form'],['.argtranslations','argument_translations'],['.literalvalues','literal_values'],['.bindingrules','binding_rules']]){const e=d.querySelector(cls);e.value=JSON.stringify(u[key]||{},null,2);e.onchange=()=>{try{const value=JSON.parse(e.value);if(!value||Array.isArray(value)||typeof value!=='object')throw Error('Нужен объект');u[key]=value;draftErrors.delete(u.id+key);changed(u);notice('')}catch(error){draftErrors.add(u.id+key);notice('JSON не принят: '+error.message)}}}
 d.querySelector('.contract').textContent=JSON.stringify({variables:u.variables,plural:u.plural,agreement:u.agreement},null,2);d.querySelector('.origin').textContent=info(u);let loaded=false;d.querySelector('details').ontoggle=e=>{if(e.target.open&&!loaded){d.querySelector('.bindings').innerHTML=bindings(u);loaded=true}};host.append(d)
 }}
document.addEventListener('click',e=>{const link=e.target.closest('[data-unit]');if(link){e.preventDefault();const u=units().get(link.dataset.unit);tab='all';$('#search').value=u.id;page=0;render()}});
$('#tabs').onclick=e=>{const b=e.target.closest('[data-tab]');if(!b)return;tab=b.dataset.tab;page=0;document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('active',x===b));render()};$('#search').oninput=()=>{page=0;render()};$('#prev').onclick=()=>{page=Math.max(0,page-1);render()};$('#next').onclick=()=>{page++;render()};
function download(name,text,type='application/json'){const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([text],{type}));a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000)}
function accept(next){if(next.schema!==2||!Array.isArray(next.units))throw Error('Неверный формат');const originals=new Map(embedded.catalog.units.map(u=>[u.id,u]));if(next.units.length!==originals.size)throw Error('Другой состав каталога');const seen=new Set();for(const u of next.units){if(seen.has(u.id)||originals.get(u.id)?.source!==u.source)throw Error('Исходник/ID отличается');seen.add(u.id);if(u.translation&&holders(u.source)!==holders(u.translation))throw Error('Параметры отличаются: '+u.id)}catalog=next;page=0;render();notice('Каталог открыт')}
$('#open').onclick=()=>$('#file').click();$('#file').onchange=async e=>{try{accept(JSON.parse(await e.target.files[0].text()))}catch(error){notice(error.message)}};
$('#save').onclick=async()=>{try{if(draftErrors.size)throw Error('Исправьте неверные параметры или JSON перед сохранением');const text=JSON.stringify(catalog,null,2)+'\n';if(window.showSaveFilePicker){handle=await window.showSaveFilePicker({suggestedName:'catalog.json',types:[{description:'Каталог JSON',accept:{'application/json':['.json']}}]});const w=await handle.createWritable();await w.write(text);await w.close()}else download('catalog.json',text);dirty=false;$('#dirty').textContent='Файл сохранён / подготовлен к скачиванию';notice('Сохраните файл в папке каталога. В подключённой сборке игра подхватит JSON автоматически. Для CSV сначала выполните его импорт.')}catch(error){notice(error.message)}};
$('#csv').onclick=()=>{if(draftErrors.size){notice('Исправьте неверные поля перед выгрузкой');return}const fields=['id','role','kind','source','translation','forms','variables','plural','argument_forms','binding_rules','agreement','gender','gender_by_form','head','literal_values','argument_translations','apply_translation','status','context'];const cell=v=>'"'+String(typeof v==='object'?JSON.stringify(v):v??'').replace(/"/g,'""')+'"';download('translations.csv','\ufeff'+fields.join(';')+'\r\n'+catalog.units.map(u=>fields.map(k=>cell(u[k])).join(';')).join('\r\n'),'text/csv;charset=utf-8')};
window.addEventListener('beforeunload',e=>{if(dirty){e.preventDefault();e.returnValue=''}});render();
</script></html>'''
