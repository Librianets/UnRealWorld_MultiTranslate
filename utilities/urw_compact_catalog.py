"""Lossless source DAG, recursive message units and translation-memory import.

Source choices/conditions are retained, never inferred by a text regex. English
operations describe the source only. Target plural/case operations are explicit
language policies, not the English functions applied to translated strings.
"""
from collections import Counter,defaultdict
import copy,hashlib,json,re,string

OPS={'literal','parameter','ref','slot','choice','concat','sequence','token_sequence','format','transform','bounded_list','unknown'}
class _Placeholders:
    """Tokenize escaped brace pairs before looking for an argument.

    ``{{{sound}}}`` means a variable inside literal braces. Lookarounds cannot
    distinguish it from the escaped literal ``{{sound}}``; the runtime's
    left-to-right tokenizer can, and the Python tools must follow that grammar.
    """
    raw=re.compile(r'\{([A-Za-z_][A-Za-z_0-9]*)(?::([^{}]+))?\}')
    def finditer(self,text):
        at=0
        while at<len(text):
            if text.startswith(('{{','}}'),at):at+=2;continue
            match=self.raw.match(text,at)if text[at]=='{'else None
            if match:yield match;at=match.end()
            else:at+=1
    def findall(self,text):return [(m[1],m[2]or'')for m in self.finditer(text)]
    def search(self,text):return next(self.finditer(text),None)
    def sub(self,replacement,text):
        parts=[];at=0
        for match in self.finditer(text):
            parts.extend([text[at:match.start()],replacement(match)if callable(replacement)else match.expand(replacement)]);at=match.end()
        parts.append(text[at:]);return ''.join(parts)
PLACEHOLDER=_Placeholders()
PRINTF=re.compile(r'%%|%[-+ #0]*\d*(?:\.\d+)?[hlL]*[sduifgc]')
def canonical(value):return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def ident(prefix,value):return prefix+hashlib.sha256(canonical(value).encode()).hexdigest()[:20]
def normalized(text):return re.sub(r'[ \t\r\n]+',' ',text).strip(' \t\r\n')
def parameterized(text):
    names={}
    def replace(m):
        name=m[1]
        if name not in names:names[name]='v'+str(len(names)+1)
        return '{'+names[name]+'}'
    return PLACEHOLDER.sub(replace,text),names
def rename(text,names):
    return PLACEHOLDER.sub(lambda m:'{'+names.get(m[1],m[1])+(':'+m[2]if m[2]else'')+'}',text)
LAYOUT_TAGS={'br','hr','blue','black','red','green','yellow','white','gray','grey','cyan','magenta'}
def has_words(text):
    text=re.sub(r'<([A-Za-z]+)>',lambda m:''if m[1].lower()in LAYOUT_TAGS else m[0],text)
    # Contractions such as "I'm" are still words even though neither side of
    # the apostrophe has two letters. The standalone pronoun I is text too.
    return len(re.findall(r'[A-Za-zА-Яа-яЁё]',text))>=2 or text.strip()=='I'
def children(node):
    op=node['op']
    if op=='ref':return [node['name']]
    if op in ('slot','transform'):return [node['value']['name']]
    if op=='choice':return [o['value']['name']for o in node['options']]
    if op in ('concat','sequence','token_sequence'):return [p['name']for p in node['parts']]
    if op=='format':return [node['format']['name']]+[p['name']for p in node['args']]
    if op=='bounded_list':return [node['item']['name']]
    return []

