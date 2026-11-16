# -*- coding: utf-8 -*-
"""
Actualitzador del catàleg de Cal Gendre
---------------------------------------
1. A Galatea, exporta el llistat d'articles a Excel i desa'l a la carpeta d'exportacions.
2. Obre aquest programa i prem el botó "Actualitza la web".

El programa agafa l'Excel més recent de la carpeta, el converteix al format del
catàleg (cataleg.csv) i el puja al repositori de GitHub de la web. En 1-2 minuts
la web mostra el catàleg nou.

Tota la configuració és a config.ini (al costat d'aquest fitxer).
"""
import base64
import configparser
import csv
import io
import json
import os
import sys
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------- configuració

def carpeta_programa() -> Path:
    # Funciona tant com a script .py com empaquetat en .exe (PyInstaller)
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).resolve().parent


def llegir_config() -> configparser.ConfigParser:
    cfg = configparser.ConfigParser(interpolation=None)
    ruta = carpeta_programa() / "config.ini"
    if not ruta.exists():
        raise ErrorUsuari(f"No trobo el fitxer de configuració:\n{ruta}")
    cfg.read(ruta, encoding="utf-8")
    return cfg


class ErrorUsuari(Exception):
    """Errors amb un missatge pensat per a la persona que fa servir el programa."""


# ------------------------------------------------------------ lectura d'Excel

def net(text) -> str:
    """minúscules, sense accents ni espais extra (per comparar noms de columna)"""
    s = unicodedata.normalize("NFD", str(text or "")).encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace("_", " ").replace(".", " ").split())


def fitxer_mes_recent(carpeta: Path) -> Path:
    if not carpeta.exists():
        raise ErrorUsuari(f"No existeix la carpeta d'exportacions:\n{carpeta}")
    candidats = [f for f in carpeta.iterdir()
                 if f.suffix.lower() in (".xlsx", ".xls", ".csv") and not f.name.startswith("~$")]
    if not candidats:
        raise ErrorUsuari(f"No hi ha cap Excel a la carpeta:\n{carpeta}\n\n"
                          "Primer exporta el llistat d'articles des de Galatea i desa'l allà.")
    return max(candidats, key=lambda f: f.stat().st_mtime)


