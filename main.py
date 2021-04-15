import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


data_ord_item = pd.read_csv("/Users/anhtung/Downloads/datasets/order_items_dataset.csv")
data_ord = pd.read_csv("/Users/anhtung/Downloads/datasets/orders_dataset.csv")
data_prod = pd.read_csv("/Users/anhtung/Downloads/datasets/products_dataset.csv")
translate = pd.read_csv("/Users/anhtung/Downloads/datasets/product_category_name_translation.csv")

"""Merging 2 files: order and order item"""
total_order = pd.merge(data_ord, data_ord_item)

"""Merging 2 files: total_order and product"""
prod_ord = pd.merge(total_order, data_prod, on='product_id')

"""DATA CLEANING PROCESS"""
master = pd.merge(prod_ord, translate)  # Translate from Portuguese to English

print("Missing values:")  # Print all missing values inside order columns
print(data_ord.isna().sum())

print("Values inside order_status column:")  # Count unique values inside order
print(data_ord['order_status'].value_counts())

find1 = data_ord[data_ord['order_approved_at'].isna()]['order_status'].value_counts()
print("Finding unexpected values in 'order_approved_at':")
print(find1)

visual1 = ((data_ord['order_approved_at'].isna()) & (data_ord['order_status'] == 'delivered'))
print("Visualize 14 incorrect orders.")
print(data_ord[visual1])

data_ord.loc[visual1, 'order_approved_at'] = data_ord.loc[visual1, 'order_purchase_timestamp']
print("Fixed 'order_approved_at' with'")
print(data_ord[data_ord['order_approved_at'].isna()]['order_status'].value_counts())

"""Creating DataFrame for the master file which only include important columns
    required for later analytic"""
df = pd.DataFrame(master, columns=['order_id', 'product_id', 'order_item_id', 'seller_id'
                                   , 'product_category_name_english', 'order_status', 'order_purchase_timestamp'
                                   ])
df = df.rename(columns={'product_category_name_english': 'category'})
"""Export to .csv file"""
df.to_csv("Master dataset.csv", index=False)
