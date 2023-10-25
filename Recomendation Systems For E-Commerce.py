# ### Data Preparation
# 1. Load the dataset, which includes customer purchase history.
# 2. Perform data cleaning and filtering to remove outliers, negative values, and rare items.
# 3. Prepare the data for the ARL algorithm, ensuring it's in a suitable format.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from efficient_apriori import apriori, generate_rules_apriori

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('display.width', 1500)
df = pd.read_excel("dataset/online_retail_II.xlsx", sheet_name="Year 2010-2011")


def check_df(dataframe, head=5):
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Types ####################")
    print(dataframe.dtypes)
    print("#################### Num of Unique ####################")
    print(dataframe.nunique())
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(head))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    print("#################### Quantiles ####################")
    print(dataframe.describe([0.01, 0.05, 0.75, 0.90, 0.95, 0.99]).T)


check_df(df)
df = df[df["StockCode"] != "POST"]
df = df.dropna()
df = df[~df["Invoice"].str.contains("C", na=False)]
df = df[df["Price"] > 0]
df = df[df["Quantity"] > 0]


def num_summary(dataframe):
    num_count = len(num_cols)

    fig, axes = plt.subplots(num_count, 2, figsize=(12, 4 * num_count))
    plt.subplots_adjust(left=0.1, right=0.9, hspace=0.5)

    for i, col in enumerate(num_cols):
        sns.histplot(data=dataframe, x=col, kde=True, ax=axes[i, 0])
        axes[i, 0].set_title(f'{col} Histogram')

        sns.boxplot(x=dataframe[col], ax=axes[i, 1])
        axes[i, 1].set_title(f'{col} Boxplot')

    plt.show(block=True)


num_cols = ["Quantity", "Price"]
num_summary(df)


def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit


def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


replace_with_thresholds(df, "Price")
replace_with_thresholds(df, "Quantity")
num_summary(df)


# ### Apriori Algorithm
# 1. Use the Apriori algorithm to discover association rules among the purchased products.
# 2. Filter the rules based on desired support and confidence levels.

df_ger = df[df['Country'] == "Germany"]
ger_invoice_df = df_ger.groupby("Invoice")["Description"].apply(list).reset_index(name="GermanUserCart")
itemsets, rules = apriori(ger_invoice_df['GermanUserCart'], min_support=0.01, min_confidence=0.10)
rule_list = []
for rule in rules:
    antecedents = list(rule.lhs)
    consequents = list(rule.rhs)
    support = rule.support
    confidence = rule.confidence
    lift = rule.lift
    rule_list.append([antecedents, consequents, support, confidence, lift])

rules_df = pd.DataFrame(rule_list, columns=["Antecedents", "Consequents", "Support", "Confidence", "Lift"])


def check_id(dataframe, stock_code):
    if stock_code in dataframe["StockCode"].values:
        product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
        print(product_name)
    else:
        print("This product isn't in the stock")


# ### Recommendations
# 1. Implement the `arl_recommender` function to recommend products to customers based on their previous purchases.
# 2. Provide recommendations for specific products (e.g., "PACK OF 6 SKULL PAPER CUPS").

# for User1
product_id = 21987
check_id(df, product_id)  # "PACK OF 6 SKULL PAPER CUPS"

# for User2
product_id = 23235
check_id(df, product_id)  # "STORAGE TIN VINTAGE LEAF"

# for User3
product_id = 22747
check_id(df, product_id)  # "POPPY'S PLAYHOUSE BATHROOM"


def arl_recommender(rules_df, product_id, rec_count=1):
    sorted_rules = rules_df.sort_values("Lift", ascending=False)
    recommendation_list = []
    # buraya caunt da atılıp, ürün sayısını sınırlandırabiliriz.
    for i, product in enumerate(sorted_rules["Antecedents"]):
        for j in list(product):
            if j == product_id:
                recommendation_list.append(list(sorted_rules.iloc[i]["Consequents"])[0])

    return recommendation_list[0:rec_count]


arl_recommender(rules_df, "PACK OF 6 SKULL PAPER CUPS")
arl_recommender(rules_df, "STORAGE TIN VINTAGE LEAF")
arl_recommender(rules_df, "POPPY'S PLAYHOUSE BATHROOM")