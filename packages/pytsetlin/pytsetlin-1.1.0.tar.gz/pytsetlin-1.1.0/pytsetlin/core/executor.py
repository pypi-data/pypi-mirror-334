from numba import njit, prange
import numpy as np
from pytsetlin.core.feedback import evaluate_clauses_training, get_update_p, update_clauses, evaluate_clause
from pytsetlin.core import config


@njit
def train_epoch(cb, wb, x, y, threshold, s_min_inv, s_inv, n_outputs, n_literals, n_literal_budget, boost_true_positives):
    

    cb = np.ascontiguousarray(cb)
    wb = np.ascontiguousarray(wb)

    indices = np.arange(x.shape[0], dtype=np.int32) # this does not need to be calulated at every epoch?
    np.random.shuffle(indices)

    clause_outputs = np.ones(cb.shape[0], dtype=np.uint8)
    literals_counts = np.zeros(cb.shape[0], dtype=np.uint32)

    y_hat = np.zeros(y.shape, dtype=np.uint32)

    for indice in indices:
        literals = x[indice]
        target = y[indice]
        
        evaluate_clauses_training(literals, cb, n_literals, clause_outputs, literals_counts)
        
        vote_values = np.dot(wb.astype(np.float32), clause_outputs.astype(np.float32))

        not_target = np.random.randint(0, n_outputs)

        while(not_target == target):
            not_target = np.random.randint(0, n_outputs)

        votes = vote_values[target]

        v_clamped_pos = np.clip(np.array(votes), -threshold, threshold)

        pos_update_p =  (threshold - v_clamped_pos) / (2*threshold)

        votes = vote_values[not_target]

        v_clamped_neg = np.clip(np.array(votes), -threshold, threshold)

        neg_update_p =  (threshold + v_clamped_neg) / (2*threshold)

        update_clauses(cb, wb, clause_outputs, literals_counts, pos_update_p, neg_update_p, target, 
                    not_target, literals, n_literals, n_literal_budget, s_min_inv, s_inv, boost_true_positives)

        y_hat[indice] = np.argmax(vote_values)

    return y_hat


@njit
def classify(x, clause_block, weight_block, n_literals):

    clause_outputs = evaluate_clause(x, clause_block, n_literals)

    class_sums = np.dot(weight_block.astype(np.float32), clause_outputs.astype(np.float32))

    return np.argmax(class_sums)
  
@njit(parallel=config.OPERATE_PARALLEL)
def eval_predict(x, cb, wb, n_literals):
    y_pred = np.zeros(x.shape[0], dtype=np.uint32)
    
    for i in prange(x.shape[0]):
        y_pred[i] = classify(x[i], cb, wb, n_literals)
    
    return y_pred
