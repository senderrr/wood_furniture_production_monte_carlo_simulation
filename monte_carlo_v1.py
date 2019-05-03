import numpy as np
import pandas as pd


def pert(low, likely, high, confidence=4, samples=10000):
    """I got this function from Instructor Weible's Lecture Notes"""

    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta


def orders(low, likely, high, daily_count_confidence, order_size_confidence, samples):
    item_order_options = ['A', 'B', 'C', 'D', 'E']
    all_orders = []
    day_counter = 0

    column_a = []
    column_b = []
    column_c = []
    column_d = []
    column_e = []
    column_day = []
    for i in range(22):
        day_counter += 1
        daily_order_count = pert(low, likely, high, confidence=daily_count_confidence, samples=samples)
        daily_order_count = np.around(daily_order_count).astype(int)
        print('daily order count:', daily_order_count)

        for j in range(daily_order_count[0]):
            order_size = pert(1, 8, 15, confidence=order_size_confidence, samples=samples)
            order_size = np.around(order_size).astype(int)
            order_items = np.random.choice(item_order_options, size=order_size, p=[0.2, 0.2, 0.3, 0.2, 0.1])
            print(order_items, 'day:', day_counter, 'order:', j + 1)

            column_day.append(day_counter)

            a_count = order_items[order_items == 'A']
            a_count = np.count_nonzero(a_count)
            column_a.append(a_count)

            b_count = order_items[order_items == 'B']
            b_count = np.count_nonzero(b_count)
            column_b.append(b_count)

            c_count = order_items[order_items == 'C']
            c_count = np.count_nonzero(c_count)
            column_c.append(c_count)

            d_count = order_items[order_items == 'D']
            d_count = np.count_nonzero(d_count)
            column_d.append(d_count)

            e_count = order_items[order_items == 'E']
            e_count = np.count_nonzero(e_count)
            column_e.append(e_count)

            all_orders.append(order_items)

    print('---')
    order_len = list(range(len(all_orders)))
    df = pd.DataFrame({'Order #': order_len, 'Day': column_day, 'Item A': column_a, 'Item B': column_b,
                       'Item C': column_c, 'Item D': column_d, 'Item E': column_e})
    df['Order #'] = df['Order #'] + 1

    return df


def fcq_hours(array, machine_time_swap, low, likely, high, confidence):
    item_count = array
    item_time = pert(low, likely, high, confidence=confidence, samples=item_count)
    item_time = np.sum(item_time)
    if item_time != 0:
        item_time = item_time + machine_time_swap
    item_time = item_time / 7.5           # change days to hours; wait time/ pick up day (floor, ceiling round; modulus); 2 shifts; first come queue with inventory
    item_time = np.around(item_time, decimals=1)  # .astype(int)
    return item_time

def pq_hours(array, machine_time_swap, low, likely, high, confidence):
    item_count = array
    item_time = pert(low, likely, high, confidence=confidence, samples=item_count)
    item_time = np.sum(item_time)
    if item_time != 0:
        item_time = item_time + machine_time_swap
    item_time = item_time / 7.5
    item_time = np.around(item_time, decimals=1)
    return item_time

def first_come_queue(df, build_confidence):
    item_a_list = []
    item_b_list = []
    item_c_list = []
    item_d_list = []
    item_e_list = []

    # https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    for index, row in df.iterrows():
        item_a_count = row['Item A']
        item_b_count = row['Item B']
        item_c_count = row['Item C']
        item_d_count = row['Item D']
        item_e_count = row['Item E']



        #print(item_a_count)

        item_a_time = fcq_hours(item_a_count, 0.5, 2, 3, 4, confidence=build_confidence)
        item_a_list.append(item_a_time)

        item_b_time = fcq_hours(item_b_count, 0.5, 1, 2, 3, confidence=build_confidence)
        item_b_list.append(item_b_time)

        item_c_time = fcq_hours(item_c_count, 0.5, 0.5, 0.75, 1, confidence=build_confidence)
        item_c_list.append(item_c_time)

        item_d_time = fcq_hours(item_d_count, 0.5, 1, 1.5, 2, confidence=build_confidence)
        item_d_list.append(item_d_time)

        item_e_time = fcq_hours(item_e_count, 0.5, 5, 7, 10, confidence=build_confidence)
        item_e_list.append(item_e_time)

        # print(row['Order #'], item_b_time, item_c_time, item_d_time, item_e_time)

    df['A T'] = item_a_list
    df['B T'] = item_b_list
    df['C T'] = item_c_list
    df['D T'] = item_d_list
    df['E T'] = item_e_list


    df['Build Time'] = df['A T'] + df['B T'] + df['C T'] + df['D T'] + df['E T']
    df['Pick Up Day'] = df['Build Time'].cumsum(axis=0)
    df['Pick Up Day'] = df['Pick Up Day'] + 1
    df['Wait Time'] = df['Pick Up Day'] - df['Day']


    # df = df[['Order #', 'Day', 'Item A', 'Item B', 'Item C', 'Item D', 'Item E',
    #          'Build Time', 'Pick Up Day', 'Wait Time']]

    print(df)
    #print(df['Build Time'].sum())
    return df

