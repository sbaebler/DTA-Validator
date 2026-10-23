#!/usr/bin/env python3
"""Erzeugt das synthetische Grossbeispiel § 302 SGB V (Hilfsmittel, Inkontinenz).

Ausgabe (neben diesem Skript):
  TSOL0001            Nutzdaten, EDIFACT, ISO 8859-1, ohne Zeilenumbrueche
  TSOL0001.AUF        Auftragssatz, 348 Byte
  TSOL0001.zeilen.txt Lesefassung: eine Hilfsmittelposition je Zeile (45.000 Zeilen)
  beispiel-kennzahlen.yaml  Erwartungswerte fuer Tests

Aufruf: python3 generate.py [--positionen 45000] [--seed 302]
Erzeugung ist deterministisch: gleicher Seed, gleiche Bytes.
"""
import argparse
import hashlib
import os
import random
from decimal import Decimal, ROUND_HALF_UP

HIER = os.path.dirname(os.path.abspath(__file__))

POS_JE_FALL = 5
LEISTUNGSMONAT = "202609"
ERSTELLT = "20261005"
UHRZEIT = "0812"
DATEINAME_APPREF = "SL076001SBK"   # Anwendungsreferenz, Muster wie im Pflege-Beispiel (11 Stellen)

# Produktarten (7-stellig) und Einzelprodukte. SYNTHETISCH: keine Eintraege aus dem
# GKV-Hilfsmittelverzeichnis. Produktgruppe 15 = Inkontinenzhilfen, die weiteren
# Stellen sind erfunden. Preise in Cent je Stueck/Packung.
PRODUKTE = [
    # (Produktart 7, Bezeichnung, [(Einzelprodukt 3, Preis_ct, Packung)])
    ("1525101", "Saugende Vorlage anatomisch leicht", [("001", 2150, 28), ("002", 2390, 28), ("003", 2610, 24)]),
    ("1525102", "Saugende Vorlage anatomisch mittel", [("001", 2890, 28), ("002", 3120, 28), ("003", 3340, 26)]),
    ("1525103", "Saugende Vorlage anatomisch stark", [("001", 3450, 28), ("002", 3780, 26), ("003", 3990, 24)]),
    ("1525201", "Inkontinenz-Pants mittel", [("001", 3290, 14), ("002", 3560, 14), ("003", 3810, 12)]),
    ("1525202", "Inkontinenz-Pants stark", [("001", 3920, 14), ("002", 4280, 14), ("003", 4510, 12)]),
    ("1525301", "Inkontinenz-Slip mit Klebeverschluss", [("001", 3690, 28), ("002", 3940, 24), ("003", 4180, 20)]),
    ("1525401", "Krankenunterlage saugend, Einmalgebrauch", [("001", 2480, 25), ("002", 2730, 25)]),
    ("1525501", "Netzhose fuer Vorlagen", [("001", 1190, 5), ("002", 1340, 5)]),
    ("1524101", "Kondomurinal", [("001", 1890, 30), ("002", 2060, 30)]),
    ("1524201", "Urinbeutel Bein mit Ablasshahn", [("001", 2540, 10), ("002", 2710, 10)]),
    ("1599101", "Hautschutz und Reinigung Inkontinenz", [("001", 890, 1), ("002", 1090, 1)]),
]
ERSATZ_ANTEIL = 0.02   # Anteil Positionen mit Ersatznummer <Produktart>900 (Hilfsmittelverzeichnis-Ersatzregel)

KOSTENTRAEGER_ANTEIL = [("1", 4000), ("2", 3000), ("3", 2000)]   # Faelle je Kostentraeger (Summe 9.000)

NAMEN = ["Abendroth", "Berger", "Conradi", "Dreyer", "Eberhard", "Fuchs", "Gruber", "Hartmann",
         "Imhof", "Jansen", "Keller", "Lindner", "Maurer", "Neumann", "Ostermann", "Pohl",
         "Quandt", "Rieger", "Sommer", "Thalmann", "Ulrich", "Vogel", "Wagner", "Zimmer"]
VORNAMEN = ["Anna", "Bernd", "Clara", "Dieter", "Elke", "Frank", "Gerda", "Hans", "Irene",
            "Jürgen", "Karin", "Lothar", "Marta", "Norbert", "Ursula", "Walter"]


def ik_pz(ik8: str) -> int:
    s = 0
    for z, g in zip(map(int, ik8[2:8]), [2, 1, 2, 1, 2, 1]):
        p = z * g
        s += p - 9 if p > 9 else p
    return s % 10


def mk_ik(klass: str, region: str, serie: str) -> str:
    k = klass + region + serie
    return k + str(ik_pz(k))


