🧠 Brains Build Code - Automated Machine Learning Pipeline

Brains Build Code is an automated machine learning pipeline designed to simplify the end-to-end machine learning workflow. It handles:

* Data preprocessing
* Feature engineering
* Model selection
* Hyperparameter tuning
* Model evaluation

Built to save you time, reduce boilerplate, and accelerate experimentation.

Installation

From PyPI:
```bash
pip install brainsbuildcode
```

Directly from GitHub:
```bash
pip install git+https://github.com/achelousace/brainsbuildcode.git
```

📖 Usage

Full Build Example:

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

Alternative (Chainable Call):

```python
from brainsbuildcode import Brain
from sklearn.datasets import load_breast_cancer

data = load_breast_cancer(as_frame=True)
df = data.frame

# Instantiate and immediately build
best_model = Brain(df, target='target', model_name='RFC', grid_search='cv').build()
```

Convert Function (Manual Data Preprocessing):

```python
from brainsbuildcode import Brain
import seaborn as sns
import pandas as pd

# Load dataset
df = sns.load_dataset("titanic")

# Step 1: Instantiate
best_model = Brain(df, target='survived', model_name='RFC', grid_search=None, drop_duplicates=True)

# Step 2: Convert
X, y, ncol, ocol, ordinal_cols = best_model.convert(
    df=df,
    target=target,
    ncol=[],           # Specify numerical columns (optional)
    ocol=[],           # Specify categorical columns (optional)
    ordinal_cols={},   # Specify ordinal columns (optional)
    ord_threshold=0,   # Auto-detect ordinal columns if unique categories <= threshold (0 disables auto-detection)
    ordname=[],        # Manually specify ordinal column names (optional)
    drop_cols=[]       # Columns to drop (optional)
)

# Now you can process `X`, `y`, `ncol`, `ocol`, `ordinal_cols` manually, or pass them back to `Brain`
```

💡 Key Features

* Automatic Detection of numerical, categorical, and ordinal features.

* Missing Value Handling with customizable strategies.

* Feature Scaling & PCA Support.

* Flexible Encoding: One-hot, label, ordinal.

* Multiple Models Supported: Random Forest, XGBoost, Logistic Regression, SVC, etc.

* Voting Classifiers & Ensemble Models.

* Hyperparameter Optimization: Grid Search & Randomized Search.

* Detailed Evaluation Metrics & Visualizations.

🔗 License
This project is licensed under the MIT License.

🛠️ Contribution
Feel free to contribute, suggest features, or report issues via pull requests and the issues section!
