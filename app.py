from flask import Flask, render_template, request, jsonify
from elliptic_curve import EllipticCurve, ECC
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cryptography')
def cryptography():
    return render_template('cryptography.html')


@app.route('/elliptic-curves')
def elliptic_curves():
    return render_template('elliptic_curves.html')


@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')


@app.route('/api/calculate_curve', methods=['POST'])
def calculate_curve():
    try:
        data = request.json
        a = int(data.get('a', 0))
        b = int(data.get('b', 7))
        p = int(data.get('p', 17))

        curve = EllipticCurve(a, b, p)
        points = curve.get_all_points()

        return jsonify({
            'success': True,
            'points': points,
            'equation': f"y² = x³ + {a}x + {b} mod {p}",
            'total_points': len(points)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/calculate_point_operations', methods=['POST'])
def calculate_point_operations():
    try:
        data = request.json
        a = int(data.get('a', 0))
        b = int(data.get('b', 7))
        p = int(data.get('p', 17))

        point1 = tuple(data.get('point1', [0, 0]))
        point2 = tuple(data.get('point2', [0, 0]))
        operation = data.get('operation', 'add')

        curve = EllipticCurve(a, b, p)

        if operation == 'add':
            result = curve.point_add(point1, point2)
        elif operation == 'double':
            result = curve.point_double(point1)
        elif operation == 'multiply':
            k = int(data.get('k', 2))
            result = curve.scalar_mult(k, point1)
        else:
            result = None

        return jsonify({
            'success': True,
            'result': result,
            'operation': operation
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/api/generate_ecc_keys', methods=['POST'])
def generate_ecc_keys():
    try:
        data = request.json
        a = int(data.get('a', 0))
        b = int(data.get('b', 7))
        p = int(data.get('p', 17))
        generator = tuple(data.get('generator', [15, 13]))

        ecc = ECC(a, b, p, generator)
        private_key, public_key = ecc.generate_keypair()

        return jsonify({
            'success': True,
            'private_key': private_key,
            'public_key': public_key
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)