def kvnr(buchstabe: str, ziffern8: str) -> str:
    """ANNAHME (nicht belegt, vgl. KB 02-krankenversichertennummer): Buchstabe -> 2 Ziffern,
    Gewichte 1-2 im Wechsel, Quersumme, mod 10. Reproduziert K74185296|7 aus dem Pflege-Beispiel."""
    z = [int(c) for c in "%02d" % (ord(buchstabe) - 64) + ziffern8]
    s = 0
    for i, d in enumerate(z):
        p = d * (1 if i % 2 == 0 else 2)
        s += p - 9 if p > 9 else p
    return buchstabe + ziffern8 + str(s % 10)


def eur(ct: int) -> str:
    return "%d,%02d" % divmod(ct, 100)


def mwst_ct(brutto_ct: int, satz: int = 7) -> int:
    d = (Decimal(brutto_ct) * satz / (100 + satz)).quantize(Decimal("1"), ROUND_HALF_UP)
    return int(d)


def erzeuge(n_pos: int, seed: int):
    rnd = random.Random(seed)
    n_faelle = n_pos // POS_JE_FALL
    assert n_faelle * POS_JE_FALL == n_pos, "Positionszahl muss Vielfaches von %d sein" % POS_JE_FALL
    skala = n_faelle / sum(n for _, n in KOSTENTRAEGER_ANTEIL)
    verteilung = [(k, round(n * skala)) for k, n in KOSTENTRAEGER_ANTEIL]
    verteilung[-1] = (verteilung[-1][0], n_faelle - sum(n for _, n in verteilung[:-1]))

    ik_le = mk_ik("59", "11", "2041")          # Klassifikation 59 Sonstige Erbringer, Region Berlin
    ik_dan = "661100423"                      # Datenannahmestelle (wie Pflege-Beispiel)
    kostentraeger = {"1": mk_ik("10", "95", "2461"), "2": mk_ik("10", "53", "1207"), "3": mk_ik("10", "84", "3318")}

    seg = []            # alle Segmente (ohne Terminator)
    zeilen = []         # Lesefassung
    unh_nr = 0
    belegnr = 0
    fall_nr = 0
    summe_pos = 0
    summe_gesamt = 0
    kennzahlen = []
    fall_daten = []     # strukturierte Faelle, fuer abgeleitete Beispiele
    seg.append("UNB+UNOC:3+%s+%s+%s:%s+1+%s+0" % (ik_le, ik_dan, ERSTELLT, UHRZEIT, DATEINAME_APPREF))

    def nachricht(typ, inhalt):
        nonlocal unh_nr
        unh_nr += 1
        # UNT zaehlt UNH und UNT mit
        seg.append("UNH+%d+%s:1" % (unh_nr, typ))
        seg.extend(inhalt)
        seg.append("UNT+%d+%d" % (len(inhalt) + 2, unh_nr))

    for kt_nr, n_k in verteilung:
        ik_kt = kostentraeger[kt_nr]
        rechnr = "20261%05d:0" % int(kt_nr)
        fkt = "FKT+01+%s+%s+%s" % (ik_le, ik_kt, ik_le)
        rec = "REC+%s+%s+1+EUR" % (rechnr, ERSTELLT)
        slla = [fkt, rec]
        kt_brutto = kt_zuz = 0
        kt_pos = 0
        for _ in range(n_k):
            fall_nr += 1
            belegnr += 1
            kv = kvnr(chr(65 + rnd.randrange(26)), "%08d" % rnd.randrange(10**7, 10**8))
            name, vorname = rnd.choice(NAMEN), rnd.choice(VORNAMEN)
            geb = "%04d%02d%02d" % (rnd.randrange(1925, 2018), rnd.randrange(1, 13), rnd.randrange(1, 29))
            slla.append("INV+%s+%07d" % (kv, belegnr))
            slla.append("NAD+%s+%s+%s" % (name, vorname, geb))
            tag = LEISTUNGSMONAT + "%02d" % rnd.randrange(1, 29)
            slla.append("ESK+" + tag)
            fall_ct = 0
            positionen = []
            kategorie = rnd.choice(PRODUKTE)
            for p in range(POS_JE_FALL):
                # Versorgung besteht meist aus 1-2 Produktarten: Hauptprodukt + Zubehoer
                art = kategorie if p < 3 else rnd.choice(PRODUKTE)
                art_nr, bez, einzel = art
                if rnd.random() < ERSATZ_ANTEIL:
                    hmnr = art_nr + "900"
                    preis, pack = rnd.choice(einzel)[1:]
                else:
                    e = rnd.choice(einzel)
                    hmnr = art_nr + e[0]
                    preis, pack = e[1], e[2]
                anzahl = rnd.choice([1, 1, 1, 2])
                ges = preis * anzahl
                fall_ct += ges
                positionen.append(dict(hmnr=hmnr, anzahl=anzahl, preis=preis, gesamt=ges, bez=bez, packung=pack))
                slla.append("EHE+%s+00+%d+%s+%s+07" % (hmnr, anzahl, eur(preis), eur(ges)))
                zeilen.append("%s|%07d|%s|%s|00|%d|%s|%s|%s" % (
                    kv, belegnr, ik_kt, hmnr, anzahl, eur(preis), eur(ges), bez))
                kt_pos += 1
            zuz_ct = 0 if rnd.random() < 0.18 else min(1000, int((Decimal(fall_ct) / 10).quantize(Decimal("1"), ROUND_HALF_UP)))
            slla.append("IAF+%s+%s++%s" % (eur(fall_ct), eur(zuz_ct), eur(fall_ct - zuz_ct)))
            fall_daten.append(dict(kt=kt_nr, ik_kt=ik_kt, kvnr=kv, belegnr=belegnr, name=name, vorname=vorname,
                                   geburt=geb, leistungstag=tag,
                                   positionen=positionen, brutto=fall_ct, zuzahlung=zuz_ct))
            kt_brutto += fall_ct
            kt_zuz += zuz_ct
        slga = [fkt, rec, "UST+DE999999999+J+01",
                "GES+%s+%s++%s+%s" % (eur(kt_brutto), eur(kt_zuz), eur(kt_brutto - kt_zuz), eur(mwst_ct(kt_brutto))),
                "NAM+Musterhaus Homecare GmbH+Inkontinenzversorgung 030 5550199"]
        nachricht("SLGA", slga)
        nachricht("SLLA", slla)
        summe_pos += kt_pos
        summe_gesamt += kt_brutto
        kennzahlen.append((kt_nr, ik_kt, rechnr, n_k, kt_pos, kt_brutto, kt_zuz))
    seg.append("UNZ+%d+1" % unh_nr)
    meta = dict(faelle_daten=fall_daten, ik_le=ik_le, ik_dan=ik_dan, positionen=summe_pos, faelle=fall_nr, nachrichten=unh_nr,
                segmente=len(seg), gesamt_ct=summe_gesamt, kt=kennzahlen)
    return "'".join(seg) + "'", zeilen, meta


