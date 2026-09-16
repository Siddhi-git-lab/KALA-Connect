import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# 1. Load the generated dataset
df = pd.read_csv('handicrafts_market.csv')

# 2. Features (X) and Target Price (y)
X = df[['category', 'material_cost', 'labor_hours', 'craft_complexity']]
y = df['selling_price']

# 3. Preprocess categorical text
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), ['category'])],
    remainder='passthrough'
)

# 4. Train the Random Forest Regressor
model = Pipeline([
    ('prep', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

print("Training model...")
model.fit(X, y)

# 5. Save the trained model
joblib.dump(model, 'pricing_model.pkl')
print("Model trained successfully and saved as pricing_model.pkl!")