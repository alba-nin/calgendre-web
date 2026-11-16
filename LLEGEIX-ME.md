# Web de Cal Gendre 1879

```
index.html, cataleg.html, agenda.html, socis.html, avis-legal.html   ← pàgines (no cal tocar-les)
contingut.js                ← llegeix els textos de contingut/ i els posa a les pàgines
contingut/                  ← ★ TEXTOS EDITABLES (veure COM-EDITAR.md)
   general.json             ← telèfon, correu, adreça, horaris
   inici.json               ← textos de l'inici, paquet lector, carta
   agenda.json              ← activitats
img/                        ← fotos i logos
actualitzador/              ← programa per actualitzar el catàleg des de Galatea
documentacio/               ← guia d'Amics i flyers
.github/workflows/          ← construeix l'actualitzador com a .exe
cataleg.csv, cataleg-info.json  ← (els crea l'actualitzador)
```

**Per canviar textos, horaris o activitats → `COM-EDITAR.md`.**

### Substituir el contingut del repositori per aquesta versió

Amb git (recomanat, conserva les carpetes):
```bash
git clone https://github.com/alba-nin/calgendre-web
cd calgendre-web
git rm -r -q .                       # treu els fitxers antics (no toca .git)
cp -r /ruta/al/zip/calgendre-web/. .  # copia la versió nova, inclosos .gitignore i .github
git add -A && git commit -m "Web organitzada en carpetes i textos editables" && git push
```
Sense git: a GitHub, *Add file → Upload files* i arrossega **les carpetes** (`img`, `contingut`…)
des de l'explorador, no els fitxers d'un en un (si no, GitHub les aplana).
Els fitxers que comencen per punt (`.gitignore`, `.github`) s'han de crear a mà
(*Add file → Create new file*) si l'explorador no els mostra.

---

## 1. Posar la web en marxa (Alba, un sol cop)

1. Crea un repositori a GitHub (p. ex. `calgendre-web`) i puja-hi tot el contingut d'aquesta carpeta.
2. **Settings → Pages** → Source: *Deploy from a branch* → `main` / `(root)`.
3. Quan tinguis el domini a cdmon: a **Settings → Pages → Custom domain** escriu `calgendre.cat`,
   i a cdmon afegeix els registres DNS que t'indica GitHub (4 registres `A` i un `CNAME` per a `www`).
   Marca **Enforce HTTPS**.
4. Omple a `cataleg.html` (al principi del `<script>`): `WHATSAPP`, `EMAIL` i, quan el tingueu, `TODOSTUSLIBROS`.
   A `index.html`: `WHATSAPP`, horaris, preus i la llista `AGENDA`.

## 2. Preparar l'actualitzador a l'ordinador de la llibreria (Alba, un sol cop)

**a) Aconseguir l'.exe** (així no cal instal·lar Python a l'ordinador de la llibreria)
- Al repositori: **Actions → Actualitzador (.exe) → Run workflow**.
- Quan acabi (uns 3 minuts), entra a l'execució i descarrega `actualitzador-windows` (a *Artifacts*).
- Dins hi ha `Actualitza la web.exe` i `config.exemple.ini`.

> Alternativa sense .exe: instal·la Python des de python.org (marcant *Add to PATH*),
> executa `pip install openpyxl xlrd` i fes servir `Actualitza la web.bat`.

**b) Crear el token de GitHub** (la "clau" perquè el programa pugui pujar el catàleg)
- GitHub → la teva foto → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
- *Repository access*: **Only select repositories** → `calgendre-web`.
- *Permissions → Repository permissions → Contents*: **Read and write**. Res més.
- Posa-hi una caducitat llarga (1 any) i apunta't al calendari quan caduca.

**c) Instal·lar-ho**
- Crea la carpeta `Documents\Actualitzador web` i posa-hi `Actualitza la web.exe`.
- Copia-hi `config.exemple.ini` amb el nom **`config.ini`** i omple: `repositori` (`usuari/calgendre-web`) i `token`.
- Crea la carpeta `Documents\Exportacions Galatea` (o canvia `carpeta_exportacions` a `config.ini`).
- Clic dret a l'.exe → *Envia a → Escriptori (crea una drecera)*.

**d) Provar-ho un cop**
- Exporta des de Galatea el llistat d'articles a Excel i desa'l a `Exportacions Galatea`.
- Obre l'actualitzador i prem el botó. Les columnes ja estan ajustades a l'exportació d'articles de Galatea
  (DESCRIPCIÓ ARTICLE, AUTOR, NOM EDITORIAL, NOM TEMA, P.V.P IVA, DISPONIBLES, CODI, NOM FAMÍLIA, DATAEDICIÓ).
  Els articles de la família «Cafeteria» no surten a la web.
- Consell: a Galatea, deixa guardat el filtre/llistat d'exportació (articles amb estoc, amb títol, autor,
  editorial, matèria, PVP, existències i ISBN) perquè la teva germana només l'hagi de tornar a llançar.

## 3. Ús diari (per a la llibreria)

1. **Galatea**: exporta el llistat d'articles a Excel → desa'l a *Exportacions Galatea*.
2. **Escriptori**: obre *Actualitza la web* → prem **Actualitza la web**.
3. Quan surti «Fet!», la web estarà al dia en 1 o 2 minuts.

No cal esborrar els Excels vells: el programa agafa sempre el més recent.
Si surt un error, el missatge diu què passa; si no s'entén, fes-ne una foto i envia-la a l'Alba.
