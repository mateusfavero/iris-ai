from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import io
import base64
import os
import json
import numpy as np
import tensorflow as tf

app = Flask(__name__)
# Habilita CORS para permitir requisições do frontend React
CORS(app)

# Configurações do modelo
CLASSES = ['Cerebro', 'Colon', 'Mama', 'Pele', 'Pulmao']
# Caminho relativo do arquivo .h5 (resolvido a partir deste arquivo)
MODEL_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'h5_models', 'modelo_identifica_orgao.h5'))

# Variável global para manter o modelo em memória
MODEL = None


def load_model_if_needed():
    """Carrega o modelo Keras na primeira requisição (lazy load)."""
    global MODEL
    if MODEL is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Modelo não encontrado em: {MODEL_PATH}")
        print(f"Carregando modelo Keras de: {MODEL_PATH}")
        MODEL = tf.keras.models.load_model(MODEL_PATH)
        print("Modelo carregado com sucesso.")
    return MODEL


def preprocess_image(pil_image, target_size=(150, 150)):
    """Converte PIL Image para array pronto para o modelo.

    - Redimensiona para `target_size`
    - Garante 3 canais RGB
    - Normaliza para [0,1]
    - Adiciona dimensão de batch
    """
    if pil_image.mode != 'RGB':
        pil_image = pil_image.convert('RGB')
    img = pil_image.resize(target_size)
    arr = np.asarray(img).astype('float32') / 255.0
    if arr.ndim == 2:
        arr = np.stack([arr] * 3, axis=-1)
    # Garantir forma (H,W,3)
    if arr.shape[-1] != 3:
        # tenta ajustar
        arr = arr[..., :3]
    batch = np.expand_dims(arr, axis=0)
    return batch


# --- Traduções de diagnóstico para modelos especialistas (mapas amigáveis)
DIAGNOSTICO_MAP_HISTO = {
    "lung_n": "Tecido Pulmonar Normal",
    "lung_aca": "Positivo: Cancro de Pulmão (Adenocarcinoma)",
    "lung_scc": "Positivo: Cancro de Pulmão (Carcinoma de Células Escamosas)",
    "colon_n": "Tecido de Cólon Normal",
    "colon_aca": "Positivo: Cancro de Cólon (Adenocarcinoma)"
}

DIAGNOSTICO_MAP_CEREBRO = {
    "no_tumor": "Normal (Sem indicação de tumor)",
    "glioma_tumor": "Positivo: Tumor Cerebral (Glioma)",
    "meningioma_tumor": "Positivo: Tumor Cerebral (Meningioma)",
    "pituitary_tumor": "Positivo: Tumor Cerebral (Tumor Pituitário)"
}

DIAGNOSTICO_MAP_PELE = {
    "nv": "Lesão Benigna (Nevo)",
    "mel": "Positivo: Cancro de Pele (Melanoma)",
    "bkl": "Lesão Benigna (Queratose Benigna)",
    "bcc": "Positivo: Cancro de Pele (Carcinoma Basocelular)",
    "akiec": "Lesão Pré-Cancerígena (Queratose Actínica)",
    "vasc": "Lesão Benigna (Vascular)",
    "df": "Lesão Benigna (Dermatofibroma)"
}

DIAGNOSTICO_MAP_MAMA = {
    "Normal": "Tecido Mamário Normal",
    "Benign": "Lesão Benigna",
    "InSitu": "Positivo: Cancro de Mama (Carcinoma In Situ)",
    "Invasive": "Positivo: Cancro de Mama (Carcinoma Invasivo)"
}


# --- Configurações dos modelos especialistas mapeadas pelo nome do órgão
H5_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'h5_models'))
SPECIALIST_CONFIGS = {
    'Cerebro': {
        'model_path': os.path.join(H5_DIR, 'modelo_cerebro.h5'),
        'classes_path': os.path.join(H5_DIR, 'classes_cerebro.json'),
        'input_shape': (150, 150, 3),
        'translation_map': DIAGNOSTICO_MAP_CEREBRO,
        'exam_name': 'Cancro Cerebral (MRI)'
    },
    'Pulmao': {
        'model_path': os.path.join(H5_DIR, 'modelo_histo_pulmao.h5'),
        'classes_path': os.path.join(H5_DIR, 'classes_histo_pulmao.json'),
        'input_shape': (150, 150, 3),
        'translation_map': DIAGNOSTICO_MAP_HISTO,
        'exam_name': 'Histopatologia Pulmão'
    },
    'Colon': {
        'model_path': os.path.join(H5_DIR, 'modelo_histo.h5'),
        'classes_path': os.path.join(H5_DIR, 'classes_histo.json'),
        'input_shape': (150, 150, 3),
        'translation_map': DIAGNOSTICO_MAP_HISTO,
        'exam_name': 'Histopatologia Cólon'
    },
    'Mama': {
        'model_path': os.path.join(H5_DIR, 'modelo_mama.h5'),
        'classes_path': os.path.join(H5_DIR, 'classes_mama.json'),
        'input_shape': (150, 150, 3),
        'translation_map': DIAGNOSTICO_MAP_MAMA,
        'exam_name': 'Cancro de Mama (Histopatologia)'
    },
    'Pele': {
        'model_path': os.path.join(H5_DIR, 'modelo_pele.h5'),
        'classes_path': os.path.join(H5_DIR, 'classes_pele.json'),
        'input_shape': (150, 150, 3),
        'translation_map': DIAGNOSTICO_MAP_PELE,
        'exam_name': 'Cancro de Pele (Dermatoscopia)'
    }
}