def llegir_files(fitxer: Path) -> list[list]:
    ext = fitxer.suffix.lower()
    if ext == ".xlsx":
        import openpyxl
        wb = openpyxl.load_workbook(fitxer, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        return [list(r) for r in ws.iter_rows(values_only=True)]
    if ext == ".xls":
        import xlrd
        ws = xlrd.open_workbook(fitxer).sheet_by_index(0)
        return [ws.row_values(i) for i in range(ws.nrows)]
    # .csv: endevina separador i codificació
    cru = fitxer.read_bytes()
    for cod in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = cru.decode(cod)
            break
        except UnicodeDecodeError:
            continue
    try:
        dialecte = csv.Sniffer().sniff(text[:5000], delimiters=";,\t")
    except csv.Error:
        dialecte = csv.excel
    return [r for r in csv.reader(io.StringIO(text), dialecte)]


def trobar_capcalera(files: list[list], sinonims: dict) -> tuple[int, dict]:
    """Busca la fila de capçalera (pot no ser la primera) i quina columna és cada camp.
    Per a cada camp es fa servir el PRIMER sinònim de la llista que existeixi a l'Excel
    (així "NOM EDITORIAL" guanya a "EDITORIAL", que a Galatea és un codi numèric)."""
    millor = (-1, {})
    for i, fila in enumerate(files[:30]):
        noms = {}
        for j, cel in enumerate(fila):
            noms.setdefault(net(cel), j)
        mapa = {}
        for camp, llista in sinonims.items():
            for sin in llista:
                if net(sin) in noms:
                    mapa[camp] = noms[net(sin)]
                    break
        if len(mapa) > len(millor[1]):
            millor = (i, mapa)
    i, mapa = millor
    if "titol" not in mapa:
        raise ErrorUsuari("No trobo la columna del títol a l'Excel.\n\n"
                          "Obre config.ini i afegeix el nom exacte de la columna a la línia 'titol ='.")
    return i, mapa


def portada_url(v, isbn, per_isbn):
    v = str(v or "").strip()
    if v.startswith("http"):
        return v
    if per_isbn and isbn:
        return f"https://covers.openlibrary.org/b/isbn/{isbn}-M.jpg?default=false"
    return ""


def gira_autor(a: str) -> str:
    """'Vila, Enric' -> 'Enric Vila' (només si hi ha una sola coma)"""
    parts = [x.strip() for x in a.split(",")]
    return f"{parts[1]} {parts[0]}" if len(parts) == 2 and parts[1] else a


def a_numero(v, enter=False):
    if v is None or v == "":
        return 0
    if isinstance(v, (int, float)):
        return int(v) if enter else float(v)
    s = str(v).strip().replace("€", "").replace(" ", "")
    if "," in s and "." in s:          # 1.234,56
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", ".")
    try:
        return int(float(s)) if enter else float(s)
    except ValueError:
        return 0


def convertir(files: list[list], cfg) -> list[dict]:
    sinonims = {camp: [x.strip() for x in cfg["columnes"][camp].split("|") if x.strip()]
                for camp in cfg["columnes"]}
    fila_cap, mapa = trobar_capcalera(files, sinonims)
    op = cfg["opcions"]
    nomes_estoc = op.getboolean("nomes_amb_estoc", fallback=True)
    nomes_web = op.getboolean("nomes_marcats_publicar_web", fallback=False)
    dies_novetat = op.getint("dies_novetat", fallback=0)
    girar = op.getboolean("girar_autor", fallback=True)
    portades = op.getboolean("portades_per_isbn", fallback=True)
    excloure = {net(x) for x in op.get("excloure_families", "").split("|") if x.strip()}
    llibres = []
    for fila in files[fila_cap + 1:]:
        val = lambda camp: (fila[mapa[camp]] if camp in mapa and mapa[camp] < len(fila) else "")
        titol = str(val("titol") or "").strip()
        if not titol:
            continue
        if excloure and net(val("familia")) in excloure:
            continue
        if nomes_web and a_numero(val("publicar_web"), enter=True) != 1:
            continue
        estoc = a_numero(val("estoc"), enter=True) if "estoc" in mapa else 1
        if nomes_estoc and estoc <= 0:
            continue
        isbn = val("isbn")
        if isinstance(isbn, float):
            isbn = f"{isbn:.0f}"
        isbn = str(isbn or "").replace("-", "").strip()
        if not (isbn.isdigit() and len(isbn) in (10, 13)):
            isbn = ""                      # codis interns (PORTES, etc.) fora
        novetat = str(val("novetat") or "").strip()
        if dies_novetat and "data_novetat" in mapa:
            d = val("data_novetat")
            if isinstance(d, datetime) and 0 <= (datetime.now() - d).days <= dies_novetat:
                novetat = "si"
        autor = str(val("autor") or "").strip()
        seccio = str(val("seccio") or "").strip()
        llibres.append({
            "titol": titol,
            "autor": gira_autor(autor) if girar else autor,
            "editorial": "" if net(val("editorial")) in ("editores varios", "varios", "varis") else str(val("editorial") or "").strip(),
            "seccio": seccio[:1].upper() + seccio[1:],
            "preu": f"{a_numero(val('preu')):.2f}",
            "estoc": str(max(estoc, 0)),
            "isbn": isbn,
            "novetat": "si" if net(novetat) in ("si", "s", "x", "1", "true") else "",
            "portada": portada_url(val("portada"), isbn, portades),
        })
    if not llibres:
        raise ErrorUsuari("L'Excel no té cap llibre amb estoc (o les columnes no s'han reconegut).")
    return llibres


def a_csv(llibres: list[dict]) -> str:
    sortida = io.StringIO()
    camps = ["titol", "autor", "editorial", "seccio", "preu", "estoc", "isbn", "novetat", "portada"]
    w = csv.DictWriter(sortida, fieldnames=camps, lineterminator="\n")
    w.writeheader()
    w.writerows(llibres)
    return sortida.getvalue()


# ----------------------------------------------------------- pujada a GitHub

def pujar_github(cfg, ruta: str, contingut: str, missatge: str):
    g = cfg["github"]
    token, repo, branca = g["token"].strip(), g["repositori"].strip(), g.get("branca", "main").strip()
    if not token or "POSA_AQUI" in token:
        raise ErrorUsuari("Falta el token de GitHub a config.ini.")
    url = f"https://api.github.com/repos/{repo}/contents/{ruta}"
    caps = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json",
            "User-Agent": "calgendre-actualitzador"}

    def crida(metode, dades=None):
        req = urllib.request.Request(url + ("" if dades else f"?ref={branca}"), method=metode, headers=caps,
                                     data=json.dumps(dades).encode() if dades else None)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)

    sha = None
    try:
        sha = crida("GET")["sha"]
    except urllib.error.HTTPError as e:
        if e.code == 401:
            raise ErrorUsuari("GitHub no accepta el token (potser ha caducat). Cal posar-ne un de nou a config.ini.")
        if e.code != 404:
            raise
    except urllib.error.URLError:
        raise ErrorUsuari("No hi ha connexió a internet. Torna-ho a provar d'aquí a una estona.")
    dades = {"message": missatge, "branch": branca,
             "content": base64.b64encode(contingut.encode("utf-8")).decode()}
    if sha:
        dades["sha"] = sha
    try:
        crida("PUT", dades)
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise ErrorUsuari("El token de GitHub no té permís per escriure al repositori.")
        raise ErrorUsuari(f"GitHub ha donat un error ({e.code}). Torna-ho a provar.")


