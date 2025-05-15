# Data

First, you should generate the data. Put `people.csv` under the main directory. Then you need the following command to generate `people_train.csv` and `people_test.csv`.

```
$ python preprocessing.py
```

`people_test.csv` and `people_train.csv` are from `people.csv` you shared, in which the data is sorted with the census year. The testing data is from 1899, and the training data is to 1899.

I did not use all data samples in each file, that is too much. I chose to use a proportion of the training data (from 1/1000 to 1/10000). There are some details on how the data is used, please refer to my writing. As well, I did not use all the testing data, but I chose 1000 people randomly and use all the corresponding census records. You can also find the details in my writing.

# Usage

```angular2html
$ python experiment_on_n_PTRs.py
$ python experiment_on_train_scope.py
$ python experiment_on_train_size.py
```

To test the method, I chose to change the training data (on the scope and size, refer to my writing), as well as how the patterns are used (on the number of patterns_to_reference, PTRs).

The method will use the expectation of NAL truth-values to judge whether two rows are from the same individual, thus a threshold is needed to change the continuous value to a binary judgment. I chose to change the threshold while give the F1 in different situations to show the reliability.
