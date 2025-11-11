import random


class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p

    def is_on_curve(self, point):
        if point is None:
            return True
        x, y = point
        return (y * y) % self.p == (x * x * x + self.a * x + self.b) % self.p

    def point_add(self, P1, P2):
        if P1 is None:
            return P2
        if P2 is None:
            return P1

        x1, y1 = P1
        x2, y2 = P2

        if x1 == x2:
            if y1 != y2:
                return None
            else:
                return self.point_double(P1)

        s = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def point_double(self, P):
        if P is None:
            return None

        x, y = P
        s = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
        x3 = (s * s - 2 * x) % self.p
        y3 = (s * (x - x3) - y) % self.p

        return (x3, y3)

    def scalar_mult(self, k, P):
        if k % self.p == 0 or P is None:
            return None

        if k < 0:
            return self.scalar_mult(-k, self.point_neg(P))

        result = None
        addend = P

        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_double(addend)
            k >>= 1

        return result

    def point_neg(self, P):
        if P is None:
            return None
        x, y = P
        return (x, -y % self.p)

    def get_all_points(self):
        """Возвращает все точки на эллиптической кривой"""
        points = []
        for x in range(self.p):
            # Вычисляем правую часть уравнения: x^3 + ax + b
            rhs = (x * x * x + self.a * x + self.b) % self.p

            # Ищем y такие, что y^2 = rhs mod p
            for y in range(self.p):
                if (y * y) % self.p == rhs:
                    points.append((x, y))
        return points


class ECC:
    def __init__(self):
        # Используем кривую y² = x³ + 7 mod 17
        self.curve = EllipticCurve(a=0, b=7, p=17)
        self.G = (15, 13)  # Генераторная точка
        self.n = 19  # Порядок группы

    def generate_keypair(self):
        private_key = random.randint(1, self.n - 1)
        public_key = self.curve.scalar_mult(private_key, self.G)
        return private_key, public_key

    def encrypt(self, public_key, message):
        k = random.randint(1, self.n - 1)
        C1 = self.curve.scalar_mult(k, self.G)
        C2 = self.curve.scalar_mult(k, public_key)
        message_point = (message, (message ** 3 + 7) % 17)
        encrypted = self.curve.point_add(C2, message_point)
        return C1, encrypted

    def decrypt(self, private_key, C1, C2):
        S = self.curve.scalar_mult(private_key, C1)
        message_point = self.curve.point_add(C2, self.curve.point_neg(S))
        return message_point[0] if message_point else None

    def get_curve_points(self):
        """Возвращает все точки эллиптической кривой"""
        return self.curve.get_all_points()

    def get_encryption_points(self, public_key, message, k):
        """Возвращает промежуточные точки для визуализации шифрования"""
        C1 = self.curve.scalar_mult(k, self.G)
        C2_temp = self.curve.scalar_mult(k, public_key)
        message_point = (message, (message ** 3 + 7) % 17)
        C2 = self.curve.point_add(C2_temp, message_point)

        return {
            'kG': C1,
            'kP': C2_temp,
            'message_point': message_point,
            'C1': C1,
            'C2': C2
        }

    def add_points(self, point1, point2):
        """Сложение двух точек на кривой"""
        return self.curve.point_add(point1, point2)

    def double_point(self, point):
        """Удвоение точки на кривой"""
        return self.curve.point_double(point)

    def multiply_point(self, k, point):
        """Умножение точки на скаляр"""
        return self.curve.scalar_mult(k, point)


class RSA:
    @staticmethod
    def generate_keys(bits=64):
        p = RSA.generate_prime(bits // 2)
        q = RSA.generate_prime(bits // 2)
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 65537
        d = pow(e, -1, phi)

        return (e, n), (d, n)

    @staticmethod
    def generate_prime(bits):
        while True:
            num = random.getrandbits(bits)
            if num > 1 and RSA.is_prime(num):
                return num

    @staticmethod
    def is_prime(n, k=5):
        if n < 2:
            return False
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
            if n % p == 0:
                return n == p

        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    @staticmethod
    def encrypt(message, public_key):
        e, n = public_key
        return pow(message, e, n)

    @staticmethod
    def decrypt(ciphertext, private_key):
        d, n = private_key
        return pow(ciphertext, d, n)