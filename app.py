from flask import Flask, render_template, request, jsonify
from elliptic_curve import ECC, RSA
import random
import os
import sys

app = Flask(__name__)

# Конфигурация для PythonAnywhere
if __name__ == '__main__':
    # Локальная разработка
    DEBUG = True
else:
    # Продакшен на PythonAnywhere
    DEBUG = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ecc')
def ecc():
    return render_template('ecc.html')


@app.route('/rsa')
def rsa():
    return render_template('rsa.html')


# API endpoints для ECC
@app.route('/api/ecc/generate_keys', methods=['POST'])
def generate_ecc_keys():
    try:
        ecc = ECC()
        private_key, public_key = ecc.generate_keypair()

        # Получаем все точки кривой для визуализации
        curve_points = ecc.get_curve_points()

        return jsonify({
            'success': True,
            'private_key': private_key,
            'public_key': public_key,
            'curve_points': curve_points,
            'generator': ecc.G,
            'curve_params': {
                'a': ecc.curve.a,
                'b': ecc.curve.b,
                'p': ecc.curve.p,
                'equation': f"y² = x³ + {ecc.curve.a}x + {ecc.curve.b} mod {ecc.curve.p}"
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/ecc/encrypt', methods=['POST'])
def ecc_encrypt():
    try:
        data = request.json
        ecc = ECC()

        public_key = tuple(data['public_key'])
        message = int(data['message'])

        C1, C2 = ecc.encrypt(public_key, message)

        # Получаем точки для визуализации
        k = random.randint(1, ecc.n - 1)
        intermediate_points = ecc.get_encryption_points(public_key, message, k)

        return jsonify({
            'success': True,
            'C1': C1,
            'C2': C2,
            'intermediate_points': intermediate_points,
            'message_point': (message, (message ** 3 + 7) % 17)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/ecc/decrypt', methods=['POST'])
def ecc_decrypt():
    try:
        data = request.json
        ecc = ECC()

        private_key = int(data['private_key'])
        C1 = tuple(data['C1'])
        C2 = tuple(data['C2'])

        decrypted = ecc.decrypt(private_key, C1, C2)

        return jsonify({
            'success': True,
            'decrypted': decrypted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/ecc/get_curve', methods=['POST'])
def get_curve():
    """Возвращает точки эллиптической кривой"""
    try:
        ecc = ECC()
        curve_points = ecc.get_curve_points()

        return jsonify({
            'success': True,
            'curve_points': curve_points,
            'generator': ecc.G,
            'curve_params': {
                'a': ecc.curve.a,
                'b': ecc.curve.b,
                'p': ecc.curve.p,
                'equation': f"y² = x³ + {ecc.curve.a}x + {ecc.curve.b} mod {ecc.curve.p}"
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/ecc/add_points', methods=['POST'])
def add_points():
    """Сложение двух точек на кривой"""
    try:
        data = request.json
        ecc = ECC()

        point1 = tuple(data['point1'])
        point2 = tuple(data['point2'])

        result = ecc.add_points(point1, point2)

        return jsonify({
            'success': True,
            'point1': point1,
            'point2': point2,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/ecc/double_point', methods=['POST'])
def double_point():
    """Удвоение точки на кривой"""
    try:
        data = request.json
        ecc = ECC()

        point = tuple(data['point'])
        result = ecc.double_point(point)

        return jsonify({
            'success': True,
            'point': point,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/ecc/multiply_point', methods=['POST'])
def multiply_point():
    """Умножение точки на скаляр"""
    try:
        data = request.json
        ecc = ECC()

        k = int(data['k'])
        point = tuple(data['point'])
        result = ecc.multiply_point(k, point)

        return jsonify({
            'success': True,
            'k': k,
            'point': point,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# API endpoints для RSA
@app.route('/api/rsa/generate_keys', methods=['POST'])
def generate_rsa_keys():
    try:
        public_key, private_key = RSA.generate_keys()

        return jsonify({
            'success': True,
            'public_key': public_key,
            'private_key': private_key
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/rsa/encrypt', methods=['POST'])
def rsa_encrypt():
    try:
        data = request.json
        message = int(data['message'])
        public_key = tuple(data['public_key'])

        encrypted = RSA.encrypt(message, public_key)

        return jsonify({
            'success': True,
            'encrypted': encrypted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/rsa/decrypt', methods=['POST'])
def rsa_decrypt():
    try:
        data = request.json
        ciphertext = int(data['ciphertext'])
        private_key = tuple(data['private_key'])

        decrypted = RSA.decrypt(ciphertext, private_key)

        return jsonify({
            'success': True,
            'decrypted': decrypted
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


# Обработчики ошибок
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Страница не найдена'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Внутренняя ошибка сервера'
    }), 500


# Health check для мониторинга
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'Crypto Lab',
        'version': '1.0.0'
    })


# Информация о API
@app.route('/api/info')
def api_info():
    return jsonify({
        'name': 'Crypto Lab API',
        'version': '1.0.0',
        'endpoints': {
            'ECC': {
                'generate_keys': '/api/ecc/generate_keys',
                'encrypt': '/api/ecc/encrypt',
                'decrypt': '/api/ecc/decrypt',
                'get_curve': '/api/ecc/get_curve',
                'add_points': '/api/ecc/add_points',
                'double_point': '/api/ecc/double_point',
                'multiply_point': '/api/ecc/multiply_point'
            },
            'RSA': {
                'generate_keys': '/api/rsa/generate_keys',
                'encrypt': '/api/rsa/encrypt',
                'decrypt': '/api/rsa/decrypt'
            }
        }
    })


if __name__ == '__main__':
    # Определяем хост и порт для разных сред
    if DEBUG:
        # Локальная разработка
        host = '0.0.0.0'
        port = 5000
        print("🚀 Запуск в режиме разработки...")
        print("📧 Сайт доступен по адресу: http://localhost:5000")
    else:
        # PythonAnywhere
        host = '0.0.0.0'
        port = int(os.environ.get('PORT', 5000))
        print("🌐 Запуск в продакшен режиме...")

    app.run(
        host=host,
        port=port,
        debug=DEBUG,
        # Отключаем reloader на PythonAnywhere для избежания конфликтов
        use_reloader=DEBUG
    )
else:
    # Это для PythonAnywhere - выводим информацию о запуске
    print("🌐 Crypto Lab запущен на PythonAnywhere")
    print("📧 Приложение готово к работе")