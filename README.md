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

Observação sobre arquivos grandes (melhor prática)
----------------------------------------------

Os modelos `.h5` do repositório são gerenciados com Git LFS (Large File Storage). Para clonar
e trabalhar com este repositório corretamente, siga estas instruções:

1. Instale o Git LFS localmente (se ainda não tiver):

```powershell
choco install git-lfs    # com Chocolatey
# ou baixar/instalar de https://git-lfs.github.com
```

2. Inicialize o Git LFS no seu clone (uma vez):

```powershell
git lfs install
```

3. Ao atualizar sua cópia para o estado remoto (após um pull/clone):

```powershell
git fetch origin
git reset --hard origin/main
git lfs pull
```

Isso garante que os arquivos `.h5` sejam baixados corretamente do servidor LFS.

Se preferir, você pode simplesmente clonar de novo em vez de resetar:

```powershell
# cd <pasta-desejada>
git clone https://github.com/mateusfavero/iris-ai.git
git lfs pull
```

Se tiver dúvidas sobre espaço ou quotas de LFS no GitHub, verifique as configurações do repositório em GitHub → Settings → Data services.