class SourceDAG:
    def __init__(self,nodes):
        self.original=nodes;self.nodes={};self.aliases={};self.active=set()
        self.origins=defaultdict(list);self.evidence={};self.by_alias=defaultdict(list)
        for name in nodes:self.named(name)
        for name,gid in self.aliases.items():self.by_alias[gid].append(name)
    def named(self,name):
        if name in self.aliases:return self.aliases[name]
        if name in self.active:raise ValueError('Recursive source '+name)
        self.active.add(name);gid=self.intern(self.original[name],name,'');self.active.remove(name)
        self.aliases[name]=gid;return gid
    def intern(self,node,owner,path):
        if node['op']=='ref':return self.named(node['name'])
        value={k:copy.deepcopy(v)for k,v in node.items()if k not in ('evidence','proof','native_format_proof')}
        def link(n,suffix):return dict(op='ref',name=self.intern(n,owner,path+suffix))
        op=node['op']
        if op in ('slot','transform'):value['value']=link(node['value'],'/value')
        elif op=='choice':
            value['options']=[{**copy.deepcopy(o),'value':link(o['value'],'/options/'+str(i))}for i,o in enumerate(node['options'])]
        elif op in ('concat','sequence','token_sequence'):value['parts']=[link(n,'/parts/'+str(i))for i,n in enumerate(node['parts'])]
        elif op=='format':value['format']=link(node['format'],'/format');value['args']=[link(n,'/args/'+str(i))for i,n in enumerate(node['args'])]
        elif op=='bounded_list':value['item']=link(node['item'],'/item')
        gid=ident('g_',value);self.nodes.setdefault(gid,value)
        origin=dict(node=owner,path=path)
        for field in ('evidence','proof','native_format_proof'):
            if node.get(field):
                eid=ident('e_',node[field]);self.evidence[eid]=node[field];origin.setdefault('evidence',[]).append(eid)
        if origin not in self.origins[gid]:self.origins[gid].append(origin)
        return gid
    def reachable(self,roots):
        seen=set()
        def visit(gid):
            if gid in seen:return
            seen.add(gid)
            for child in children(self.nodes[gid]):visit(child)
            if self.nodes[gid].get('seed_domain'):visit(self.aliases[self.nodes[gid]['seed_domain']])
        for root in roots:visit(root)
        return seen
    def expanded(self,gid):
        node=copy.deepcopy(self.nodes[gid]);op=node['op']
        def expand(n):return self.expanded(n['name'])
        if op in ('slot','transform'):node['value']=expand(node['value'])
        elif op=='choice':
            for o in node['options']:o['value']=expand(o['value'])
        elif op in ('concat','sequence','token_sequence'):node['parts']=[expand(n)for n in node['parts']]
        elif op=='format':node['format']=expand(node['format']);node['args']=[expand(n)for n in node['args']]
        elif op=='bounded_list':node['item']=expand(node['item'])
        return node

TARGET_POLICIES={
 'lower':'locale_lower','lower_game':'locale_lower','lower_ascii_crt':'locale_lower','upper_game':'locale_upper',
 'upper_first':'locale_upper_first','upper_first_game':'locale_upper_first',
 'lower_first':'locale_lower_first','lower_first_game':'locale_lower_first',
 'plural_en':'lexeme_plural','plural_game':'lexeme_plural','singular_game':'lexeme_singular',
 'article_en':'omit_article','list_and_en':'list_and','list_or_en':'list_or',
 'stream_commas_3':'list_punctuation','stream_commas_2':'list_punctuation',
 'place_gloss_en':'place_gloss','wood_material_en':'material_agreement',
 'journal_message_en':'display_journal_cleanup','journal_message_case_preserved_en':'display_journal_cleanup_case_preserved',
 'truncate_30':'source_storage_limit_only','truncate_39':'source_storage_limit_only','legacy_menu_clip34':'source_storage_limit_only','legacy_inventory_clip40':'source_storage_limit_only','legacy_armour_caption_clip26':'source_storage_limit_only','legacy_menu_selection_en':'display_legacy_menu_selection','quote_if_unquoted_en':'source_quote_if_unquoted'}

