#!/usr/bin/env python3
"""Negativtests fuer pruefe_paket.py: je ein eingebauter Fehler muss den erwarteten Pruefcode ausloesen.
Aufruf: python3 test_pruefe_paket.py   (Exitcode 0 = alle Tests bestanden)"""
import importlib.util
import os
import re
import shutil
import sys
import tempfile
import zipfile

HIER = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("pruefe_paket", os.path.join(HIER, "pruefe_paket.py"))
pp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pp)

SRC, DTA = os.path.join(HIER, "imagelink-paket"), os.path.join(HIER, "TSOL0002")
Z = "D261012.T081200.T1IM0003"   # 20 Belege


def lauf(fn, auf_nachziehen=True):
    d = tempfile.mkdtemp()
    shutil.copytree(SRC, d, dirs_exist_ok=True)
    zin = zipfile.ZipFile(os.path.join(SRC, Z))
    items = [(i.filename, zin.read(i)) for i in zin.infolist()]
    neu = fn(items, d)
    if neu is not None:
        with zipfile.ZipFile(os.path.join(d, Z), "w", zipfile.ZIP_DEFLATED) as z:
            for n, data in neu:
                z.writestr(n, data)
        if auf_nachziehen:
            a = open(os.path.join(d, Z + ".AUF"), "rb").read().decode("latin1")
            sz = str(os.path.getsize(os.path.join(d, Z))).rjust(12, "0")
            open(os.path.join(d, Z + ".AUF"), "wb").write((a[:178] + sz + sz + a[202:]).encode("latin1"))
    fehler, _ = pp.pruefe(d, DTA)
    shutil.rmtree(d)
    return {x.split()[0] for x in fehler}


def ersetze_in_erster_xml(items, alt, neu):
    out, fertig = [], False
    for n, data in items:
        if n.endswith(".XML") and not fertig and alt in data.decode():
            data, fertig = data.decode().replace(alt, neu, 1).encode(), True
        out.append((n, data))
    assert fertig
    return out


erste_kvnr = lambda items: re.search(r'PKKVDE">(\w+)<', items[1][1].decode()).group(1)  # noqa: E731

FAELLE = {
    "gueltiges_paket": (lambda it, d: None, set()),
    "eingangskanal_7": (lambda it, d: ersetze_in_erster_xml(it, "<Eingangskanal>2<", "<Eingangskanal>7<"), {"P01"}),
    "falsche_kvnr": (lambda it, d: ersetze_in_erster_xml(it, erste_kvnr(it), "A000000000"), {"P04"}),
    "falsche_belegnummer": (lambda it, d: ersetze_in_erster_xml(
        it, '"Belegnummer"><NutzdatumString>0000007001', '"Belegnummer"><NutzdatumString>0000007999'), {"P07"}),
    "dokument_fehlt": (lambda it, d: it[2:], {"P07"}),
    "xml_kleinbuchstaben": (lambda it, d: [(n[:-3] + "xml" if k == 1 else n, x) for k, (n, x) in enumerate(it)], {"P02", "P07"}),
    "vorgangsumfang_2": (lambda it, d: ersetze_in_erster_xml(it, 'Vorgangsumfang="001"', 'Vorgangsumfang="002"'), {"P03"}),
    "pdf_kaputt": (lambda it, d: [(n, b"kaputt" if k == 0 else x) for k, (n, x) in enumerate(it)], {"P08"}),
    "namen_zu_lang": (lambda it, d: [(n.replace("SUE_SU", "SUE_ZZZZZZZZZZSU") if k < 2 else n, x) for k, (n, x) in enumerate(it)],
                      {"P02", "P03", "P05"}),
}

if __name__ == "__main__":
    schlecht = 0
    for name, (fn, soll) in FAELLE.items():
        ist = lauf(fn)
        ok = soll <= ist and (ist == soll if not soll else True)
        print("%-22s %s  erwartet %s, gefunden %s" % (name, "OK " if ok else "FEHLT", sorted(soll), sorted(ist)))
        schlecht += not ok
    # AUF-Groesse stimmt nicht: ZIP aendern, AUF nicht nachziehen
    ist = lauf(lambda it, d: it + [("SUE_SU20261012000301/ZUSATZ.TXT", b"x")], auf_nachziehen=False)
    print("%-22s %s  erwartet ['P06'], gefunden %s" % ("auf_groesse", "OK " if "P06" in ist else "FEHLT", sorted(ist)))
    schlecht += "P06" not in ist
    sys.exit(1 if schlecht else 0)
