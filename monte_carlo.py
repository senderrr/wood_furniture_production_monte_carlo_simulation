import numpy as np
import queue

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



# confidence 2
# miller & ranom

# what to do about my rounding?
def orders(low, likely, high, daily_count_confidence, order_size_confidence, samples):
    item_order_options = ['A', 'B', 'C', 'D', 'E']

    all_items = []

    # time_counter = 0
    # while time_counter <= 8:
    #     time_counter += j + 1

    for i in range(5):
        print(i + 1)
        daily_order_count = pert(low, likely, high, confidence=daily_count_confidence, samples=samples)
        daily_order_count = np.around(daily_order_count).astype(int)
        print('daily order count:', daily_order_count)
        # L = queue.Queue(maxsize=daily_order_count)
        # for z in range(daily_order_count[0])
        # daily order_count = z
        # for q in range(daily_order_count[0])
        #     daily_order_count = pert(low, likely, high, confidence=order_count_confidence, samples=samples)
        for j in range(daily_order_count[0]):
            order_size = pert(1, 3, 10, confidence=order_size_confidence, samples=samples)
            order_size = np.around(order_size).astype(int)
            order_items = np.random.choice(item_order_options, size=order_size, p=[0.1, 0.2, 0.4, 0.2, 0.1]) # put in probablity
            print(order_items, 'day:', i + 1, 'order:', j + 1)
            all_items.append(order_items)
# 6, 5, 5, 7, 4
        #print(order_items)
        # L.put(order_items)
        # t = L.get()
        # print(t)

        #print(order_items)

    return all_items

#def priority():

def get_que(Q, build_confidnece, samples):
    # daily_que  = queue.Queue(maxsize=20)
    # work = True
    # while work is True:
    #     time_counter = 0
    #
    time_counter = 0
    while time_counter <= 7.5:
        a_counter = 0
        b_counter = 0
        c_counter = 0
        d_counter = 0
        e_counter = 0

        for t in Q:
            #print(t)
            items_A = np.count_nonzero(t == 'A')
            a_counter += items_A
            #print('max',np.max(a_counter))
            # A_list.append(items_A)
            #print(np.count_nonzero(items_A))
            items_B = np.count_nonzero(t == 'B')
            b_counter += items_B

            items_C = np.count_nonzero(t == 'C')
            c_counter += items_C

            items_D = np.count_nonzero(t == 'D')
            d_counter += items_D

            items_E = np.count_nonzero(t == 'E')
            e_counter += items_E



        order_A_time_range = pert(7, 10, 15, confidence=build_confidnece, samples=samples)
        order_A_time_range = np.around(order_A_time_range, decimals=2)

        order_B_time_range = pert(1, 2, 5, confidence=build_confidnece, samples=samples)
        order_B_time_range = np.around(order_B_time_range, decimals=2)

        order_C_time_range= pert(6, 8, 10, confidence=build_confidnece, samples=samples)
        order_C_time_range = np.around(order_C_time_range, decimals=2)

        order_D_time_range = pert(5, 9, 13, confidence=build_confidnece, samples=samples)
        order_D_time_range = np.around(order_D_time_range, decimals=2)


        order_E_time_range = pert(12, 15, 20, confidence=build_confidnece, samples=samples)
        order_E_time_range = np.around(order_E_time_range, decimals=2)

        order_A_time = a_counter * order_A_time_range
        #print(order_A_time)
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
            #print(time_counter)
            #print('days to build:', time_counter/7.5)
            break


        #print(np.count_nonzero(items_A))

            # print('Order A: hours to build:', order_A_time)
            # print('Order B: hours to build:', order_B_time)
            # print('Order C: hours to build:', order_C_time)
            # print('Order D: hours to build:', order_D_time)
            # print('Order E: hours to build:', order_E_time)
            # print('All Orders : hours to build:', (order_A_time + order_B_time + order_C_time + order_D_time + order_E_time))



#def time():

get_que(orders(1, 5, 10, daily_count_confidence=4, order_size_confidence=2, samples=1), build_confidnece=2, samples=1)