# Cache para modelos especialistas carregados
SPECIALIST_CACHE = {}


def load_specialist_model(organ_name):
    """Carrega e retorna (model, class_list, config) para o organ_name."""
    if organ_name not in SPECIALIST_CONFIGS:
        return None, None, None

    if organ_name in SPECIALIST_CACHE:
        return SPECIALIST_CACHE[organ_name]

    cfg = SPECIALIST_CONFIGS[organ_name]
    model_path = cfg['model_path']
    classes_path = cfg['classes_path']

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo especialista não encontrado: {model_path}")
    if not os.path.exists(classes_path):
        raise FileNotFoundError(f"Arquivo de classes não encontrado: {classes_path}")

    # Carrega modelo (compile=False para inferência)
    specialist_model = tf.keras.models.load_model(model_path, compile=False)

    # Carrega classes
    with open(classes_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if isinstance(data, dict) and 'classes' in data:
            class_list = data['classes']
        elif isinstance(data, list):
            class_list = data
        else:
            # tenta extrair valores
            class_list = list(data.values()) if isinstance(data, dict) else []

    SPECIALIST_CACHE[organ_name] = (specialist_model, class_list, cfg)
    return specialist_model, class_list, cfg


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
        
        # Pré-processa a imagem e chama o modelo
        preprocessed = preprocess_image(image, target_size=(150, 150))
        model = load_model_if_needed()
        preds = model.predict(preprocessed)[0]

        # Interpreta resultado
        best_idx = int(np.argmax(preds))
        confidence = float(np.max(preds))
        if best_idx < len(CLASSES):
            predicted_class = CLASSES[best_idx]
        else:
            predicted_class = 'unknown'

        # Probabilidades por classe (percentual)
        probabilities = {cls: float(p) for cls, p in zip(CLASSES, preds)}

        width, height = image.size

        # Monta resposta inicial com resultado do classificador de órgãos
        response = {
            'organ_classifier': {
                'examType': 'Identificacao de Orgao',
                'diagnosis': predicted_class,
                'confidence': confidence * 100.0,
                'probabilities': probabilities
            },
            'image_width': width,
            'image_height': height
        }

        # Se tivermos um modelo especialista para esse órgão, carregue e rode a predição especializada
        try:
            specialist_model, class_list, cfg = load_specialist_model(predicted_class)
            if specialist_model is not None and class_list:
                # Pré-processa conforme input shape do especialista
                target = cfg.get('input_shape', (150, 150, 3))
                preproc_spec = preprocess_image(image, target_size=(target[0], target[1]))
                preds_spec = specialist_model.predict(preproc_spec)[0]
                idx_spec = int(np.argmax(preds_spec))
                conf_spec = float(np.max(preds_spec))
                pred_class_name = class_list[idx_spec] if idx_spec < len(class_list) else 'unknown'

                # Tradução amigável do diagnóstico (se disponível)
                translation_map = cfg.get('translation_map', {})
                friendly = translation_map.get(pred_class_name, pred_class_name)

                response['specialist'] = {
                    'examType': cfg.get('exam_name', 'Especialista'),
                    'predicted_class': pred_class_name,
                    'diagnosis': friendly,
                    'confidence': conf_spec * 100.0,
                    'probabilities': {cls: float(p) for cls, p in zip(class_list, preds_spec)}
                }
        except FileNotFoundError as fnf:
            # modelo especialista não disponível — apenas retornamos o classificador de órgãos
            print(f"Aviso: especialista não disponível: {fnf}")
        except Exception as ex:
            # se ocorrer erro no especialista, log e retornamos análise do classificador
            print(f"Erro ao executar modelo especialista: {ex}")

        return jsonify(response), 200
        
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
