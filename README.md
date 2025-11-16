# Iris AI

Frontend + Backend de exemplo para análise de imagens médicas com modelos Keras (.h5).

Como usar localmente:

```powershell
# 1) Criar venv para o backend (a partir da raiz do repo):
python -m venv backend-example/.venv

# 2) Instalar dependências do backend:
.\backend-example\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\backend-example\.venv\Scripts\python.exe -m pip install -r backend-example\requirements.txt

# 3) Rodar todo o projeto (backend + frontend):
powershell -ExecutionPolicy Bypass -File .\run-dev.ps1
```

O backend Flask está em `backend-example/app.py` e os modelos `.h5` ficam em `h5_models/`.

Desenvolvido por: sua equipe (remova referências externas para torná-lo autoral).
