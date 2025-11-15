"""
EXEMPLO DE BACKEND FLASK PARA INTEGRAÇÃO COM O MODELO DE ML

Este é um exemplo básico de como criar um backend Flask que recebe
imagens e retorna a classificação e diagnóstico.

Para usar este exemplo:
1. Instale as dependências: pip install flask flask-cors pillow tensorflow numpy
2. Substitua a função mock_model_prediction() pela sua lógica real de ML
3. Execute: python app.py
4. O servidor estará rodando em http://localhost:5000
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64

app = Flask(__name__)
# Habilita CORS para permitir requisições do frontend React
CORS(app)

# SUBSTITUA ESTA FUNÇÃO PELA SUA LÓGICA DE MODELO REAL
def mock_model_prediction(image_data):
    """
    Esta é uma função de exemplo. Substitua pela sua implementação real.
    
    Args:
        image_data: PIL Image object
        
    Returns:
        dict com examType, diagnosis, confidence
    """
    # Aqui você deve:
    # 1. Pré-processar a imagem (resize, normalizar, etc)
    # 2. Passar a imagem pelo seu modelo de ML
    # 3. Interpretar os resultados
    # 4. Retornar a classificação e diagnóstico
    
    # Exemplo de retorno (inclui dimensões da imagem para facilitar testes):
    width, height = image_data.size
    return {
        "examType": "Raio-X Torácico",
        "diagnosis": "Análise automática detectou estruturas pulmonares normais. Recomenda-se revisão por especialista.",
        "confidence": 92,
        "image_width": width,
        "image_height": height
    }


@app.route('/analyze', methods=['POST'])
def analyze_image():
    """
    Endpoint principal que recebe a imagem e retorna a análise
    """
    try:
        # Verifica se há arquivo na requisição
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem foi enviada'}), 400
        
        file = request.files['image']
        
        # Verifica se o arquivo foi selecionado
        if file.filename == '':
            return jsonify({'error': 'Arquivo vazio'}), 400
        
        # Lê a imagem
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Converte para RGB se necessário (alguns modelos requerem)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # AQUI: Chame seu modelo de ML
        # Por exemplo:
        # preprocessed_image = preprocess_image(image)
        # prediction = your_model.predict(preprocessed_image)
        # result = interpret_prediction(prediction)
        
        result = mock_model_prediction(image)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Erro ao processar imagem: {str(e)}")
        return jsonify({'error': f'Erro ao processar imagem: {str(e)}'}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de verificação de saúde do servidor
    """
    return jsonify({'status': 'ok', 'message': 'Servidor rodando'}), 200


if __name__ == '__main__':
    print("="*60)
    print("SERVIDOR FLASK INICIADO")
    print("="*60)
    print("\nPara integrar com o frontend React:")
    print("1. Certifique-se de que o servidor está rodando em http://localhost:5000")
    print("2. No arquivo src/pages/Index.tsx, descomente as linhas de fetch")
    print("3. A URL do endpoint é: http://localhost:5000/analyze")
    print("\nLembre-se de implementar sua lógica de ML na função mock_model_prediction()!")
    print("="*60)
    print()
    
    # Roda o servidor em modo debug
    app.run(debug=True, host='0.0.0.0', port=5000)
