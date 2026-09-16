import pandas as pd
import numpy as np

# Quick synthetic data generator
np.random.seed(42)
n = 800
categories = ['Terracotta', 'Zari Work', 'Madhubani', 'Woodcraft', 'Brassware']
mat_costs = np.random.uniform(100, 2000, n)
hours = np.random.uniform(2, 40, n)
complexity = np.random.randint(1, 6, n)

# Formula: base cost + hourly labor + complexity multiplier + margin
prices = (mat_costs + (hours * 90) + (complexity * 150)) * np.random.uniform(1.15, 1.45, n)

df = pd.DataFrame({
    'category': np.random.choice(categories, n),
    'material_cost': np.round(mat_costs, 2),
    'labor_hours': np.round(hours, 1),
    'craft_complexity': complexity,
    'selling_price': np.round(prices, 2),
    'demand_score': np.random.randint(40, 99, n)
})
df.to_csv('handicrafts_market.csv', index=False)