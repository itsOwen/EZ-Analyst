import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('amazon_reviews.csv')

# Display the first 5 rows of the dataset
print(df.head())

# Check for any missing values in the dataset
print(df.isnull().sum())

# Summary statistics of the dataset
print(df.describe())

# Visualize the distribution of scores
plt.figure(figsize=(8, 6))
sns.countplot(x='score', data=df)
plt.title('Distribution of Scores')
plt.xlabel('Score')
plt.ylabel('Count')
plt.savefig('score_distribution.png')
plt.show()

# Insights from the score distribution plot:
# The majority of reviews have a score of 5, indicating that most users are satisfied with the app.

# Plot the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Matrix')
plt.savefig('correlation_matrix.png')
plt.show()

# Insights from the correlation matrix:
# There doesn't seem to be a strong correlation between any of the numerical variables in the dataset.

# Visualize the distribution of thumbs up count
plt.figure(figsize=(8, 6))
sns.histplot(df['thumbsUpCount'], bins=30, kde=True)
plt.title('Distribution of Thumbs Up Count')
plt.xlabel('Thumbs Up Count')
plt.ylabel('Frequency')
plt.savefig('thumbs_up_distribution.png')
plt.show()

# Insights from the thumbs up count distribution plot:
# The majority of reviews have zero thumbs up counts, indicating that most reviews do not receive any likes from other users. 

# Create a bar plot for the app versions
plt.figure(figsize=(10, 8))
sns.countplot(x='appVersion', data=df, order=df['appVersion'].value_counts().index)
plt.title('Distribution of App Versions')
plt.xlabel('App Version')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.savefig('app_version_distribution.png')
plt.show()

# Insights from the app version distribution plot:
# The distribution of app versions used by reviewers can provide insights into the popularity of different versions and help in identifying any potential issues or trends.