def priority_queue(df, build_confidence):
    pq_df = df

    order_a_list = []
    order_b_list = []
    order_c_list = []
    order_d_list = []
    order_e_list = []

    # https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    for index, row in pq_df.iterrows():
        order_a_count = row['Item A']
        order_b_count = row['Item B']
        order_c_count = row['Item C']
        order_d_count = row['Item D']
        order_e_count = row['Item E']

        order_a_time = pq_hours(order_a_count, 0, 2, 3, 4, confidence=build_confidence)
        order_a_list.append(order_a_time)

        order_b_time = pq_hours(order_b_count, 0, 1, 2, 3, confidence=build_confidence)
        order_b_list.append(order_b_time)

        order_c_time = pq_hours(order_c_count, 0, 0.5, 0.75, 1, confidence=build_confidence)
        order_c_list.append(order_c_time)

        order_d_time = pq_hours(order_d_count, 0, 1, 1.5, 2, confidence=build_confidence)
        order_d_list.append(order_d_time)

        order_e_time = pq_hours(order_e_count, 0, 5, 7, 10, confidence=build_confidence)
        order_e_list.append(order_e_time)

    pq_df['A T'] = order_a_list
    pq_df['B T'] = order_b_list
    pq_df['C T'] = order_c_list
    pq_df['D T'] = order_d_list
    pq_df['E T'] = order_e_list

    day_2 = pq_df[pq_df['Day'] == 2]
    import warnings
    warnings.filterwarnings('ignore')
    day_2['a_build'] = day_2['A T'].cumsum(axis=0)
    a_tail = day_2['a_build'].tail(1)
    print(a_tail)
    day_2['b_build'] = day_2['B T'].cumsum(axis=0)

    day_2['b_build'] = day_2['b_build'] + day_2['a_build'].tail(1)
    day_2['c_build'] = day_2['C T'].cumsum(axis=0)
    day_2['c_build'] = day_2['c_build'] + day_2['b_build'].tail(1)
    day_2['d_build'] = day_2['D T'].cumsum(axis=0)
    day_2['d_build'] = day_2['d_build'] + day_2['c_build'].tail(1)
    day_2['e_build'] = day_2['E T'].cumsum(axis=0)
    day_2['e_build'] = day_2['e_build'] + day_2['d_build'].tail(1)

    #print(day_2)
    day_3 = pq_df[pq_df['Day'] == 3]
    day_3['b_build'] = day_3['B T'].cumsum(axis=0)
    day_3['a_build'] = day_3['A T'].cumsum(axis=0)
    day_3['b_build'] = day_3['b_build'] + day_3['a_build'].tail(1)
    day_3['c_build'] = day_3['C T'].cumsum(axis=0)
    day_3['c_build'] = day_3['c_build'] + day_3['b_build'].tail(1)
    day_3['d_build'] = day_3['D T'].cumsum(axis=0)
    day_3['d_build'] = day_3['d_build'] + day_3['c_build'].tail(1)
    day_3['e_build'] = day_3['E T'].cumsum(axis=0)
    day_3['e_build'] = day_3['e_build'] + day_3['d_build'].tail(1)
    #print(day_3)
    all_days = pd.concat([day_2, day_3])
    all_days['b_build'] = all_days.groupby(['Order #', 'Day'])['a_build'].tail(1) + all_days['b_build']
    #print(all_days)

    # test = pq_df
    #
    # test['a_build'] = test.groupby(['Order #', 'Day'])['A T'].cumsum(axis=0)
    # test['b_build'] = test.groupby(['Order #', 'Day'])['B T'].cumsum(axis=0)
    #
    # test['b_build'] = test['b_build'] + test['a_build'].tail(1)
    # print(test)



    # t['A cumsum'] = t.groupby(by=['A T']).cumsum(axis=0)
    # t['B cumsum'] = t.groupby(by=['B T']).cumsum(axis=0)
    # t['C cumsum'] = t.groupby(by=['C T']).cumsum(axis=0)
    # t['D cumsum'] = t.groupby(by=['D T']).cumsum(axis=0)
    # t['E cumsum'] = t.groupby(by=['E T']).cumsum(axis=0)
    # print(t)

    test2 = pq_df.groupby(['Order #', 'Day'])['A T', 'B T', 'C T', 'D T', 'E T'].sum(axis=0).reset_index()

    pq_df['A cumsum'] = pq_df.groupby(['Day'])['A T'].cumsum(axis=0)
    pq_df['B cumsum'] = pq_df.groupby(['Day'])['B T'].cumsum(axis=0)
    pq_df['C cumsum'] = pq_df.groupby(['Day'])['C T'].cumsum(axis=0)
    pq_df['D cumsum'] = pq_df.groupby(['Day'])['D T'].cumsum(axis=0)
    pq_df['E cumsum'] = pq_df.groupby(['Day'])['E T'].cumsum(axis=0)

    ba = pq_df.groupby('Day')['A cumsum'].max()
    bb = pq_df.groupby('Day')['B cumsum'].max()
    bc = pq_df.groupby('Day')['C cumsum'].max()
    bd = pq_df.groupby('Day')['D cumsum'].max()
    be = pq_df.groupby('Day')['E cumsum'].max()

    # https://stackoverflow.com/questions/12307099/modifying-a-subset-of-rows-in-a-pandas-dataframe
    for l in range(1, 23):
        pq_df.loc[pq_df.Day == l, 'batch A T'] = ba[l] + 0.5
        pq_df.loc[pq_df.Day == l, 'batch B T'] = bb[l] + 0.5
        pq_df.loc[pq_df.Day == l, 'batch C T'] = bc[l] + 0.5
        pq_df.loc[pq_df.Day == l, 'batch D T'] = bd[l] + 0.5
        pq_df.loc[pq_df.Day == l, 'batch E T'] = be[l] + 0.5



    #pq_df['batch E T'] = np.where(pq_df['E cumsum'] != 0, pq_df['E cumsum'], pq_df['E cumsum'])

    pq_df['Build Time'] = pq_df['batch A T'] + pq_df['batch B T'] + pq_df['batch C T'] + \
                              pq_df['batch D T'] + pq_df['batch E T']

    #print(pq_df)
    # df_test['batch E T'] = np.where(df_test['E T'] != 0, df_test['batch E T'], df_test['E T'])

    batch_made = pq_df.groupby('Day')['Build Time'].max()
    batch_made = batch_made.cumsum()

    merge = pd.merge(pq_df, batch_made, left_on='Day', right_on='Day', how='inner', suffixes=(' ', ' merge'))


    print(merge.head(15))

    # https://stackoverflow.com/questions/49161120/pandas-python-set-value-of-one-column-based-on-value-in-another-column
    # for j in range(1, 23):
    #     pq_df.loc[pq_df.Day == j, 'Pick Up Day'] = pq_df['Build Time'] + pq_df['Pick Up Day'][j-1]
        #pq_df['Pick Up Day'] = np.where(pq_df['Day'] == 1, pq_df['Build Time'], pq_df['Build Time'])



desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 18)

generate_orders = orders(0, 3, 7, daily_count_confidence=4, order_size_confidence=4, samples=1)

first_come_queue(generate_orders, build_confidence=4)
#priority_queue(generate_orders, build_confidence=4)

# https://stackoverflow.com/questions/22650833/pandas-groupby-cumulative-sum -- not currenlty using this url

# print(df_test)
# A = df_test
# A = A.groupby(['Order #', 'Day'])['A T', 'B T', 'C T', 'D T', 'E T'].sum(axis=0).reset_index()
# #A['tot'] = A['A T'] + A['B T'] + A['C T'] + A['D T'] + A['E T']
# print(A)
#
# # get the total item batch time per order
# df_test['A cumsum'] = df_test.groupby(['Day'])['A T'].cumsum(axis=0)
# df_test['B cumsum'] = df_test.groupby(['Day'])['B T'].cumsum(axis=0)
# df_test['C cumsum'] = df_test.groupby(['Day'])['C T'].cumsum(axis=0)
# df_test['D cumsum'] = df_test.groupby(['Day'])['D T'].cumsum(axis=0)
# df_test['E cumsum'] = df_test.groupby(['Day'])['E T'].cumsum(axis=0)
#
# # extract when last item done
# ba = df_test.groupby('Day')['A cumsum'].max()
# bb = df_test.groupby('Day')['B cumsum'].max()
# bc = df_test.groupby('Day')['C cumsum'].max()
# bd = df_test.groupby('Day')['D cumsum'].max()
# be = df_test.groupby('Day')['E cumsum'].max()
#
# # https://stackoverflow.com/questions/12307099/modifying-a-subset-of-rows-in-a-pandas-dataframe
# for i in range(1, 23):
#     df_test.loc[df_test.Day == i, 'batch A T'] = ba[i] + 0.5
#     df_test.loc[df_test.Day == i, 'batch B T'] = bb[i] + 0.5
#     df_test.loc[df_test.Day == i, 'batch C T'] = bc[i] + 0.5
#     df_test.loc[df_test.Day == i, 'batch D T'] = bd[i] + 0.5
#     df_test.loc[df_test.Day == i, 'batch E T'] = be[i] + 0.5
#
#
# df_test['Build Time'] = df_test['batch A T'] + df_test['batch B T'] + df_test['batch C T'] + \
#                             df_test['batch D T'] + + df_test['batch E T']
#
# # df_test['batch E T'] = np.where(df_test['E T'] != 0, df_test['batch E T'], df_test['E T'])
#
# max_df = df_test.groupby('Day')['Build Time'].max()
# max_df = max_df.cumsum()
#
# merge = pd.merge(df_test, max_df, left_on='Day', right_on='Day', how='inner', suffixes=(' ', ' merge'))
# print(merge.head(15))
#
#
#
#
# # https://stackoverflow.com/questions/49161120/pandas-python-set-value-of-one-column-based-on-value-in-another-column
# for j in range(1, 23):
#     # df_test.loc[df_test.Day == j, 'Pick Up Day'] = df_test['Build Time'] + df_test['Pick Up Day'][j-1]
#     df_test['Pick Up Day'] = np.where(df_test['Day'] == 1, df_test['Build Time'], df_test['Build Time'])
#
#     # cumsum_df = df_test.groupby('Day')['Build Time'].max()
#     # cumsum_df = max_df.cumsum()
#     # df_test['Pick Up Day'] = np.where(df_test['Day'] == 1, df_test['Build Time'], df_test['Build Time'])
#
#
#
#
#
#
#





    #df_test['Pick Up Day'] = np.where(df_test['Day'] != 1, df_test['Build Time'], df_test['Build Time'])
    # df_test.loc[df_test.Day == j, 'Pick Up Day'] = (df_test['Build Time'])
    # df_test['Pick Up Day'] = np.where(df_test['Day'] == 1, df_test['Build Time'], df_test['Build Time'] + max_df[j])
    #
    # if df_test.loc[df_test.Day > 1]:
    #     df_test['Pick Up Day'] = df_test['Pick Up Day'][j-1] + df_test['Build Time'][j]


