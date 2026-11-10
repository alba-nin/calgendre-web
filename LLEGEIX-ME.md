# Web de Cal Gendre 1879

```
index.html                 pàgina principal
cataleg.html               catàleg de llibres
cataleg.csv                (el crea l'actualitzador) llibres en estoc
cataleg-info.json          (el crea l'actualitzador) data de l'última actualització
img/                       fotos i logos (marró i crema, PNG transparents)
actualitzador/             programa per actualitzar el catàleg des de Galatea
.github/workflows/         construeix l'actualitzador com a .exe per a Windows
```

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
