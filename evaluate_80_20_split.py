"""
Evaluate GDP Prediction Model using 80/20 Train-Test Split
Compares temporal split vs random split performance
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
import joblib
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from config import DATASET_PATH, MODEL_PARAMS


def create_lagged_features(df):
    """Create lagged features (T-1) to predict GDP at time T"""
    print("\n📊 Creating lagged features (T-1)...")
    df = df.sort_values(['Country', 'Year']).reset_index(drop=True)
    
    lagged_features = [
        'Population_Growth_Rate',
        'Exports of goods and services_Growth_Rate',
        'Imports of goods and services_Growth_Rate',
        'Gross capital formation_Growth_Rate',
        'Final consumption expenditure_Growth_Rate',
        'Government_Expenditure_Growth_Rate'
    ]
    
    for feature in lagged_features:
        df[f'{feature}_Lag1'] = df.groupby('Country')[feature].shift(1)
    
    rows_before = len(df)
    df = df.dropna()
    rows_after = len(df)
    print(f"   Dropped {rows_before - rows_after} rows with NaN values")
    print(f"   Remaining samples: {rows_after}")
    
    return df


def prepare_features(df, encoder=None, fit_encoder=False):
    """Prepare features for training/prediction"""
    if encoder is None:
        encoder = LabelEncoder()
        fit_encoder = True
    
    if fit_encoder:
        df['Country_Encoded'] = encoder.fit_transform(df['Country'])
    else:
        df['Country_Encoded'] = encoder.transform(df['Country'])
    
    # Rename lagged features
    feature_mapping = {
        'Population_Growth_Rate_Lag1': 'Population_Growth_Rate_Lag1',
        'Exports of goods and services_Growth_Rate_Lag1': 'Exports_Growth_Rate_Lag1',
        'Imports of goods and services_Growth_Rate_Lag1': 'Imports_Growth_Rate_Lag1',
        'Gross capital formation_Growth_Rate_Lag1': 'Investment_Growth_Rate_Lag1',
        'Final consumption expenditure_Growth_Rate_Lag1': 'Consumption_Growth_Rate_Lag1',
        'Government_Expenditure_Growth_Rate_Lag1': 'Govt_Spend_Growth_Rate_Lag1'
    }
    
    df = df.rename(columns=feature_mapping)
    
    feature_columns = [
        'Country_Encoded',
        'Population_Growth_Rate_Lag1',
        'Exports_Growth_Rate_Lag1',
        'Imports_Growth_Rate_Lag1',
        'Investment_Growth_Rate_Lag1',
        'Consumption_Growth_Rate_Lag1',
        'Govt_Spend_Growth_Rate_Lag1'
    ]
    
    X = df[feature_columns]
    y = df['GDP_Growth_Rate']
    
    return X, y, encoder


def evaluate_model(model, X_train, y_train, X_test, y_test, split_name):
    """Evaluate model performance"""
    print(f"\n{'='*60}")
    print(f"{split_name} - Model Performance")
    print(f"{'='*60}")
    
    # Training performance
    y_train_pred = model.predict(X_train)
    train_r2 = r2_score(y_train, y_train_pred)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
    train_mae = mean_absolute_error(y_train, y_train_pred)
    train_mape = mean_absolute_percentage_error(y_train, y_train_pred) * 100
    
    print(f"\n📊 Training Set ({len(X_train)} samples):")
    print(f"   R² Score:  {train_r2:.4f}")
    print(f"   RMSE:      {train_rmse:.4f}")
    print(f"   MAE:       {train_mae:.4f}")
    print(f"   MAPE:      {train_mape:.2f}%")
    
    # Test performance
    y_test_pred = model.predict(X_test)
    test_r2 = r2_score(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_mape = mean_absolute_percentage_error(y_test, y_test_pred) * 100
    
    print(f"\n📊 Test Set ({len(X_test)} samples):")
    print(f"   R² Score:  {test_r2:.4f}")
    print(f"   RMSE:      {test_rmse:.4f}")
    print(f"   MAE:       {test_mae:.4f}")
    print(f"   MAPE:      {test_mape:.2f}%")
    
    # Overfitting check
    overfit_score = train_r2 - test_r2
    print(f"\n🔍 Overfitting Analysis:")
    print(f"   Train R² - Test R²: {overfit_score:.4f}")
    if overfit_score < 0.1:
        print(f"   Status: ✅ Good generalization")
    elif overfit_score < 0.2:
        print(f"   Status: ⚠️ Slight overfitting")
    else:
        print(f"   Status: ❌ Significant overfitting")
    
    return {
        'train_r2': train_r2,
        'train_rmse': train_rmse,
        'train_mae': train_mae,
        'train_mape': train_mape,
        'test_r2': test_r2,
        'test_rmse': test_rmse,
        'test_mae': test_mae,
        'test_mape': test_mape,
        'y_test': y_test,
        'y_test_pred': y_test_pred
    }


def plot_predictions(results_80_20, results_temporal):
    """Plot prediction comparisons"""
    fig, axes = plt.subplots(1, 2, figsize=(15, 5))
    
    # 80/20 Split
    ax1 = axes[0]
    ax1.scatter(results_80_20['y_test'], results_80_20['y_test_pred'], alpha=0.5)
    ax1.plot([results_80_20['y_test'].min(), results_80_20['y_test'].max()],
             [results_80_20['y_test'].min(), results_80_20['y_test'].max()],
             'r--', lw=2)
    ax1.set_xlabel('Actual GDP Growth Rate (%)')
    ax1.set_ylabel('Predicted GDP Growth Rate (%)')
    ax1.set_title(f'80/20 Random Split\nR² = {results_80_20["test_r2"]:.4f}')
    ax1.grid(True, alpha=0.3)
    
    # Temporal Split
    ax2 = axes[1]
    ax2.scatter(results_temporal['y_test'], results_temporal['y_test_pred'], alpha=0.5)
    ax2.plot([results_temporal['y_test'].min(), results_temporal['y_test'].max()],
             [results_temporal['y_test'].min(), results_temporal['y_test'].max()],
             'r--', lw=2)
    ax2.set_xlabel('Actual GDP Growth Rate (%)')
    ax2.set_ylabel('Predicted GDP Growth Rate (%)')
    ax2.set_title(f'Temporal Split (2019+)\nR² = {results_temporal["test_r2"]:.4f}')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('model_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\n📊 Comparison plot saved as 'model_comparison.png'")


def main():
    """Main evaluation pipeline"""
    print("=" * 60)
    print("GDP PREDICTION MODEL - 80/20 SPLIT EVALUATION")
    print("=" * 60)
    
    # Load data
    print(f"\n📂 Loading data from: {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"   Loaded {len(df)} samples")
    print(f"   Countries: {df['Country'].nunique()}")
    print(f"   Years: {df['Year'].min()} - {df['Year'].max()}")
    
    # Create lagged features
    df = create_lagged_features(df)
    
    # ========================================
    # METHOD 1: 80/20 Random Split
    # ========================================
    print("\n" + "=" * 60)
    print("METHOD 1: 80/20 RANDOM SPLIT")
    print("=" * 60)
    
    # Prepare features
    X, y, encoder_80_20 = prepare_features(df.copy(), fit_encoder=True)
    
    # 80/20 split with shuffle
    X_train_80, X_test_80, y_train_80, y_test_80 = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42,
        shuffle=True
    )
    
    print(f"\n📊 Data Split:")
    print(f"   Training: {len(X_train_80)} samples (80%)")
    print(f"   Test: {len(X_test_80)} samples (20%)")
    
    # Train model
    print(f"\n🤖 Training Random Forest...")
    model_80_20 = RandomForestRegressor(**MODEL_PARAMS)
    model_80_20.fit(X_train_80, y_train_80)
    print(f"   ✅ Training complete!")
    
    # Evaluate
    results_80_20 = evaluate_model(
        model_80_20, X_train_80, y_train_80, X_test_80, y_test_80,
        "80/20 Random Split"
    )
    
    # ========================================
    # METHOD 2: Temporal Split (for comparison)
    # ========================================
    print("\n" + "=" * 60)
    print("METHOD 2: TEMPORAL SPLIT (2019+)")
    print("=" * 60)
    
    # Temporal split
    train_df = df[df['Year'] < 2019].copy()
    test_df = df[df['Year'] >= 2019].copy()
    
    print(f"\n📊 Data Split:")
    print(f"   Training: {len(train_df)} samples (years < 2019)")
    print(f"   Test: {len(test_df)} samples (years >= 2019)")
    
    # Prepare features
    X_train_temp, y_train_temp, encoder_temp = prepare_features(train_df, fit_encoder=True)
    X_test_temp, y_test_temp, _ = prepare_features(test_df, encoder=encoder_temp, fit_encoder=False)
    
    # Train model
    print(f"\n🤖 Training Random Forest...")
    model_temporal = RandomForestRegressor(**MODEL_PARAMS)
    model_temporal.fit(X_train_temp, y_train_temp)
    print(f"   ✅ Training complete!")
    
    # Evaluate
    results_temporal = evaluate_model(
        model_temporal, X_train_temp, y_train_temp, X_test_temp, y_test_temp,
        "Temporal Split"
    )
    
    # ========================================
    # COMPARISON
    # ========================================
    print("\n" + "=" * 60)
    print("COMPARISON: 80/20 vs TEMPORAL SPLIT")
    print("=" * 60)
    
    comparison_df = pd.DataFrame({
        'Metric': ['Train R²', 'Test R²', 'Train RMSE', 'Test RMSE', 'Train MAE', 'Test MAE', 'Train MAPE', 'Test MAPE'],
        '80/20 Split': [
            f"{results_80_20['train_r2']:.4f}",
            f"{results_80_20['test_r2']:.4f}",
            f"{results_80_20['train_rmse']:.4f}",
            f"{results_80_20['test_rmse']:.4f}",
            f"{results_80_20['train_mae']:.4f}",
            f"{results_80_20['test_mae']:.4f}",
            f"{results_80_20['train_mape']:.2f}%",
            f"{results_80_20['test_mape']:.2f}%"
        ],
        'Temporal Split': [
            f"{results_temporal['train_r2']:.4f}",
            f"{results_temporal['test_r2']:.4f}",
            f"{results_temporal['train_rmse']:.4f}",
            f"{results_temporal['test_rmse']:.4f}",
            f"{results_temporal['train_mae']:.4f}",
            f"{results_temporal['test_mae']:.4f}",
            f"{results_temporal['train_mape']:.2f}%",
            f"{results_temporal['test_mape']:.2f}%"
        ]
    })
    
    print("\n" + comparison_df.to_string(index=False))
    
    # Key insights
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    
    print("\n1️⃣ 80/20 Random Split:")
    print(f"   ✅ Higher test R² ({results_80_20['test_r2']:.4f})")
    print(f"   ✅ Lower test RMSE ({results_80_20['test_rmse']:.4f})")
    print(f"   ⚠️ May not reflect real forecasting ability")
    print(f"   ⚠️ Test set contains data from all years (1973-2021)")
    
    print("\n2️⃣ Temporal Split:")
    print(f"   📊 Lower test R² ({results_temporal['test_r2']:.4f})")
    print(f"   📊 Higher test RMSE ({results_temporal['test_rmse']:.4f})")
    print(f"   ✅ Realistic forecasting validation")
    print(f"   ✅ Tests on actual future data (2019-2021)")
    
    print("\n3️⃣ Recommendation:")
    if results_80_20['test_r2'] > results_temporal['test_r2']:
        diff = results_80_20['test_r2'] - results_temporal['test_r2']
        print(f"   📌 80/20 split shows {diff:.4f} higher R² than temporal split")
        print(f"   📌 This is expected! 80/20 split is easier because:")
        print(f"      - Test data is randomly mixed with training years")
        print(f"      - Model sees similar patterns in test set")
        print(f"   📌 For production deployment, use TEMPORAL SPLIT")
        print(f"      - It validates actual forecasting ability")
        print(f"      - More honest about model performance")
    
    # Plot comparison
    try:
        plot_predictions(results_80_20, results_temporal)
    except Exception as e:
        print(f"\n⚠️ Could not create plot: {e}")
    
    # Save comparison report
    print("\n💾 Saving comparison report...")
    with open('80_20_evaluation_report.txt', 'w') as f:
        f.write("GDP PREDICTION MODEL - 80/20 SPLIT EVALUATION\n")
        f.write("=" * 60 + "\n\n")
        f.write(comparison_df.to_string(index=False))
        f.write("\n\n" + "=" * 60 + "\n")
        f.write("KEY INSIGHTS\n")
        f.write("=" * 60 + "\n\n")
        f.write("80/20 Random Split:\n")
        f.write(f"  Test R²: {results_80_20['test_r2']:.4f}\n")
        f.write(f"  Test RMSE: {results_80_20['test_rmse']:.4f}\n")
        f.write(f"  Test MAE: {results_80_20['test_mae']:.4f}\n\n")
        f.write("Temporal Split:\n")
        f.write(f"  Test R²: {results_temporal['test_r2']:.4f}\n")
        f.write(f"  Test RMSE: {results_temporal['test_rmse']:.4f}\n")
        f.write(f"  Test MAE: {results_temporal['test_mae']:.4f}\n")
    
    print(f"   ✅ Report saved as '80_20_evaluation_report.txt'")
    
    print("\n" + "=" * 60)
    print("EVALUATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
