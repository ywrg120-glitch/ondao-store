"""Processa os ficheiros postos em media/entrada/: corta para o tamanho do lugar,
comprime e grava em assets/ com o nome que o site usa. Os originais vão para
media/originais/. Usado pela GitHub Action (.github/workflows/media.yml) e
também pode correr no computador: python media/ferramentas/processar.py"""
import json, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ENTRADA, ORIGINAIS, ASSETS = RAIZ / "media/entrada", RAIZ / "media/originais", RAIZ / "assets"
SLOTS = {k: v for k, v in json.loads((RAIZ / "media/slots.json").read_text()).items() if not k.startswith("_")}
IMG = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".avif", ".bmp", ".tif", ".tiff"}
VID = {".mp4", ".mov", ".m4v", ".webm"}

def normal(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")

def achar_slot(nome):
    n = normal(nome)
    if n in SLOTS: return n
    # aceita também o nome final (ondao-01-topo-telemovel) ou sufixos como "-v2"
    for k, v in SLOTS.items():
        if n == normal(Path(v["ficheiro"]).stem) or n.startswith(k + "-"): return k
    return None

def imagem(orig, slot):
    from PIL import Image, ImageOps
    try:
        import pillow_heif; pillow_heif.register_heif_opener()
    except Exception: pass
    im = ImageOps.exif_transpose(Image.open(orig)).convert("RGB")
    im = ImageOps.fit(im, (slot["largura"], slot["altura"]), Image.LANCZOS, centering=tuple(slot.get("foco", [0.5, 0.5])))
    destino = ASSETS / slot["ficheiro"]
    q = 85
    while True:
        im.save(destino, "JPEG", quality=q, optimize=True, progressive=True)
        if destino.stat().st_size < 600_000 or q <= 60: break
        q -= 5
    return destino

def video(orig, slot):
    w, h = slot["largura"], slot["altura"]
    destino = ASSETS / slot["ficheiro"]
    filtro = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},fps=30"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(orig), "-t", "15", "-vf", filtro,
                    "-c:v", "libx264", "-preset", "slow", "-crf", "26", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", "-an", str(destino)], check=True)
    return destino

def baixar_links():
    """Um ficheiro .url (ou .txt) com um link dentro é descarregado primeiro.
    Nomes começados por "elenco-" vão para media/elenco/ (referências, não entram no site)."""
    import urllib.request
    for f in sorted(ENTRADA.iterdir()):
        if f.suffix.lower() not in {".url", ".txt"}: continue
        link = next((l.strip() for l in f.read_text().splitlines() if l.strip().startswith("http")), "")
        if not link: continue
        ext = Path(link.split("?")[0]).suffix.lower() or ".png"
        destino = (RAIZ / "media/elenco" if f.stem.startswith("elenco-") else ENTRADA) / (f.stem + ext)
        destino.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(destino, "wb") as out:
            shutil.copyfileobj(r, out)
        f.unlink()
        print(f"Descarregado: {f.name} -> {destino.relative_to(RAIZ)}")

def main():
    ORIGINAIS.mkdir(parents=True, exist_ok=True)
    baixar_links()
    feitos, ignorados = [], []
    for f in sorted(ENTRADA.iterdir()):
        if f.name.startswith(".") or f.name.lower() == "leia-me.md": continue
        k, ext = achar_slot(f.stem), f.suffix.lower()
        slot = SLOTS.get(k)
        if not slot or (slot["tipo"] == "imagem" and ext not in IMG) or (slot["tipo"] == "video" and ext not in VID):
            ignorados.append(f.name); continue
        d = imagem(f, slot) if slot["tipo"] == "imagem" else video(f, slot)
        shutil.move(str(f), ORIGINAIS / f.name)
        feitos.append(f"{f.name} -> assets/{d.name} ({d.stat().st_size // 1024} KB)")
    print("\n".join(["Processados:"] + feitos if feitos else ["Nada para processar."]))
    if ignorados:
        print("Nome não reconhecido (veja media/slots.json):", ", ".join(ignorados))
    return 0

if __name__ == "__main__":
    sys.exit(main())