class UnitBuilder:
    def __init__(self,dag,families):
        self.dag=dag;self.families=families;self.units={};self.bindings={};self.done=set();self.counts=Counter()
        self.family_roots={f['id']:dag.aliases[f['node']]for f in families}
        self.graph_families=defaultdict(set)
        self.generators={}
        self.prepare_generators()
        for f in families:
            if f.get('coverage_kind','').startswith('classified_'):continue
            for gid in dag.reachable([self.family_roots[f['id']]]):self.graph_families[gid].add(f['id'])
    def prepare_generators(self):
        """Recover the reviewed eight-bit smith list, checking every source mask.
        No global search-and-replace or guessed sentence similarity is involved.
        """
        if 'finish_smith_categories'not in self.dag.aliases:return
        gid=self.dag.aliases['finish_smith_categories'];n=self.dag.nodes[gid]
        assert n['op']=='choice'and n['key']=='smith_category_mask'and len(n['options'])==256
        options={int(o['id']):self.dag.nodes[o['value']['name']]['text']for o in n['options']}
        items=[options[1<<i]for i in range(8)]
        assert items==['tools','knives','axes','spears','arrowheads','swords','a helmet','a shield']
        for mask,value in options.items():
            selected=[word for i,word in enumerate(items)if mask&(1<<i)]
            expected=', '.join(selected[:-1])+' and '+selected[-1]if len(selected)>1 else''.join(selected)
            assert expected==value,(mask,value,expected)
        self.generators[gid]=dict(kind='ordered_bitset_list',input='category_mask',bits=8,
            items=[dict(bit=i,graph=next(o['value']['name']for o in n['options']if int(o['id'])==1<<i))for i in range(8)],
            source_conjunction='and',ru_conjunction='и',separator=', ',source_function='0x0053A700',all_source_masks_verified=256)
    def name_for(self,gid):
        n=self.dag.nodes[gid];op=n['op']
        if op in ('parameter','slot'):return re.sub(r'\W','_',n['name'])
        names=self.dag.by_alias.get(gid,[]);joined=' '.join(names).lower()
        for words,name in [('item weapon carcass','item'),('npc creature animal','creature'),('player_identity','player'),('place location region terrain','location'),('direction','direction'),('distance','distance'),('level','level'),('skill','skill'),('reward','reward'),('list','list')]:
            if any(w in joined for w in words.split()):return name
        return 'part'
    def pattern(self,gid):
        args={};names=Counter();parameter_names={}
        def arg(child):
            n=self.dag.nodes[child];base=self.name_for(child)
            if n['op']=='parameter'and n['name'] in parameter_names:return '{'+parameter_names[n['name']]+'}'
            names[base]+=1;name=base if names[base]==1 else base+str(names[base])
            while name in args:names[base]+=1;name=base+str(names[base])
            kind=n.get('type','grammar')
            args[name]=dict(graph=child,type=kind,domain=n.get('domain',''),source_binding=n.get('name',''))
            if n['op']=='parameter':parameter_names[n['name']]=name
            return '{'+name+'}'
        def render(child,top=False):
            n=self.dag.nodes[child];op=n['op']
            if op=='literal':return n['text'].replace('{','{{').replace('}','}}')
            if op in ('parameter','slot','choice','transform','bounded_list'):return arg(child)
            if not top and self.dag.by_alias.get(child):return arg(child)
            if op in ('concat','sequence','token_sequence'):
                parts=[render(c['name'])for c in n['parts']]
                if op=='token_sequence':
                    text=''
                    for token in [t for part in parts for t in re.findall(r'<[^>]+>|[^\s<>]+',part)]:
                        if text and not token.startswith('.'):text+=' '
                        text+=token
                    return text
                return n.get('separator',' 'if op=='sequence'else'').join(parts)
            if op=='format':
                fmt=self.dag.nodes[n['format']['name']]
                if fmt['op']!='literal':return arg(child)
                text=fmt['text'];out=[];cursor=0;index=0
                for m in PRINTF.finditer(text):
                    out.append(text[cursor:m.start()].replace('{','{{').replace('}','}}'));cursor=m.end()
                    if m[0]=='%%':out.append('%');continue
                    if index>=len(n['args']):raise ValueError('Insufficient format arguments '+child)
                    bound=n['args'][index]['name'];index+=1
                    value=self.dag.nodes[bound]
                    if value['op']=='literal':out.append(render(bound))
                    else:
                        token=arg(bound);args[token[1:-1]]['printf']=m[0];out.append(token)
                if index!=len(n['args']):raise ValueError('Unused format arguments '+child)
                out.append(text[cursor:].replace('{','{{').replace('}','}}'));return ''.join(out)
            if op=='unknown':raise ValueError('Unknown source graph '+child)
            raise ValueError('Unknown operator '+op)
        text=render(gid,True)
        return text,args
    def visit(self,gid,role='component'):
        key=(gid,role)
        if key in self.done:return
        self.done.add(key);n=self.dag.nodes[gid];op=n['op']
        if gid in self.generators:
            for item in self.generators[gid]['items']:self.visit(item['graph'],'component')
            return
        if op=='choice':
            for child in children(n):self.visit(child,role)
            return
        if op=='slot':self.visit(n['value']['name'],'component');return
        if op=='parameter':
            # Resource identifiers are validated by a closed source domain, but
            # never become editable vocabulary (nor inherit a prose translation).
            if n.get('seed_domain') and not n.get('preserve') and n.get('translation_policy') not in ('preserve_resource_key','preserve_path'):
                self.visit(self.dag.aliases[n['seed_domain']],'component')
            return
        if op=='bounded_list':self.visit(n['item']['name'],'component');return
        if op=='transform':
            if n['name']not in TARGET_POLICIES:raise ValueError('Missing target policy '+n['name'])
            self.visit(n['value']['name'],role);return
        if op=='unknown':raise ValueError('Reachable unknown source '+gid)
        text,args=self.pattern(gid)
        # A pure forwarding variable is represented by its grammar, not a new
        # fake message requiring translation of "{part}" into itself.
        if len(args)==1 and text=='{'+next(iter(args))+'}':
            for value in args.values():self.visit(value['graph'],role)
            return
        structural=not has_words(PLACEHOLDER.sub('',text))and len(args)>=2
        if not has_words(PLACEHOLDER.sub('',text))and not structural:
            for value in args.values():self.visit(value['graph'],'component')
            return
        shape,names=parameterized(text);contracts={names[k]:{a:v for a,v in val.items()if a in ('type','printf')}for k,val in args.items()}
        uid=ident('u_',dict(source=shape,variables=contracts,role=role))
        unit=self.units.setdefault(uid,dict(id=uid,kind='assembly'if structural else'template'if args else'exact',role=role,source=shape,translation='',forms={},variables=contracts,context='',status='untranslated',apply_translation=2))
        if structural:
            unit.update(translation=shape,status='structural',apply_translation=1,method='explicit_target_component_order')
            ordered=list(args)
            if len(args)==2 and shape=='{v1} {v2}'and args[ordered[0]]['type']=='integer':
                subject=self.dag.nodes[args[ordered[1]]['graph']]
                if 'item'in subject.get('name','')or'plant'in subject.get('name',''):
                    unit['argument_forms']={'v2':dict(number='v1',operation='count_agreement')}
        binding=dict(unit=uid,arguments={names[k]:v for k,v in args.items()})
        self.bindings.setdefault(gid,{})[role]=binding
        for val in args.values():self.visit(val['graph'],'component')
    def build(self):
        for f in self.families:
            if not f.get('coverage_kind','').startswith('classified_'):self.visit(self.family_roots[f['id']],'message')
        return self.units

