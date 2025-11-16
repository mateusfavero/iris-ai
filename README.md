
# Iris AI

Projeto exemplo: frontend (Vite + React + TypeScript) e backend (Flask/Python) para
análise automatizada de imagens médicas usando modelos Keras (.h5).

Este README descreve como configurar, executar e contribuir com o projeto localmente,
além de orientações sobre os modelos grandes que são gerenciados com Git LFS.

Índice
 - [Visão geral](#visão-geral)
 - [Estrutura do repositório](#estrutura-do-repositório)
 - [Pré-requisitos](#pré-requisitos)
 - [Instalação (Windows / PowerShell)](#instalação-windows--powershell)
 - [Rodando o backend (Flask)](#rodando-o-backend-flask)
 - [Rodando o frontend (Vite)](#rodando-o-frontend-vite)
 - [Como enviar imagens para análise (API)](#como-enviar-imagens-para-análise-api)
 - [Exemplo de resposta JSON](#exemplo-de-resposta-json)
 - [Modelos (.h5) e Git LFS](#modelos-h5-e-git-lfs)
 - [Scripts úteis](#scripts-úteis)
 - [Windows — problemas comuns e soluções](#windows--problemas-comuns-e-soluções)
 - [Deploy (Docker) rápido](#deploy-docker-rápido)
 - [Contribuição](#contribuição)
 - [Contato / próximos passos](#contato--próximos-passos)

Visão geral
----------

O objetivo deste repositório é prover um exemplo funcional de pipeline full-stack para
classificação de exames médicos por IA. O backend em `backend-example/app.py` recebe um
arquivo de imagem via POST e retorna uma resposta JSON com as predições. O frontend
provê uma interface simples para o usuário enviar imagens e visualizar resultados.

Estrutura do repositório
------------------------

- `backend-example/`  : aplicação Flask, dependências e scripts Python.
- `h5_models/`        : modelos Keras (.h5) e arquivos `classes_*.json` com rótulos.
- `public/`           : imagens públicas/estáticas usadas pelo frontend (exemplos).
- `src/`              : código do frontend (React + TypeScript).
- `scripts/`          : scripts utilitários (restauração/backup, etc.).

Pré-requisitos
--------------

- Node.js (recomendado LTS) e `npm` para o frontend.
- Python 3.10+ para o backend (venv recomendado).
- `git` e `git-lfs` (Git Large File Storage) para gerenciar modelos grandes.

Instalação (Windows / PowerShell)
--------------------------------

1) Clone o repositório:

```powershell
git clone https://github.com/mateusfavero/iris-ai.git
cd iris-ai
```

2) Instale o Git LFS (necessário para baixar os modelos `.h5`):

```powershell
# Com Chocolatey (opcional)
choco install git-lfs

# ou instale manualmente: https://git-lfs.github.com
git lfs install
git lfs pull
```

Rodando o backend (Flask)
-------------------------

Recomendo usar um virtual environment isolado para o backend:

```powershell
# a partir da raiz do repositório
python -m venv backend-example\.venv
.\backend-example\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\backend-example\.venv\Scripts\python.exe -m pip install -r backend-example\requirements.txt

# rodar o servidor Flask
.\backend-example\.venv\Scripts\python.exe backend-example\app.py
```

O servidor Flask escuta, por padrão, em `http://127.0.0.1:5000`.

Rodando o frontend (Vite)
------------------------

Na pasta raiz do projeto:

```powershell
npm install
npm run dev
```

Por padrão, o Vite serve o app em `http://localhost:5173`.

Como enviar imagens para análise (API)
-------------------------------------

Endpoint principal:

- `POST /analyze` — recebe `multipart/form-data` com o campo `image` (o arquivo).

Exemplo com `curl`:

```bash
curl -F "image=@/caminho/para/exame.jpg" http://127.0.0.1:5000/analyze
```

Exemplo de resposta JSON
------------------------

O backend retorna um JSON com, no mínimo, a predição do classificador de órgão
(`organ_classifier`) e — quando aplicável — a predição do especialista (`specialist`).

Exemplo real aproximado (formato usado pelo `backend-example/app.py`):

```json
{
  "organ_classifier": {
    "examType": "colonoscopy",
    "diagnosis": "lesão suspeita",
    "confidence": 0.87
  },
  "specialist": {
    "examType": "colon_polyp",
    "predicted_class": "adenoma",
    "confidence": 0.81,
    "top_k": [
      {"class":"adenoma","score":0.81},
      {"class":"hyperplastic","score":0.12}
    ]
  }
}
```

Se preferir que eu adapte esse exemplo ao formato exato do seu `backend-example/app.py`, eu atualizo com precisão.

Modelos (.h5) e Git LFS
-----------------------

Os modelos `.h5` em `h5_models/` são grandes e, portanto, estão gerenciados com Git LFS.
Isso permite manter o repositório Git leve enquanto armazena binários grandes separadamente.

Boa prática:

- Nunca comite grandes binários direto no Git sem usar LFS.
- Se clonar o repositório, rode `git lfs pull` para baixar os modelos.

Como adicionar um novo modelo `.h5` (exemplo):

```powershell
git lfs track "h5_models/*.h5"
git add .gitattributes
git add h5_models/novo_modelo.h5
git commit -m "Add modelo X via Git LFS"
git push
```

Scripts úteis
-------------

- `run-dev.ps1` — inicia backend e frontend juntos (útil no Windows/PowerShell).
- `backend-example/run-backend.ps1` — forma alternativa de iniciar o backend sem ativar o venv manualmente.

Windows — problemas comuns e soluções
------------------------------------

- Erro `npm.ps1 cannot be loaded`: use `npm.cmd` ou rode `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` como administrador para permitir a execução de scripts.

```powershell
# permitir scripts no escopo do usuário (poderá pedir confirmação)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# alternativa: chamar diretamente o shim npm.cmd
npm.cmd install
npm.cmd run dev
```

- Falha ao instalar pacotes Python com compilação (ex.: Pillow): atualize `pip`, `setuptools` e `wheel` e tente instalar binários pré-compilados quando possível.

```powershell
.\backend-example\.venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel
.\backend-example\.venv\Scripts\python.exe -m pip install --only-binary :all: pillow
```

- Se precisar compilar extensões nativas no Windows, instale o Build Tools (Visual Studio Build Tools) ou use uma distribuição que já forneça wheels (ex.: instalar do conda).

Deploy (Docker) rápido
----------------------

Um `Dockerfile` simples para servir a API Flask pode ser assim (exemplo):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend-example/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend-example/ .
EXPOSE 5000
CMD ["python", "app.py"]
```

Para o frontend (Vite) em produção, gere o build e sirva via um nginx leve ou use `serve`.

Contribuição
------------

- Abra issues para bugs e features.
- Para adicionar modelos: inclua `classes_*.json` descrevendo rótulos, confirme o pré-processamento e registre a entrada no README ou em um arquivo de metadados.
- Use mensagens de commit claras: `feat: add model X`, `fix: backend preprocess bug`, etc.

Contato / próximos passos
-------------------------

Se quiser, posso:
- transformar o índice em âncoras com links (já feito);
- adaptar o exemplo JSON ao formato exato do `backend-example/app.py` (se desejar);
- adicionar instruções de CI/CD (GitHub Actions) para rodar lint/testes e preparar builds.

Comandos úteis para commitar e enviar o README atualizado (PowerShell):

```powershell
git add README.md
git commit -m "docs: improve README (anchors, Windows notes, example JSON, Docker, contrib)"
git push origin main
```

Obrigado — diga se quer que eu faça o commit/push por você (posso fornecer os comandos ou orientações). 

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