# print df.groupby(by=['name','day']).sum().groupby(level=[0]).cumsum()
#df_test = df_test[['Order #', 'Day',  'Build Time', 'Item A', 'A T', 'test A', 'batch A T']]

#https://stackoverflow.com/questions/48123368/pandas-error-when-using-if-else-to-create-new-column-the-truth-value-of-a-serie/48123413
#df = df.assign(C=np.where(df['B'] != 0, df['A'] / df['B'], sentinel))



# https://stackoverflow.com/questions/48123368/pandas-error-when-using-if-else-to-create-new-column-the-truth-value-of-a-serie/48123413
# if then else
# go back to days loc !!

#df_test['batch A T'] = np.where(df_test['B T'] == 0, df_test['test A'], df_test['batch B T'])

#df_test['batch A T'] = np.where((df_test['B T'] == 0) | (df_test['C T'] == 0), 0, df_test['batch A T'])

# df_test['batch B T'] = np.where(df_test['B T'] == 0, df_test['test B'], df_test['test B'])
# df_test['batch C T'] = np.where(df_test['C T'] == 0, df_test['test C'], df_test['test C'])
# df_test['batch C T'] = np.where(df_test['C T'] != 0, df_test['batch C T'], df_test['C T'])
#
# df_test['Build Time'] = df_test['batch A T'] + df_test['batch B T'] + df_test['batch C T']
#df_test['Pick Up Day'] = df_test.groupby('Day')['Build Time'].cumsum() #.groupby(level=[0]).cumsum()  # use max equation subset
#max_df = df_test.groupby('Day')['Build Time'].max().cumsum()
# max_df = df_test.groupby('Day')['Pick Up Day'].max().cumsum()


# stock_df['Build Item A'] = np.where(stock_df['Surplus A Stock'] >= 1, 0, stock_df['Item A'])
