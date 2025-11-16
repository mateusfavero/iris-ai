#!/usr/bin/env python3
"""
Substitui arquivos de imagem por imagens pretas.
- Preserva o tamanho original quando possível.
- Se Pillow não estiver instalado, tenta instalar com pip (opção --user).
Execute a partir da raiz do repositório:
    python .\scripts\replace_with_black.py
"""
from pathlib import Path
import sys
import subprocess

FILES = [
    "public/colonca1.jpeg",
    "public/ISIC_0024329.jpg",
    "public/Tr-no_0010.jpg",
    "public/Tr-pi_0010.jpg",
]

repo_root = Path(__file__).resolve().parent.parent

try:
    from PIL import Image
except Exception:
    print("Pillow não encontrado — instalando via pip (opção --user)...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "Pillow"])  # --user evita alterar ambiente global
    from PIL import Image


def make_black(path: Path):
    # Se arquivo existir, tenta obter o tamanho; caso contrário, usa 512x512
    size = (512, 512)
    if path.exists():
        try:
            with Image.open(path) as im:
                size = im.size
        except Exception as e:
            print(f"Aviso: não foi possível abrir {path.name} para ler tamanho: {e}. Usando {size}.")
    else:
        # Certifique-se de que o diretório existe
        path.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", size, (0, 0, 0))
    # Salva usando extensão original (JPEG/ JPG)
    try:
        img.save(path, quality=95)
    except Exception as e:
        print(f"Erro salvando {path}: {e}")


if __name__ == "__main__":
    print("Iniciando substituição por imagens pretas...")
    for rel in FILES:
        p = repo_root / rel
        print(f"Processando: {p}")
        make_black(p)
    print("Concluído: as imagens foram sobrescritas (ou criadas). Verifique o diretório public/.")
