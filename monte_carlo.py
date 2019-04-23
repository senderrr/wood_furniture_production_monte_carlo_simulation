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
            order_size = pert(1, 2, 15, confidence=order_size_confidence, samples=samples)
            order_size = np.around(order_size).astype(int)
            order_items = np.random.choice(item_order_options, size=order_size, p=[0.1, 0.2, 0.4, 0.2, 0.1])
            print(order_items, 'day:', day_counter,'order:', j + 1)

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
    df = pd.DataFrame({'Order #': order_len,
                    'Day': column_day,
                    'Item A': column_a,
                    'Item B': column_b,
                    'Item C': column_c,
                    'Item D': column_d,
                    'Item E': column_e})
    df['Order #'] = df['Order #'] + 1

    print(df)
    return df
    # dictionary version
    # start = z[0] + 1
    # stop = z[-1] + 1
    # order_id = range(start,stop)
    # for fcq in all_orders:
    #     t = fcq.tolist()
    #     all_orders.append(t)
    # res = dict(zip(order_id, all_orders))
    # print(res)


def fcq_hours(array, machine_time_swap, low, likely, high, confidence):
    item_count = array
    item_time = pert(low, likely, high, confidence=confidence, samples=item_count)
    item_time = np.sum(item_time)
    if item_time != 0:
        item_time = item_time + machine_time_swap
    item_time = item_time/7.5
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

        item_a_time = fcq_hours(item_a_count, 0.5, 4, 8, 11, confidence=build_confidence)
        item_a_list.append(item_a_time)

        item_b_time = fcq_hours(item_b_count,0.5, 1, 2, 5, confidence=build_confidence)
        item_b_list.append(item_b_time)

        item_c_time = fcq_hours(item_c_count, 0.5, 0.5, 1, 3, confidence=build_confidence)
        item_c_list.append(item_c_time)

        item_d_time = fcq_hours(item_d_count, 0.5, 2, 3, 6, confidence=build_confidence)
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
    df = df[['Order #', 'Day', 'Item A', 'Item C', 'Item D', 'Item E',
             'Build Time', 'Pick Up Day']]

    # pd.set_option('display.max_columns', 15)

    # print(q)decade_df['Year'] = decade_df['Year'].str[:3]
    print(df)


def priority_queue(Q, build_confidence, samples):
    week_time_counter = []
    time_counter = 0
    while time_counter <= 7.5:
        a_counter = 0

        for pq in Q:
            #print(t)
            items_A = np.count_nonzero(pq == 'A')
            a_counter += items_A

        order_A_time_range = pert(7, 10, 15, confidence=build_confidence, samples=samples)
        order_A_time_range = np.around(order_A_time_range, decimals=2)
        order_A_time = a_counter * order_A_time_range


generate_orders = orders(0, 2, 10, daily_count_confidence=4, order_size_confidence=4, samples=1)
first_come_queue(generate_orders, build_confidence=4)

# priority_queue(generate_orders), build_confidence=4, samples=1)

# old code
       # print(q)
# def first_come_queue(q, build_confidence, samples):

# order_counter = 0

    # for fcq in q:
    #     order_counter += 1
    #     a_count = fcq[fcq == 'A']
    #     a_count = np.count_nonzero(a_count)
    #
    #     time_list = []
    #     machine_time_swap = 0.5
    #
    #     for a in range(a_count):
    #         order_a_time = pert(4, 8, 11, confidence=build_confidence, samples=samples)
    #         order_a_time = order_a_time/7.5
    #         order_a_time = order_a_time + machine_time_swap
    #         order_a_time = np.around(order_a_time, decimals=1)
    #
    #         time_list.append(order_a_time)
    #
    #
    #     all_item_build_time = np.sum(time_list)
    #     all_item_build_time = np.around(all_item_build_time, decimals=1)
    #     time_to_make_order = all_item_build_time  # + machine_swap_time
    #     time_to_make_order = np.around(time_to_make_order, decimals=1)
    #     time_to_make_order = str(time_to_make_order)
    #     print('Order', order_counter, ':', fcq, '---', 'Time to make Order. \ +
    #   Days:', time_to_make_order[0], 'Hours:', time_to_make_order[2], time_to_make_order)