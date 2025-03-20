import numpy as np
import pandas as pd
from IPython.display import display

class Convert:
    def __init__(self, df, target):
        self.df = df.copy()
        self.target = target

    def apply(self, ncol=None, ocol=None, ordinal_cols=None, ord_threshold=None, ordname=(), drop_cols=(), typeval=80, convrate=80):
        df = self.df.copy()
        target = self.target

        if not ncol:
            ncol = [col for col in df.select_dtypes(include=['float64', 'int64']).columns.tolist() if col != target]
        if not ocol:
            ocol = [col for col in df.select_dtypes(include=['object']).columns.tolist() if col != target]

        if not ordinal_cols:
            ordinal_cols = {}
            if ord_threshold is not None:
                for col in df.columns:
                    if df[col].dtype == 'object' and df[col].nunique() <= ord_threshold:
                        ordinal_cols[col] = df[col].unique().tolist()

        if ordname:
            if isinstance(ordname, str):
                ordname = [ordname]
            for col in ordname:
                if col in ocol:
                    ordinal_cols[col] = sorted(df[col].unique())
                    ocol.remove(col)

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