class TranslationMemory:
    def __init__(self,catalog):
        self.exact=defaultdict(list);self.folded=defaultdict(list);self.templates=defaultdict(list);self.lexemes=defaultdict(list)
        self.casefolded=defaultdict(list)
        self.entries={r['id']:r for r in catalog['entries']}
        for row in catalog['entries']:
            if not row.get('translation')or not row.get('enabled',False)or row['kind']=='dynamic':continue
            self.add(row)
        for row in catalog['lexicon']:
            self.lexemes[row['source']].append(row)
            self.add(dict(**row,kind='exact',enabled=True))
    def add_csv(self,path):
        """Read prior editable translations; only rows already accepted there."""
        import csv
        from build_urw_hook_catalog import printf_pair
        with path.open(encoding='utf-8-sig',newline='')as stream:
            head=stream.readline();stream.seek(0);sep=max([',',';','\t'],key=head.count)
            for i,row in enumerate(csv.DictReader(stream,delimiter=sep),2):
                if row.get('apply_translation','1')not in ('1',1):continue
                source=row.get('text',row.get('source',''));target=row.get('text_translate','')
                if not source or not target:continue
                source,target,error,args=printf_pair(source,target)
                if error:continue
                # Message-file macros become typed slots in the recovered DAG.
                # Layout tags remain literal and must still match structurally.
                def macros(text):
                    return re.sub(r'<([A-Za-z_][A-Za-z_0-9:]*)>',lambda m:m[0]if m[1].lower()in LAYOUT_TAGS else'{'+m[1].replace(':','_')+'}',text)
                source,target=macros(source),macros(target)
                self.add(dict(id=path.name+':'+str(i),source=source,translation=target,kind='template'if PLACEHOLDER.search(source)else'exact',enabled=True,priority=1))
    def add(self,row):
        if row.get('kind')=='template':
            shape,names=parameterized(row['source']);self.templates[normalized(shape)].append((row,names))
        else:
            self.exact[row['source']].append(row);self.folded[normalized(row['source'])].append(row)
            self.casefolded[normalized(row['source']).casefold()].append(row)
    def lookup(self,unit):
        text=unit['source'];possibilities=[]
        if unit['kind']in ('template','assembly'):
            shape,names=parameterized(text);reverse={v:k for k,v in names.items()}
            for row,old in self.templates.get(normalized(shape),[]):
                mapping={k:reverse[v]for k,v in old.items()}
                value=rename(row['translation'],mapping)
                if set(PLACEHOLDER.findall(value))!=set(PLACEHOLDER.findall(text)):continue
                forms={k:rename(v,mapping)for k,v in row.get('plural',{}).items()if k!='variable'}
                plurality=dict(variable=mapping[row['plural']['variable']],forms=forms)if forms else{}
                possibilities.append(dict(translation=value,forms={},plural=plurality,origin=row['id'],method='existing_structural_template',priority=row.get('priority',0),variables={mapping.get(k,k):v for k,v in row.get('variables',{}).items()}))
        else:
            candidates=self.exact.get(text)or self.folded.get(normalized(text),[])
            case_equivalent=False
            if not candidates and unit['role']=='component':
                candidates=self.casefolded.get(normalized(text).casefold(),[]);case_equivalent=bool(candidates)
            for row in candidates:
                value=row['translation']
                if case_equivalent:
                    if text.isupper():value=value.upper()
                    elif text[:1].isupper():value=value[:1].upper()+value[1:]
                    elif text[:1].islower():value=value[:1].lower()+value[1:]
                possibilities.append(dict(translation=value,forms=row.get('forms',{}),origin=row['id'],priority=row.get('priority',0),method='existing_case_equivalent'if case_equivalent else'existing_exact'if row['source']==text else'existing_whitespace_equivalent'))
        if possibilities:
            best=min(p['priority']for p in possibilities);possibilities=[p for p in possibilities if p['priority']==best]
            # Missing forms on an EXE caption do not conflict with a glossary
            # supplying the same translation's forms. Actual disagreements stay.
            translations={p['translation'].casefold()for p in possibilities}
            if len(translations)==1:
                merged={};safe=True
                for p in possibilities:
                    for key,value in p.get('forms',{}).items():
                        if key in merged and merged[key].casefold()!=value.casefold():safe=False
                        merged.setdefault(key,value)
                plurals={canonical(p['plural'])for p in possibilities if p.get('plural')}
                variables={canonical(p['variables'])for p in possibilities if p.get('variables')}
                if safe and len(plurals)<=1 and len(variables)<=1:
                    result={**possibilities[0],'forms':merged,'origins':sorted({p['origin']for p in possibilities}),'status':'imported'}
                    if plurals:result['plural']=json.loads(next(iter(plurals)))
                    if variables:result['variable_rules']=json.loads(next(iter(variables)))
                    return result
        unique=defaultdict(list)
        for p in possibilities:unique[canonical({k:p[k]for k in ('translation','forms','plural','variables')if k in p})].append(p)
        if len(unique)==1:
            group=next(iter(unique.values()));return dict(**group[0],origins=sorted({p['origin']for p in group}),status='imported')
        if unique:return dict(status='conflict',candidates=[group[0]for group in unique.values()])
        return dict(status='untranslated')

