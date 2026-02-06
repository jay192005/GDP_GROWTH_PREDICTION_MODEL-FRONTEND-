"""
Test script for refactored GDP Prediction API
Tests all endpoints and validation logic
"""

import requests
import json

BASE_URL = "http://localhost:5000"


def test_home():
    """Test home endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Home Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_countries():
    """Test countries endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Countries Endpoint")
    print("="*60)
    
    response = requests.get(f"{BASE_URL}/api/countries")
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        countries = response.json()
        print(f"Total Countries: {len(countries)}")
        print(f"First 10 Countries: {countries[:10]}")
    else:
        print(f"Error: {response.json()}")


def test_history():
    """Test history endpoint"""
    print("\n" + "="*60)
    print("TEST 3: History Endpoint")
    print("="*60)
    
    country = "United States"
    response = requests.get(f"{BASE_URL}/api/history", params={"country": country})
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Data points for {country}: {len(data)}")
        print(f"First record: {data[0]}")
        print(f"Last record: {data[-1]}")
    else:
        print(f"Error: {response.json()}")


def test_valid_prediction():
    """Test valid prediction"""
    print("\n" + "="*60)
    print("TEST 4: Valid Prediction")
    print("="*60)
    
    payload = {
        "Country": "United States",
        "Population": 1.1,
        "Exports": 5.2,
        "Imports": 4.8,
        "Investment": 3.5,
        "Consumption": 2.8,
        "Govt_Spend": 2.0
    }
    
    print(f"Request Payload: {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_missing_field():
    """Test prediction with missing field"""
    print("\n" + "="*60)
    print("TEST 5: Missing Field Validation")
    print("="*60)
    
    payload = {
        "Country": "United States",
        "Population": 1.1,
        "Exports": 5.2,
        # Missing: Imports, Investment, Consumption, Govt_Spend
    }
    
    print(f"Request Payload (incomplete): {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400


def test_invalid_value():
    """Test prediction with invalid value"""
    print("\n" + "="*60)
    print("TEST 6: Invalid Value Validation")
    print("="*60)
    
    payload = {
        "Country": "United States",
        "Population": "not_a_number",  # Invalid
        "Exports": 5.2,
        "Imports": 4.8,
        "Investment": 3.5,
        "Consumption": 2.8,
        "Govt_Spend": 2.0
    }
    
    print(f"Request Payload (invalid value): {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400


def test_unknown_country():
    """Test prediction with unknown country"""
    print("\n" + "="*60)
    print("TEST 7: Unknown Country Validation")
    print("="*60)
    
    payload = {
        "Country": "Atlantis",  # Non-existent country
        "Population": 1.1,
        "Exports": 5.2,
        "Imports": 4.8,
        "Investment": 3.5,
        "Consumption": 2.8,
        "Govt_Spend": 2.0
    }
    
    print(f"Request Payload (unknown country): {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400


def test_out_of_range():
    """Test prediction with out of range value"""
    print("\n" + "="*60)
    print("TEST 8: Out of Range Validation")
    print("="*60)
    
    payload = {
        "Country": "United States",
        "Population": 150.0,  # Unrealistic growth rate
        "Exports": 5.2,
        "Imports": 4.8,
        "Investment": 3.5,
        "Consumption": 2.8,
        "Govt_Spend": 2.0
    }
    
    print(f"Request Payload (out of range): {json.dumps(payload, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400


def run_all_tests():
    """Run all tests"""
    print("\n" + "🧪 " + "="*58)
    print("GDP PREDICTION API - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    tests = [
        ("Home Endpoint", test_home),
        ("Countries List", test_countries),
        ("Historical Data", test_history),
        ("Valid Prediction", test_valid_prediction),
        ("Missing Field", test_missing_field),
        ("Invalid Value", test_invalid_value),
        ("Unknown Country", test_unknown_country),
        ("Out of Range", test_out_of_range)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
            print(f"✅ {test_name} - PASSED")
        except Exception as e:
            failed += 1
            print(f"❌ {test_name} - FAILED: {e}")
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60)


if __name__ == "__main__":
    print("⚠️  Make sure the Flask server is running on http://localhost:5000")
    print("   Run: python app.py")
    input("\nPress Enter to start tests...")
    
    run_all_tests()
