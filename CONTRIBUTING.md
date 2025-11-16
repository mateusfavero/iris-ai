# Contribuindo — Iris AI

Obrigado por querer contribuir! Este documento explica o fluxo básico para abrir issues,
criar pull requests e adicionar novos modelos ao repositório.

1) Issues
- Abra uma issue descrevendo o problema ou feature desejada com passos para reproduzir
  (quando aplicável), e forneça informações do ambiente (SO, versões do Python/Node).

2) Branches e Pull Requests
- Crie uma branch com prefixo claro: `feat/`, `fix/`, `docs/` (ex.: `feat/add-model-colon`).
- Faça commits pequenos e com mensagens claras: `feat: add colon polyp model`,
  `fix: preprocess image dtype bug`.
- Abra um PR direcionado para `main`, descreva o que foi alterado e inclua instruções
  para testar localmente.

3) Adicionando modelos Keras (.h5)
- Os modelos pesados devem ser versionados com Git LFS. Já há rastreamento para
  `h5_models/*.h5` no repositório; para adicionar um novo modelo:

```powershell
git lfs track "h5_models/*.h5"    # só se ainda não estiver em .gitattributes
git add .gitattributes
git add h5_models/novo_modelo.h5
git add h5_models/classes_novo_modelo.json
git commit -m "feat(model): add novo_modelo for colon polyp"
git push origin sua-branch
```

- Sempre inclua um arquivo `classes_*.json` ao lado do `.h5` com a lista de classes
  (ex.: `classes_colon_polyp.json`) e, se necessário, um pequeno `README` ou metadado
  indicando o pré-processamento usado (resolução, normalização, recorte, ordem dos canais).

4) Testes e validação
- Inclua um script de teste mínimo quando fizer alterações no backend (por exemplo,
  um script que carrega o modelo e executa uma inferência rápida com uma imagem exemplo).
- Para mudanças em frontend, verifique `npm run build` e que a interface não quebre.

5) Estilo de código
- Frontend: siga as regras do `eslint` já configurado no projeto.
- Backend: formate com `black` e rode checagens básicas de lint (`flake8` se desejar).

6) Segurança e privacidade
- Nunca suba imagens de pacientes reais com dados pessoais identificáveis.
- Para dados sensíveis, mantenha-os fora do repositório e documente no PR a origem
  e as permissões de uso dos dados de treino/teste.

7) Contato
- Se tiver dúvida sobre os critérios para adicionar um novo modelo ou como formatar
  `classes_*.json`, abra uma issue e marque `@mateusfavero`.

Obrigado por contribuir — seu trabalho ajuda o projeto a ficar mais robusto.
