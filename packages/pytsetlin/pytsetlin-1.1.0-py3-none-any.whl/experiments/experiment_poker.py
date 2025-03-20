import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pytsetlin.data.poker import get_poker, downsample_data
from pytsetlin import TsetlinMachine




if __name__ == "__main__":

    x_train, y_train, x_test, y_test = get_poker(selected_labels=[0, 1, 2, 3])
    x_train, y_train = downsample_data(x_train, y_train, verbose=True)

    tm = TsetlinMachine(n_clauses=1000,
                        threshold=9650,
                        s=2.5, 
                        n_threads=6)
                                
    tm.set_train_data(x_train, y_train)

    tm.set_eval_data(x_test, y_test)

    r = tm.train(training_epochs=1000)
    
    print(r)


