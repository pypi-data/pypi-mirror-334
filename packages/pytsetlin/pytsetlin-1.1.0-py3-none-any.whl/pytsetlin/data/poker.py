from ucimlrepo import fetch_ucirepo 
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from sklearn.utils import resample
from sklearn.metrics import classification_report
from time import perf_counter
from tqdm import tqdm

def get_poker(train_size=0.8, test_size=0.2, verbose=False, seed=42, selected_labels=None):

    poker_hand = fetch_ucirepo(id=158) 
    
    df_x = poker_hand.data.features 
    df_y = poker_hand.data.targets['CLASS'].to_numpy(dtype=np.uint32)  

    s_cols = [col for col in df_x.columns if col.startswith('S')]
    c_cols = [col for col in df_x.columns if col.startswith('C')]

    s_encoder = OneHotEncoder(sparse_output=False)
    c_encoder = OneHotEncoder(sparse_output=False)

    s_binary = pd.DataFrame(
        s_encoder.fit_transform(df_x[s_cols]),
        columns=[f"{col}_{i}" for col in s_cols for i in range(1, 5)],
        index=df_x.index
    )

    c_binary = pd.DataFrame(
        c_encoder.fit_transform(df_x[c_cols]),
        columns=[f"{col}_{i}" for col in c_cols for i in range(1, 14)],
        index=df_x.index
    )

    binary_df_x = pd.concat([s_binary, c_binary], axis=1).to_numpy(dtype=np.uint8)


    if selected_labels is not None:
        mask = np.isin(df_y, selected_labels)
        binary_df_x = binary_df_x[mask]
        df_y = df_y[mask]
        
        label_map = {label: i for i, label in enumerate(sorted(np.unique(df_y)))}
        df_y = np.array([label_map[y] for y in df_y], dtype=np.uint32)

    x_train, x_test, y_train, y_test = train_test_split(binary_df_x, df_y, train_size=train_size, test_size=test_size, random_state=seed)

    if verbose:

        unique_values, counts = np.unique(y_test, return_counts=True)
        percentages = (counts / len(y_test)) * 100

        for value, percentage, count in zip(unique_values, percentages, counts):
            print(f"Class {value}: {percentage:.2f}% ({count})")

    return x_train, y_train, x_test, y_test


def get_match_statistics(large_set, small_set):
    
    match_count = 0
    for small_arr in tqdm(small_set, total=len(small_set)):
        if np.any(np.all(large_set == small_arr, axis=1)):
            match_count += 1
    
    percentage = (match_count / len(small_set)) * 100

    return {
        'total_matches': match_count,
        'percentage': percentage,
        'total_compared': len(small_set)
    }



def downsample_data(X, y, verbose=False):


    unique_classes, class_counts = np.unique(y, return_counts=True)
    
    min_count = np.min(class_counts)
    
    downsampled_X = []
    downsampled_y = []
    
    for cls in unique_classes:
        X_class = X[y == cls]
        y_class = y[y == cls]
        
        X_downsampled, y_downsampled = resample(
            X_class, 
            y_class, 
            replace=False,  # Sample without replacement
            n_samples=min_count, 
            random_state=42  # For reproducibility
        )
        
        downsampled_X.append(X_downsampled)
        downsampled_y.append(y_downsampled)
    
    X_balanced = np.vstack(downsampled_X, dtype=np.uint8)
    y_balanced = np.concatenate(downsampled_y, dtype=np.uint32)
    
    if verbose:

        unique_values, counts = np.unique(y_balanced, return_counts=True)
        percentages = (counts / len(y_balanced)) * 100

        for value, percentage, count in zip(unique_values, percentages, counts):
            print(f"Class {value}: {percentage:.2f}% ({count})")


    return X_balanced, y_balanced



if __name__ == "__main__":

    st = perf_counter()
    x_train, y_train, x_test, y_test = get_poker(train_size=10000, selected_labels=[0, 1])
    et = perf_counter()
    print(et - st)
    st = perf_counter()
    x_train, y_train = downsample_data(x_train, y_train, verbose=False)
    et = perf_counter()
    print(et - st)

    st = perf_counter()
    stats = get_match_statistics(x_train, x_test)
    et = perf_counter()
    print(et - st)
    

    print(stats)

    # clf = RandomForestClassifier()
    # clf.fit(x_train, y_train)

    # pred = clf.predict(x_test)

    # print(np.mean(pred == y_test))


    # print(classification_report(y_test, pred))