import pandas as pd

# Convert the dictionary into DataFrame
df = pd.read_csv('USB-IDS-1-TRAINING.csv')
print("\Before modifying first column:\n", df.columns)

df.columns = df.columns.str.strip()
# df.columns = df.rename(str.strip, axis = 'columns')
   
# After renaming the columns
print("\nAfter modifying first column:\n", df.columns)
df.to_csv('USB-IDS-1-TRAINING.csv')
