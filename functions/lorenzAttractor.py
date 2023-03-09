
import textwrap
class LorenzAttractor:
    def __init__(self, x: float, y: float, z: float, a: float, b: float, c: float, key: str):
        self.x = x
        self.y = y
        self.z = z
        self.a = a
        self.b = b
        self.c = c
        self.key = key

    def calculate_next_values(self, t: float) -> tuple[float, float, float]:
        x, y, z = self.x, self.y, self.z
        x_dot = -self.a * (x - y)
        y_dot = self.c * x - y - x * z
        z_dot = -self.b * z + x * y

        self.x = x + x_dot * t
        self.y = y + y_dot * t
        self.z = z + z_dot * t

        return self.x, self.y, self.z

    def _get_key_dict(self) -> dict[str, str]:
        key_bin = bin(int(self.key, 16))[2:].zfill(256)
        key_dict = {}
        key_32_parts = [key_bin[i:i+8] for i in range(0, 256, 8)]
        for i, key_part in enumerate(key_32_parts):
            key_dict[f'k{i+1}'] = key_part
        return key_dict

    def update_lorentz(self):
        t1, t2, t3 = 0, 0, 0
        key_dict = self._get_key_dict()
        for i in range(1, 12):
            t1 ^= int(key_dict[f'k{i}'], 2)
        for i in range(12, 23):
            t2 ^= int(key_dict[f'k{i}'], 2)
        for i in range(23, 33):
            t3 ^= int(key_dict[f'k{i}'], 2) 
        x0=x0 + t1/256            
        y0=y0 + t2/256            
        z0=z0 + t3/256
        return x0, y0, z0