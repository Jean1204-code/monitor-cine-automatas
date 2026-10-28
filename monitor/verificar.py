import json,itertools,random
from pathlib import Path
from automata import *
def verificar():
    n=construir_afnd(); e=eliminar_epsilon(n); d=determinizar(e); m=minimizar(d); count=0
    assert equivalentes(d,m)[0]
    for length in range(5):
        for letters in itertools.product(ALFABETO,repeat=length):
            w="".join(letters); expected=bool(referencia(w))
            assert simular_afnd(n,w)==simular_afnd(e,w)==simular_afd(d,w)==simular_afd(m,w)==expected
            count+=1
    r=random.Random(2026)
    for _ in range(1000):
        w="".join(r.choices(ALFABETO,k=r.randint(5,100)))
        assert simular_afnd(n,w)==simular_afd(m,w)==bool(referencia(w))
    try: simular_afd(m,"X")
    except ValueError: pass
    else: raise AssertionError("No se detectó símbolo desconocido")
    return dict(exhaustivas=count,aleatorias=1000,equivalencia=True,estados_afd=len(d["states"]),estados_minimo=len(m["states"]))
if __name__=="__main__":
    r=verificar(); out=Path(__file__).resolve().parents[1]/"tablas/resultados/pruebas.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(r,indent=2)); print(r)
