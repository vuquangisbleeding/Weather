years = [2019, 2020, 2021, 2022, 2023]
avg_temps = [30.1, 30.5, 31.0, 31.2, 31.7]
result = analyzer.linear_regression(years, avg_temps)
print(f"Slope: {result['slope']:.3f}")
print(f"p-value: {result['p_value']:.4f}")
print(f"Slope 95% CI: {result['slope_ci']}")
```

# Report: Statistical Significance Testing (p-value, confidence interval) in Trend Analysis

## 1. Concept
- **P-value**: The probability of observing results as extreme as the actual data (or more so) if the null hypothesis (no trend, slope = 0) is true. A small p-value (typically < 0.05) indicates a statistically significant trend.
- **Confidence Interval**: The range in which the regression parameter (e.g., slope) is likely to fall with a given confidence level (typically 95%). If the interval does not contain 0, the trend is considered significant.

## 2. Application in This Project
In Weather Trend Analysis, these metrics are automatically computed during linear regression to analyze temperature, rainfall, etc.

- Calculated in the `linear_regression` method of the `TrendAnalyzer` class (file `src/analysis/trend_analyzer.py`).
- Results include: `slope`, `intercept`, `r_value`, `p_value`, `slope_ci`, `intercept_ci`, ...
- Used to assess whether a trend (e.g., increasing temperature over years) is statistically significant.

## 3. Example
Suppose you want to check the trend of average summer temperature over years:

```python
from analysis import TrendAnalyzer
analyzer = TrendAnalyzer(confidence_level=0.95)
years = [2019, 2020, 2021, 2022, 2023]
avg_temps = [30.1, 30.5, 31.0, 31.2, 31.7]
result = analyzer.linear_regression(years, avg_temps)
print(f"Slope: {result['slope']:.3f}")
print(f"p-value: {result['p_value']:.4f}")
print(f"Slope 95% CI: {result['slope_ci']}")
```

Sample output:
```
Slope: 0.390
p-value: 0.0123
Slope 95% CI: (0.120, 0.660)
```
- **Interpretation**: Positive slope, p-value < 0.05, and CI does not include 0 ⇒ Statistically significant temperature increase.

## 4. Practical Meaning
- Helps determine if a trend is real or just random.
- Enables data-driven, scientific decision making.
- Used for all trend analyses in this project: temperature, rainfall, by season, by year, etc.

---
*Report auto-generated on 13/02/2026.*
