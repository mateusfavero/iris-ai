# Backend Flask para Iris AI

Este é um exemplo de backend Flask para integração com o modelo de Machine Learning.

## Como usar

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o servidor

```bash
python app.py
```

O servidor estará rodando em `http://localhost:5000`

### 3. Integrar com o frontend

No arquivo `src/pages/Index.tsx`, descomente as linhas do fetch:

```typescript
const formData = new FormData();
formData.append('image', file);
const response = await fetch('http://localhost:5000/analyze', {
  method: 'POST',
  body: formData
});
const data = await response.json();
```

E comente/remova a simulação de dados mock.

## Estrutura do Endpoint

### POST /analyze

Recebe uma imagem e retorna a análise.

**Request:**
- Content-Type: multipart/form-data
- Body: imagem com key 'image'

**Response:**
```json
{
  "examType": "Raio-X Torácico",
  "diagnosis": "Análise detalhada...",
  "confidence": 92
}
```

## Próximos passos

1. Implementar a lógica do seu modelo de ML na função `mock_model_prediction()`
2. Adicionar pré-processamento de imagens conforme necessário para seu modelo
3. Adicionar validações e tratamento de erros
4. Considerar adicionar autenticação se necessário
5. Para produção, usar um servidor WSGI como Gunicorn

## Notas importantes

- Este é um exemplo básico para desenvolvimento
- Para produção, considere usar Lovable Cloud para backend integrado
- Certifique-se de ter as permissões corretas para uso de imagens médicas
- Valide e sanitize todas as entradas