def apply_memory(units,memory):
    for unit in units.values():
        if unit['status']=='structural':continue
        result=memory.lookup(unit)
        if 'variables'in result:result['variable_rules']=result.pop('variables')
        unit['status']=result.pop('status');unit.update(result)
        unit['apply_translation']=1 if unit['status']=='imported'else 2
    return Counter(u['status']for u in units.values())

def merge_roles(units,bindings):
    """Share identical localized units without merging different contextual uses.

    Keep legacy IDs as aliases. Personal context or differing agreement/plural
    contracts prevent merging; this is not approximate sentence clustering.
    """
    groups={};result={};aliases={}
    semantic=['source','variables','translation','forms','plural','argument_forms',
              'agreement','gender','variable_rules','apply_translation','context']
    for unit in sorted(units.values(),key=lambda u:(u['role']!='message',u['id'])):
        key=canonical({k:unit[k]for k in semantic if k in unit})
        if key not in groups:
            groups[key]=unit['id'];result[unit['id']]=copy.deepcopy(unit)
            result[unit['id']]['roles']=unit.get('roles',[unit['role']])[:]
        else:
            uid=groups[key];aliases[unit['id']]=uid
            result[uid]['roles']=sorted(set(result[uid]['roles']+unit.get('roles',[unit['role']])))
            result[uid]['origins']=sorted(set(result[uid].get('origins',[])+unit.get('origins',[])))
    for roles in bindings.values():
        for binding in roles.values():binding['unit']=aliases.get(binding['unit'],binding['unit'])
    return result,aliases

