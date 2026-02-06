"""
GDP Growth Prediction Model Training Script
Fixes:
1. Data leakage via lagged features (T-1 to predict T)
2. Temporal train/test split
3. Consistent paths via config.py
4. Proper validation and error handling
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

# Import configuration
from config import (
    DATASET_PATH, MODEL_PATH, ENCODER_PATH,
    FEATURE_COLUMNS, TARGET_COLUMN,
    TEMPORAL_SPLIT_YEAR, MODEL_PARAMS
)


def create_lagged_features(df):
    """
    Create lagged features (T-1) to predict GDP at time T
    This prevents data leakage by using previous year's data
    
    Args:
        df: DataFrame with columns [Country, Year, features...]
    
    Returns:
        DataFrame with lagged features
    """
    print("\n📊 Creating lagged features (T-1)...")
    
    # Sort by Country and Year to ensure proper ordering
    df = df.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    # Create lagged features grouped by Country
    # This ensures data doesn't bleed between countries
    lagged_features = [
        'Population_Growth_Rate',
        'Exports of goods and services_Growth_Rate',
        'Imports of goods and services_Growth_Rate',
        'Gross capital formation_Growth_Rate',
        'Final consumption expenditure_Growth_Rate',
        'Government_Expenditure_Growth_Rate'
    ]
    
    for feature in lagged_features:
        # Shift by 1 within each country group
        df[f'{feature}_Lag1'] = df.groupby('Country')[feature].shift(1)
    
    # Drop rows with NaN values created by shifting
    # (first year for each country will have NaN)
    rows_before = len(df)
    df = df.dropna()
    rows_after = len(df)
    print(f"   Dropped {rows_before - rows_after} rows with NaN values from lagging")
    print(f"   Remaining samples: {rows_after}")
    
    return df


def temporal_train_test_split(df, split_year):
    """
    Split data temporally: train on years < split_year, test on years >= split_year
    This validates the model's ability to forecast future data
    
    Args:
        df: DataFrame with Year column
        split_year: Year to split on
    
    Returns:
        train_df, test_df
    """
    print(f"\n⏰ Performing temporal split at year {split_year}...")
    
    train_df = df[df['Year'] < split_year].copy()
    test_df = df[df['Year'] >= split_year].copy()
    
    print(f"   Training set: {len(train_df)} samples (years < {split_year})")
    print(f"   Test set: {len(test_df)} samples (years >= {split_year})")
    print(f"   Train years: {train_df['Year'].min()} - {train_df['Year'].max()}")
    print(f"   Test years: {test_df['Year'].min()} - {test_df['Year'].max()}")
    
    return train_df, test_df


def prepare_features(df, encoder=None, fit_encoder=False):
    """
    Prepare features for training/prediction
    
    Args:
        df: DataFrame with lagged features
        encoder: LabelEncoder for countries (optional)
        fit_encoder: Whether to fit the encoder
    
    Returns:
        X, y, encoder
    """
    # Encode country names
    if encoder is None:
        encoder = LabelEncoder()
        fit_encoder = True
    
    if fit_encoder:
        df['Country_Encoded'] = encoder.fit_transform(df['Country'])
    else:
        df['Country_Encoded'] = encoder.transform(df['Country'])
    
    # Rename lagged features to match config
    feature_mapping = {
        'Population_Growth_Rate_Lag1': 'Population_Growth_Rate_Lag1',
        'Exports of goods and services_Growth_Rate_Lag1': 'Exports_Growth_Rate_Lag1',
        'Imports of goods and services_Growth_Rate_Lag1': 'Imports_Growth_Rate_Lag1',
        'Gross capital formation_Growth_Rate_Lag1': 'Investment_Growth_Rate_Lag1',
        'Final consumption expenditure_Growth_Rate_Lag1': 'Consumption_Growth_Rate_Lag1',
        'Government_Expenditure_Growth_Rate_Lag1': 'Govt_Spend_Growth_Rate_Lag1'
    }
    
    df = df.rename(columns=feature_mapping)
    
    # Select features
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]
    
    return X, y, encoder


def evaluate_model(model, X_train, y_train, X_test, y_test):
    """
    Evaluate model performance on train and test sets
    """
    print("\n📈 Model Performance:")
    print("=" * 60)
    
    # Training performance
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    
    print(f"Training Set:")
    print(f"   R² Score: {train_r2:.4f}")
    print(f"   RMSE: {train_rmse:.4f}")
    print(f"   MAE: {train_mae:.4f}")
    
    # Test performance
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    
    print(f"\nTest Set (Future Prediction):")
    print(f"   R² Score: {test_r2:.4f}")
    print(f"   RMSE: {test_rmse:.4f}")
    print(f"   MAE: {test_mae:.4f}")
    
    print("=" * 60)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': FEATURE_COLUMNS,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print("\n🔍 Feature Importance:")
    for idx, row in feature_importance.iterrows():
        print(f"   {row['Feature']}: {row['Importance']:.4f}")


def main():
    """
    Main training pipeline
    """
    print("=" * 60)
    print("GDP Growth Prediction Model Training")
    print("=" * 60)
    
    # 1. Load data
    print(f"\n📂 Loading data from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"   Loaded {len(df)} samples")
    print(f"   Countries: {df['Country'].nunique()}")
    print(f"   Years: {df['Year'].min()} - {df['Year'].max()}")
    
    # 2. Create lagged features (Fix Issue #1: Data Leakage)
    df = create_lagged_features(df)
    
    # 3. Temporal train/test split (Fix Issue #2: Time-Series Awareness)
    train_df, test_df = temporal_train_test_split(df, TEMPORAL_SPLIT_YEAR)
    
    # 4. Prepare features
    print("\n🔧 Preparing features...")
    X_train, y_train, encoder = prepare_features(train_df, fit_encoder=True)
    X_test, y_test, _ = prepare_features(test_df, encoder=encoder, fit_encoder=False)
    
    print(f"   Training features shape: {X_train.shape}")
    print(f"   Test features shape: {X_test.shape}")
    
    # 5. Train model
    print(f"\n🤖 Training Random Forest Regressor...")
    print(f"   Parameters: {MODEL_PARAMS}")
    
    model = RandomForestRegressor(**MODEL_PARAMS)
    model.fit(X_train, y_train)
    
    print("   ✅ Training complete!")
    
    # 6. Evaluate model
    evaluate_model(model, X_train, y_train, X_test, y_test)
    
    # 7. Save model and encoder (Fix Issue #3: Consistent Paths)
    print(f"\n💾 Saving model to: {MODEL_PATH}")
    joblib.dump(model, MODEL_PATH)
    
    print(f"💾 Saving encoder to: {ENCODER_PATH}")
    joblib.dump(encoder, ENCODER_PATH)
    
    print("\n✅ Training pipeline complete!")
    print("=" * 60)
    
    # 8. Show example prediction
    print("\n🧪 Example Prediction:")
    sample = X_test.iloc[0:1]
    prediction = model.predict(sample)[0]
    actual = y_test.iloc[0]
    print(f"   Predicted GDP Growth: {prediction:.2f}%")
    print(f"   Actual GDP Growth: {actual:.2f}%")
    print(f"   Error: {abs(prediction - actual):.2f}%")


if __name__ == "__main__":
    main()
