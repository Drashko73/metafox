import joblib
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

class ChurnModel:

    """ Wrapper for loading and serving pre-trained model"""
  
    def train(self, data, target_column):
        df = pd.DataFrame(data)
        df = pd.get_dummies(df)

        X = df.drop(target_column, axis=1)
        y = df[target_column]
        
        # Split the data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize and train the model
        self.model = XGBClassifier()
        self.model.fit(X_train, y_train)
        
        # # Save the model to a file
        # joblib.dump(self.model, self.model_path)
        
        return self.model