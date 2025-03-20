import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytsetlin.data.parity import get_parity
from pytsetlin import TsetlinMachine






if __name__ == "__main__":

    x, y = get_parity(n_rows = 1000)
    xt, yt = get_parity(n_rows = 200)


    tm = TsetlinMachine(n_clauses=100,
                        threshold=200,
                        s=2.0)

    tm.set_train_data(x, y)

    tm.set_eval_data(xt, yt)

    tm.train(training_epochs=100)


