# Maven Roasters Coffee Sales Analysis

Comprehensive sales analytics for Maven Roasters, a fictitious coffee shop operating across three NYC locations. This project analyzes transaction patterns, customer behavior, and product performance to drive data-informed business decisions.

## Project Overview

This analysis examines Maven Roasters' sales data to answer critical business questions:
- How have sales trended over time?
- Which days of the week are busiest?
- What times of day see peak traffic?
- Which products drive the most volume and revenue?

## Key Findings

### Sales Trends
- **Strong Growth**: Sales increased from $81,678 (Jan) to $166,486 (Jun)
- **Peak Month**: May showed the highest growth rate at 31.77%
- **Overall Performance**: 104% growth from January to June

### Day of Week Patterns
- **Busiest Day**: Friday (21,701 transactions, 14.55%)
- **Top 3 Days**: Friday → Thursday → Monday
- **Slowest Day**: Saturday (20,510 transactions, 13.75%)
- **Key Insight**: Weekday work culture drives traffic; weekend sees 5.8% drop

### Time of Day Analysis
- **Peak Hour**: 10 AM (18,545 transactions)
- **Morning Rush**: 7-10 AM accounts for highest volume
- **Slowest Period**: 8 PM (603 transactions)
- **Strategic Insight**: Critical staffing needed 7-10 AM

### Product Performance

#### Volume Leaders
1. Brewed Chai tea (17,183 units)
2. Gourmet brewed coffee (16,912 units)
3. Barista Espresso (16,403 units)

#### Revenue Champions
1. Barista Espresso ($91,406 | $5.57/transaction)
2. Brewed Chai tea ($77,082 | $4.49/transaction)
3. Hot chocolate ($72,416 | $6.31/transaction)

**Key Insight**: Hot chocolate has the highest margin at $6.31/transaction despite lower volume

#### Underperformers
- Green beans (134 units)
- Green tea (159 units)
- House blend Beans (183 units)

## 📁 Project Structure

```
Coffe-shop-sales/
├── README.md                           # Project documentation
└── Coffee Sales.ipynb                  # Main analysis notebook
```

## Analysis Components

The notebook includes:

1. **Sales Trend Analysis**
   - Monthly revenue tracking
   - Period-over-period growth rates
   - Visual trend line with value labels

2. **Day of Week Analysis**
   - Transaction volume by weekday
   - Percentage distribution
   - Month-by-month busiest day variation

3. **Hourly Traffic Patterns**
   - Transaction volume by hour
   - Peak period identification
   - Morning rush visualization (7-10 AM)

4. **Product Performance**
   - Most/least sold products
   - Revenue contribution analysis
   - Average revenue per transaction
   - Margin analysis by product

## Visualizations

All analyses include professional matplotlib visualizations:
- Line charts with area fills for trends
- Bar charts with gradient colors for comparisons
- Pie charts for distribution analysis
- Dual-axis charts for multi-metric comparison
- Heatmap-style grouped visualizations

## Business Recommendations

### Staffing Optimization
- **Peak Coverage**: Maximum staff 7-10 AM (morning rush)
- **Heavy Days**: Prioritize Thu-Fri-Mon scheduling
- **Saturday Opportunity**: Consider promotions to boost weekend traffic

### Product Strategy
- **Promote High-Margin Items**: Push Hot chocolate ($6.31/transaction)
- **Upsell Opportunities**: Bundle Barista Espresso with pastries
- **Inventory Management**: Reduce stock for Green beans, House blend
- **Discontinuation Candidates**: Review bottom 3 performers

### Revenue Growth
- **Premium Focus**: Emphasize higher-margin products (Espresso, Hot chocolate)
- **Volume Driver**: Maintain strong Chai tea supply (volume leader)
- **Seasonal Testing**: Investigate April Sunday spike for replication

## Technical Stack

- **Platform**: Databricks
- **Languages**: Python, SQL
- **Libraries**: 
  - pandas (data manipulation)
  - matplotlib (visualization)
  - PySpark (data processing)
- **Database**: Unity Catalog (`coffee_shop_sales.coffee_sales`)


## Getting Started

1. Open the **Coffee Sales** notebook in Databricks
2. Ensure access to the `coffee_shop_sales.coffee_sales` table
3. Run all cells sequentially (Cells 2-23)
4. Review visualizations and insights

## Analysis Methodology

### SQL Queries
- Window functions for period-over-period analysis
- Aggregations for volume/revenue metrics
- Ranking functions for top/bottom performers
- Date/time functions for temporal patterns

### Python Analysis
- DataFrame operations for data transformation
- Statistical calculations for insights
- Custom visualizations with matplotlib
- Data type conversions for numeric precision

## Data Coverage

- **Time Period**: January - June 2026
- **Locations**: 3 NYC stores
- **Total Transactions**: 149,116
- **Products**: 30+ unique product types

## Key Exploration 

1. **Work Week Dominance**: Coffee consumption strongly correlates with work schedules
2. **Morning Peak**: 7-10 AM window is critical for revenue
3. **Margin Matters**: Volume leader ≠ revenue leader (Hot chocolate insight)
4. **Monthly Variation**: External factors (events, weather) significantly impact daily patterns
5. **Product Mix**: 20% of products drive 80% of revenue (Pareto principle)

## Contact

For questions or insights about this analysis, please reach out to me @ danielarebu@outlook.com.

