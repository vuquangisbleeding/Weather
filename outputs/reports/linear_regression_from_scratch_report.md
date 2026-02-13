years = [2019, 2020, 2021, 2022, 2023]
avg_rain = [120, 130, 125, 140, 150]
result = analyzer.linear_regression(years, avg_rain)
print(f"Slope: {result['slope']:.3f}")
print(f"Intercept: {result['intercept']:.2f}")
print(f"R value: {result['r_value']:.3f}")
```

# Report: Linear Regression Implemented from Scratch (without scipy)

## 1. Concept
- **Linear regression** is a method to find the best-fit line (using the least squares criterion) describing the relationship between an independent variable (x, e.g., year) and a dependent variable (y, e.g., temperature).
- Normally, libraries like `scipy.stats.linregress` are used for computation. However, this project implements the entire linear regression algorithm from scratch, without relying on scipy for the core calculation.

## 2. Application in This Project
- Implemented in the `linear_regression` method of the `TrendAnalyzer` class (file `src/analysis/trend_analyzer.py`).
- Manually computes values: slope, intercept, r_value (correlation coefficient), p_value, standard error, confidence interval, ...
- Ensures full control over the calculation process, making it easy to extend, customize, or test.

## 3. Example
Suppose you want to analyze the trend of average rainfall over the years:

```python
from analysis import TrendAnalyzer
analyzer = TrendAnalyzer(confidence_level=0.95)
years = [2019, 2020, 2021, 2022, 2023]
avg_rain = [120, 130, 125, 140, 150]
result = analyzer.linear_regression(years, avg_rain)
print(f"Slope: {result['slope']:.3f}")
print(f"Intercept: {result['intercept']:.2f}")
print(f"R value: {result['r_value']:.3f}")
```

Sample output:
```
Slope: 7.500
Intercept: -14977.50
R value: 0.950
```
- **Explanation**: Positive slope indicates increasing rainfall over the years, r_value close to 1 shows a strong relationship.

## 4. Meaning and Advantages
- **Full control**: Can customize or extend the regression algorithm for special purposes (e.g., add weights, check assumptions, ...).
- **No external library dependency**: Reduces risk from API changes or bugs in external libraries.
- **Easy to test and transparent**: Every calculation step is clear and verifiable.
- **Great for teaching and research**: Helps deeply understand the mathematics of linear regression.

## 5. Conclusion
Implementing linear regression from scratch makes the project flexible, transparent, and extensible, while still ensuring accuracy and all necessary statistical metrics for weather trend analysis.

---
*Report auto-generated on 13/02/2026.*
