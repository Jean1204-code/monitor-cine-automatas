import argparse,json
from pathlib import Path
import pandas as pd
from automata import simular_afd
ROOT=Path(__file__).resolve().parents[1]
def procesar(entrada,salida,clave=None):
    m=json.loads((ROOT/"automatas/04_afd_minimo.json").read_text())
    d=pd.read_csv(entrada); cols={"id_evento","fecha_hora","id_sesion","simbolo"}
    if not cols<=set(d): raise ValueError("Faltan columnas: "+str(cols-set(d)))
    if d[list(cols)].isna().any().any(): raise ValueError("Datos obligatorios ausentes")
    if d.id_evento.duplicated().any(): raise ValueError("id_evento duplicado")
    d["fecha_hora"]=pd.to_datetime(d.fecha_hora,format="mixed",errors="raise"); rows=[]
    for sid,g in d.groupby("id_sesion"):
        w="".join(g.sort_values(["fecha_hora","id_evento"]).simbolo)
        try: label="alerta" if simular_afd(m,w) else "sin_alerta"; error=""
        except ValueError as e: label="no_evaluable"; error=str(e)
        rows.append(dict(id_sesion=sid,cadena=w,prediccion=label,error=error))
    r=pd.DataFrame(rows,columns=["id_sesion","cadena","prediccion","error"])
    salida=Path(salida); salida.parent.mkdir(parents=True,exist_ok=True); r.to_csv(salida,index=False)
    if clave:
        k=pd.read_csv(clave)
        if k.id_sesion.duplicated().any() or set(k.id_sesion)!=set(r.id_sesion): raise ValueError("La clave no coincide con los casos")
        if not set(k.etiqueta)<={"alerta","sin_alerta"}: raise ValueError("Etiquetas desconocidas")
        if r.prediccion.eq("no_evaluable").any(): raise ValueError("Hay casos no evaluables; revisar el reporte")
        r=r.merge(k[["id_sesion","etiqueta"]],on="id_sesion",validate="one_to_one")
        y=r.etiqueta.eq("alerta"); p=r.prediccion.eq("alerta")
        vp=int((y&p).sum()); fp=int((~y&p).sum()); fn=int((y&~p).sum()); vn=int((~y&~p).sum())
        met=dict(VP=vp,FP=fp,FN=fn,VN=vn,precision=vp/(vp+fp) if vp+fp else None,exhaustividad=vp/(vp+fn) if vp+fn else None)
        Path(str(salida)+".metricas.json").write_text(json.dumps(met,indent=2)); return met
    return {"casos":len(r),"alertas":int(r.prediccion.eq("alerta").sum())}
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("csv"); p.add_argument("--salida",default=str(ROOT/"tablas/resultados/detecciones.csv")); p.add_argument("--clave"); a=p.parse_args(); print(procesar(a.csv,a.salida,a.clave))
