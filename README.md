## Business Problem

Our main objective is to analyze the relationships between the products in customer baskets and provide the most suitable product recommendations for customers in Germany during the years 2010-2011. In this case, the basket information of three different customers has been provided, and based on this basket data, we need to determine which products to recommend to make customers' shopping experiences more enjoyable. These recommendations will be derived using association rule analysis. In other words, by examining the products that customers purchase together, we will provide recommendations to similar shoppers. This is a data mining approach that can be used to enhance customer satisfaction and increase sales.

## Dataset

The Online Retail II dataset contains online sales transactions for a retail company based in the United Kingdom. It covers transactions from 01/12/2009 to 09/12/2011. The company's product catalog includes gift items, and it is worth noting that the majority of its customers are wholesalers. Here are some key details about the dataset:

- `InvoiceNo`: Invoice Number (Starting with 'C' indicates canceled transactions)
- `StockCode`: Product Code (Unique for each product)
- `Description`: Product Name
- `Quantity`: Quantity of Products (Number of items sold in invoices)
- `InvoiceDate`: Invoice Date
- `UnitPrice`: Invoice Price (in Sterling Pounds)
- `CustomerID`: Unique Customer Number
- `Country`: Country Name

This dataset can be utilized for various analyses, predictions, and data mining projects.

## Task

### Data Preparation
1. Load the dataset, which includes customer purchase history.
2. Perform data cleaning and filtering to remove outliers, negative values, and rare items.
3. Prepare the data for the ARL algorithm, ensuring it's in a suitable format.

### Apriori Algorithm
1. Use the Apriori algorithm to discover association rules among the purchased products.
2. Filter the rules based on desired support and confidence levels.

### Recommendations
1. Implement the `arl_recommender` function to recommend products to customers based on their previous purchases.
2. Provide recommendations for specific products (e.g., "PACK OF 6 SKULL PAPER CUPS").

## Results

The ARL-based recommender system provides valuable product recommendations to customers based on their purchase history. By analyzing associations between products, this system helps businesses suggest complementary or relevant items to customers, potentially increasing sales and customer satisfaction.

Based on the `Confidence metric`, I can make recommendations to customers by suggesting products that are compatible with their shopping baskets. This can lead to increased customer satisfaction as they receive personalized recommendations and individualized promotions.
Using the `Lift metric`, I can recommend products that have a strong association with the items that customers usually purchase. By encouraging cross-selling and suggesting complementary products, I can enhance the shopping experience for customers and potentially increase sales.