def validate_units(units):
    """Validate editable data before writing; never silently discard parameters."""
    errors=[]
    for u in units.values()if isinstance(units,dict)else units:
        label=u['id'];source=set(PLACEHOLDER.findall(u['source']))
        if u['apply_translation']not in (0,1,2,3,4):errors.append([label,'invalid apply_translation'])
        target=u.get('translation','')
        if u['apply_translation']==1 and not target:errors.append([label,'empty active translation'])
        if target and set(PLACEHOLDER.findall(target))!=source:errors.append([label,'placeholder mismatch',u['source'],target])
        for value in u.get('forms',{}).values():
            if not isinstance(value,str)or not set(PLACEHOLDER.findall(value))<=source:errors.append([label,'invalid lexical form'])
        for value in u.get('plural',{}).get('forms',{}).values():
            if set(PLACEHOLDER.findall(value))!=source:errors.append([label,'plural placeholder mismatch'])
        if u.get('plural')and u['plural'].get('variable')not in u.get('variables',{}):errors.append([label,'unknown plural variable'])
        if not set(u.get('argument_forms',{}))<=set(u.get('variables',{})):errors.append([label,'unknown agreement argument'])
        for rule in u.get('argument_forms',{}).values():
            for key in ['number','agree_with']:
                if key in rule and rule[key]not in u.get('variables',{}):errors.append([label,'unknown agreement dependency'])
        if not isinstance(u.get('agreement',{}),dict)or not all(isinstance(v,str)for v in u.get('agreement',{}).values()):errors.append([label,'invalid gender agreement'])
        genders=u.get('gender_by_form',{})
        if not isinstance(genders,dict)or not all(isinstance(v,str)and v in ('m','f','n','plural')for v in genders.values()):errors.append([label,'invalid per-form gender'])
        if u.get('head')and u['head']not in u.get('variables',{}):errors.append([label,'unknown head argument'])
        for field in ['literal_values','argument_translations']:
            values=u.get(field,{})
            if not isinstance(values,dict)or not set(values)<=set(u.get('variables',{})):
                errors.append([label,'invalid argument dictionary',field]);continue
            for value in values.values():
                valid=isinstance(value,str)if field=='literal_values'else isinstance(value,dict)and all(isinstance(k,str)and isinstance(v,str)for k,v in value.items())
                if not valid:errors.append([label,'invalid argument dictionary value',field])
    return errors
