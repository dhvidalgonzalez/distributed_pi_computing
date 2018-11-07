import random as r
import math as m
#import _thread
import requests


def aproximation_pi(n_points):
  # Number of darts that land inside.
  inside = 0

  # Iterate for the number of darts.
  i = 0
  while i < n_points:
    # Generate random x, y in [0, 1].
    x2 = r.random()**2
    y2 = r.random()**2
    # Increment if inside unit circle.
    if m.sqrt(x2 + y2) < 1.0:
      inside += 1
    i += 1

  # It works!
  return float(inside)

def integration_exp(n, a, b):

  sum = 0.0
  for i in range(n):
    x = -a + (a + b)*r.random()
    sum += (x*m.exp(x))
  
  return sum/float(n)


def parallel_work(route):
  value = requests.get(route).content
  return value