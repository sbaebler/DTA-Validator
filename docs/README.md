# `docs/` — die öffentliche Wiki-Seite

[`index.html`](index.html) ist eine **selbsttragende** Referenzseite zum Projekt: Sie fasst
Domäne, Verfahrensfamilie, Transportrahmen und das siebenstufige Prüfmodell zusammen und
rechnet alles am Beispiel-Dateipärchen
[`beispiele/pflege-105-sgbxi/`](../beispiele/pflege-105-sgbxi/) durch.

Selbsttragend heißt: keine externen Abhängigkeiten außer Google Fonts, keine Links, die
Zugang zum Repository voraussetzen. Der Auftragssatz und die Nutzdatendatei stehen
**vollständig und byte-genau** in der Seite — sie lässt sich also auch von Personen lesen,
die das Repository nicht sehen.

## Veröffentlichen über GitHub Pages

Das Repository ist derzeit **privat**; GitHub Pages ist noch nicht aktiviert. Zum
Veröffentlichen:

1. *Settings → Pages → Build and deployment → Source:* **Deploy from a branch**
2. Branch **`main`**, Ordner **`/docs`**, speichern.
3. Die Seite erscheint unter `https://sbaebler.github.io/DTA-Validator/`.

Pages aus einem privaten Repository setzt einen kostenpflichtigen GitHub-Plan voraus.
Alternativ das Repository auf *public* stellen — die Seite enthält ausschließlich
synthetische Daten und keine Sozialdaten, dem steht fachlich nichts entgegen.

`.nojekyll` schaltet die Jekyll-Verarbeitung ab; die Datei wird unverändert ausgeliefert.

## Inhalt aktualisieren

Ändert sich das Beispiel, müssen Lineal und EDIFACT-Listing in `index.html` mitgezogen
werden. Beide lassen sich gegen die Originaldateien prüfen:

```bash
python3 - <<'PY'
import re, html
src = open('docs/index.html', encoding='utf-8').read()

ruler = re.search(r'<div class="ruler".*?</div>\s*</div>', src, re.S).group(0)
rec = ''.join(html.unescape(v) for v in
              re.findall(r'<span class="v"[^>]*>(.*?)</span>', ruler, re.S))
auf = open('beispiele/pflege-105-sgbxi/TPLG0001.AUF', encoding='utf-8').read().rstrip('\n')
print('Auftragssatz identisch:', rec == auf, len(rec))

def strip(s):
    s = re.sub(r'<span class="tag">.*?</span>', '', s, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', '', s))
nutz = ''.join(strip(s) for s in re.findall(r'<div class="seg">.*?</div>', src, re.S))
soll = open('beispiele/pflege-105-sgbxi/TPLG0001', encoding='utf-8').read().rstrip('\n')
print('Nutzdaten identisch:  ', nutz == soll, len(nutz))
PY
```
