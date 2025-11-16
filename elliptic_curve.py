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

        try:
            s = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
            x3 = (s * s - x1 - x2) % self.p
            y3 = (s * (x1 - x3) - y1) % self.p
        except:
            return None

        return (x3, y3)

    def point_double(self, P):
        if P is None:
            return None

        x, y = P

        try:
            s = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
            x3 = (s * s - 2 * x) % self.p
            y3 = (s * (x - x3) - y) % self.p
        except:
            return None

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
            rhs = (x * x * x + self.a * x + self.b) % self.p
            for y in range(self.p):
                if (y * y) % self.p == rhs:
                    points.append((x, y))
        return points


class ECC:
    def __init__(self, a=0, b=7, p=17, G=(15, 13)):
        self.curve = EllipticCurve(a, b, p)
        self.G = G
        self.n = 19  # Порядок группы (для примера)

    def generate_keypair(self):
        private_key = random.randint(1, self.n - 1)
        public_key = self.curve.scalar_mult(private_key, self.G)
        return private_key, public_key

    def encrypt(self, public_key, message):
        k = random.randint(1, self.n - 1)
        C1 = self.curve.scalar_mult(k, self.G)
        C2 = self.curve.scalar_mult(k, public_key)
        return C1, C2

    def decrypt(self, private_key, C1, C2):
        S = self.curve.scalar_mult(private_key, C1)
        message_point = self.curve.point_add(C2, self.curve.point_neg(S))
        return message_point