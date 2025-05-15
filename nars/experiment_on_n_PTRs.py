import random

import matplotlib.pyplot as plt
import numpy as np
import pandas
from tqdm import tqdm

from Config import train_scope, print_step_results, p_pool_size, test_epoch
from Utils import match, Pattern_pool

# training stage
# ======================================================================================================================

F1s = []

for n_PTRs in np.linspace(10, 100, 5):

    n_PTRs = int(n_PTRs)

    p_pool = Pattern_pool(p_pool_size)
    df = np.array(pandas.read_csv("./people_train.csv", low_memory=False))
    for i, r1 in tqdm(enumerate(df)):
        if random.random() < 1 / 10000:
            for j in range(i + 1, i + 1 + int(train_scope)):
                if j >= len(df):
                    continue
                r2 = df[j]
                score = match(r1, r2, p_pool, n_PTRs)
                if print_step_results:
                    print(score, "|", 1 if r1[11] == r2[11] else 0)

    # testing stage
    # ======================================================================================================================

    df = np.array(pandas.read_csv("./people_test.csv", low_memory=False))
    id_under_test = random.sample([each for each in list(set(df[:, 11])) if not np.isnan(each)], test_epoch)
    tmp = []
    for each in df:
        if each[11] in id_under_test:
            tmp.append(each)
    df = np.row_stack(tmp)

    scores = np.ones([test_epoch, test_epoch])
    label = np.ones([test_epoch, test_epoch])
    for i in tqdm(range(test_epoch)):
        r1 = df[i, :]
        for j in range(test_epoch):
            if i == j: continue
            r2 = df[j, :]
            tmp = match(r1, r2, p_pool, n_PTRs, True)
            scores[i, j] = tmp
            label[i, j] = 1 if r1[11] == r2[11] else 0

    F1 = []
    for offset in np.linspace(0, 0.5, 101):

        TP, FP, TN, FN = 0, 0, 0, 0
        for i in range(scores.shape[0]):
            for j in range(scores.shape[1]):
                if label[i, j] == 1:
                    if scores[i, j] > 0.5 + offset:
                        TP += 1
                    else:
                        FN += 1
                else:
                    if scores[i, j] < 0.5 - offset:
                        TN += 1
                    else:
                        FP += 1

        print([TP, FP], [FN, TN])
        recall = TP / (TP + FN + 1e-5)
        print(f"recall: {recall}")
        precision = TP / (TP + FP + 1e-5)
        print(f"precision: {precision}")
        f1 = 2 * recall * precision / (recall + precision + 1e-5)
        print(f"F1: {f1}")
        F1.append(f1)

    F1s.append(F1)

plt.figure()
plt.grid()
plt.xlabel("threshold")
plt.ylabel("F1")
for i, each in enumerate(F1s):
    plt.plot(np.linspace(0, 0.5, 101), each, label=f"num PTRs = {int(np.linspace(10, 100, 5)[i])}")
plt.legend()
plt.show()
