from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


class ArnoldCipher:
    def __init__(self, image, key1, key2, key3):
        # --- данные объекта ---
        self.image = image
        self.size = max(image.shape[:2])
        self.key1 = int(key1)
        self.key2 = int(key2)
        self.key3 = key3

        # --- производные данные, которые считаем один раз ---
        self.period = self.find_period(self.size)
        self.mix_count = self.key_reading_for_mixing(self.period, self.key1)
        self.cipher_key = self.transform_key(self.key3)

    # ---------- вспомогательные "методы" ----------
    @staticmethod
    def find_period(N, max_iter=1_000_000):
        A = np.array([[2, 1], [1, 1]]) % N
        M = A.copy()
        period = 1
        while not np.array_equal(M, np.eye(2, dtype=int)):
            M = (M @ A) % N
            period += 1
            if period > max_iter:
                raise RuntimeError("Период не найден")
        return period

    @staticmethod
    def transform_key(key):
        return [ord(c) for c in key]

    @staticmethod
    def key_reading_for_mixing(period, key):
        return period // 2 + ((-1) ** (period // 200)) * ((key + period) % 11)

    @staticmethod
    def cat_arnold(image, itera, length):
        f = [[1, 0], [0, 1]]
        for _ in range(itera):
            f = [
                [(f[0][0] + f[1][0]) % length, (f[0][1] + f[1][1]) % length],
                [(f[0][0] + 2 * f[1][0]) % length, (f[0][1] + 2 * f[1][1]) % length],
            ]
        new_img = np.zeros_like(image)
        for x in range(length):
            for y in range(length):
                new_img[(f[0][0] * x + f[0][1] * y) % length][(f[1][0] * x + f[1][1] * y) % length] = image[x][y]
        return new_img

    @staticmethod
    def cat_arnold2(image, itera, length):
        f = [[1, 0], [0, 1]]
        for _ in range(itera):
            f = [
                [(2 * f[0][0] + f[1][0]) % length, (2 * f[0][1] + f[1][1]) % length],
                [(f[0][0] + f[1][0]) % length, (f[0][1] + f[1][1]) % length],
            ]
        new_img = np.zeros_like(image)
        for x in range(length):
            for y in range(length):
                new_img[(f[0][0] * x + f[0][1] * y) % length][(f[1][0] * x + f[1][1] * y) % length] = image[x][y]
        return new_img

    def poly_plus(self, image):
        l = len(self.cipher_key)
        cou = 0
        for x in range(len(image)):
            for y in range(len(image)):
                for ch in range(3):
                    image[x][y][ch] = (image[x][y][ch] + self.cipher_key[cou]) % 256
                cou = (cou + 1) % l
        return image

    def poly_minus(self, image):
        l = len(self.cipher_key)
        cou = 0
        for x in range(len(image)):
            for y in range(len(image)):
                for ch in range(3):
                    image[x][y][ch] = (image[x][y][ch] - self.cipher_key[cou]) % 256
                cou = (cou + 1) % l
        return image

    # ---------- "публичные" действия ----------
    def encoding_image(self):
        img = self.image.copy()
        for _ in range(self.key2):
            img = self.cat_arnold(img, self.period - self.mix_count, self.size)
            img = self.poly_plus(img)
            img = self.cat_arnold2(img, self.period - self.mix_count, self.size)
        return img

    def decoding_image(self):
        img = self.image.copy()
        for _ in range(self.key2):
            img = self.cat_arnold2(img, self.mix_count, self.size)
            img = self.poly_minus(img)
            img = self.cat_arnold(img, self.mix_count, self.size)
        return img
def to_square(arr):
    q = arr.shape
    a = q[0]
    b = q[1]
    if a == b:
        return arr
    elif a > b:
        black_column = np.array([[0, 0, 0] for i in range(a - b)])
        new_arr = []
        for i in range(a):
            new_arr.append(np.concatenate([black_column, arr[i]]))
        return np.array(new_arr)   # <-- тут был список, поправил
    else:
        black_string = np.array([[[0, 0, 0] for j in range(b)] for i in range(b - a)])
        new_arr = np.concatenate([black_string, arr])
        return new_arr

img = Image.open('q.jpg')
arr = np.array(img)

redacted_image = to_square(arr)
plt.imshow(redacted_image, cmap='gray')
plt.axis('off')
plt.show()

print("что вы хотите сделать:")
target = input("введите цифру(1-шифровка, 2-дешифровка):")
while target != "1" and target != "2":   # <-- было 'or', из-за чего цикл всегда срабатывал
    print("ошибка")
    target = input("введите цифру(1-шифровка, 2-дешифровка):")

key1 = input("Введите ключ шифрования 1 (число):")
while not key1.isdigit():
    print("error")
    key1 = input("Введите ключ шифрования 1 (число):")

while True:
    keyp = input("Введите ключ шифрования 2 (число <= 30):")
    try:
        key2 = int(keyp)
    except ValueError:
        print("error")
        continue
    if key2 > 30:
        print("Число должно быть меньше 30.")
        continue
    break

key3 = input("Введите ключ шифрования 3 (пароль):").replace(" ", "")

# создаём ОБЪЕКТ — конкретный шифровальщик для этой картинки и этих ключей
cipher = ArnoldCipher(redacted_image, key1, key2, key3)

match target:
    case "1":
        result = cipher.encoding_image()
    case "2":
        result = cipher.decoding_image()

plt.imshow(result, cmap='gray')
plt.axis('off')
plt.show()