def auftragssatz(meta, groesse, transfer="001", appref=DATEINAME_APPREF, erstellt=ERSTELLT):
    def N(v, l): return str(v).rjust(l, "0")
    def A(v, l): return str(v).ljust(l)
    felder = [
        N(500000, 6), "01", N(348, 8), N(0, 3), "TSOL0", transfer, A("", 5),
        A(meta["ik_le"], 15), A(meta["ik_le"], 15), A(meta["ik_dan"], 15), A(meta["ik_dan"], 15),
        N(0, 6), N(0, 6), appref,
        erstellt + UHRZEIT + "00", erstellt + UHRZEIT + "30", N(0, 14), N(0, 14),
        N(0, 6), "0", N(groesse, 12), N(groesse, 12), "I1", "00", "00", "00",
        A("", 3), N(0, 5), N(0, 8), " ", N(0, 2), "5", N(0, 10), N(0, 6),
        A("", 28), A("", 44), "01" + " " * 26 + "01",
    ]
    s = "".join(felder)
    assert len(s) == 348, len(s)
    return s.encode("latin-1")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--positionen", type=int, default=45000)
    ap.add_argument("--seed", type=int, default=302)
    a = ap.parse_args()
    daten, zeilen, meta = erzeuge(a.positionen, a.seed)
    raw = daten.encode("latin-1")
    with open(os.path.join(HIER, "TSOL0001"), "wb") as f:
        f.write(raw)
    with open(os.path.join(HIER, "TSOL0001.AUF"), "wb") as f:
        f.write(auftragssatz(meta, len(raw)))
    with open(os.path.join(HIER, "TSOL0001.zeilen.txt"), "w", encoding="latin-1", newline="\n") as f:
        f.write("\n".join(zeilen) + "\n")
    with open(os.path.join(HIER, "beispiel-kennzahlen.yaml"), "w") as f:
        f.write("# Erwartungswerte, erzeugt von generate.py (Seed %d)\n" % a.seed)
        f.write("positionen: %d\nabrechnungsfaelle: %d\nnachrichten: %d\nsegmente: %d\n"
                % (meta["positionen"], meta["faelle"], meta["nachrichten"], meta["segmente"]))
        f.write("nutzdaten_bytes: %d\nnutzdaten_sha256: %s\n" % (len(raw), hashlib.sha256(raw).hexdigest()))
        f.write("gesamtbrutto_eur: \"%s\"\nik_leistungserbringer: \"%s\"\nik_datenannahmestelle: \"%s\"\n"
                % (eur(meta["gesamt_ct"]), meta["ik_le"], meta["ik_dan"]))
        f.write("rechnungen:\n")
        for kt_nr, ik_kt, rn, nf, npos, br, zu in meta["kt"]:
            f.write("  - {rechnungsnummer: \"%s\", ik_kostentraeger: \"%s\", faelle: %d, positionen: %d, "
                    "brutto_eur: \"%s\", zuzahlung_eur: \"%s\"}\n" % (rn, ik_kt, nf, npos, eur(br), eur(zu)))
    print(meta["positionen"], "Positionen,", meta["faelle"], "Faelle,", len(raw), "Byte")


if __name__ == "__main__":
    main()
