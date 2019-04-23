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

    # start = z[0] + 1
    # stop = z[-1] + 1
    # order_id = range(start,stop)
    # for fcq in all_orders:
    #     t = fcq.tolist()
    #     all_orders.append(t)
    # res = dict(zip(order_id, all_orders))
    # print(res)

    print('---')

    return df
    # return all_orders


# def first_come_queue(q, build_confidence, samples):

# order_counter = 0

    # for fcq in q:
    #     order_counter += 1
    #     a_count = fcq[fcq == 'A']
    #     a_count = np.count_nonzero(a_count)
    #
    #     b_count = fcq[fcq == 'B']
    #     b_count = np.count_nonzero(b_count)
    #
    #     c_count = fcq[fcq == 'C']
    #     c_count = np.count_nonzero(c_count)
    #
    #     d_count = fcq[fcq == 'D']
    #     d_count = np.count_nonzero(d_count)
    #
    #     e_count = fcq[fcq == 'E']
    #     e_count = np.count_nonzero(e_count)
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
    #     for b in range(b_count):
    #         order_b_time = pert(1, 2, 5, confidence=build_confidence, samples=b_count)
    #         order_b_time = order_b_time/7.5
    #         order_b_time = order_b_time + machine_time_swap
    #         order_b_time = np.around(order_b_time, decimals=1)
    #         time_list.append(order_b_time)
    #
    #
    #     for c in range(c_count):
    #         order_c_time = pert(.5, 1, 3, confidence=build_confidence, samples=samples)
    #         order_c_time = order_c_time/7.5
    #         order_c_time = order_c_time + machine_time_swap
    #         order_c_time = np.around(order_c_time, decimals=1)
    #         time_list.append(order_c_time)
    #
    #
    #     for d in range(d_count):
    #         order_d_time = pert(2, 3, 6, confidence=build_confidence, samples=samples)
    #         order_d_time = order_d_time/7.5
    #         order_d_time = order_d_time + machine_time_swap
    #         order_d_time = np.around(order_d_time, decimals=1)
    #         time_list.append(order_d_time)
    #
    #
    #     for e in range(e_count):
    #         order_e_time = pert(5, 7, 10, confidence=build_confidence, samples=samples)
    #         order_e_time = order_e_time/7.5
    #         order_e_time = order_e_time + machine_time_swap
    #         order_e_time = np.around(order_e_time, decimals=1)
    #         time_list.append(order_e_time)
    #
    #
    #     all_item_build_time = np.sum(time_list)
    #     all_item_build_time = np.around(all_item_build_time, decimals=1)
    #     time_to_make_order = all_item_build_time  # + machine_swap_time
    #     time_to_make_order = np.around(time_to_make_order, decimals=1)
    #     time_to_make_order = str(time_to_make_order)
    #     print('Order', order_counter, ':', fcq, '---', 'Time to make Order. Days:', time_to_make_order[0], 'Hours:', time_to_make_order[2], time_to_make_order)


def priority_queue(Q, build_confidence, samples):
    # daily_que  = queue.Queue(maxsize=20)
    # work = True
    # while work is True:
    #     time_counter = 0
    #
    week_time_counter = []
    time_counter = 0
    while time_counter <= 7.5:
        a_counter = 0
        b_counter = 0
        c_counter = 0
        d_counter = 0
        e_counter = 0

        for pq in Q:
            #print(t)
            items_A = np.count_nonzero(pq == 'A')
            a_counter += items_A
            #print('max',np.max(a_counter))
            # A_list.append(items_A)
            #print(np.count_nonzero(items_A))
            items_B = np.count_nonzero(pq == 'B')
            b_counter += items_B

            items_C = np.count_nonzero(pq == 'C')
            c_counter += items_C

            items_D = np.count_nonzero(pq == 'D')
            d_counter += items_D

            items_E = np.count_nonzero(pq == 'E')
            e_counter += items_E


        order_A_time_range = pert(7, 10, 15, confidence=build_confidence, samples=samples)
        order_A_time_range = np.around(order_A_time_range, decimals=2)

        order_B_time_range = pert(1, 2, 5, confidence=build_confidence, samples=samples)
        order_B_time_range = np.around(order_B_time_range, decimals=2)

        order_C_time_range= pert(6, 8, 10, confidence=build_confidence, samples=samples)
        order_C_time_range = np.around(order_C_time_range, decimals=2)

        order_D_time_range = pert(5, 9, 13, confidence=build_confidence, samples=samples)
        order_D_time_range = np.around(order_D_time_range, decimals=2)


        order_E_time_range = pert(12, 15, 20, confidence=build_confidence, samples=samples)
        order_E_time_range = np.around(order_E_time_range, decimals=2)

        order_A_time = a_counter * order_A_time_range
        order_B_time = b_counter * order_B_time_range
        order_C_time = c_counter * order_C_time_range
        order_D_time = d_counter * order_D_time_range
        order_E_time = e_counter * order_E_time_range

        if order_A_time != 0:
            time_counter += order_A_time
        elif order_B_time != 0:
            time_counter += order_B_time
        elif order_C_time != 0:
            time_counter += order_C_time
        elif order_D_time != 0:
            time_counter += order_D_time
        elif order_E_time != 0:
            time_counter += order_E_time
        else:
            time_counter.append(week_time_counter)
            print(week_time_counter)
            #print(time_counter)
            #print('days to build:', time_counter/7.5)
            continue
    print(week_time_counter)


        #print(np.count_nonzero(items_A))

            # print('Order A: hours to build:', order_A_time)
            # print('Order B: hours to build:', order_B_time)
            # print('Order C: hours to build:', order_C_time)
            # print('Order D: hours to build:', order_D_time)
            # print('Order E: hours to build:', order_E_time)
            # print('All Orders : hours to build:', (order_A_time + order_B_time + order_C_time + order_D_time + order_E_time))



#def time():
orders(0, 2, 10, daily_count_confidence=4, order_size_confidence=4, samples=1)
#first_come_queue(orders(0, 2, 10, daily_count_confidence=4, order_size_confidence=4, samples=1), build_confidence=4, samples=1)
#priority_queue(orders(0, 2, 10, daily_count_confidence=4, order_size_confidence=4, samples=1), build_confidnece=4, samples=1)