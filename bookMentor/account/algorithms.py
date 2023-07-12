import pandas as pd
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import coo_matrix
from account.models import Profile
from books.models import Book


def change_values(tags, coeff):
    for key in tags.keys():
        tags[key] = tags[key] * (coeff / 5.)
    return tags


def remove_bad(tags, df):
    for key in list(tags.keys()):
        if key not in df.columns.tolist():
            del tags[key]
    return tags


def update_csv(csv_path, profile, tags, coeff=5.):
    df = pd.read_csv(csv_path)
    tags = remove_bad(tags, df)
    tags = change_values(tags, coeff)
    if len(df.loc[df['profile'] == profile]) == 0:
        tags.update({'profile': profile})
        df.loc[len(df.index)] = tags
        df.fillna(value=0., inplace=True)
    else:
        for key in tags.keys():
            df.loc[df['profile'] == profile, key] += tags.get(key)

    # print(df)
    df.to_csv(csv_path, index=False)


def get_coefficients_from_df(csv_path, profile):
    df = pd.read_csv(csv_path)
    if len(df.loc[df['profile'] == profile]) == 0:
        return None
    ret = df.loc[df['profile'] == profile].to_dict()
    del ret['profile']
    for key in ret.keys():
        ret[key] = ret.get(key).get(df.loc[df['profile'] == profile].index[0])
    return ret


def normalize(x):
    x = x.astype(float)
    x_sum = x.sum()
    x_num = x.astype(bool).sum()
    x_mean = x_sum / x_num

    if x_num == 1 or x.std() == 0:
        return 0.0
    return (x - x_mean) / (x.max() - x.min())


def build(ratings, userID, save=True):
    ratings_normalized = ratings.apply(normalize, axis=1)

    cor = cosine_similarity(ratings_normalized, dense_output=False)

    index_values = ratings.index.values.tolist()
    # print(index_values)

    ID = index_values.index(userID)
    user_row = cor[ID]

    # print(user_row)

    def get_n_max_indexes(arr, N):
        indexes = sorted(range(len(arr)), key=lambda i: arr[i], reverse=True)[:N]
        return indexes

    N = int(len(user_row) * 0.9)  # top 30% of most similar users
    top_similar_users_rows = get_n_max_indexes(user_row, N)
    top_similar_users_id = []
    for index in top_similar_users_rows:
        top_similar_users_id.append(index_values[index])

    # print(top_similar_users_rows)
    # print(top_similar_users_id)

    candidate_books = {}

    profiles = Profile.objects.all()
    for i in range(1, len(top_similar_users_id)):
        for profile in profiles.all():
            id_slicnog = top_similar_users_id[i]
            if profile.pk == id_slicnog:
                for book in profile.books.all():
                    if book in candidate_books:
                        candidate_books[book] += 1.2
                    else:
                        candidate_books[book] = 1.2

    return candidate_books


def get_books_from_dict(dict):
    i = 0
    titles = []
    for book_object in dict.keys():
        if i == 15:
            break
        titles.append(book_object.title)
        i = i + 1
    return Book.objects.all().filter(title__in=titles)


def get_most_popular_books_by_topics(features):
    # books_by_topics = Book.objects.all().filter(topic__in=features).order_by('-popularity')
    # return books_by_topics
    books = []
    for feature in features:
        instances = Book.objects.all().filter(topic=feature).order_by('-popularity')
        if len(instances) < 3:
            cnt = len(instances)
        else:
            cnt = 3
        instances = instances[:cnt]
        for book in instances:
            books.append(book)
    return books


def description_rec(ratings, userID, candidate_books, save=True):
    user_ratings = ratings.loc[userID]  # ratings je u stvari red za usera
    user_grades = user_ratings.values

    N = int(len(user_ratings) * 0.1)  # top 10% feature book
    top_indices = np.argsort(user_grades)[::-1][:N]

    top_features = list(ratings.columns[top_indices])

    books = get_most_popular_books_by_topics(top_features)
    for book in books:
        if book in candidate_books:
            candidate_books[book] += 1
        else:
            candidate_books[book] = 1
