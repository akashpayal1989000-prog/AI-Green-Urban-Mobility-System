import pandas as pd


df = pd.read_csv('data/cleaned_traffic_history.csv')


rankings = df.groupby('location')['congestion_level'].mean().sort_values(ascending=False)

print("--- Dehradun Traffic Rankings (3-Day Average) ---")
print(rankings)


peak_moment = df.loc[df['congestion_level'].idxmax()]
print(f"\n--- Worst Traffic Recorded ---")
print(f"Location: {peak_moment['location']}")
print(f"Time: {peak_moment['timestamp']}")
print(f"Congestion: {peak_moment['congestion_level']}")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv('data/cleaned_traffic_history.csv')

# 2. Calculate average congestion per location
rankings = df.groupby('location')['congestion_level'].mean().sort_values(ascending=False)

# 3. Convert the Series to a DataFrame for the Heatmap
# We reshape it so locations are rows and the 'Mean Congestion' is the column
ranking_df = rankings.to_frame()

# 4. Plotting
plt.figure(figsize=(8, 10))
sns.heatmap(ranking_df, 
            annot=True,            # Show the actual numbers in the cells
            cmap="YlOrRd",         # Yellow to Red color scale (classic traffic colors)
            cbar_kws={'label': 'Average Congestion Index'},
            linewidths=.5)

plt.title('Figure 4.1: Dehradun Traffic Density Heatmap (Node-wise)')
plt.ylabel('Junction Name (Node)')
plt.xlabel('Congestion Metric')

# 5. Save and Show
plt.savefig('traffic_heatmap.png', bbox_inches='tight')
plt.show()