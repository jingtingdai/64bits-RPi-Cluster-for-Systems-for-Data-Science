

## Model Answer 11

1. A large part of the exercise was about following the instructions of the SparkML notebook. One of the more free-form tasks was to go back and to modify the parameters that are used for the model, e.g., by trying out different features from the feature set (sl, sw, pl, pw). The best feature set I found varies a bit (the dataset is rather small, so a random split can have an influence on the outcome), but petal width (pw) always seemed to be among the features selected for the best model.

2. For this exercise, a modified version of the SparkML notebook can be used. The general procedure does not change. Nevertheless, one of the things to look out for is the naming of the columns in the diabetes dataset. While the independent variable was called "label" in the iris dataset, it is now called "outcome".
