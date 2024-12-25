import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Set random seed for reproducibility
np.random.seed(42)

# Generate data that follows a normal distribution
mean = 65
std_dev = 20
num_samples = 800

# Generate the data
data = np.random.normal(loc=mean, scale=std_dev, size=num_samples)

# Clip the data to ensure values are between 0 and 100
data = np.clip(data, 0, 100)

# Convert the data to integers
data = np.round(data).astype(int)

# Count occurrences in the ranges 90-94 and 95-100
count_90_94 = np.sum((data >= 90) & (data <= 94))
count_95_100 = np.sum((data >= 95) & (data <= 100))

# Ensure that the number of students in the 95-100 range is < 1% of the total data
max_95_100 = int(0.01 * num_samples)
if count_95_100 > max_95_100:
    excess_95_100 = count_95_100 - max_95_100
    data = data[data < 95]  # Remove excess values in 95-100 range

# Ensure that the number of students in the 90-94 range is < 2% of the total data
max_90_94 = int(0.02 * num_samples)
if count_90_94 > max_90_94:
    excess_90_94 = count_90_94 - max_90_94
    data = data[~((data >= 90) & (data <= 94))]  # Remove excess values in 90-94 range

# Ensure there's at least one student in both 90-94 and 95-100 ranges
if np.sum((data >= 90) & (data <= 94)) == 0:
    data = np.append(data, np.random.randint(90, 95))  # Add a student to the 90-94 range

if np.sum((data >= 95) & (data <= 100)) == 0:
    data = np.append(data, np.random.randint(95, 101))  # Add a student to the 95-100 range

# Input the score
score = int(input("Enter your score: "))

# Calculate the percentile for the given score
percentile = np.percentile(data, score)
print(f"Your score of {score} is in the top {percentile}%.")

# Create a histogram of the data
plt.figure(figsize=(10, 6))

# Custom bin edges: [0-4.5], [5-9.5], [10-14.5], ..., [95-99.5]
bin_edges = np.arange(0, 105, 5) - 0.5
counts, bins, patches = plt.hist(data, bins=bin_edges, density=False, alpha=0.6, color='g', label="Score Distribution")

# Fit a normal distribution curve
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mean, std_dev)
plt.plot(x, p * len(data) * (xmax - xmin) / 100, 'k', linewidth=2, label="Normal Distribution Fit")

# Set the x-axis ticks to be every 5 points from 0 to 100
plt.xticks(np.arange(0, 101, 5))

# Add title and labels
plt.title("Score Distribution and Normal Distribution Fit")
plt.xlabel("Score")
plt.ylabel("Number of Students")
plt.legend()

# Display the plot
plt.show()
