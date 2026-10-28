from collections import deque
ALFABETO=list("STFBLPVR")
PATRONES=["PPP","PPS","BBP"]
def construir_afnd():
    estados=["i"]; finales=[]; delta={"i":{"":[]}}
    for k,p in enumerate(PATRONES,1):
        qs=[f"p{k}_{j}" for j in range(4)]; estados+=qs; finales.append(qs[-1]); delta["i"][""].append(qs[0])
        for q in qs: delta[q]={}
        for a in ALFABETO: delta[qs[0]][a]=[qs[0]]; delta[qs[3]][a]=[qs[3]]
        for j,a in enumerate(p):
            delta[qs[j]].setdefault(a,[]).append(qs[j+1])
            if j: delta[qs[j]]["V"]=[qs[j]]
    return dict(states=estados,alphabet=ALFABETO,start="i",finals=finales,delta=delta)
def clausura(m,qs):
    r=set(qs); pendientes=list(qs)
    while pendientes:
        for q in m["delta"].get(pendientes.pop(),{}).get("",[]):
            if q not in r: r.add(q); pendientes.append(q)
    return r
def simular_afnd(m,w):
    qs=clausura(m,[m["start"]])
    for a in w:
        if a not in m["alphabet"]: raise ValueError("Símbolo desconocido: "+a)
        qs=clausura(m,{t for q in qs for t in m["delta"].get(q,{}).get(a,[])})
    return bool(qs & set(m["finals"]))
def eliminar_epsilon(m):
    d={}; fs=[]
    for q in m["states"]:
        c=clausura(m,[q]); d[q]={}
        if c & set(m["finals"]): fs.append(q)
        for a in m["alphabet"]:
            d[q][a]=sorted(clausura(m,{t for r in c for t in m["delta"].get(r,{}).get(a,[])}))
    return dict(m,delta=d,finals=fs)
def determinizar(m):
    s=frozenset(clausura(m,[m["start"]])); subs=[s]; ids={s:"d0"}; d={}; fs=[]
    for sub in subs:
        q=ids[sub]; d[q]={}
        if set(sub)&set(m["finals"]): fs.append(q)
        for a in m["alphabet"]:
            nxt=frozenset(clausura(m,{t for r in sub for t in m["delta"].get(r,{}).get(a,[])}))
            if nxt not in ids: ids[nxt]=f"d{len(ids)}"; subs.append(nxt)
            d[q][a]=[ids[nxt]]
    return dict(states=list(d),alphabet=m["alphabet"],start="d0",finals=fs,delta=d,subsets={ids[s]:sorted(s) for s in subs})
def minimizar(m):
    fs=set(m["finals"]); parts=[s for s in [fs,set(m["states"])-fs] if s]; history=[]
    while True:
        history.append([sorted(s) for s in parts]); idx={q:i for i,s in enumerate(parts) for q in s}; new=[]
        for block in parts:
            groups={}
            for q in sorted(block):
                sig=tuple(idx[m["delta"][q][a][0]] for a in m["alphabet"])
                groups.setdefault(sig,set()).add(q)
            new+=list(groups.values())
        if len(new)==len(parts): break
        parts=new
    names={q:f"m{i}" for i,s in enumerate(parts) for q in s}; d={}
    for i,s in enumerate(parts):
        q=sorted(s)[0]; d[f"m{i}"]={a:[names[m["delta"][q][a][0]]] for a in m["alphabet"]}
    return dict(states=list(d),alphabet=m["alphabet"],start=names[m["start"]],finals=sorted({names[q] for q in fs}),delta=d,classes={f"m{i}":sorted(s) for i,s in enumerate(parts)},partitions=history)
def simular_afd(m,w):
    q=m["start"]
    for a in w:
        if a not in m["alphabet"]: raise ValueError("Símbolo desconocido: "+a)
        q=m["delta"][q][a][0]
    return q in m["finals"]
def referencia(w):
    if set(w)-set(ALFABETO): raise ValueError("Símbolo desconocido")
    w=w.replace("V","")
    return [f"P{i}" for i,p in enumerate(PATRONES,1) if p in w]
def equivalentes(a,b):
    todo=deque([((a["start"],b["start"]),"")]); vistos={(a["start"],b["start"])}
    while todo:
        (x,y),w=todo.popleft()
        if (x in a["finals"])!=(y in b["finals"]): return False,w
        for c in ALFABETO:
            z=(a["delta"][x][c][0],b["delta"][y][c][0])
            if z not in vistos: vistos.add(z); todo.append((z,w+c))
    return True,None
