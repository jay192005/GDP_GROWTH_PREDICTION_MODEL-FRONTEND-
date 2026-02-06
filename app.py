"""
GDP Growth Prediction API - Flask Backend
Fixes:
1. Uses lagged features (T-1) for prediction
2. Proper input validation with error handling
3. Consistent paths via config.py
4. Clear error messages
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import traceback

# Import configuration (Fix Issue #3: Consistent Paths)
from config import DATASET_PATH, MODEL_PATH, ENCODER_PATH

app = Flask(__name__)
CORS(app)

# Global variables for model and data
model = None
encoder = None
df_history = None


def load_model_and_data():
    """
    Load ML model, encoder, and historical data
    """
    global model, encoder, df_history
    
    # Load Model & Encoder
    try:
        model = joblib.load(MODEL_PATH)
        encoder = joblib.load(ENCODER_PATH)
        print(f"✅ Model loaded from: {MODEL_PATH}")
        print(f"✅ Encoder loaded from: {ENCODER_PATH}")
    except Exception as e:
        print(f"⚠️ Model/Encoder not found. Error: {e}")
        print("Predictions will use fallback simulation.")
        model = None
        encoder = None
    
    # Load Historical Data
    try:
        df_history = pd.read_csv(DATASET_PATH)
        
        # Select columns for frontend
        df_history = df_history[[
            'Country', 
            'Year', 
            'GDP_Growth_Rate', 
            'Exports of goods and services_Growth_Rate', 
            'Imports of goods and services_Growth_Rate'
        ]]
        
        # Rename for simplicity
        df_history.columns = [
            'Country', 'Year', 'GDP_Growth', 
            'Exports_Growth', 'Imports_Growth'
        ]
        
        print(f"✅ Historical data loaded from: {DATASET_PATH}")
        print(f"   Countries: {df_history['Country'].nunique()}")
        print(f"   Years: {df_history['Year'].min()} - {df_history['Year'].max()}")
        
    except Exception as e:
        print(f"⚠️ Historical Data Error: {e}")
        df_history = pd.DataFrame()


# Load on startup
load_model_and_data()


@app.route('/')
def home():
    """
    API health check and information
    """
    return jsonify({
        'message': 'GDP Growth Prediction API',
        'status': 'running',
        'version': 'v3.0-refactored',
        'model_loaded': model is not None,
        'encoder_loaded': encoder is not None,
        'data_loaded': not df_history.empty if df_history is not None else False,
        'endpoints': {
            '/': 'GET - API information',
            '/api/countries': 'GET - List all countries',
            '/api/history': 'GET - Historical data for a country (param: country)',
            '/predict': 'POST - Predict GDP growth rate'
        },
        'note': 'Model uses lagged features (T-1) to predict GDP at time T'
    })


@app.route('/api/countries', methods=['GET'])
def get_countries():
    """
    Get list of all available countries
    """
    try:
        if df_history is None or df_history.empty:
            return jsonify({
                'error': 'Historical data not available'
            }), 500
        
        countries = sorted(df_history['Country'].unique().tolist())
        return jsonify(countries)
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve countries',
            'details': str(e)
        }), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Get historical GDP data for a specific country
    """
    try:
        country = request.args.get('country')
        
        if not country:
            return jsonify({
                'error': 'Missing required parameter: country'
            }), 400
        
        if df_history is None or df_history.empty:
            return jsonify({
                'error': 'Historical data not available'
            }), 500
        
        # Filter for country
        country_data = df_history[df_history['Country'] == country].sort_values('Year')
        
        if country_data.empty:
            return jsonify({
                'error': f'No data found for country: {country}'
            }), 404
        
        # Convert to JSON
        data_json = country_data.replace({np.nan: None}).to_dict(orient='records')
        return jsonify(data_json)
    
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve historical data',
            'details': str(e)
        }), 500


