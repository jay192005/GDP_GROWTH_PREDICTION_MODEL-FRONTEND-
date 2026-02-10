"""
Verify that predictions come from ML model, not simple formula
"""

import requests
import json

BASE_URL = "http://localhost:5000"

print("=" * 60)
print("VERIFYING ML MODEL vs FORMULA")
print("=" * 60)

# Test 1: Same inputs should give same output (ML model consistency)
print("\n1️⃣ Test ML Model Consistency")
print("-" * 60)

scenario1 = {
    "Country": "United States",
    "Population_Growth_Rate": 1.0,
    "Exports_Growth_Rate": 5.0,
    "Imports_Growth_Rate": 4.0,
    "Investment_Growth_Rate": 3.0,
    "Consumption_Growth_Rate": 2.0,
    "Govt_Spend_Growth_Rate": 2.0
}

# Make same request twice
r1 = requests.post(f"{BASE_URL}/simulate", json=scenario1)
r2 = requests.post(f"{BASE_URL}/simulate", json=scenario1)

result1 = r1.json()['predicted_gdp_growth']
result2 = r2.json()['predicted_gdp_growth']

print(f"First prediction: {result1}%")
print(f"Second prediction: {result2}%")
print(f"Consistent: {'✅ YES' if result1 == result2 else '❌ NO'}")

# Test 2: Simple formula check
print("\n2️⃣ Test Against Simple Formula")
print("-" * 60)

# If it were using GDP = C + I + G + (X - M), the result would be:
simple_formula = (
    scenario1['Consumption_Growth_Rate'] +
    scenario1['Investment_Growth_Rate'] +
    scenario1['Govt_Spend_Growth_Rate'] +
    (scenario1['Exports_Growth_Rate'] - scenario1['Imports_Growth_Rate'])
)

print(f"ML Model prediction: {result1}%")
print(f"Simple formula (C+I+G+(X-M)): {simple_formula}%")
print(f"Difference: {abs(result1 - simple_formula):.2f}%")

if abs(result1 - simple_formula) > 0.5:
    print("✅ Using ML MODEL (predictions differ from simple formula)")
else:
    print("⚠️ Might be using simple formula (predictions too similar)")

# Test 3: Non-linear behavior check
print("\n3️⃣ Test Non-Linear Behavior")
print("-" * 60)

# Test with different consumption values
test_cases = [
    {"Consumption_Growth_Rate": 2.0, "label": "Consumption 2%"},
    {"Consumption_Growth_Rate": 4.0, "label": "Consumption 4%"},
    {"Consumption_Growth_Rate": 8.0, "label": "Consumption 8%"},
]

predictions = []
for test in test_cases:
    scenario = scenario1.copy()
    scenario['Consumption_Growth_Rate'] = test['Consumption_Growth_Rate']
    
    r = requests.post(f"{BASE_URL}/simulate", json=scenario)
    pred = r.json()['predicted_gdp_growth']
    predictions.append(pred)
    
    print(f"{test['label']}: GDP = {pred}%")

# Check if relationship is linear
diff1 = predictions[1] - predictions[0]
diff2 = predictions[2] - predictions[1]

print(f"\nDifference 2% → 4%: {diff1:.2f}%")
print(f"Difference 4% → 8%: {diff2:.2f}%")

if abs(diff1 - diff2) > 0.1:
    print("✅ Non-linear behavior detected (ML model)")
else:
    print("⚠️ Linear behavior (might be simple formula)")

# Test 4: Country-specific predictions
print("\n4️⃣ Test Country-Specific Predictions")
print("-" * 60)

countries = ["United States", "China", "India"]
country_predictions = []

for country in countries:
    scenario = scenario1.copy()
    scenario['Country'] = country
    
    r = requests.post(f"{BASE_URL}/simulate", json=scenario)
    pred = r.json()['predicted_gdp_growth']
    country_predictions.append(pred)
    
    print(f"{country}: GDP = {pred}%")

# Check if predictions differ by country
if len(set(country_predictions)) > 1:
    print("✅ Country-specific predictions (ML model uses country encoding)")
else:
    print("⚠️ Same prediction for all countries")

# Test 5: Complex scenario
print("\n5️⃣ Test Complex Scenario")
print("-" * 60)

complex_scenario = {
    "Country": "Germany",
    "Population_Growth_Rate": 0.3,
    "Exports_Growth_Rate": 12.5,
    "Imports_Growth_Rate": 8.7,
    "Investment_Growth_Rate": 6.2,
    "Consumption_Growth_Rate": 4.8,
    "Govt_Spend_Growth_Rate": 3.1
}

r = requests.post(f"{BASE_URL}/simulate", json=complex_scenario)
result = r.json()

print(f"Scenario: {json.dumps(complex_scenario, indent=2)}")
print(f"\nML Model Prediction: {result['predicted_gdp_growth']}%")
print(f"Model Type: {result['model_type']}")

# Calculate what simple formula would give
simple_calc = (
    complex_scenario['Consumption_Growth_Rate'] +
    complex_scenario['Investment_Growth_Rate'] +
    complex_scenario['Govt_Spend_Growth_Rate'] +
    (complex_scenario['Exports_Growth_Rate'] - complex_scenario['Imports_Growth_Rate'])
)

print(f"Simple Formula: {simple_calc}%")
print(f"Difference: {abs(result['predicted_gdp_growth'] - simple_calc):.2f}%")

# Test 6: Check model file
print("\n6️⃣ Verify Model File")
print("-" * 60)

import os
import joblib

if os.path.exists('gdp_scenario_model.pkl'):
    print("✅ Model file exists: gdp_scenario_model.pkl")
    
    # Load and inspect model
    model = joblib.load('gdp_scenario_model.pkl')
    print(f"✅ Model type: {type(model).__name__}")
    print(f"✅ Model class: {model.__class__.__module__}.{model.__class__.__name__}")
    
    if hasattr(model, 'n_estimators'):
        print(f"✅ Number of trees: {model.n_estimators}")
    if hasattr(model, 'feature_importances_'):
        print(f"✅ Feature importances available: {len(model.feature_importances_)} features")
else:
    print("❌ Model file not found!")

# Final verdict
print("\n" + "=" * 60)
print("FINAL VERDICT")
print("=" * 60)

checks = [
    ("Model Consistency", result1 == result2),
    ("Different from Formula", abs(result1 - simple_formula) > 0.5),
    ("Non-linear Behavior", abs(diff1 - diff2) > 0.1),
    ("Country-Specific", len(set(country_predictions)) > 1),
    ("Model File Exists", os.path.exists('gdp_scenario_model.pkl'))
]

passed = sum(1 for _, check in checks if check)
total = len(checks)

print(f"\nChecks Passed: {passed}/{total}")
for name, result in checks:
    print(f"  {'✅' if result else '❌'} {name}")

if passed >= 4:
    print("\n✅ CONFIRMED: Using ML MODEL (Random Forest)")
    print("   Predictions come from trained model, not simple formula")
elif passed >= 2:
    print("\n⚠️ LIKELY: Using ML MODEL with some formula elements")
else:
    print("\n❌ WARNING: Might be using simple formula")

print("\n" + "=" * 60)
