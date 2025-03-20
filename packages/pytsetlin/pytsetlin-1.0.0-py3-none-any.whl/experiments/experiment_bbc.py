import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.bbc import get_bbc_news

from tsetlin_machine import TsetlinMachine




if __name__ == "__main__":

    x_train, y_train, x_test, y_test = get_bbc_news()

    tm = TsetlinMachine(n_clauses=200,
                        threshold=200,
                        s=2.0,
                        n_literal_budget=5)

    tm.set_train_data(x_train, y_train)

    tm.set_eval_data(x_test, y_test)

    r = tm.train(training_epochs=50)
    
    print(r)


