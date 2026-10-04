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