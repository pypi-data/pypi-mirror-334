    
from sklearn.datasets import fetch_openml
import numpy as np



def get_mnist():


    X, y = fetch_openml('mnist_784', version=1, return_X_y=True, as_frame=False)

    X = np.where(X.reshape((X.shape[0], 28 * 28)) > 75, 1, 0).astype(np.uint8)

    y = y.astype(np.uint32)

    x_train, x_test = X[:60000], X[60000:]
    y_train, y_test = y[:60000], y[60000:]


    return x_train, x_test, y_train, y_test



if __name__ == "__main__":

    X_train, X_test, y_train, y_test = get_mnist()

