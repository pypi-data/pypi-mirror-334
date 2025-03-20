# **🧠 Brains Build Code - Automated Machine Learning Pipeline**

**Brains Build Code** is an automated machine learning pipeline designed to simplify the end-to-end machine learning workflow. It handles:

* Data preprocessing
* Feature engineering
* Model selection
* Hyperparameter tuning
* Model evaluation

Built to save you time, reduce boilerplate, and accelerate experimentation.

# **Installation**

**From PyPI**
```bash
pip install brainsbuildcode
```

**Directly from GitHub**
```bash
pip install git+https://github.com/achelousace/brainsbuildcode.git
```

# **📖 Usage**

## **Fast Build Example**

```python
from brainsbuildcode import Brain
from sklearn.datasets import load_breast_cancer
import pandas as pd

# Load dataset
data = load_breast_cancer(as_frame=True)
df = data.frame

# Instantiate and build the model
best_model = Brain(df, target='target', model_name='RFC', grid_search=None)
best_model.build()
```

## **Alternative (Chainable Call)**

```python
from brainsbuildcode import Brain
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer(as_frame=True)
df = data.frame

# Instantiate and immediately build
best_model = Brain(df, target='target', model_name='RFC', grid_search='cv').build()
```

## **Full Pipline Example**

```python
from sklearn.datasets import load_iris
import pandas as pd
from brainsbuildcode import Convert, Brain

# Load dataset
data = load_iris(as_frame=True)
df = data.frame
df['target'] = data.target


# Full Pipline of Brain class
brain = Brain(df=df,
              target='target',                        # Target column name
              model_name='RFC',                       # Model name ('RFC', 'XGBC', etc.)
              task='classification',                  # Task type: 'classification' or 'regression'
              
              # Scaling and PCA
              scale=True,                             # Apply scaling to numerical columns (True) or disable scaling (False)
              pca=False,                              # Apply PCA (True) or not (False)
              pca_comp=0.9,                           # PCA components to retain (if pca=True), default 90% variance

              # Data splitting and CV
              test_size=0.2,                          # Test set size (0.2 = 20% test)
              cv=5,                                   # Number of cross-validation folds
              
              # Missing values handling
              miss=True,                              # Show missing values summary (True) or skip (False)
              ynan=False,                             # Drop rows with NaN in target (True) or keep (False)
              
              # Columns to process
              numerical_cols=[],                      # Manually specify numerical columns (empty = auto-detect)
              categorical_cols=[],                    # Manually specify categorical columns (empty = auto-detect)
              ordinal_cols={},                        # Dict of ordinal columns: {column: [order]}
              drop_cols=(),                           # Columns to drop before processing
              
              # Encoding and Imputation
              categorical_encoding='onehot',          # 'onehot' or 'label' encoding for categorical features
              ordinal_encoding=False,                 # Apply ordinal encoding (True) or skip (False)
              numerical_impute_strategy='mean',       # Imputation strategy for numerical columns
              categorical_impute_strategy='most_frequent',  # Imputation strategy for categorical
              ordinal_impute_strategy='most_frequent',      # Imputation strategy for ordinal
              categorical_fill_value=None,            # Fill value for categorical imputation
              ordinal_fill_value=None,                # Fill value for ordinal imputation
              
              # Display options
              showx=True,                            # Display processed X_train/X_test (True) or skip (False)
              summary=True,                          # Display data summary (True) or skip (False)
              objvalue=True,                         # Display value counts of categorical columns (True/False)
              xtype=True,                            # Display column data types (True/False)
              
              # Duplicate handling
              drop_duplicates=False,    # False = keep duplicates, True = drop first occurrence, 'all' = drop all duplicates
              
              # Target encoding
              yencode=None,                           # 'encode' = LabelEncode target, 'bin' = Binarize, None = no encoding
              
              # Grid Search / Hyperparameter tuning
              grid_search=None,                       # None = no tuning, 'cv' = GridSearchCV, 'rand' = RandomizedSearchCV
              voting='soft',                          # Voting method if using ensemble voting ('soft' or 'hard')
              voteclass=[],                           # List of classifiers for voting model
              pa=0,                                   # Grid search plot: index of hyperparameter to visualize (0 = first param)

              # Column value filtering
              dropc=False,                            # Drop rows based on column values (True/False)
              column_value={},                        # Dict of {column_name: values_to_drop} if dropc=True

              # Ordinal detection
              ord_threshold=None,                     # Auto-detect ordinal columns if unique values <= threshold (None disables)
              ordname=(),                             # Tuple of ordinal column names to treat manually
              
              # Conversion thresholds for object columns
              typeval=80,                             # % threshold: convert object column to numeric if >= this %
              convrate=80,                            # % threshold: if numeric, convert to int if >= this %, else float

              preprocessed_out=False                  # Return preprocessed dataset (True) or train model (False)
             )

# Build, preprocess, and train the model
brain.build()
```

