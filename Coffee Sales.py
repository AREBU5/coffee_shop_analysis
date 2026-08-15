# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC Transaction records for Maven Roasters, a fictitious coffee shop operating out of three NYC locations. Dataset includes the transaction date, timestamp and location, along with product-level details.
# MAGIC
# MAGIC ### Business Question 
# MAGIC
# MAGIC How have Maven Roasters sales trended over time?
# MAGIC
# MAGIC Which days of the week tend to be busiest, and why do you think that's the case?
# MAGIC
# MAGIC What times of day tend to be most popular? Does the same trend hold across all locations?
# MAGIC
# MAGIC Which products are sold most and least often? Which drive the most revenue for the business?

# COMMAND ----------

# MAGIC %sql
# MAGIC USE `coffee_shop_sales`.`coffee_sales`;

# COMMAND ----------

# MAGIC %md
# MAGIC ### How have Maven Roasters sales trended over time?

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH SALES_TREND AS (
# MAGIC SELECT 
# MAGIC        MONTH(LEFT(transaction_date,10)) AS date_num
# MAGIC       ,MONTHNAME(LEFT(transaction_date,10)) AS transaction_date
# MAGIC       ,ROUND(SUM(transaction_qty * unit_price),2) AS Total_Sales
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY date_num 
# MAGIC           ,MONTHNAME(LEFT(transaction_date,10))
# MAGIC ORDER BY date_num
# MAGIC ),
# MAGIC calculations AS (
# MAGIC SELECT 
# MAGIC     date_num
# MAGIC     ,transaction_date
# MAGIC     ,total_sales
# MAGIC     ,LAG(Total_Sales) OVER(ORDER BY date_num) AS Previous_Month
# MAGIC     ,total_sales - LAG(Total_Sales) OVER(ORDER BY date_num) AS Sales_Diff
# MAGIC FROM SALES_TREND
# MAGIC )
# MAGIC SELECT 
# MAGIC     transaction_date
# MAGIC     ,total_sales
# MAGIC     ,ROUND((total_sales - previous_month )/previous_month *100,2) AS PCT_Change
# MAGIC FROM calculations;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Which days of the week tend to be busiest, and why do you think that's the case?

# COMMAND ----------

# MAGIC %md
# MAGIC ### Overall Pattern
# MAGIC
# MAGIC Friday is the busiest day with 21,701 transactions, followed closely by Thursday (21,654) and Monday (21,643)
# MAGIC Saturday is the slowest day with only 20,510 transactions - notably lower than other days
# MAGIC The difference between busiest and slowest is about 1,200 transactions (~5.8%)
# MAGIC Why Friday-Thursday-Monday are busiest:
# MAGIC
# MAGIC Weekday work culture: People need their coffee fix during the work week, especially starting Monday and ending the week strong on Thursday/Friday
# MAGIC Friday social factor: Could be more group orders or people treating themselves before the weekend
# MAGIC Monday momentum: People returning to work need that caffeine boost
# MAGIC Saturday dip: People sleep in on weekends, brew coffee at home, or have different routines
# MAGIC Month-by-Month Variation (Cell 8): Your second query reveals that the busiest day varies by month, which is fascinating:
# MAGIC
# MAGIC June had the highest single-day volume (Friday with 5,960 transactions)
# MAGIC April's Sunday was unusually busy (4,279) - could indicate special events or seasonal patterns
# MAGIC No consistent pattern - different days win each month, suggesting external factors (weather, holidays, local events) influence traffic
# MAGIC What this tells you about the business:
# MAGIC
# MAGIC Staffing should prioritize Thu-Fri-Mon coverage
# MAGIC Saturday might be an opportunity for promotions to drive traffic
# MAGIC The monthly variation suggests you should analyze specific dates for holidays/events that drove Sunday/Tuesday spikes

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     WEEKDAY(transaction_date) + 1 AS NUM_of_Week,
# MAGIC     DAYNAME(transaction_date) AS Day_of_week,
# MAGIC     COUNT(*) AS Number_of_Transactions,
# MAGIC     ROUND(
# MAGIC         COUNT(*) / SUM(COUNT(*)) OVER() * 100,
# MAGIC         2
# MAGIC     ) AS Percentage,
# MAGIC     RANK() OVER (ORDER BY COUNT(*) DESC) AS RANK
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY 
# MAGIC     WEEKDAY(transaction_date),
# MAGIC     DAYNAME(transaction_date)
# MAGIC ORDER BY NUM_of_Week;
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC WITH aggregate_transcations AS(
# MAGIC SELECT 
# MAGIC MONTH(transaction_date) AS MonthNum
# MAGIC ,MONTHNAME(transaction_date) AS Month_of_year
# MAGIC ,dayofweek(transaction_date) AS Day_of_week_num
# MAGIC ,DAYNAME(transaction_date) AS Day_of_week
# MAGIC ,COUNT(*) AS Number_of_Transactions
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY 
# MAGIC     MonthNum
# MAGIC     ,Month_of_year
# MAGIC     ,Day_of_week_num
# MAGIC     ,Day_of_week
# MAGIC ),
# MAGIC RANKING AS (
# MAGIC SELECT 
# MAGIC MonthNum
# MAGIC ,Month_of_year
# MAGIC ,Day_of_week_num
# MAGIC ,Day_of_week
# MAGIC ,Number_of_Transactions
# MAGIC ,Rank() OVER(PARTITION BY Month_of_year ORDER BY Number_of_Transactions DESC) AS RNK
# MAGIC FROM aggregate_transcations
# MAGIC ) 
# MAGIC SELECT 
# MAGIC     *
# MAGIC     
# MAGIC FROM RANKING
# MAGIC WHERE RNK <= 2
# MAGIC ORDER BY MonthNum;

# COMMAND ----------

# MAGIC %md
# MAGIC What times of day tend to be most popular?

# COMMAND ----------

# MAGIC %md
# MAGIC ### Time of Day Patterns:
# MAGIC
# MAGIC Clear Morning Rush (7-10 AM): Peak period with 10 AM hitting 18,545 transactions - the single busiest hour.
# MAGIC Early Morning Surge: 7-9 AM is extremely strong (13K-18K each hour) - classic coffee shop commute pattern.
# MAGIC
# MAGIC ### Business Insights:
# MAGIC
# MAGIC Staffing priority: 7-10 AM is critical - need maximum coverage.
# MAGIC Prep timing: Highest inventory should be ready by 7 AM.

# COMMAND ----------

# DBTITLE 1,Cell 10
# MAGIC %sql
# MAGIC SELECT 
# MAGIC       HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)) AS Hour
# MAGIC       ,CASE 
# MAGIC         WHEN HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)) = 0 THEN '12 AM'
# MAGIC         WHEN HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)) BETWEEN 1 AND 11 THEN CONCAT(HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)), ' AM')
# MAGIC         WHEN HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)) = 12 THEN '12 PM'
# MAGIC         WHEN HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)) BETWEEN 13 AND 23 THEN CONCAT(HOUR(RIGHT(TRY_CAST(transaction_time AS timestamp),9)) - 12, ' PM')
# MAGIC         ELSE NULL
# MAGIC       END AS Time_of_Day 
# MAGIC     ,COUNT(*) AS Total_Transactions
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY Time_of_Day, Hour
# MAGIC ORDER BY Hour ASC;
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Which products are sold most and least often? Which drive the most revenue for the business?

# COMMAND ----------

# MAGIC %md
# MAGIC ### Product Performance Analysis:
# MAGIC
# MAGIC ### Most Sold:
# MAGIC Brewed Chai tea (17,183) - volume leader
# MAGIC Gourmet brewed coffee (16,912)
# MAGIC Barista Espresso (16,403)
# MAGIC
# MAGIC ### Least Sold:
# MAGIC Green beans (134) - 128x less than top seller
# MAGIC Green tea (159)
# MAGIC House blend Beans (183)
# MAGIC
# MAGIC ### Revenue Drivers:
# MAGIC Barista Espresso - $91,406 (despite being #3 in volume)
# MAGIC Brewed Chai tea - $77,082
# MAGIC Hot chocolate - $72,416
# MAGIC
# MAGIC
# MAGIC **Key Insight: Value Arbitrage**
# MAGIC Barista Espresso generates 19% more revenue than Chai tea despite 5% fewer transactions.
# MAGIC
# MAGIC Espresso avg: $5.57/transaction
# MAGIC Chai avg: $4.49/transaction
# MAGIC
# MAGIC 24% price premium
# MAGIC Hot chocolate is the margin champion: $6.31/transaction with half the volume of leaders
# MAGIC
# MAGIC Strategic Actions:
# MAGIC Discontinue/Clearance:

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC -- Top 5 Products Sold the Most 
# MAGIC SELECT 
# MAGIC product_type
# MAGIC ,COUNT(product_id) AS Quantity_Sold 
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY 
# MAGIC         product_type
# MAGIC ORDER BY Quantity_Sold DESC
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top 5 products with least sales 
# MAGIC SELECT 
# MAGIC product_type
# MAGIC ,COUNT(product_id) AS Quantity_Sold 
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY 
# MAGIC         product_type
# MAGIC ORDER BY Quantity_Sold ASC
# MAGIC LIMIT 5;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top 5 products that drive the most revenue for the business 
# MAGIC SELECT 
# MAGIC  product_type
# MAGIC ,COUNT(product_id) AS Quantity_Sold 
# MAGIC ,ROUND(SUM(transaction_qty * unit_price),0) AS Total_Revenue
# MAGIC FROM coffee_shop_sales
# MAGIC GROUP BY 
# MAGIC         product_type
# MAGIC ORDER BY Total_Revenue DESC
# MAGIC LIMIT 5;