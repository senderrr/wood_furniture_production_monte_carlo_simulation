"""This is what I had in my stock_inventory_queue before I build my when_to_build_stock_inventory function"""
# Start Stock x: How much inventory the manufactory has of the item
# stock_df['Start Stock A'] = 0
# # Surplus Stock: How much stock there is after taking items from stock inventory to fulfill order
# stock_df['Surplus A Stock'] = a_stock - stock_df.groupby('Day')['Item A'].cumsum(axis=0)
# # set stock to input stock value
# stock_df['Start Stock A'] = stock_df.groupby('Day')['Surplus A Stock'].shift(1).fillna(a_stock).astype('int')
# # How many items needed to be built to fulfil and/or restock inventory
# stock_df['Build Item A'] = np.where(stock_df['Surplus A Stock'] >= 1, 0,
#                                     np.where(stock_df['Start Stock A'] >= 1,
#                                              stock_df['Item A'] - stock_df['Start Stock A'], stock_df['Item A']))

# Take note that Surplus x stock was used as a means to an end. Since I had to make negative numbers zero,
# in order to get accurate restock num. It has no negative effect on the simulation because all negative numbers
# in the simulation have the same value as any other negative number. Additionally, I changed the value to zero
# after I was already using it. Hence, when it is turned to zero, it is only used to calculate the restock column.
# Lastly, I am simulating that restocking take place for the last order  items are build directly for the customer as they come, and then
# restocked at the end of the day
# stock_df['Surplus A Stock'] = np.where(stock_df['Surplus A Stock'] < 0, 0, stock_df['Surplus A Stock'])
# stock_df['Restock A'] = stock_df.groupby('Day')['Surplus A Stock'].tail(1)
# stock_df['Restock A'] = a_stock - stock_df['Restock A']
# stock_df['Restock A'] = stock_df['Restock A'].fillna(0)


# stock_df['Build Item A'] = stock_df['Build Item A'] + stock_df['Restock A']

# stock_df['Start Stock B'] = 0
# stock_df['Surplus B Stock'] = b_stock - stock_df.groupby('Day')['Item B'].cumsum(axis=0)
# stock_df['Start Stock B'] = stock_df.groupby('Day')['Surplus B Stock'].shift(1).fillna(b_stock).astype('int')
# stock_df['Build Item B'] = np.where(stock_df['Surplus B Stock'] >= 1, 0,
#                                     np.where(stock_df['Start Stock B'] >= 1,
#                                              stock_df['Item B'] - stock_df['Start Stock B'], stock_df['Item B']))
# stock_df['Surplus B Stock'] = np.where(stock_df['Surplus B Stock'] < 0, 0, stock_df['Surplus B Stock'])
# stock_df['Restock B'] = stock_df.groupby('Day')['Surplus B Stock'].tail(1)
# stock_df['Restock B'] = b_stock - stock_df['Restock B']
# stock_df['Restock B'] = stock_df['Restock B'].fillna(0)
# stock_df['Build Item B'] = stock_df['Build Item B'] + stock_df['Restock B']
# def stock_inventory_queue_columns(df, stock, item_column, start_stock, surplus_stock, build_item, restock):

# stock_df['Start Stock C'] = 0
# stock_df['Surplus C Stock'] = c_stock - stock_df.groupby('Day')['Item C'].cumsum(axis=0)
# stock_df['Start Stock C'] = stock_df.groupby('Day')['Surplus C Stock'].shift(1).fillna(c_stock).astype('int')
# stock_df['Build Item C'] = np.where(stock_df['Surplus C Stock'] >= 1, 0,
#                                     np.where(stock_df['Start Stock C'] >= 1,
#                                              stock_df['Item C'] - stock_df['Start Stock C'], stock_df['Item C']))
# stock_df['Surplus C Stock'] = np.where(stock_df['Surplus C Stock'] < 0, 0, stock_df['Surplus C Stock'])
# stock_df['Restock C'] = stock_df.groupby('Day')['Surplus C Stock'].tail(1)
# stock_df['Restock C'] = c_stock - stock_df['Restock C']
# stock_df['Restock C'] = stock_df['Restock C'].fillna(0)
# stock_df['Build Item C'] = stock_df['Build Item C'] + stock_df['Restock C']


# stock_df['Start Stock D'] = 0
# stock_df['Surplus D Stock'] = d_stock - stock_df.groupby('Day')['Item D'].cumsum(axis=0)
# stock_df['Start Stock D'] = stock_df.groupby('Day')['Surplus D Stock'].shift(1).fillna(d_stock).astype('int')
# stock_df['Build Item D'] = np.where(stock_df['Surplus D Stock'] >= 1, 0,
#                                     np.where(stock_df['Start Stock D'] >= 1,
#                                              stock_df['Item D'] - stock_df['Start Stock D'], stock_df['Item D']))
# stock_df['Surplus D Stock'] = np.where(stock_df['Surplus D Stock'] < 0, 0, stock_df['Surplus D Stock'])
# stock_df['Restock D'] = stock_df.groupby('Day')['Surplus D Stock'].tail(1)
# stock_df['Restock D'] = d_stock - stock_df['Restock D']
# stock_df['Restock D'] = stock_df['Restock D'].fillna(0)
# stock_df['Build Item D'] = stock_df['Build Item D'] + stock_df['Restock D']


# stock_df['Start Stock E'] = 0
# stock_df['Surplus E Stock'] = e_stock - stock_df.groupby('Day')['Item E'].cumsum(axis=0)
# stock_df['Start Stock E'] = stock_df.groupby('Day')['Surplus E Stock'].shift(1).fillna(e_stock).astype('int')
# stock_df['Build Item E'] = np.where(stock_df['Surplus E Stock'] >= 1, 0,
#                                     np.where(stock_df['Start Stock E'] >= 1,
#                                              stock_df['Item E'] - stock_df['Start Stock E'], stock_df['Item E']))
# stock_df['Surplus E Stock'] = np.where(stock_df['Surplus E Stock'] < 0, 0, stock_df['Surplus E Stock'])
# stock_df['Restock E'] = stock_df.groupby('Day')['Surplus E Stock'].tail(1)
# stock_df['Restock E'] = e_stock - stock_df['Restock E']
# stock_df['Restock E'] = stock_df['Restock E'].fillna(0)
# stock_df['Build Item E'] = stock_df['Build Item E'] + stock_df['Restock E']