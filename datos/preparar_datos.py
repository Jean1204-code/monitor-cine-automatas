import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"monitor"))
from automata import referencia
MAP={1:"S",-1:"T",-2:"F",-3:"B",-4:"L",-5:"P",-6:"V",-7:"R"}
def preparar(source,out):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    h=pd.read_csv(source).drop_duplicates()
    required={"ticket_id","customer_id","time","status_id"}
    if not required<=set(h): raise ValueError("Faltan columnas")
    if h[list(required)].isna().any().any(): raise ValueError("Campos obligatorios vacíos")
    if not set(h.status_id)<=set(MAP): raise ValueError("Estado desconocido")
    h["time"]=pd.to_datetime(h["time"],format="mixed"); h=h.sort_values(["customer_id","time","ticket_id"])
    h["symbol"]=h.status_id.map(MAP); h["year"]=h.time.dt.year
    rows=[]
    for (u,y),a in h.groupby(["customer_id","year"],sort=True):
        if 3<=len(a)<=20: rows.append((u,y,"".join(a.symbol)))
    c=pd.DataFrame(rows,columns=["customer_id","year","cadena"]); c["positive"]=c.cadena.map(lambda w:bool(referencia(w)))
    pos=c[c.positive].drop_duplicates("customer_id").sample(frac=1,random_state=2026)
    neg=c[(~c.positive)&(~c.customer_id.isin(pos.customer_id))].drop_duplicates("customer_id").sample(frac=1,random_state=2026)
    rare=pos[pos.cadena.map(lambda w:"P3" in referencia(w))]; common=pos[~pos.customer_id.isin(rare.customer_id)]
    if len(rare)<3 or len(common)<60 or len(neg)<287: raise ValueError("Fuente insuficiente para el muestreo especificado")
    batches={"validacion":pd.concat([rare.iloc[:2],common.iloc[:52],neg.iloc[:246]]),"prueba":pd.concat([rare.iloc[2:3],common.iloc[52:60],neg.iloc[246:287]])}
    manifest=[]
    assert not set(batches["validacion"].customer_id)&set(batches["prueba"].customer_id)
    for name,b in batches.items():
        events=[]; keys=[]
        for j,r in enumerate(b.sample(frac=1,random_state=2026).itertuples(),1):
            sid=f"{name[:3].upper()}-{j:04d}"; actor=f"ACT-{name[:3]}-{j:04d}"; a=h[(h.customer_id==r.customer_id)&(h.year==r.year)]
            pats=referencia(r.cadena); lab="alerta" if pats else "sin_alerta"
            keys.append(dict(id_sesion=sid,etiqueta=lab,tipo_patron=";".join(pats),cadena=r.cadena))
            for k,e in enumerate(a.itertuples(),1):
                row=dict(id_evento=f"{sid}-{k:02d}",fecha_hora=str(e.time),id_sesion=sid,actor=actor,evento=f"STATUS_{e.status_id}",simbolo=e.symbol)
                if name=="validacion": row.update(etiqueta=lab,tipo_patron=";".join(pats))
                events.append(row)
            manifest.append(dict(id_sesion=sid,particion=name,anio=r.year,eventos=len(a)))
        pd.DataFrame(events).to_csv(out/f"{name}.csv",index=False); pd.DataFrame(keys).to_csv(out/f"clave_{name}.csv",index=False)
    pd.DataFrame(manifest).to_csv(out/"manifiesto.csv",index=False)
    return dict(elegibles=len(c),positivos=int(c.positive.sum()))
if __name__=="__main__":
    print(preparar(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else Path(__file__).parent/"local"))
