import numpy as np
from perlin_noise import PerlinNoise


def gen_seed():
    return np.random.randint(10000, 1000000)

def gen_perlin(x, y, seed):
    noise = PerlinNoise(octaves=3, seed=seed)

    perlin = np.array([[noise([i/x, j/y]) for j in range(x)] for i in range(y)])
    mn, mx = np.min(perlin), np.max(perlin)

    return (perlin - mn) / (mx - mn)

def gen_base(x, y):
    def inbounds(a, b, h, k, px, py):
        return  ((((px - h) ** 2) / a) + (((py - k) ** 2) / b)) <= 1.3

    h, k = x // 2, y // 2
    a, b = (h - 3) ** 2, (k - 3) ** 2
    return np.array([[inbounds(a, b, h, k, px, py) for px in range(x)] for py in range(y)]).astype(int)
            
def gen_world(x, y, seed, land_prob = 0.4):
    return np.multiply(gen_base(x, y), gen_perlin(x, y, seed) > land_prob)

seed = gen_seed()
world = gen_world(48, 32, seed)

with open("world.txt", "w+") as f:
    for row in world:
        f.write("".join("X" if x else " " for x in row) + "\n")