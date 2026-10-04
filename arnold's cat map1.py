from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def cat_arnold(image, itera, lenght):
  f = [[1, 0], [0, 1]]
  for i in range(itera):
    f1 = [[(f[0][0] + f[1][0]) % lenght, (f[0][1] + f[1][1]) % lenght], [(f[0][0] + 2 * f[1][0]) % lenght, (f[0][1] + 2 * f[1][1]) % lenght]]
    f = f1
  new_img = np.zeros_like(image)
  for x in range(lenght):
    for y in range(lenght):
      new_img[(f[0][0] * x + f[0][1] * y) % lenght][(f[1][0] * x + f[1][1] * y) % lenght] = image[x][y]
  return new_img

def cat_arnold2(image, itera, lenght):
  f = [[1, 0], [0, 1]]
  for i in range(itera):
    f1 = [[(2 * f[0][0] + f[1][0]) % lenght, (2 * f[0][1] + f[1][1]) % lenght], [(f[0][0] + f[1][0]) % lenght, (f[0][1] + f[1][1]) % lenght]]
    f = f1
  new_img = np.zeros_like(image)
  for x in range(lenght):
    for y in range(lenght):
      new_img[(f[0][0] * x + f[0][1] * y) % lenght][(f[1][0] * x + f[1][1] * y) % lenght] = image[x][y]
  return new_img

def find_period(N, max_iter=1000000):
  """
  Находит период отображения кота Арнольда для размера N.
  Период — минимальное k, при котором A^k ≡ I (mod N).
  """
  A = np.array([[2, 1], [1, 1]]) % N
  M = A.copy()
  period = 1
  while not np.array_equal(M, np.eye(2, dtype=int)):
    M = (M @ A) % N
    period += 1
    if period > max_iter:
      raise RuntimeError(f"Период не найден за {max_iter} итераций")
  return period

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
    return new_arr
  else:
    black_string = np.array([[[0, 0, 0] for j in range(b)] for i in range(b - a)])
    new_arr = np.concatenate([black_string,arr])
    return new_arr

def transform_key(key):
  ans = []
  for i in range(len(key)):
    ans.append(ord(key[i]))
  return ans

def key_reading_for_mixing(period, key):
  ans = period // 2 + ((-1) ** (period // 200)) * ((key + period) % 11)
  return ans

def polyalphabet_cipher(image, key1):
  leni = len(image)
  cou = 0
  l = len(key1)
  for x in range(leni):
    for y in range(leni):
      image[x][y][0] = (image[x][y][0] + key1[cou]) % 256
      image[x][y][1] = (image[x][y][1] + key1[cou]) % 256
      image[x][y][2] = (image[x][y][2] + key1[cou]) % 256
      cou += 1
      cou = (cou % l)
  return image

def polyalphabet_cipher2(image, key1):
  leni = len(image)
  cou = 0
  l = len(key1)
  for x in range(leni):
    for y in range(leni):
      image[x][y][0] = (image[x][y][0] - key1[cou]) % 256
      image[x][y][1] = (image[x][y][1] - key1[cou]) % 256
      image[x][y][2] = (image[x][y][2] - key1[cou]) % 256
      cou += 1
      cou = (cou % l)
  return image

#дешифровка
def decryption_image(imag, k1, k2, k3):
  len_img = len(imag)
  period = find_period(len_img)
  count_mix = key_reading_for_mixing(period, k1)
  k3 = transform_key(k3)
  for i in range(k2):
    imag = cat_arnold2(imag, count_mix, len_img)
    plt.imshow(imag, cmap='gray')   # для 2D
    plt.axis('off')                   # убрать оси
    plt.show()
    imag = polyalphabet_cipher2(imag, k3)
    imag = cat_arnold(imag, count_mix, len_img)
  return imag

#шифруем изображение
def encoding_image(arr, key1, key2, key3):
  lenght_max = max(arr.shape)
  period = find_period(lenght_max)
  count_mix = key_reading_for_mixing(period, key1)
  redacted_key3 = transform_key(key3)
  for _ in range(key2):
    redacted_image = cat_arnold(redacted_image, period - count_mix, lenght_max)
    redacted_image = polyalphabet_cipher(redacted_image, redacted_key3)
    redacted_image = cat_arnold2(redacted_image, period - count_mix, lenght_max)
  return redacted_image