def validate_prediction_input(data):
    """
    Validate incoming prediction request (Fix Issue #4: Input Validation)
    
    Args:
        data: JSON request data
    
    Returns:
        tuple: (is_valid, error_message, validated_data)
    """
    required_fields = [
        'Country',
        'Population',
        'Exports',
        'Imports',
        'Investment',
        'Consumption',
        'Govt_Spend'
    ]
    
    # Check if data exists
    if not data:
        return False, 'Request body is empty', None
    
    # Check for missing fields
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f'Missing required fields: {", ".join(missing_fields)}', None
    
    # Validate and convert to float
    validated_data = {}
    
    # Country should be string
    try:
        validated_data['Country'] = str(data['Country']).strip()
        if not validated_data['Country']:
            return False, 'Country name cannot be empty', None
    except Exception:
        return False, 'Invalid Country value', None
    
    # Numeric fields should be convertible to float
    numeric_fields = [
        'Population', 'Exports', 'Imports', 
        'Investment', 'Consumption', 'Govt_Spend'
    ]
    
    for field in numeric_fields:
        try:
            value = float(data[field])
            
            # Check for reasonable ranges (growth rates typically -100% to +100%)
            if not -100 <= value <= 100:
                return False, f'{field} value {value} is outside reasonable range (-100 to 100)', None
            
            validated_data[field] = value
            
        except (ValueError, TypeError):
            return False, f'Invalid {field} value: must be a number', None
    
    return True, None, validated_data


@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict GDP growth rate using lagged features
    
    Expected JSON body:
    {
        "Country": "United States",
        "Population": 1.1,
        "Exports": 5.2,
        "Imports": 4.8,
        "Investment": 3.5,
        "Consumption": 2.8,
        "Govt_Spend": 2.0
    }
    
    Note: These values represent growth rates from year T-1
    The model will predict GDP growth for year T
    """
    try:
        # Get JSON data
        data = request.get_json()
        
        # Validate input (Fix Issue #4: Input Validation)
        is_valid, error_msg, validated_data = validate_prediction_input(data)
        
        if not is_valid:
            return jsonify({
                'error': 'Invalid input',
                'message': error_msg,
                'required_fields': [
                    'Country', 'Population', 'Exports', 'Imports',
                    'Investment', 'Consumption', 'Govt_Spend'
                ]
            }), 400
        
        # Check if model is loaded
        if model is None or encoder is None:
            # Fallback simulation
            sim_growth = (
                validated_data['Consumption'] * 0.6 +
                validated_data['Exports'] * 0.2 -
                validated_data['Imports'] * 0.1
            )
            return jsonify({
                'growth': round(sim_growth, 2),
                'method': 'Simulation (Model not loaded)',
                'warning': 'Using fallback simulation. Model file not found.'
            })
        
        # Check if country is in encoder
        try:
            country_code = encoder.transform([validated_data['Country']])[0]
        except ValueError:
            return jsonify({
                'error': 'Unknown country',
                'message': f"Country '{validated_data['Country']}' not found in training data",
                'available_countries': encoder.classes_.tolist()[:10]  # Show first 10
            }), 400
        
        # Prepare features (using lagged values from T-1)
        features = [
            country_code,
            validated_data['Population'],
            validated_data['Exports'],
            validated_data['Imports'],
            validated_data['Investment'],
            validated_data['Consumption'],
            validated_data['Govt_Spend']
        ]
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        return jsonify({
            'growth': round(prediction, 2),
            'method': 'AI Model (Random Forest)',
            'note': 'Prediction based on lagged features (T-1 → T)',
            'country': validated_data['Country']
        })
    
    except Exception as e:
        # Log full error for debugging
        print(f"❌ Prediction Error: {e}")
        print(traceback.format_exc())
        
        # Return user-friendly error
        return jsonify({
            'error': 'Prediction failed',
            'message': 'An unexpected error occurred during prediction',
            'details': str(e)
        }), 500


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            '/', '/api/countries', '/api/history', '/predict'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred on the server'
    }), 500


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