## **Convert Function (Manual Data Preprocessing)**

```python
from sklearn.datasets import load_iris
from brainsbuildcode import Convert, Brain
import seaborn as sns
import pandas as pd

# Load dataset
df = sns.load_dataset("titanic")

# Define target
target = 'survived'

# Step 1: Apply conversion
converter = Convert(df, target)
X, y, ncol, ocol, ordinal_cols = converter.apply()

# Now you can process `X`, `y`, `ncol`, `ocol`, `ordinal_cols` manually, or pass them back to `Brain`
```

## **Pass Convert to Brain Manually**

```python
from sklearn.datasets import load_iris
from brainsbuildcode import Convert, Brain
import seaborn as sns
import pandas as pd

# Load dataset
df = sns.load_dataset("titanic")

# Define target
target = 'survived'

# Step 1: Apply conversion
converter = Convert(df, target)
X, y, ncol, ocol, ordinal_cols = converter.apply()

# Step 2: Instantiate Brain with converted column info
best_model = Brain(
    df=df,
    target=target,
    model_name='RFC',
    grid_search=None,
    drop_duplicates=True,
    numerical_cols=ncol,        # Pass numerical columns from Convert
    categorical_cols=ocol,      # Pass categorical columns from Convert
    ordinal_cols=ordinal_cols   # Pass ordinal columns from Convert
)

# Step 3: Build the model
best_model.build()
```

# **Models Names**

| Model_Name | Model Name                 | Task                     |
|------------|----------------------------|--------------------------|
| LR         | LogisticRegression         | classification           |
| RFC        | RandomForestClassifier     | classification           |
| XGBC       | XGBClassifier              | classification           |
| KNNC       | KNeighborsClassifier       | classification           |
| DTC        | DecisionTreeClassifier     | classification           |
| SVC        | SVC                        | classification           |
| MLPC       | MLPClassifier              | classification           |
| ADAC       | AdaBoostClassifier         | classification           |
| GBC        | GradientBoostingClassifier | classification           |
| BC         | BaggingClassifier          | classification           |
| NBC        | BernoulliNB                | classification           |
| Linear     | LinearRegression           | regression               |
| RFR        | RandomForestRegressor      | regression               |
| XGBR       | XGBRegressor               | regression               |
| KNNR       | KNeighborsRegressor        | regression               |
| DTR        | DecisionTreeRegressor      | regression               |
| SVR        | SVR                        | regression               |
| MLPR       | MLPRegressor               | regression               |
| ADAR       | AdaBoostRegressor          | regression               |
| GBR        | GradientBoostingRegressor  | regression               |
| BR         | BaggingRegressor           | regression               |
| NBR        | BayesianRidge              | regression               |
| LRmulti    | LogisticRegression         | multi-class classification |
| RFmulti    | RandomForestClassifier     | multi-class classification |
| XGBmulti   | XGBClassifier              | multi-class classification |
| KNNmulti   | KNeighborsClassifier       | multi-class classification |
| DTmulti    | DecisionTreeClassifier     | multi-class classification |
| SVCmulti   | SVC                        | multi-class classification |
| MLPCmulti  | MLPClassifier              | multi-class classification |
| ADAmulti   | AdaBoostClassifier         | multi-class classification |
| GBmulti    | GradientBoostingClassifier | multi-class classification |
| BCmulti    | BaggingClassifier          | multi-class classification |
| NBmulti    | ComplementNB               | multi-class classification |
| vote       | VotingClassifier           | Ensamble                 |


# 💡 **Key Features**

* Automatic Detection of numerical, categorical, and ordinal features.

* Missing Value Handling with customizable strategies.

* Feature Scaling & PCA Support.

* Flexible Encoding: One-hot, label, ordinal.

* Multiple Models Supported: Random Forest, XGBoost, Logistic Regression, SVC, etc.

* Voting Classifiers & Ensemble Models.

* Hyperparameter Optimization: Grid Search & Randomized Search.

* Detailed Evaluation Metrics & Visualizations.

# **🔗 License**
This project is licensed under the MIT License.

# **🛠️ Contribution**
Feel free to contribute, suggest features, or report issues via pull requests and the issues section!
