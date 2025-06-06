import json
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
import os
from datetime import datetime

def load_data(filepath):
    return pd.read_csv(filepath)

def preprocess_data(data):
    # Convert Date to datetime and extract Year, Month, Day
    data['Date'] = pd.to_datetime(data['Date'])
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Day'] = data['Date'].dt.day
    data.drop(columns='Date', inplace=True)

    # Label encode Location and Store
    le = LabelEncoder()
    data['Location'] = le.fit_transform(data['Location'])
    data['Store'] = le.fit_transform(data['Store'])

    return data

def split_data(data, target_column, test_size=0.2, random_state=42):
    X = data.drop(columns=target_column)
    y = data[target_column]

    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def train_model(X_train, y_train):
    model = LogisticRegression()
    model.fit(X_train, y_train)

    return model

def save_model(model, filepath):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    joblib.dump(model, filepath)

def evaluate_model(model, X_test, y_test):
    return model.score(X_test, y_test)

def save_model_score(score):
    # Create scores directory if it doesn't exist
    os.makedirs('scores', exist_ok=True)
    
    # Load existing scores or create new list
    scores_file = 'scores/model_scores.json'
    if os.path.exists(scores_file):
        with open(scores_file, 'r') as f:
            model_scores = json.load(f)
    else:
        model_scores = []
    
    # Add new score
    model_scores.append({
        'score': score,
        'timestamp': datetime.now().isoformat()
    })
    
    # Save updated scores
    with open(scores_file, 'w') as f:
        json.dump(model_scores, f, indent=2)

def main():
    # Load the data
    data = load_data('data/credit_card_records.csv')

    # Preprocess the data
    data = preprocess_data(data)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = split_data(data, 'Fraudulent')

    # Train the model
    model = train_model(X_train, y_train)

    # Save the model
    save_model(model, 'models/model.pkl')

    # Test the model
    score = evaluate_model(model, X_test, y_test)
    
    # Save the score
    save_model_score(score)
    
    # Print score
    print("Model accuracy is: ", score)
    return score

if __name__ == "__main__":
    main()