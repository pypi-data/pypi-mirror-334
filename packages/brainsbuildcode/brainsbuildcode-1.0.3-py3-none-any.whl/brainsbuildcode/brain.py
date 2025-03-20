import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from xgboost import XGBClassifier, XGBRegressor
import os
from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV, ParameterGrid
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, LabelEncoder, Binarizer
from sklearn.linear_model import LogisticRegression, LinearRegression, BayesianRidge
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier, AdaBoostClassifier, BaggingClassifier, VotingClassifier, GradientBoostingRegressor, AdaBoostRegressor, BaggingRegressor
from sklearn.naive_bayes import BernoulliNB, ComplementNB
from sklearn.metrics import classification_report, mean_absolute_error, mean_squared_error, r2_score, ConfusionMatrixDisplay, precision_recall_curve, accuracy_score, root_mean_squared_error
from sklearn.decomposition import PCA
from sklearn.multiclass import OneVsRestClassifier
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC, SVR
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
from tqdm import tqdm
import random

pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)

class Brain:
    def __init__(self,
                 df,
                 target,
                 model_name,
                 task='classification',
                 scale=False,
                 grid_search=None,
                 test_size=0.2,
                 cv=5,
                 voteclass=[],
                 numerical_cols=[],
                 categorical_cols=[],
                 ordinal_encoding=True,
                 ordinal_cols={},
                 ynan=True,
                 categorical_encoding='onehot',
                 numerical_impute_strategy='mean',
                 showx=False,
                 summary=False,
                 miss=False,
                 categorical_impute_strategy='most_frequent',
                 ordinal_impute_strategy='most_frequent',
                 preprocessed_out=False,
                 yencode='encode',
                 categorical_fill_value=None,
                 ordinal_fill_value=None,
                 pca=False,
                 pca_comp=0.9,
                 objvalue=True,
                 drop_duplicates=False,
                 xtype=False,
                 voting='soft',
                 pa=0,
                 dropc=False,
                 column_value={},
                 # Parameters for conversion:
                 ord_threshold=None,
                 ordname=(),
                 drop_cols=(),
                 typeval=80,
                 convrate=80):
        self.df = df.copy()
        self.target = target
        self.model_name = model_name
        self.task = task
        self.scale = scale
        self.grid_search = grid_search
        self.test_size = test_size
        self.cv = cv
        self.voteclass = voteclass
        self.numerical_cols = numerical_cols
        self.categorical_cols = categorical_cols
        self.ordinal_encoding = ordinal_encoding
        self.ordinal_cols = ordinal_cols
        self.ynan = ynan
        self.categorical_encoding = categorical_encoding
        self.numerical_impute_strategy = numerical_impute_strategy
        self.showx = showx
        self.summary = summary
        self.miss = miss
        self.categorical_impute_strategy = categorical_impute_strategy
        self.ordinal_impute_strategy = ordinal_impute_strategy
        self.preprocessed_out = preprocessed_out
        self.yencode = yencode
        self.categorical_fill_value = categorical_fill_value
        self.ordinal_fill_value = ordinal_fill_value
        self.pca = pca
        self.pca_comp = pca_comp
        self.objvalue = objvalue
        self.drop_duplicates = drop_duplicates
        self.xtype = xtype
        self.voting = voting
        self.pa = pa
        self.dropc = dropc
        self.column_value = column_value
        self.ord_threshold = ord_threshold
        self.ordname = ordname
        self.drop_cols = drop_cols
        self.typeval = typeval
        self.convrate = convrate
        

    def convert(self, df, target, ncol=None, ocol=None, ordinal_cols=None,
                                        ord_threshold=None, ordname=(), drop_cols=(), typeval=80, convrate=80):
        # If ncol and ocol are not provided, extract them
        if not ncol:
            ncol = [col for col in df.select_dtypes(include=['float64', 'int64']).columns.tolist() if col != target]
        if not ocol:
            ocol = [col for col in df.select_dtypes(include=['object', 'category']).columns.tolist() if col != target]

        # Identify ordinal columns (if ord_threshold is specified)
        if not ordinal_cols:
            ordinal_cols = {}
            if ord_threshold is not None:
                for col in df.columns:
                    if df[col].dtype == 'object' and df[col].nunique() <= ord_threshold:
                        ordinal_cols[col] = df[col].unique().tolist()

        # Handling ordname
        if ordname:
            if isinstance(ordname, str):
                ordname = [ordname]
            for col in ordname:
                if col in ocol:
                    ordinal_cols[col] = sorted(df[col].unique())
                    ocol.remove(col)
        # Remove specified drop columns
        ncol = [col for col in ncol if col not in drop_cols]
        ocol = [col for col in ocol if col not in drop_cols]
        ordinal_cols = {key: value for key, value in ordinal_cols.items() if key not in drop_cols}

        print(f"Initial ncol = {ncol}")
        print(f"Initial ocol = {ocol}")
        print(f"Initial ordinal_cols = {ordinal_cols}")

        X = df[ncol + ocol + list(ordinal_cols.keys())].copy()
        y = df[target].copy()

        numeric_columns = []
        column_types = []
        for column in X.columns:
            if X[column].dtype == 'object':
                cleaned_column = X[column].astype(str).replace({r'[\*\D]': ''}, regex=True)
                cleaned_column = cleaned_column.str.replace(r'\s+', '', regex=True)
                is_numeric = cleaned_column.apply(lambda x: pd.to_numeric(x, errors='coerce')).notna()
                num_count = is_numeric.sum()
                total_count = len(X[column])
                if (num_count / total_count) * 100 >= typeval:
                    try:
                        int_values = cleaned_column.apply(lambda x: int(x) if x.isdigit() else np.nan)
                        float_values = cleaned_column.apply(lambda x: float(x) if x.replace('.', '', 1).isdigit() else np.nan)
                        int_count = int_values.notna().sum()
                        if (int_count / num_count) * 100 >= convrate:
                            X[column] = int_values
                            numeric_columns.append(column)
                            column_types.append('int')
                        else:
                            X[column] = float_values
                            numeric_columns.append(column)
                            column_types.append('float')
                        if column in ocol or column in ordinal_cols:
                            ncol.append(column)
                            if column in ocol:
                                ocol.remove(column)
                    except ValueError:
                        pass
        if numeric_columns:
            conversion_info = ', '.join(f"{col} (converted to {typ})" for col, typ in zip(numeric_columns, column_types))
            print("-" * 30)
            print(f"Columns converted to numeric: {conversion_info}")
        else:
            print("No columns were converted to numeric.")
        print("-" * 30)
        print("Updated DataFrames:")
        print("X:")
        display(X.head(3))
        display(X.info())
        print("ncol:", ncol)
        print("ocol:", ocol)
        print("ordinal_cols:", ordinal_cols)
        return X, y, ncol, ocol, ordinal_cols

    def preprocess_data(self, X_train, X_test, numerical_cols, categorical_cols, ordinal_cols,
                        numerical_impute_strategy='mean', categorical_impute_strategy='most_frequent',
                        ordinal_impute_strategy='most_frequent', categorical_fill_value=None, ordinal_fill_value=None,
                        ordinal_encoding=True, categorical_encoding='onehot'):
        transformers = []
        if numerical_cols:
            num_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy=numerical_impute_strategy))])
            transformers.append(('num', num_transformer, numerical_cols))
        if categorical_cols:
            if categorical_encoding == 'onehot':
                cat_transformer_steps = [
                    ('imputer', SimpleImputer(strategy=categorical_impute_strategy, fill_value=categorical_fill_value)),
                    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
                ]
                cat_transformer = Pipeline(steps=cat_transformer_steps)
                transformers.append(('cat', cat_transformer, categorical_cols))
            elif categorical_encoding == 'label':
                cat_transformer_steps = [
                    ('imputer', SimpleImputer(strategy=categorical_impute_strategy, fill_value=categorical_fill_value)),
                    ('label_encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
                ]
                cat_transformer = Pipeline(steps=cat_transformer_steps)
                transformers.append(('cat', cat_transformer, categorical_cols))
        if ordinal_cols and ordinal_encoding:
            for col, categories in ordinal_cols.items():
                ordinal_imputer = SimpleImputer(strategy=ordinal_impute_strategy, fill_value=ordinal_fill_value)
                transformers.append((col, Pipeline(steps=[('imputer', ordinal_imputer),
                                                          ('encoder', OrdinalEncoder(categories=[categories]))]),
                                      [col]))
        preprocessor = ColumnTransformer(transformers, remainder='passthrough')
        X_train_trans = preprocessor.fit_transform(X_train)
        X_test_trans = preprocessor.transform(X_test)
        feature_names = []
        if numerical_cols:
            feature_names.extend(numerical_cols)
        if categorical_cols and categorical_encoding == 'onehot':
            cat_feature_names = list(preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_cols))
            feature_names.extend(cat_feature_names)
        elif categorical_cols and categorical_encoding == 'label':
            feature_names.extend(categorical_cols)
        if ordinal_cols:
            feature_names.extend(list(ordinal_cols.keys()))
        passthrough_cols = [col for col in X_train.columns if col not in list(numerical_cols) + list(categorical_cols) + list(ordinal_cols.keys())]
        feature_names.extend(passthrough_cols)
        if len(feature_names) != X_train_trans.shape[1]:
            raise ValueError(f"Feature names length {len(feature_names)} does not match the number of columns in preprocessed data {X_train_trans.shape[1]}.")
        x_train_pros = pd.DataFrame(X_train_trans, columns=feature_names)
        x_test_pros = pd.DataFrame(X_test_trans, columns=feature_names)
        return x_train_pros, x_test_pros

    def build(self):
        # Check if column information is already provided
        if self.numerical_cols and self.categorical_cols and self.ordinal_cols is not None:
            print("Skipping convert() because column info is already provided.")
            X = self.df[self.numerical_cols + self.categorical_cols + list(self.ordinal_cols.keys())].copy()
            y = self.df[self.target].copy()
        else:
            # Process and convert the dataframe only if not already specified
            X, y, ncol_conv, ocol_conv, ordinal_cols_conv = self.convert(
                self.df, self.target, self.numerical_cols, self.categorical_cols,
                self.ordinal_cols, self.ord_threshold, self.ordname, self.drop_cols, self.typeval, self.convrate
            )
            # Update columns
            self.numerical_cols = ncol_conv
            self.categorical_cols = ocol_conv
            self.ordinal_cols = ordinal_cols_conv

        if self.xtype:
            grouped_cols = self.df.columns.groupby(self.df.dtypes)
            for dtype, cols in grouped_cols.items():
                print(f"\nColumns with dtype {dtype}:")
                self.df[cols].info()

        if self.ynan:
            non_nan_indices_y = ~y.isna()
            y = y[non_nan_indices_y]

                
        def check_duplicates(X, drop_duplicates=False):
            num_duplicates = self.df.duplicated().sum()
            if num_duplicates > 0:
                print(f"Found {num_duplicates} duplicated rows.")
                duplicate_df = self.df[self.df.duplicated(keep=False)].copy()
                percentage_per_column = (self.df.duplicated(subset=self.df.columns, keep=False).sum() / self.df.shape[0]) * 100
                percentage_per_column = pd.Series(percentage_per_column, index=self.df.columns)
                columns_with_percentage = [f"{col} ({percentage:.2f}%)" for col, percentage in percentage_per_column.items()]
                duplicate_df.columns = columns_with_percentage
                duplicate_df_sorted = duplicate_df.sort_values(by=list(duplicate_df.columns), ascending=False)

                if drop_duplicates:
                    if drop_duplicates == 'all':
                        self.df.drop_duplicates(keep=False, inplace=True)
                        print("All duplicates dropped.")
                    else:
                        self.df.drop_duplicates(keep='first', inplace=True)
                        print("First occurrence of duplicates dropped.")
                
                print("Duplicate rows:")
                display(duplicate_df_sorted)
            else:
                print("No duplicated rows found.")



        def missing_info(df):
            missing_count = df.isnull().sum()
            non_null_count = df.notnull().sum()
            missing_percentage = (missing_count / len(df)) * 100
            non_null_percentage = (non_null_count / len(df)) * 100
            missing_df = pd.DataFrame({
                'Column': df.columns,
                'Missing Count': missing_count.values,
                'Non-Null Count': non_null_count.values,
                'Missing %': missing_percentage.values,
                'Non-Null %': non_null_percentage.values})
            missing_df.set_index('Column', inplace=True)
            display(missing_df)
            return missing_df

        def display_value_counts(X):
            result_df = pd.DataFrame()
            for col in X.select_dtypes(include=['object', 'category']).columns:
                value_counts = X[col].value_counts()
                value_counts_df = value_counts.reset_index()
                value_counts_df.columns = [col + '_value', col + '_count']
                result_df = pd.concat([result_df, value_counts_df], axis=1)
            display(result_df)

        if self.objvalue:
            print("-" * 30)
            print("Value Counts of object Columns in X before Processing:")
            display_value_counts(X)
            print("-" * 30)
            check_duplicates(X, self.drop_duplicates)
            print("-" * 30)

        def drop_value_from_column(X, y, column_value):
            if isinstance(column_value, dict):
                for column_name, values in column_value.items():
                    if column_name not in X.columns:
                        raise ValueError(f"Column '{column_name}' does not exist in the DataFrame.")
                    if isinstance(values, list):
                        rows_to_keep = ~X[column_name].isin(values)
                    else:
                        rows_to_keep = X[column_name] != values
                    X = X[rows_to_keep]
                    y = y[rows_to_keep]
                X.reset_index(drop=True, inplace=True)
                y.reset_index(drop=True, inplace=True)
            else:
                raise TypeError("column_value argument should be a dictionary with column names as keys and values to drop as values.")
            return X, y

        if self.dropc:
            X, y = drop_value_from_column(X, y, self.column_value)

        def classification_metrics(y_true, y_pred, label='', output_dict=False, figsize=(8,4),
                                   normalize='true', cmap='Blues', colorbar=False, zero_division=0):
            report = classification_report(y_true, y_pred, zero_division=zero_division)
            header = "-"*70
            print(header, f" Classification Metrics: {label}", header, sep='\n')
            print(report)
            fig, axes = plt.subplots(ncols=2, figsize=figsize)
            ConfusionMatrixDisplay.from_predictions(y_true, y_pred, normalize=None,
                                                      cmap='gist_gray', colorbar=colorbar, ax=axes[0])
            axes[0].set_title(f"{y.name} Raw Counts")
            ConfusionMatrixDisplay.from_predictions(y_true, y_pred, normalize=normalize,
                                                      cmap=cmap, colorbar=colorbar, ax=axes[1])
            axes[1].set_title(f"{y.name} Normalized")
            fig.tight_layout()
            plt.show()
            if output_dict:
                report_dict = classification_report(y_true, y_pred, output_dict=True, zero_division=zero_division)
                return report_dict

        def evaluate_classification(model, X_train, y_train, X_test, y_test, figsize=(12,6), normalize='true',
                                    output_dict=False, cmap_train='Blues', cmap_test='Reds', colorbar=False):
            y_train_pred = model.predict(X_train)
            results_train = classification_metrics(y_train, y_train_pred, output_dict=True, figsize=figsize,
                                                    colorbar=colorbar, cmap=cmap_train, label='Training Data')
            print()
            y_test_pred = model.predict(X_test)
            results_test = classification_metrics(y_test, y_test_pred, output_dict=True, figsize=figsize,
                                                   colorbar=colorbar, cmap=cmap_test, label='Test Data')
            if output_dict:
                return {'train': results_train, 'test': results_test}

        def evaluate_regression(model, X_train, y_train, X_test, y_test):
            y_train_pred = model.predict(X_train)
            print("Training Data:")
            print_regression_metrics(y_train, y_train_pred)
            y_test_pred = model.predict(X_test)
            print("Test Data:")
            print_regression_metrics(y_test, y_test_pred)

        def print_regression_metrics(y_true, y_pred):
            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = root_mean_squared_error(y_true, y_pred)
            MAPE = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
            r2 = r2_score(y_true, y_pred)
            print(f"  Mean Absolute Error: {mae:.4f}")
            print(f"  Mean Squared Error: {mse:.4f}")
            print(f"  Root Mean Squared Error: {rmse:.4f}")
            print(f"  Mean Absolute Percentage Error: {MAPE:.4f}%")
            print(f"  R^2 Score: {r2:.4f}")

        def preprocess_data(X_train, X_test, numerical_cols, categorical_cols, ordinal_cols,
                            numerical_impute_strategy='mean', categorical_impute_strategy='most_frequent',
                            ordinal_impute_strategy='most_frequent', categorical_fill_value=None, ordinal_fill_value=None,
                            ordinal_encoding=True, categorical_encoding='onehot'):
            transformers = []
            if numerical_cols:
                num_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy=numerical_impute_strategy))])
                transformers.append(('num', num_transformer, numerical_cols))
            if categorical_cols:
                if categorical_encoding == 'onehot':
                    cat_transformer_steps = [
                        ('imputer', SimpleImputer(strategy=categorical_impute_strategy, fill_value=categorical_fill_value)),
                        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
                    ]
                    cat_transformer = Pipeline(steps=cat_transformer_steps)
                    transformers.append(('cat', cat_transformer, categorical_cols))
                elif categorical_encoding == 'label':
                    cat_transformer_steps = [
                        ('imputer', SimpleImputer(strategy=categorical_impute_strategy, fill_value=categorical_fill_value)),
                        ('label_encoder', OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1))
                    ]
                    cat_transformer = Pipeline(steps=cat_transformer_steps)
                    transformers.append(('cat', cat_transformer, categorical_cols))
            if ordinal_cols and ordinal_encoding:
                for col, categories in ordinal_cols.items():
                    ordinal_imputer = SimpleImputer(strategy=ordinal_impute_strategy, fill_value=ordinal_fill_value)
                    transformers.append((col, Pipeline(steps=[('imputer', ordinal_imputer),
                                                              ('encoder', OrdinalEncoder(categories=[categories]))]),
                                         [col]))
            preprocessor = ColumnTransformer(transformers, remainder='passthrough')
            X_train_trans = preprocessor.fit_transform(X_train)
            X_test_trans = preprocessor.transform(X_test)
            feature_names = []
            if numerical_cols:
                feature_names.extend(numerical_cols)
            if categorical_cols and categorical_encoding == 'onehot':
                cat_feature_names = list(preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_cols))
                feature_names.extend(cat_feature_names)
            elif categorical_cols and categorical_encoding == 'label':
                feature_names.extend(categorical_cols)
            if ordinal_cols:
                feature_names.extend(list(ordinal_cols.keys()))
            passthrough_cols = [col for col in X_train.columns if col not in list(numerical_cols) + list(categorical_cols) + list(ordinal_cols.keys())]
            feature_names.extend(passthrough_cols)
            if len(feature_names) != X_train_trans.shape[1]:
                raise ValueError(f"Feature names length {len(feature_names)} does not match the number of columns in preprocessed data {X_train_trans.shape[1]}.")
            x_train_pros = pd.DataFrame(X_train_trans, columns=feature_names)
            x_test_pros = pd.DataFrame(X_test_trans, columns=feature_names)
            return x_train_pros, x_test_pros

        def detect_imputation(original_df, preprocessed_df, categorical_cols, categorical_encoding='onehot'):
            imputed_data = {}
            for col in original_df.columns:
                if original_df[col].isna().any() and col in preprocessed_df.columns:
                    original_na = original_df[col].isna()
                    preprocessed_na = preprocessed_df[col].isna()
                    if not np.array_equal(original_na, preprocessed_na):
                        imputed_data[col] = {'original_na': original_df[col].isna().sum(),
                                             'preprocessed_na': preprocessed_df[col].isna().sum()}
            if categorical_encoding == 'onehot':
                onehot_feature_names = preprocessed_df.columns[preprocessed_df.columns.str.startswith('cat_')]
                col_to_features = {col: [f for f in onehot_feature_names if f.startswith(f'cat_{col}_')] for col in categorical_cols}
                for col, features in col_to_features.items():
                    if col in original_df.columns and original_df[col].isna().any():
                        original_na_count = original_df[col].isna().sum()
                        preprocessed_na_count = sum(preprocessed_df[feature].isna().sum() for feature in features)
                        if original_na_count > 0:
                            imputed_data[col] = {'original_na': original_na_count, 'preprocessed_na': preprocessed_na_count}
            return imputed_data

        if self.miss:
            print("-" * 30)
            print('Missing Values Of All Dataframe:')
            print("-" * 30)
            missing_info(self.df)
            print("-" * 30)
            print('Missing Values Of Training Data Before Imputation:')
            print("-" * 30)
            missing_info(X)

        if 'multi' in self.model_name:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42, stratify=y)
        else:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)

        X_train_preprocessed, X_test_preprocessed = preprocess_data(X_train, X_test, self.numerical_cols, self.categorical_cols, self.ordinal_cols,
                                                                     self.numerical_impute_strategy, self.categorical_impute_strategy, self.ordinal_impute_strategy,
                                                                     self.categorical_fill_value, self.ordinal_fill_value, self.ordinal_encoding, self.categorical_encoding)
        imputation_summary = detect_imputation(X, pd.concat([X_train_preprocessed, X_test_preprocessed]), self.categorical_cols, self.categorical_encoding)
        if imputation_summary:
            print("-" * 30)
            print("Imputation Summary:")
            for col, info in imputation_summary.items():
                print(f"Column '{col}':")
                print(f"  Original NA count: {info['original_na']}")
                print(f"  Post-Imputation NA count: {info['preprocessed_na']}")
                print("-" * 30)
        else:
            print("No imputation detected.")

        if self.summary:
            print("-" * 30)
            print("X_train_preprocessed:")
            print(X_train_preprocessed.info())
            print("-" * 30)
            print("X_test_preprocessed:")
            print(X_test_preprocessed.info())
            print("-" * 30)

        if self.showx:
            print('X_Train_preprocessed:')
            display(pd.DataFrame(X_train_preprocessed))
            print('X_Test_preprocessed:')
            display(pd.DataFrame(X_test_preprocessed))

        if self.scale:
            numerical_cols_preprocessed = [col for col in X_train_preprocessed.columns if col in self.numerical_cols]
            scaler = StandardScaler()
            X_train_preprocessed[numerical_cols_preprocessed] = scaler.fit_transform(X_train_preprocessed[numerical_cols_preprocessed])
            X_test_preprocessed[numerical_cols_preprocessed] = scaler.transform(X_test_preprocessed[numerical_cols_preprocessed])
            print("Scaling was applied to the data.")
        else:
            print("Scaling was not applied to the data.")

        if self.showx:
            print("-" * 30)
            print('X_Train_preprocessed_Scaled:')
            display(pd.DataFrame(X_train_preprocessed))
            print('X_Test_preprocessed_Scaled:')
            display(pd.DataFrame(X_test_preprocessed))

        if self.pca:
            pca90 = PCA(n_components=self.pca_comp, svd_solver='full', random_state=42)
            X_train_preprocessed = pca90.fit_transform(X_train_preprocessed)
            X_test_preprocessed = pca90.transform(X_test_preprocessed)
            print("-" * 30)
            print(f"Explained variance ratio with {self.pca_comp} components: {pca90.explained_variance_ratio_.sum()}")
            print(f"PCA components: {pca90.n_components_}")
            print("-" * 30)
            X_train = X_train_preprocessed
            X_test = X_test_preprocessed
            print("Train Set PCA:")
            display(pd.DataFrame(X_train))
            print("Test Set PCA:")
            display(pd.DataFrame(X_test))

        def process_target(y_train, y_test):
            le = LabelEncoder()
            if y_train.dtype == 'object' or y_test.dtype == 'object':
                if y_train.dtype == 'object':
                    y_train = le.fit_transform(y_train)
                if y_test.dtype == 'object':
                    y_test = le.transform(y_test)
            return y_train, y_test

        def process_target2(y_train, y_test):
            le = LabelEncoder()
            if y_train.dtype == 'object' or y_test.dtype == 'object':
                if y_train.dtype == 'object':
                    y_train = le.fit_transform(y_train)
                if y_test.dtype == 'object':
                    y_test = le.transform(y_test)
            if np.issubdtype(y_train.dtype, np.number) and np.issubdtype(y_test.dtype, np.number):
                binarizer = Binarizer(threshold=0.5)
                y_train = binarizer.fit_transform(y_train.reshape(-1, 1)).ravel()
                y_test = binarizer.transform(y_test.reshape(-1, 1)).ravel()
            return y_train, y_test

        if self.yencode == 'encode':
            y_train, y_test = process_target(y_train, y_test)
        elif self.yencode == 'bin':
            y_train, y_test = process_target2(y_train, y_test)

        if self.preprocessed_out and self.pca:
            X_train_preprocessed = pd.DataFrame(X_train_preprocessed)
            X_test_preprocessed = pd.DataFrame(X_test_preprocessed)
            newdf = pd.concat([X_train_preprocessed, X_test_preprocessed])
            return newdf
        if self.preprocessed_out:
            newdf = pd.concat([X_train_preprocessed, X_test_preprocessed])
            return newdf

        if 'multi' in self.model_name:
            print("Training classes:", np.unique(y_train))
            print("Test classes:", np.unique(y_test))
            print("Y Is Stratifyied")

        # Define parameter grids for models
        l2_params = {'solver': ['lbfgs', 'liblinear', 'newton-cg', 'sag', 'saga'], 'penalty': ['l2'],
                     'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        l1_params = {'solver': ['liblinear', 'saga'], 'penalty': ['l1'],
                     'C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        elasticnet_params = {'solver': ['saga'], 'penalty': ['elasticnet'],
                             'l1_ratio': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
        none_params = {'solver': ['lbfgs', 'newton-cg', 'sag', 'saga'], 'penalty': [None]}

        l2_params_multi = {'estimator__solver': ['lbfgs', 'liblinear', 'newton-cg', 'sag', 'saga'],
                           'estimator__penalty': ['l2'],
                           'estimator__C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        l1_params_multi = {'estimator__solver': ['liblinear', 'saga'],
                           'estimator__penalty': ['l1'],
                           'estimator__C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        elasticnet_params_multi = {'estimator__solver': ['saga'],
                                   'estimator__penalty': ['elasticnet'],
                                   'estimator__l1_ratio': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
        none_params_multi = {'estimator__solver': ['lbfgs', 'newton-cg', 'sag', 'saga'],
                             'estimator__penalty': [None]}

        classifiers_pool = {
            'LR':  LogisticRegression(max_iter=10000, random_state=42, n_jobs=-1),
            'RF':  RandomForestClassifier(random_state=42, n_jobs=-1),
            'XGB': XGBClassifier(random_state=42, n_jobs=-1),
            'KNN': KNeighborsClassifier(n_jobs=-1),
            'Dec': DecisionTreeClassifier(random_state=42),
            'SVC': SVC(probability=True, random_state=42),
            'MLP': MLPClassifier(max_iter=10000, random_state=42),
            'Ada': AdaBoostClassifier(algorithm='SAMME', random_state=42),
            'GB':  GradientBoostingClassifier(random_state=42),
            'Bag': BaggingClassifier(random_state=42, n_jobs=-1),
            'NB':  BernoulliNB()
        }
        LRl2_params = {'LR__solver': ['lbfgs', 'liblinear', 'newton-cg', 'sag', 'saga'],
                       'LR__penalty': ['l2'],
                       'LR__C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        LRl1_params = {'LR__solver': ['liblinear', 'saga'],
                       'LR__penalty': ['l1'],
                       'LR__C': [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        LRelasticnet_params = {'LR__solver': ['saga'],
                               'LR__penalty': ['elasticnet'],
                               'LR__l1_ratio': [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]}
        LRnone_params = {'LR__solver': ['lbfgs', 'newton-cg', 'sag', 'saga'],
                         'LR__penalty': [None]}
        LRall_params = {**LRl2_params, **LRl1_params, **LRelasticnet_params, **LRnone_params}
        RF_params = {'RF__n_estimators': [50, 100, 150, 200],
                     'RF__max_depth': [None, 10, 15, 20],
                     'RF__min_samples_split': [2, 5, 10],
                     'RF__min_samples_leaf': [1, 2, 4],
                     'RF__max_features': ['sqrt', 'log2']}
        XGB_params = {'XGB__booster': ['gbtree', 'dart'],
                      'XGB__n_estimators': [100, 150, 200],
                      'XGB__learning_rate': [0.001, 0.01, 0.1, 0.2],
                      'XGB__max_depth': [3, 4, 5],
                      'XGB__min_child_weight': [1, 5],
                      'XGB__subsample': [0.8, 1.0],
                      'XGB__colsample_bytree': [0.8, 1.0],
                      'XGB__gamma': [0, 0.1]}
        KNN_params = {'KNN__n_neighbors': [3, 5, 7, 9, 10, 11],
                      'KNN__weights': ['uniform', 'distance']}
        Dec_params = {'Dec__criterion': ['gini', 'entropy'],
                      'Dec__max_depth': [None, 10, 20, 30],
                      'Dec__min_samples_split': [2, 5, 10],
                      'Dec__min_samples_leaf': [1, 2, 4]}
        SVC_params = {'SVC__C': [0.1, 1, 10],
                      'SVC__kernel': ['linear', 'rbf'],
                      'SVC__gamma': ['scale', 'auto']}
        MLP_params = {'MLP__hidden_layer_sizes': [(50,), (100,), (50, 50)],
                      'MLP__activation': ['relu', 'tanh'],
                      'MLP__solver': ['adam', 'sgd']}
        Ada_params = {'Ada__n_estimators': [50, 100, 200],
                      'Ada__learning_rate': [0.01, 0.1, 1]}
        GB_params = {'GB__n_estimators': [50, 100, 200],
                     'GB__learning_rate': [0.01, 0.1, 1],
                     'GB__max_depth': [1, 2, 3]}
        Bag_params = {'Bag__n_estimators': [10, 50, 100],
                      'Bag__max_samples': [0.5, 0.75, 1.0]}
        NB_params = {'NB__alpha': [0.01, 0.1, 1.0]}

        def select_classifiers(classifier_names):
            if isinstance(classifier_names, str) and classifier_names.startswith('random'):
                num_classifiers = int(classifier_names.split()[1])
                selected_classifiers = random.sample(list(classifiers_pool.items()), num_classifiers)
            else:
                selected_classifiers = [(name, classifiers_pool[name]) for name in classifier_names]
            return selected_classifiers

        def select_params(selected_classifiers):
            params = {}
            classifier_names = [name for name, _ in selected_classifiers]
            for name in classifier_names:
                if name == 'LR':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in LRall_params.items()})
                elif name == 'RF':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in RF_params.items()})
                elif name == 'XGB':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in XGB_params.items()})
                elif name == 'KNN':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in KNN_params.items()})
                elif name == 'Dec':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in Dec_params.items()})
                elif name == 'SVC':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in SVC_params.items()})
                elif name == 'MLP':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in MLP_params.items()})
                elif name == 'Ada':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in Ada_params.items()})
                elif name == 'GB':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in GB_params.items()})
                elif name == 'Bag':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in Bag_params.items()})
                elif name == 'NB':
                    params.update({f'{name}__{key.split("__")[1]}': value for key, value in NB_params.items()})
            return params

        chosen_classifiers = self.voteclass
        selected_classifiers = select_classifiers(chosen_classifiers)
        selected_params = select_params(selected_classifiers)

        models = {
            'LR': {'model': LogisticRegression(max_iter=10000, random_state=42, n_jobs=-1),
                       'params': [l2_params, l1_params, elasticnet_params, none_params], 'task': 'classification'},
            'RFC': {'model': RandomForestClassifier(random_state=42, n_jobs=-1),
                       'params': {'n_estimators': [50, 100, 150, 200],
                                  'max_depth': [None, 10, 15, 20],
                                  'min_samples_split': [2, 5, 10],
                                  'min_samples_leaf': [1, 2, 4],
                                  'max_features': ['sqrt', 'log2']}, 'task': 'classification'},
            'XGBC': {'model': XGBClassifier(random_state=42, n_jobs=-1),
                       'params': {'booster': ['gbtree', 'dart'],
                                  'n_estimators': [100, 150, 200],
                                  'learning_rate': [0.01, 0.1, 0.2],
                                  'max_depth': [3, 4, 5],
                                  'min_child_weight': [1, 5],
                                  'subsample': [0.8, 1.0],
                                  'colsample_bytree': [0.8, 1.0],
                                  'gamma': [0, 0.1]}, 'task': 'classification'},
            'KNNC': {'model': KNeighborsClassifier(n_jobs=-1),
                       'params': {'n_neighbors': list(range(1,33,2)),
                                  'weights': ['uniform', 'distance']}, 'task': 'classification'},
            'DTC': {'model': DecisionTreeClassifier(random_state=42),
                       'params': {'criterion': ['gini', 'entropy'],
                                  'max_depth': [None, 10, 20, 30],
                                  'min_samples_split': [2, 5, 10],
                                  'min_samples_leaf': [1, 2, 4]}, 'task': 'classification'},
            'SVC': {'model': SVC(random_state=42),
                       'params': {'C': [0.1, 1, 10],
                                  'kernel': ['linear', 'rbf'],
                                  'gamma': ['scale', 'auto']}, 'task': 'classification'},
            'MLPC': {'model': MLPClassifier(max_iter=10000, random_state=42),
                       'params': {'hidden_layer_sizes': [(50,), (100,), (50, 50)],
                                  'activation': ['relu', 'tanh'],
                                  'solver': ['adam', 'sgd']}, 'task': 'classification'},
            'ADAC': {'model': AdaBoostClassifier(algorithm='SAMME', random_state=42),
                       'params': {'n_estimators': [50, 100, 200],
                                  'learning_rate': [0.01, 0.1, 1]}, 'task': 'classification'},
            'GBC': {'model': GradientBoostingClassifier(random_state=42),
                       'params': {'n_estimators': [50, 100, 200],
                                  'learning_rate': [0.01, 0.1, 1],
                                  'max_depth': [1, 2, 3]}, 'task': 'classification'},
            'BC':{'model': BaggingClassifier(random_state=42, n_jobs=-1),
                       'params': {'n_estimators': [10, 50, 100],
                                  'max_samples': [0.5, 0.75, 1.0]}, 'task': 'classification'},
            'NBC':{'model': BernoulliNB(),
                       'params': {'alpha': [0.01, 0.1, 1.0]}, 'task': 'classification'},
            'Linear': {'model': LinearRegression(), 'params': {}, 'task': 'regression'},
            'RFR': {'model': RandomForestRegressor(random_state=42, n_jobs=-1),
                       'params': {'max_depth': [None, 10, 15, 20],
                                  'n_estimators': [10, 100, 150, 200],
                                  'min_samples_leaf': [2, 3, 4],
                                  'max_features': ['sqrt', 'log2', None]}, 'task': 'regression'},
            'XGBR': {'model': XGBRegressor(random_state=42, n_jobs=-1),
                       'params': {'booster': ['gbtree', 'dart'],
                                  'n_estimators': [100, 150, 200],
                                  'learning_rate': [0.01, 0.1, 0.2],
                                  'max_depth': [3, 4, 5],
                                  'min_child_weight': [1, 5],
                                  'subsample': [0.8, 1.0],
                                  'colsample_bytree': [0.8, 1.0],
                                  'gamma': [0, 0.1]}, 'task': 'regression'},
            'KNNR': {'model': KNeighborsRegressor(n_jobs=-1),
                       'params': {'n_neighbors': [3, 5, 7, 9, 10, 11],
                                  'weights': ['uniform', 'distance']}, 'task': 'regression'},
            'DTR': {'model': DecisionTreeRegressor(random_state=42),
                       'params': {'max_depth': [None, 10, 20, 30],
                                  'min_samples_split': [2, 5, 10],
                                  'min_samples_leaf': [1, 2, 4]}, 'task': 'regression'},
            'SVR': {'model': SVR(),
                       'params': {'kernel': ['linear', 'rbf'],
                                  'C': [0.1, 1, 10]}, 'task': 'regression'},
            'MLPR': {'model': MLPRegressor(max_iter=10000, random_state=42),
                       'params': {'hidden_layer_sizes': [(50,), (100,), (50, 50)],
                                  'activation': ['relu', 'tanh'],
                                  'solver': ['adam', 'sgd']}, 'task': 'regression'},
            'ADAR': {'model': AdaBoostRegressor(random_state=42),
                       'params': {'n_estimators': [50, 100, 200],
                                  'learning_rate': [0.01, 0.1, 1]}, 'task': 'regression'},
            'GBR': {'model': GradientBoostingRegressor(random_state=42),
                       'params': {'n_estimators': [50, 100, 200],
                                  'learning_rate': [0.01, 0.1, 1],
                                  'max_depth': [1, 2, 3]}, 'task': 'regression'},
            'BR': {'model': BaggingRegressor(random_state=42, n_jobs=-1),
                       'params': {'n_estimators': [10, 50, 100],
                                  'max_samples': [0.5, 0.75, 1.0]}, 'task': 'regression'},
            'NBR': {'model': BayesianRidge(max_iter=10000),
                       'params': {'n_iter': [100, 200, 300]}, 'task': 'regression'},
            'LRmulti': {'model': OneVsRestClassifier(LogisticRegression(max_iter=10000, random_state=42, n_jobs=-1), n_jobs=-1),
                           'params': [l2_params_multi, l1_params_multi, elasticnet_params_multi, none_params_multi], 'task': 'classification'},
            'RFmulti': {'model': OneVsRestClassifier(RandomForestClassifier(random_state=42, n_jobs=-1), n_jobs=-1),
                           'params': {'estimator__n_estimators': [50, 100, 150, 200],
                                      'estimator__max_depth': [None, 10, 15, 20],
                                      'estimator__min_samples_split': [2, 5, 10],
                                      'estimator__min_samples_leaf': [1, 2, 4],
                                      'estimator__max_features': ['sqrt', 'log2']}, 'task': 'classification'},
            'XGBmulti': {'model': OneVsRestClassifier(XGBClassifier(random_state=42), n_jobs=-1),
                           'params': {'estimator__booster': ['gbtree', 'dart'],
                                      'estimator__n_estimators': [100, 150, 200],
                                      'estimator__learning_rate': [0.01, 0.1, 0.2],
                                      'estimator__max_depth': [3, 4, 5],
                                      'estimator__min_child_weight': [1, 5],
                                      'estimator__subsample': [0.8, 1.0],
                                      'estimator__colsample_bytree': [0.8, 1.0],
                                      'estimator__gamma': [0, 0.1]}, 'task': 'classification'},
            'KNNmulti': {'model': OneVsRestClassifier(KNeighborsClassifier(n_jobs=-1), n_jobs=-1),
                           'params': {'estimator__n_neighbors': [3, 5, 7, 9, 10, 11],
                                      'estimator__weights': ['uniform', 'distance']}, 'task': 'classification'},
            'DTmulti': {'model': OneVsRestClassifier(DecisionTreeClassifier(random_state=42), n_jobs=-1),
                           'params': {'estimator__criterion': ['gini', 'entropy'],
                                      'estimator__max_depth': [None, 10, 20, 30],
                                      'estimator__min_samples_split': [2, 5, 10],
                                      'estimator__min_samples_leaf': [1, 2, 4]}, 'task': 'classification'},
            'SVCmulti': {'model': OneVsRestClassifier(SVC(random_state=42), n_jobs=-1),
                           'params': {'estimator__C': [0.1, 1, 10],
                                      'estimator__kernel': ['linear', 'rbf'],
                                      'estimator__gamma': ['scale', 'auto']}, 'task': 'classification'},
            'model7multi': {'model': OneVsRestClassifier(MLPClassifier(max_iter=10000, random_state=42), n_jobs=-1),
                           'params': {'estimator__hidden_layer_sizes': [(50,), (100,), (50, 50)],
                                      'estimator__activation': ['relu', 'tanh'],
                                      'estimator__solver': ['adam', 'sgd']}, 'task': 'classification'},
            'ADAmulti': {'model': OneVsRestClassifier(AdaBoostClassifier(algorithm='SAMME', random_state=42), n_jobs=-1),
                           'params': {'estimator__n_estimators': [50, 100, 200],
                                      'estimator__learning_rate': [0.01, 0.1, 1]}, 'task': 'classification'},
            'GBmulti': {'model': OneVsRestClassifier(GradientBoostingClassifier(random_state=42), n_jobs=-1),
                           'params': {'estimator__n_estimators': [50, 100, 200],
                                      'estimator__learning_rate': [0.01, 0.1, 1],
                                      'estimator__max_depth': [1, 2, 3]}, 'task': 'classification'},
            'BCmulti': {'model': OneVsRestClassifier(BaggingClassifier(random_state=42, n_jobs=-1), n_jobs=-1),
                            'params': {'estimator__n_estimators': [10, 50, 100],
                                       'estimator__max_samples': [0.5, 0.75, 1.0]}, 'task': 'classification'},
            'NBmulti': {'model': OneVsRestClassifier(ComplementNB(), n_jobs=-1),
                            'params': {'estimator__alpha': [0.01, 0.1, 1.0]}, 'task': 'classification'},
            'vote': {'model': VotingClassifier(estimators=selected_classifiers, voting=self.voting, n_jobs=-1),
                     'params': [selected_params], 'task': 'classification'},
        }

        def get_n_iter(param_grid):
            if isinstance(param_grid, list):
                total_combinations = sum(len(list(ParameterGrid(grid))) for grid in param_grid)
            else:
                total_combinations = len(list(ParameterGrid(param_grid)))
            return total_combinations

        if self.model_name not in models:
            raise ValueError(f"Unsupported model_name: {self.model_name}")
        model_info = models[self.model_name]
        model = model_info['model']
        params = model_info['params']
        task = model_info['task']

        if self.grid_search == 'cv':
            param_grid = params if isinstance(params, list) else [params]
            print("Parameter Grid:", param_grid)
            grid_search = GridSearchCV(model, param_grid, cv=self.cv,
                                       scoring='accuracy' if task == 'classification' else 'neg_mean_squared_error', n_jobs=-1)
            total_combinations = np.prod([len(v) for v in param_grid])
            with tqdm(total=total_combinations, desc="GridSearch Progress") as pbar:
                for parameters in ParameterGrid(param_grid):
                    model.set_params(**parameters)
                    grid_search.fit(X_train_preprocessed, y_train)
                    pbar.update(1)
            model = grid_search.best_estimator_
            print("Best parameters:", grid_search.best_params_)
            cv_results = pd.DataFrame(grid_search.cv_results_)
            display(cv_results.head())
            param_name = 'param_' + list(grid_search.best_params_.keys())[self.pa]
            if param_name in cv_results.columns:
                cv_results = cv_results.sort_values('mean_test_score', ascending=False)
                ax = cv_results.plot(x=param_name, y='mean_test_score', style='-o')
                ax.set(ylabel="Accuracy", title=f'Change in Test Accuracy Over Values for {param_name}')
                print()
        elif self.grid_search == 'rand':
            param_grid = params if isinstance(params, list) else [params]
            print("Parameter Grid:", param_grid)
            total_combinations = get_n_iter(param_grid)
            n_iter = min(total_combinations, 10)
            grid_search = RandomizedSearchCV(model, param_grid, cv=self.cv,
                                             scoring='accuracy' if task == 'classification' else 'neg_mean_squared_error',
                                             n_iter=n_iter, n_jobs=-1)
            with tqdm(total=n_iter, desc="RandomizedSearch Progress") as pbar:
                grid_search.fit(X_train_preprocessed, y_train)
                pbar.update(n_iter)
            model = grid_search.best_estimator_
            print('\n')
            print("Best parameters:", grid_search.best_params_)
            cv_results = pd.DataFrame(grid_search.cv_results_)
            display(cv_results.head())
            param_name = 'param_' + list(grid_search.best_params_.keys())[self.pa]
            if param_name in cv_results.columns:
                cv_results = cv_results.sort_values('mean_test_score', ascending=False)
                ax = cv_results.plot(x=param_name, y='mean_test_score', style='-o')
                ax.set(ylabel="Accuracy", title=f'Change in Test Accuracy Over Values for {param_name}')
                print()
        elif self.grid_search is None:
            model.fit(X_train_preprocessed, y_train)
        if task == 'classification':
            evaluate_classification(model, X_train_preprocessed, y_train, X_test_preprocessed, y_test)
        elif task == 'regression':
            evaluate_regression(model, X_train_preprocessed, y_train, X_test_preprocessed, y_test)
        return model