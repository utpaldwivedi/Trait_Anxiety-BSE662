import pandas as pd

# Read CSV file
df = pd.read_csv("trait anxiety score3.csv", header=None)

# Drop the first row
df = df.drop(0)
# df2=df[[2]]

# Drop first 3 columns
df = df.iloc[:, 3:]

# Reset the index after dropping the row
df = df.reset_index(drop=True)

# Reassign values of the columns
df.columns = range(len(df.columns))

# Typecast all columns data to integer
for j in df.columns:
    df[j] = pd.to_numeric(df[j])
    
    
print(df)   

# Subtract a constant value from column names
cols = [0, 5, 6, 9, 12, 15, 18]
for i in range(len(cols)):
    df[cols[i]]=5-df[cols[i]]

# Print DataFrame
print(df)

# Add all column values of each row
df[20] = df.sum(axis=1)

# Print DataFrame with the total column added
print(df)

df2 =df[[20]]

# Export the selected column to a new CSV file
df2.to_csv('STAI-Y_score_database.csv', index=False, header=None)

