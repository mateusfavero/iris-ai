import requests
from PIL import Image
import io
import sys

TEST_IMAGE = 'test_image.jpg'
URLS = [
    'http://127.0.0.1:5000/analyze',
    'http://localhost:5000/analyze'
]

# Create a small red test image
img = Image.new('RGB', (64, 64), color=(255, 0, 0))
img.save(TEST_IMAGE, 'JPEG')
print(f'Created test image: {TEST_IMAGE}')

for url in URLS:
    try:
        print(f'Posting to {url} ...')
        with open(TEST_IMAGE, 'rb') as f:
            files = {'image': f}
            r = requests.post(url, files=files, timeout=10)
        print('Status code:', r.status_code)
        try:
            print('JSON response:', r.json())
        except Exception:
            print('Text response:', r.text)
        break
    except requests.exceptions.RequestException as e:
        print(f'Failed to POST to {url}:', e)
else:
    print('All POST attempts failed. Is the Flask server running?')
    sys.exit(1)