# --------------------------------------------------------------- feina sencera

def actualitzar(prova=False, fitxer=None) -> str:
    cfg = llegir_config()
    carpeta = Path(os.path.expandvars(os.path.expanduser(cfg["opcions"]["carpeta_exportacions"])))
    fitxer = Path(fitxer) if fitxer else fitxer_mes_recent(carpeta)
    llibres = convertir(llegir_files(fitxer), cfg)
    text = a_csv(llibres)
    ara = datetime.now()
    info = json.dumps({"actualitzat": ara.strftime("%Y-%m-%dT%H:%M"), "llibres": len(llibres)})
    if prova:
        (carpeta_programa() / "cataleg.csv").write_text(text, encoding="utf-8")
        return f"Prova feta amb «{fitxer.name}»: {len(llibres)} llibres.\nS'ha desat cataleg.csv (sense pujar res)."
    g = cfg["github"]
    pujar_github(cfg, g.get("ruta_csv", "cataleg.csv"), text, f"Catàleg actualitzat {ara:%d/%m/%Y %H:%M}")
    pujar_github(cfg, g.get("ruta_info", "cataleg-info.json"), info, "Data del catàleg")
    return (f"Fet! S'han pujat {len(llibres)} llibres.\n\n"
            f"Fitxer: {fitxer.name}\n"
            "La web es veurà actualitzada en 1 o 2 minuts.")


# ------------------------------------------------------------------ finestra

def finestra():
    import tkinter as tk
    from tkinter import filedialog

    MARRO, CREMA = "#5a2e0c", "#f4ecdf"
    arrel = tk.Tk()
    arrel.title("Cal Gendre · Actualitza la web")
    arrel.configure(bg=CREMA)
    arrel.geometry("460x360")
    arrel.resizable(False, False)

    tk.Label(arrel, text="CAL GENDRE 1879", bg=CREMA, fg=MARRO, font=("Georgia", 20)).pack(pady=(26, 2))
    tk.Label(arrel, text="Actualitzador del catàleg", bg=CREMA, fg=MARRO, font=("Georgia", 12, "italic")).pack()
    estat = tk.Label(arrel, text="1. Exporta l'Excel des de Galatea\n2. Prem el botó",
                     bg=CREMA, fg="#2a1708", font=("Georgia", 11), justify="center", wraplength=400)
    estat.pack(pady=22)

    def executa(fitxer=None):
        boto.config(state="disabled", text="Actualitzant…")
        estat.config(text="Un moment…", fg="#2a1708")
        arrel.update()
        try:
            estat.config(text=actualitzar(fitxer=fitxer), fg="#3d6b2a")
        except ErrorUsuari as e:
            estat.config(text=str(e), fg="#a0331f")
        except Exception as e:  # error inesperat: el mostrem perquè es pugui enviar
            estat.config(text=f"Error inesperat:\n{e}\n\nFes una foto d'aquest missatge i envia-la a l'Alba.", fg="#a0331f")
        boto.config(state="normal", text="Actualitza la web")

    boto = tk.Button(arrel, text="Actualitza la web", command=executa, bg=MARRO, fg=CREMA,
                     activebackground="#3b1d07", activeforeground=CREMA, relief="flat",
                     font=("Georgia", 15), padx=26, pady=12, cursor="hand2")
    boto.pack()

    def tria():
        f = filedialog.askopenfilename(title="Tria l'Excel de Galatea",
                                       filetypes=[("Excel o CSV", "*.xlsx *.xls *.csv")])
        if f:
            executa(f)

    tk.Button(arrel, text="Triar un altre fitxer…", command=tria, bg=CREMA, fg=MARRO,
              relief="flat", font=("Georgia", 10, "underline"), cursor="hand2").pack(pady=12)
    arrel.mainloop()


if __name__ == "__main__":
    if "--prova" in sys.argv:          # per provar sense finestra ni pujada
        args = [a for a in sys.argv[1:] if a != "--prova"]
        try:
            print(actualitzar(prova=True, fitxer=args[0] if args else None))
        except ErrorUsuari as e:
            print("ERROR:", e)
            sys.exit(1)
    else:
        finestra()
