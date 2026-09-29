#!/usr/bin/env python3
"""Controlla le previsioni di 2026-09-29_reranker-gpu sulle esecuzioni di
esegui.sh e archivia il riassunto: per SciFact e NFCorpus, in float32 e
float16 su CUDA, mediana, p90 e p99 del tempo di riordino per query, nDCG@10 e
MRR@10 accanto a quelli del Mac (i rapporti del Mac valutati con lo stesso
binario), e la quota di query con i primi dieci identici a quelli del Mac.

    analizza.py
"""
import datetime, glob, json, os, statistics, subprocess, sys

QUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("TESI_RISULTATI") or os.path.join(QUI, "..", "..")
DIR = os.path.join(BASE, "esperimenti", "2026-09-29_reranker-gpu")
MAC = os.path.join(QUI, "..", "2026-09-28_reranker")


def ultimo(cartella, nome, base=DIR):
    trovati = sorted(glob.glob(os.path.join(base, cartella, f"*_{nome}.json")))
    if not trovati:
        sys.exit(f"manca {cartella}/{nome}")
    d = json.load(open(trovati[-1], encoding="utf8"))
    assert d["config"].get("modifiche_non_committate") in ("false", False), f"{trovati[-1]}: codice non committato"
    return os.path.basename(trovati[-1]), d


def percentile(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, max(0, round(p / 100 * len(xs) + 0.5) - 1))]


righe, file = {}, {}
for c in ("scifact", "nfcorpus"):
    fm, rap_mac = ultimo("riordinati", f"{c}-rr-LA", MAC)
    fvm, val_mac = ultimo("evaluate", f"{c}-rr-LA-mac")
    file[f"{c} mac"] = {"riordino": fm, "valutazione": fvm}
    mac = {"ndcg@10": val_mac["mean_ndcg@10"], "mrr@10": val_mac["mean_mrr@10"],
           "mediana_ms": statistics.median(x["ms"] for x in rap_mac["query"])}
    righe[f"{c} mac"] = mac
    for t in ("float32", "float16"):
        fq, rap = ultimo("riordinati", f"{c}-rr-LA-{t}")
        fv, val = ultimo("evaluate", f"{c}-rr-LA-{t}")
        assert rap["config"]["primo_stadio_sha256"] == rap_mac["config"]["primo_stadio_sha256"], f"{fq}: primo stadio diverso dal Mac"
        assert rap["config"]["dtype"] == t and rap["config"]["dispositivo"] == "cuda", fq
        assert [q["query"] for q in rap["query"]] == [q["query"] for q in rap_mac["query"]], f"{fq}: query diverse dal Mac"
        ms = [x["ms"] for x in rap["query"]]
        uguali = sum(a["ids"][:10] == b["ids"][:10] for a, b in zip(rap["query"], rap_mac["query"]))
        file[f"{c} {t}"] = {"riordino": fq, "valutazione": fv}
        righe[f"{c} {t}"] = {"ndcg@10": val["mean_ndcg@10"], "mrr@10": val["mean_mrr@10"],
                             "mediana_ms": statistics.median(ms), "p90_ms": percentile(ms, 90),
                             "p99_ms": percentile(ms, 99), "query": len(ms),
                             "primi_10_uguali_al_mac": round(uguali / len(ms), 4),
                             "torch": rap["config"]["torch"], "revisione_modello": rap["config"]["revisione"]}
for n, r in righe.items():
    extra = "" if n.endswith("mac") else f"  p90 {r['p90_ms']:.0f}  p99 {r['p99_ms']:.0f}  primi 10 uguali {r['primi_10_uguali_al_mac']:.3f}"
    print(f"{n:17} nDCG@10 {r['ndcg@10']:.4f}  MRR@10 {r['mrr@10']:.4f}  mediana {r['mediana_ms']:.0f} ms{extra}")

previsioni = {}


def prev(k, testo, ok, valore):
    previsioni[k] = {"previsione": testo, "valore": valore, "esito": "confermata" if ok else "smentita"}
    print(f"{k}. {previsioni[k]['esito']:10} {testo}: {valore}")


print()
s32, n32, s16, n16 = (righe[k]["mediana_ms"] for k in ("scifact float32", "nfcorpus float32", "scifact float16", "nfcorpus float16"))
prev(1, "fp32 SciFact: mediana fra 2,5 e 5 s", 2500 <= s32 <= 5000, f"{s32:.0f} ms")
prev(2, "fp32 NFCorpus: mediana entro il 20% di SciFact", abs(n32 - s32) <= 0.2 * s32, f"{n32:.0f} contro {s32:.0f} ms")
prev(3, "fp16: SciFact fra 0,7 e 2,5 s, almeno due volte più veloce di fp32", 700 <= s16 <= 2500 and s32 >= 2 * s16 and n32 >= 2 * n16,
     f"SciFact {s16:.0f} ms ({s32 / s16:.2f}x), NFCorpus {n16:.0f} ms ({n32 / n16:.2f}x)")


def scarti(t):
    return {c: max(abs(righe[f"{c} {t}"][m] - righe[f"{c} mac"][m]) for m in ("ndcg@10", "mrr@10")) for c in ("scifact", "nfcorpus")}


d32, d16 = scarti("float32"), scarti("float16")
u32 = {c: righe[f"{c} float32"]["primi_10_uguali_al_mac"] for c in ("scifact", "nfcorpus")}
prev(4, "fp32: metriche entro 0,001 dal Mac, almeno 95% delle query con i primi dieci identici",
     max(d32.values()) <= 0.001 and min(u32.values()) >= 0.95,
     "; ".join(f"{c} scarto {d32[c]:.4f}, primi dieci uguali {u32[c]:.3f}" for c in d32))
prev(5, "fp16: metriche entro 0,005 dal Mac", max(d16.values()) <= 0.005,
     "; ".join(f"{c} scarto {d16[c]:.4f}" for c in d16))

ora = datetime.datetime.now(datetime.timezone.utc)
git = lambda *x: subprocess.run(["git", "-C", QUI, *x], capture_output=True, text=True, check=True).stdout.strip()
esito = {"ran_at": ora.strftime("%Y-%m-%dT%H:%M:%SZ"),
         "config": {"commit": git("rev-parse", "--short", "HEAD"),
                    "modifiche_non_committate": "true" if git("status", "--porcelain", "--untracked-files=no", "--", QUI) else "false",
                    "file": file},
         "righe": righe, "previsioni": previsioni}
if not os.environ.get("TESI_RISULTATI"):
    sys.exit("!!! RISULTATO NON ARCHIVIATO: TESI_RISULTATI non è impostata.")
o = ora.strftime("%Y-%m-%dT%H%M%SZ"); p = os.path.join(DIR, f"{o}_esito.json"); k = 2
while os.path.exists(p):
    p = os.path.join(DIR, f"{o}-{k}_esito.json"); k += 1
open(p, "x", encoding="utf8").write(json.dumps(esito, indent=2, ensure_ascii=False))
print("archiviato in", p)
