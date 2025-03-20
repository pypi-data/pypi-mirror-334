import numpy as np


def get_xor(n_rows=1000, 
            number_features=6, 
            noise_fraction=0.3, 
            seed=42):
    
    rng = np.random.default_rng(seed)
    X = rng.integers(0, 2, size=(n_rows, number_features))
    y = np.logical_xor(X[:, 0:1], X[:, 1:2])
    flips = rng.random((n_rows, 1)) < noise_fraction
    y = np.logical_xor(y, flips)
   
    y = y*1

    return X.astype(np.uint8), y.reshape(y.shape[0]).astype(np.uint32)


if __name__ == "__main__":

    x, y = get_xor()
