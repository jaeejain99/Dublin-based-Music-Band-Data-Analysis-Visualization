import matplotlib.pyplot as plt
import numpy as np

# Given values
point_estimate = -1.04  # Mean difference
margin_of_error = 0.6664  # Calculated as z * Standard Error
lower_limit = point_estimate - margin_of_error
upper_limit = point_estimate + margin_of_error

# Plot
plt.figure(figsize=(8, 4))
plt.errorbar(
    x=0, 
    y=point_estimate, 
    yerr=margin_of_error, 
    fmt='o', 
    color='blue', 
    ecolor='red', 
    capsize=5, 
    label='95% Confidence Interval'
)

# Add horizontal lines for the confidence interval
plt.hlines(
    y=[lower_limit, upper_limit], 
    xmin=-0.2, xmax=0.2, 
    colors='red', linestyles='dashed'
)

# Reference line for zero
plt.axhline(y=0, color='black', linestyle='--', label='Null Hypothesis (μ1 - μ2 = 0)')

# Add text annotations for the values
plt.text(0.25, point_estimate, f'Point Estimate: {point_estimate:.2f}', color='blue', fontsize=10, verticalalignment='center')
plt.text(0.25, lower_limit, f'Lower Limit: {lower_limit:.2f}', color='red', fontsize=10, verticalalignment='center')
plt.text(0.25, upper_limit, f'Upper Limit: {upper_limit:.2f}', color='red', fontsize=10, verticalalignment='center')

# Formatting the plot
plt.title('95% Confidence Interval for Mean Difference')
plt.ylabel('Mean Difference (μ1 - μ2)')
plt.xticks([])
plt.xlim(-1, 1)
plt.ylim(lower_limit - 0.5, upper_limit + 0.5)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Display the plot
plt.show()
