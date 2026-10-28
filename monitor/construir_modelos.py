import json,csv,xml.etree.ElementTree as ET
from pathlib import Path
from automata import construir_afnd,eliminar_epsilon,determinizar,minimizar
ROOT=Path(__file__).resolve().parents[1]
def guardar_jff(m,path,reorganizado=False):
    root=ET.Element("structure"); ET.SubElement(root,"type").text="fa"; au=ET.SubElement(root,"automaton")
    ids={q:str(i) for i,q in enumerate(m["states"])}
    coords={"m1":(140,420),"m2":(470,220),"m4":(850,220),"m3":(470,710),"m5":(850,710),"m0":(1190,420)}
    for i,q in enumerate(m["states"]):
        st=ET.SubElement(au,"state",id=ids[q],name=q); x,y=coords[q] if reorganizado else (100+i%7*160,100+i//7*180)
        ET.SubElement(st,"x").text=str(x); ET.SubElement(st,"y").text=str(y)
        if q==m["start"]: ET.SubElement(st,"initial")
        if q in m["finals"]: ET.SubElement(st,"final")
    for q,row in m["delta"].items():
        for a,ts in row.items():
            for t in ts:
                tr=ET.SubElement(au,"transition"); ET.SubElement(tr,"from").text=ids[q]; ET.SubElement(tr,"to").text=ids[t]; ET.SubElement(tr,"read").text=a or None
    ET.indent(root); ET.ElementTree(root).write(path,encoding="utf-8",xml_declaration=True)
def construir():
    out=ROOT/"automatas"; tables=ROOT/"tablas"; out.mkdir(exist_ok=True); tables.mkdir(exist_ok=True)
    n=construir_afnd(); e=eliminar_epsilon(n); d=determinizar(e); m=minimizar(d)
    models={"01_afnd_unido_epsilon":n,"02_afnd_sin_epsilon":e,"03_afd":d,"04_afd_minimo":m}
    for k in range(1,4):
        qs=[q for q in n["states"] if q.startswith(f"p{k}_")]
        models[f"00_afnd_P{k}"]=dict(states=qs,alphabet=n["alphabet"],start=qs[0],finals=[qs[-1]],delta={q:n["delta"][q] for q in qs})
    for name,a in models.items():
        (out/f"{name}.json").write_text(json.dumps(a,indent=2))
        guardar_jff(a,out/f"{name}.jff")
        with (tables/f"{name}_tabla.csv").open("w",newline="") as f:
            w=csv.writer(f); w.writerow(["estado"]+a["alphabet"]+["final"])
            for q in a["states"]: w.writerow([q]+[",".join(a["delta"].get(q,{}).get(c,[])) or "∅" for c in a["alphabet"]]+[q in a["finals"]])
    guardar_jff(m,out/"04_afd_minimo_reorganizado.jff",True)
    with (tables/"subconjuntos.csv").open("w",newline="") as f:
        w=csv.writer(f); w.writerow(["estado_afd","subconjunto"])
        for q,ss in d["subsets"].items(): w.writerow([q,",".join(ss)])
    (tables/"refinamiento.json").write_text(json.dumps(m["partitions"],indent=2))
if __name__=="__main__": construir()
