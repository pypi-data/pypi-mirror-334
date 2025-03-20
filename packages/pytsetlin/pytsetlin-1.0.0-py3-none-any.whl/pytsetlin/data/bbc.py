
import datasets
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
import numpy as np
from sklearn.utils import shuffle



def get_bbc_news(train_size=None, test_size=None, seed=42, max_features=20000, features=1000, max_df=0.80, min_df=3, ngram_range_max=3):

    imdb = datasets.load_dataset('SetFit/bbc-news')
    x_train, y_train, x_test, y_test = imdb['train']['text'], imdb['train']['label'], imdb['test']['text'], imdb['test']['label']


    if train_size:
        x_train, y_train = shuffle(x_train, y_train, n_samples=train_size, random_state=seed)
    if test_size:
        x_test, y_test = shuffle(x_test, y_test, n_samples=test_size, random_state=seed)

    vectorizer = CountVectorizer(
        analyzer = 'word',
        binary=True,
        ngram_range=(1, ngram_range_max),
        max_features=max_features,
        max_df=max_df,
        min_df=min_df,
    )


    x_train = vectorizer.fit_transform(x_train).toarray().astype(np.uint8)
    y_train = np.array(y_train).astype(np.uint32)
    x_test = vectorizer.transform(x_test).toarray().astype(np.uint8)
    y_test = np.array(y_test).astype(np.uint32)

    
    SKB = SelectKBest(score_func=chi2, k=features)
    SKB.fit(x_train, y_train)

    x_train = SKB.transform(x_train)
    x_test = SKB.transform(x_test)

    return x_train, y_train, x_test, y_test


if __name__ == "__main__":


    get_bbc_news()