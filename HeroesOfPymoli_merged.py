
# Dependencies and Setup
import pandas as pd
import numpy as np

# Raw data file
file_to_load = "Resources/purchase_data.csv"

# Read purchasing file and store into pandas data frame
purchase_data = pd.read_csv(file_to_load)

# Find the total number of unique players
player_demograph = purchase_data.loc[:, ["SN", "Gender", "Age"]]
total_players = player_demograph["SN"].nunique()
# Create dataframe of unique players
pd.DataFrame({"Total Players": [total_players]})

# Run basic calculations for avg price, total price, total purchases and # of unique items
avg_price = purchase_data["Price"].mean()
total_price = purchase_data["Price"].sum()
total_purchases = purchase_data["Price"].count()
total_unique_items = purchase_data["Item ID"].nunique()

# Create dataframe of purchase data summary
summary_purchase = pd.DataFrame({"Average Price": [avg_price], 
                                 "Number of Purchases": [total_purchases], 
                                 "Total Items": [total_unique_items], 
                                 "Total Revenue": [total_price]})

# Convert average price and total revenue to currency
summary_purchase["Average Price"] = summary_purchase["Average Price"].map("${:,.2f}".format)
summary_purchase["Total Revenue"] = summary_purchase["Total Revenue"].map("${:,.2f}".format)

# Display data frame
summary_purchase

# Calculate the percenatge and total number of male, female and undisclosed players
gender_total = player_demograph["Gender"].value_counts()
gender_percent = (gender_total / total_players) * 100

# Create summary dataframe for gender demographics
gender_demographics = pd.DataFrame({"Percentage of Players": gender_percent, "Total Count": gender_total})

gender_demographics.round(2)

# Calculate average purchase price, total purchase value, total purchases by gender and avg purchase total/person
total_purch_price_gender = purchase_data.groupby(["Gender"]).sum()["Price"]
avg_purch_price_gender = purchase_data.groupby(["Gender"]).mean()["Price"]
gender_purch_counts = player_demograph["Gender"].value_counts()
avg_purch_total_person = total_purch_price_gender / gender_total

# Create dataframe for purchasing analysis by gender
gender_purchasing_analysis = pd.DataFrame({"Purchase Count": gender_purch_counts, 
                                           "Average Purchase Price": avg_purch_price_gender, 
                                           "Total Purchases Value": total_purch_price_gender, 
                                           "Avg Purchase Total per Person": avg_purch_total_person})

# Convert average purchase price, total purchase value and avg purchase total per person to currency
gender_purchasing_analysis["Average Purchase Price"] = gender_purchasing_analysis["Average Purchase Price"].map("${:,.2f}".format)
gender_purchasing_analysis["Total Purchases Value"] = gender_purchasing_analysis["Total Purchases Value"].map("${:,.2f}".format)
gender_purchasing_analysis["Avg Purchase Total per Person"] = gender_purchasing_analysis["Avg Purchase Total per Person"].map("${:,.2f}".format)

# Display data frame
gender_purchasing_analysis

# Establish bins for ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

#Slice the data and place it into bins
player_demograph["Age Ranges"] = pd.cut(player_demograph["Age"], age_bins, labels=group_names)

# Run calculations for numbers and and percenatages by age group
age_demo_total = player_demograph["Age Ranges"].value_counts()
age_demo_percent = (age_demo_total / total_players) * 100

# Create dataframe for age demographics
age_demographics_df = pd.DataFrame({"Percentage of Players": age_demo_percent, "Total Count": age_demo_total})

age_demographics_df.sort_index().round(2)

# Bin purchases_data by age
purchase_data["Age Ranges"] = pd.cut(purchase_data["Age"], age_bins, labels=group_names)

# Run calculations to get purchase count, avg. purchase price, total puchase value and avg. purchase total by age group
purch_count_age = purchase_data.groupby(["Age Ranges"]).count()["Price"]
avg_purch_price_age = purchase_data.groupby(["Age Ranges"]).mean()["Price"]
total_purch_value_age = purchase_data.groupby(["Age Ranges"]).sum()["Price"]
avg_purch_total_person_age =  total_purch_value_age / purch_count_age

