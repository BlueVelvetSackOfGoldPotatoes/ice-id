import numpy as np
import pandas as pd

df = np.array(pd.read_csv("./people_sorted.csv", low_memory=False))
first_row = ["id", "heimild", "nafn_norm", "first_name", "middle_name", "patronym", "surname", "birthyear",
             "sex", "status", "marriagestatus", "person", "partner", "father", "mother", "source_partner",
             "source_father", "source_mother", "source_farm", "farm", "county", "parish", "district"]
df_train = []
df_test = []
for each in df:
    if each[1] <= 1899:
        df_train.append(each)
    else:
        df_test.append(each)
df_train.sort(key=lambda x: x[11])
df_test.sort(key=lambda x: x[11])
df_train = [first_row] + df_train
df_test = [first_row] + df_test
pd.DataFrame(np.row_stack(df_train)).to_csv("../people_train.csv", index=False, header=False)
pd.DataFrame(np.row_stack(df_test)).to_csv("../people_test.csv", index=False, header=False)
