from autots import AutoTS
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np
from datetime import datetime
from dateutil.parser import parse
import re
 
 
def autots_model_automate(df,date_column,target,join_col_name,forecast_length,frequency):
 
    model = AutoTS(
            forecast_length=forecast_length,
            frequency=frequency,  # 5-minute intervals
            prediction_interval=0.9,
            ensemble=None,  # Disable ensemble to save memory and CPU
            model_list=["ARIMA"],  # Use a smaller set of simple models
            transformer_list=None,  # Reduces data preprocessing overhead
            max_generations=1,  # Keep low to avoid memory spikes
            num_validations=1,  # Minimal validation to conserve RAM
            n_jobs=5,  # Run models sequentially to avoid overloading memory
            verbose=False  # Helps track what's happening if it crashes again
 
            )

    try:
        model = model.fit(df, date_col=date_column, value_col=target, id_col=join_col_name)
        forecast = model.predict().forecast
        print(model.score_breakdown,"=-=-=-=-=-=-=-=-=-=-=-=*******score_breakdown***********-------------------------------------------************")
        best_scores = model.score_breakdown[model.score_breakdown.index == model.best_model_id]
        print("best_scores-=====-=-=-=-=-=-=-=-=-=-=--",best_scores)
        SMAPE_Score = best_scores.mean().get('smape')
        mape_Score = (SMAPE_Score / 2) * (1 + (SMAPE_Score / 100))
 
        return forecast, mape_Score
 
    except KeyError as e:
        if 'TransformationParameters' in str(e):
            print("Error: Missing 'TransformationParameters' in the template.")
        else:
            print(f"Unexpected KeyError: {e}")
 
    except Exception as e:
        print(f"An error occurred: {e}")
 
    return None, None
 
def auto_robust_parse_date(val):
    """
    Try to parse a value as a date.
    - If the value is an 8-digit number, assume YYYYMMDD.
    - Otherwise, require that the string contains at least one typical date delimiter ('-', '/', or '.'),
      and does NOT contain letters mixed with numbers.
    - If these conditions are not met, return NaT.
    Returns a datetime if parsing succeeds and the year is plausible; otherwise returns pd.NaT.
    """
    s = str(val).strip()
    if not s:
        return pd.NaT
 
    # If the string is all digits and exactly 8 characters, assume YYYYMMDD.
    if s.isdigit() and len(s) == 8:
        try:
            dt = datetime.strptime(s, '%Y%m%d')
            if 1900 <= dt.year <= 2100:
                return dt
        except ValueError:
            return pd.NaT
 
    # If it contains any letters, do not attempt parsing.
    if re.search(r"[A-Za-z]", s):
        return pd.NaT
 
    # For non-digit-only strings, require a delimiter (-, /, .).
    if not any(delim in s for delim in ['-', '/', '.']):
        return pd.NaT
 
    try:
        dt = parse(s, fuzzy=False)  # Set fuzzy=False to avoid extracting parts of strings
        if 1900 <= dt.year <= 2100:
            return dt
    except Exception:
        return pd.NaT
 
    return pd.NaT
 
# -----------------------------------------------------------
# Function to Auto-detect Multiple Datetime Columns
# -----------------------------------------------------------
def auto_detect_datetime_columns(df, selected_cols, threshold=0.8, exclude_non_date_text=True):
    """
    Detect all columns in selected_cols that have a high fraction of datetime values.
    
    Parameters:
    - df: Pandas DataFrame
    - selected_cols: List of columns to check
    - threshold: Minimum fraction of valid datetime values to classify as datetime (default 80%)
    - exclude_non_date_text: Whether to exclude columns with alphanumeric non-date patterns.
 
    Returns:
    - List of column names that qualify as datetime columns
    - Dictionary of columns with their datetime ratio
    """
    date_cols = []
    datetime_ratios = {}
 
    for col in selected_cols:
        # Only consider columns that are object or mixed type.
        if not pd.api.types.is_object_dtype(df[col]):
            continue
        
        # Exclude columns with non-date-like alphanumeric values
        if exclude_non_date_text:
            alphanumeric_ratio = df[col].astype(str).str.contains(r"[A-Za-z].*\d|\d.*[A-Za-z]").mean()
            if alphanumeric_ratio > 0.5:  # If more than 50% contain mixed text/numbers, ignore
                continue
 
        parsed = df[col].apply(auto_robust_parse_date)
        ratio = parsed.notnull().mean()  # Fraction of valid datetime parses.
 
        # Store results
        datetime_ratios[col] = ratio
 
        if ratio >= threshold:
            date_cols.append(col)
 
    return date_cols, datetime_ratios
 
def autots_run_pipeline(df, selected_feature, target, forecast_length, frequency):
    datetime_column = None
    valid_datetime_columns = []
    join_on_symbol = '__Jos__'
 
    # for feature in selected_feature[:]:  # Iterate over a copy
    #     if feature in df.columns:
    #         # ✅ Ensure only object or datetime columns are considered
    #         if not pd.api.types.is_object_dtype(df[feature]) and not pd.api.types.is_datetime64_any_dtype(df[feature]):
    #             continue  # Skip non-date columns (like latitude)
 
    #         try:
    #             converted = pd.to_datetime(df[feature], errors="coerce", infer_datetime_format=True)
                
    #             # ✅ Only store it if all values are valid datetime (no NaT values)
    #             if converted.notna().all():  
    #                 valid_datetime_columns.append(feature)
 
    #                 # ✅ Select the first valid datetime column
    #                 if datetime_column is None:
    #                     df[feature] = converted
    #                     datetime_column = feature
 
    #         except Exception as e:
    #             print(f"Error converting {feature}: {e}")
    #             continue  # Skip to the next feature if there's an error
 
    # # ✅ Remove all valid datetime columns from selected_feature
 
    valid_datetime_columns, best_ratio = auto_detect_datetime_columns(df, selected_feature)
    selected_feature = [col for col in selected_feature if col not in valid_datetime_columns]
 
    print(f"Valid datetime columns: {valid_datetime_columns}")
    print(f"Selected feature: {selected_feature}")
    # print(datetime_column)
    
    date_column = valid_datetime_columns[0]
    features = selected_feature
    target = target
 
    print(date_column, target, features)
 
    join_col_name = join_on_symbol.join(features)  # Join with '__|__'
    print(join_col_name,'join_col_name-=========================================================---------------------')
    df[join_col_name] = df[features].astype(str).agg(join_on_symbol.join, axis=1)
 
    df = df[[date_column, target, join_col_name]]
    print(df.head())
 
    df[date_column] = pd.to_datetime(df[date_column], errors="coerce")
    try:
        forecasted_df,smape_score=autots_model_automate(df,date_column,target,join_col_name,forecast_length,frequency)
        print(forecasted_df)
        forecast_df = forecasted_df.reset_index().rename(columns={"index":date_column})
        df_melted = forecast_df.melt(id_vars=[date_column], var_name=join_col_name, value_name=target)
 
        # df_melted=df_melted[[date_column,join_col_name,target]]
        original_col=join_col_name.split(join_on_symbol)
 
        
    
        df_melted[original_col] = df_melted[join_col_name].str.split(join_on_symbol, expand=True)
        # print(split_df.head())
        if len(selected_feature)>1:
            df_melted.drop(columns=[join_col_name], inplace=True)
 
        print(df_melted.head())
        forecasted_df=df_melted[[date_column]+original_col+[target]]
 
        return forecasted_df,smape_score
    
    except Exception as e:
        return None,None
 
 
 
 
 
 
 