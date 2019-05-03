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




    pq_df['Build Time'] = pq_df['batch A T'] + pq_df['batch B T'] + pq_df['batch C T'] + \
                              pq_df['batch D T'] + pq_df['batch E T']


    batch_made = pq_df.groupby('Day')['Build Time'].max()
    batch_made = batch_made.cumsum()

    merge = pd.merge(pq_df, batch_made, left_on='Day', right_on='Day', how='inner', suffixes=(' ', ' merge'))


    print(merge.head(15))



desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 18)

generate_orders = orders(0, 3, 7, daily_count_confidence=4, order_size_confidence=4, samples=1)

#first_come_queue(generate_orders, build_confidence=4)
priority_queue(generate_orders, build_confidence=4)