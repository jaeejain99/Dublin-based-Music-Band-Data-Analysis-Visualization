import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

# Parameters for the t-distribution
df = 35  # Degrees of freedom
alpha = 0.05  # Significance level (two-tailed test)
t_stat = -3.11  # Example test statistic
t_critical = t.ppf(1 - alpha / 2, df)  # Critical t-value (two-tailed)

# Generate x-values for the t-distribution
x = np.linspace(-4, 4, 100)  # Range for t-values
y = t.pdf(x, df)  # Probability density function for t-distribution

# Plot the t-distribution curve
plt.figure(figsize=(10, 4))
plt.plot(x, y, color="teal", label="t-Distribution", linewidth=1)

# Fill the rejection regions (both tails)
plt.fill_between(x, y, where=(x < -t_critical), color="red", alpha=0.3, label="Rejection Region (Left Tail)")
plt.fill_between(x, y, where=(x > t_critical), color="red", alpha=0.3, label="Rejection Region (Right Tail)")

# Mark the critical values
plt.axvline(x=-t_critical, color="red", linestyle="--", linewidth=1, label=f"Critical t = {-round(t_critical, 2)}")
plt.axvline(x=t_critical, color="red", linestyle="--", linewidth=1, label=f"Critical t = {round(t_critical, 2)}")

# Mark the test statistic
plt.axvline(x=t_stat, color="black", linestyle="--", linewidth=1, label=f"t₀ = {t_stat}")

# Add labels and legend
plt.axhline(y=0, color="gray", linewidth=0.8, linestyle="--")  # Horizontal baseline
plt.legend(fontsize=8, loc="upper left")
plt.tick_params(axis='both', labelsize=8) 
# Show the plot
plt.tight_layout()
plt.show()
