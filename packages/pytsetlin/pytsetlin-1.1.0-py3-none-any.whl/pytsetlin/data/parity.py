import numpy as np


def get_parity(n_rows=1000, n_digits=10):


    x = np.random.choice(a = [0, 1], size=(n_rows, n_digits)).astype(np.uint8)

    y = np.sum(x, axis=1, dtype=np.uint32) % 2

    return x, y


if __name__ == "__main__":

    get_parity(n_digits=3, n_rows=2)
