"""
Restaura 4 imagens enviadas pelo usuário para os caminhos em `public/`.
Uso:
  1) Coloque os 4 arquivos (qualquer nome) em `scripts/to_restore/`.
  2) Execute: `python scripts\restore_from_uploads.py`

O script ordena os arquivos por nome e copia/renomeia para:
  - public/colonca1.jpeg
  - public/ISIC_0024329.jpg
  - public/Tr-no_0010.jpg
  - public/Tr-pi_0010.jpg

Se já existirem arquivos com esses nomes, eles serão sobrescritos (faça backup se quiser).
"""
from pathlib import Path
import shutil

repo_root = Path(__file__).resolve().parent.parent
src_dir = repo_root / "scripts" / "to_restore"
dst_dir = repo_root / "public"

TARGETS = [
    "colonca1.jpeg",
    "ISIC_0024329.jpg",
    "Tr-no_0010.jpg",
    "Tr-pi_0010.jpg",
]


def main():
    if not src_dir.exists():
        print(f"Pasta de origem não encontrada: {src_dir}\nCrie a pasta e coloque os 4 anexos nela.")
        return

    files = sorted([p for p in src_dir.iterdir() if p.is_file()])
    if len(files) < 4:
        print(f"Foram encontrados {len(files)} arquivos em {src_dir}. Coloque exatamente 4 anexos e rode novamente.")
        for f in files:
            print(" -", f.name)
        return

    print("Arquivos encontrados (ordenados):")
    for i, f in enumerate(files[:4], start=1):
        print(f" {i}. {f.name}")

    for src, target in zip(files, TARGETS):
        dst = dst_dir / target
        print(f"Copiando {src.name} -> {dst}")
        shutil.copy2(src, dst)

    print("Restauração concluída. Verifique a pasta public/.")


if __name__ == '__main__':
    main()
