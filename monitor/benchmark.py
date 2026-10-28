import argparse,time,statistics,json,platform
from pathlib import Path
import pandas as pd
from automata import *
if __name__=="__main__":
    p=argparse.ArgumentParser(); p.add_argument("claves",nargs="+"); a=p.parse_args()
    words=[]
    for f in a.claves: words+=pd.read_csv(f).cadena.tolist()
    n=construir_afnd(); m=minimizar(determinizar(eliminar_epsilon(n))); out={}
    for name,fun,model in [("AFND",simular_afnd,n),("AFD_minimo",simular_afd,m)]:
        times=[]
        for _ in range(7):
            start=time.perf_counter()
            for repeat in range(10):
                for w in words: fun(model,w)
            times.append((time.perf_counter()-start)/10*1000)
        out[name]={"mediana_ms":statistics.median(times),"min_ms":min(times),"max_ms":max(times)}
    out["entorno"]={"python":platform.python_version(),"plataforma":platform.platform(),"cadenas":len(words)}
    dest=Path(__file__).resolve().parents[1]/"tablas/resultados/benchmark.json"; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(json.dumps(out,indent=2)); print(json.dumps(out,indent=2))