# Create dataframe for purchasing analysis by age
purchasing_analysis_age_df = pd.DataFrame({"Purchase Count": purch_count_age, 
                                           "Average Purchase Price": avg_purch_price_age,
                                           "Total Purchase Value": total_purch_value_age, 
                                           "Average Purchase Total per Person": avg_purch_total_person_age})
#Convert purchase values to currency format
purchasing_analysis_age_df["Average Purchase Price"] = purchasing_analysis_age_df['Average Purchase Price'].map("${:,.2f}".format)
purchasing_analysis_age_df["Total Purchase Value"] = purchasing_analysis_age_df['Total Purchase Value'].map("${:,.2f}".format)
purchasing_analysis_age_df["Average Purchase Total per Person"] = purchasing_analysis_age_df['Average Purchase Total per Person'].map("${:,.2f}".format)

purchasing_analysis_age_df

# Find the total number of purchases by user, avg spent on purchase and total amount paid for purchases
user_total = purchase_data.groupby(["SN"]).count()["Price"]
avg_purch_price_user = purchase_data.groupby(["SN"]).mean()["Price"]
total_purch_price_user = purchase_data.groupby(["SN"]).sum()["Price"]

# Create dataframe for top spenders
top_spender_df = pd.DataFrame({"Purchase Count": user_total, 
                               "Average Purchase Price": avg_purch_price_user, 
                               "Total Purchase Value": total_purch_price_user})

# Sort by Total Purchase vale in decsending order
top_spender_sorted_df = top_spender_df.sort_values("Total Purchase Value", ascending=False)

# Convert purchase values to currency
top_spender_sorted_df["Average Purchase Price"] = top_spender_sorted_df["Average Purchase Price"].map("${:,.2f}".format)
top_spender_sorted_df["Total Purchase Value"] = top_spender_sorted_df["Total Purchase Value"].map("${:,.2f}".format)


# Display data frame
top_spender_sorted_df.head(5)

# Retrieve the item ID, Item Name and Item Price from purchase data
item_data = purchase_data.loc[:,["Item ID", "Item Name", "Price"]]

# Calculate purchase count, item price, and total purchase value by item ID/item name
item_count = item_data.groupby(["Item ID", "Item Name"]).count()["Price"]
item_price = item_data.groupby(["Item ID", "Item Name"]).mean()["Price"]
item_value = item_data.groupby(["Item ID", "Item Name"]).sum()["Price"]

# Create most popular item data frame
most_pop = pd.DataFrame({"Purchase Count": item_count, 
                         "Item Price": item_price,
                         "Total Purchase Value": item_value})

# Sort data frame by purchase count in descending order
most_pop_sort = most_pop.sort_values("Purchase Count", ascending=False)

# Convert item price and total purchase value to currency
most_pop_sort["Item Price"] = most_pop_sort["Item Price"].map("${:,.2f}".format)
most_pop_sort["Total Purchase Value"] = most_pop_sort["Total Purchase Value"].map("${:,.2f}".format)


# Display data frame
most_pop_sort.head()

# Sort the most popular items in descending order by total purchase value
most_profit = most_pop.sort_values("Total Purchase Value", ascending=False)

# Convert item price and total purchase value to currency
most_profit["Item Price"] = most_profit["Item Price"].map("${:,.2f}".format)
most_profit["Total Purchase Value"] = most_profit["Total Purchase Value"].map("${:,.2f}".format)

#Display data rame preview
most_profit.head()

# Three Observations from the Heroes of Pymoli Purchase Data
# The age 35-39 demographic is willing to pay more for items. 
# There are more male players than there are total players. This could point to an issue with data set
# Players are willing to pay up for the high dollar items. This is evident that the cheaper items are purchased the least
