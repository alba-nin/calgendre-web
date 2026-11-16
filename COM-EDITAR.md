# Com canviar els textos de la web (sense saber HTML)

Tots els textos que canvien sovint són a la carpeta **`contingut/`** del repositori:

| Fitxer | Què hi ha |
|---|---|
| `contingut/general.json` | Telèfon, WhatsApp, correu, adreça, **horaris**, catàleg «pròximament» sí/no |
| `contingut/inici.json` | Textos de la pàgina d'inici, el **paquet lector** i la **carta** |
| `contingut/agenda.json` | **Activitats de l'agenda** (surten a l'inici i al calendari) |

La resta de fitxers (`.html`, `contingut.js`, `img/`…) no cal tocar-los mai.

---

## 1. Donar accés a la teva germana (Alba, un sol cop)

1. La teva germana es fa un compte gratuït a **github.com** (*Sign up*).
2. Al repositori `calgendre-web`: **Settings → Collaborators → Add people** → escriu el seu usuari o correu.
3. Ella rep un correu i prem **Accept invitation**. A partir d'aquí pot editar.

Consell: que desi l'enllaç **github.com/alba-nin/calgendre-web/tree/main/contingut** a les adreces preferides del navegador.

---

## 2. Editar un text

1. Obre la carpeta **`contingut`** i el fitxer que vulguis (p. ex. `general.json`).
2. Prem el **llapis ✎** (a dalt a la dreta del fitxer).
3. Canvia **només el que hi ha entre cometes a la dreta dels dos punts**:
   ```
   "telefon": "930 968 669",
               ^^^^^^^^^^^  això és el que es canvia
   ```
4. Prem **Commit changes…** → torna a prémer **Commit changes**.
5. En 1–2 minuts el canvi és a la web (recarrega la pàgina).

### Les 3 regles d'or
- **No esborris cap cometa `"`**, ni la del principi ni la del final del text.
- **No esborris les comes `,`** del final de les línies.
- Si dins el text vols posar cometes, fes servir les cometes angulars **« »**.

Si t'equivoques, GitHub ho avisa: a la llista de canvis (*Commits*) sortirà una **✗ vermella**
al costat del teu canvi. Clica-la i et dirà a quina línia és l'error. Ho pots arreglar tornant a editar,
o desfer-ho: obre el fitxer → **History** → el canvi anterior → *…* → *View file* i copia'l.

---

## 3. Afegir una activitat a l'agenda

Obre `contingut/agenda.json` → llapis ✎. Cada activitat és un bloc entre `{ }`.
**Copia un bloc sencer, enganxa'l a sota posant una coma entre els dos blocs**, i canvia'n els textos:

```json
[
  {
    "data": "2026-11-28",
    "hora": "11–21 h",
    "tipus": "Inauguració",
    "titol": "Festa d'inauguració de Cal Gendre",
    "text": "Llibreria oberta i brindis, recital…",
    "inscripcio": "",
    "places": "Entrada lliure",
    "destacat": true
  },
  {
    "data": "2026-12-12",
    "hora": "19:30 h",
    "tipus": "Club de lectura",
    "titol": "Club de lectura de desembre",
    "text": "Parlarem de **Canto jo i la muntanya balla**.",
    "inscripcio": "whatsapp",
    "places": "12 places",
    "destacat": false
  }
]
```

- **data**: sempre així: `"any-mes-dia"` → `"2026-12-12"`.
- **inscripcio**: `""` (entrada lliure) · `"whatsapp"` (botó que obre WhatsApp) · o un enllaç `"https://…"` a un formulari.
- **destacat**: `true` = es pinta en lila (actes especials) · `false` = normal. **Sense cometes.**
- L'**últim** bloc **no** porta coma després de `}`.
- Les activitats passades s'amaguen soles: no cal esborrar-les.

---

## 4. Coses que es canvien amb `true` / `false`

| On | Què | Valor |
|---|---|---|
| `inici.json` → `"carta"` | `"proximament"` | `true` = carta difuminada amb «Pròximament» · `false` = es veu la carta |
| `general.json` | `"cataleg_proximament"` | `true` = catàleg amb «Pròximament» · `false` = catàleg actiu |

(`true` i `false` van **sense cometes**.)

## 5. La carta

A `inici.json`, dins `"carta"` → `"seccions"`, cada producte és:
```json
{ "nom": "Cafè amb llet", "preu": "1,80" }
```
Si `"preu"` és buit (`""`) surt «— €».

## 6. Trucs de format (a qualsevol text)

| Escrius | Surt |
|---|---|
| `**llibres**` | **llibres** (negreta) |
| `__la calma__` | <u>la calma</u> (subratllat) |

---

**Fotos:** per canviar una foto, puja la nova a la carpeta `img/` **amb el mateix nom** que la que vols substituir
(*Add file → Upload files* dins la carpeta `img`). Si no tens clar quin nom té, demana-ho a l'Alba.
