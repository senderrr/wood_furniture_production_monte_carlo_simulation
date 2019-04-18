import numpy as np

def pert(low, likely, high, confidence=4, samples=10000):

    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta



# generate weekly orders
# confidence 2
# miller & ranom

# what to do about my rounding?
def orders(low, likely, high, confidence, samples):
    item_order_options = ['A', 'B', 'C', 'D', 'E']
    for i in range(5):
        daily_order_count = pert(low, likely, high, confidence=confidence, samples=samples)  # what should samples be?
        daily_order_count = np.around(daily_order_count).astype(int)
        #print(daily_order_count)
        all_items = []

        for j in range(daily_order_count[0]):
            order_size = pert(1, 3, 10, confidence=4, samples=samples)
            order_size = np.around(order_size).astype(int)
            print(order_size)
            order_items = np.random.choice(item_order_options, size=order_size, p=[0.1, 0.2, 0.4, 0.2, 0.1]) # put in probablity
            all_items.append(order_items)
            print(order_items)

    #print(all_items)
    for w in all_items:
        print(w)
    #need to add swapping machines (this is for doing like items at the same time)
        order_A = np.count_nonzero(w == 'A')
        order_B = np.count_nonzero(w == 'B')
        order_C = np.count_nonzero(w == 'C')
        order_D = np.count_nonzero(w == 'D')
        order_E = np.count_nonzero(w == 'E')


        order_A_time = order_A * 10
        order_B_time = order_B * 3
        order_C_time = order_C * 8
        order_D_time = order_D * 9
        order_E_time = order_E * 15

        print('Order A: hours to build:', order_A_time)
        print('Order B: hours to build:', order_B_time)
        print('Order C: hours to build:', order_C_time)
        print('Order D: hours to build:', order_D_time)
        print('Order E: hours to build:', order_E_time)
        print('All Orders : hours to build:', (order_A_time + order_B_time + order_C_time + order_D_time + order_E_time))

# generate how many workers are available
# def worker_count(low, likely, high, n_workers, samples):
#     worker_range = pert(low, likely, high, samples=samples)
#
#     total_weekly_hours_missed = max(worker_range)
#     hour_missed_range = round(total_weekly_hours_missed, 0)
#     print(hour_missed_range)
#
#     weekly_hours_missed = np.random.randint(hour_missed_range, size=n_workers)
#     print(weekly_hours_missed)
#
#     total_worker_hours = (n_workers * 35) - np.sum(weekly_hours_missed)
#     print(total_worker_hours)




orders(0, 5, 10, confidence=4, samples=1)

# worker_count(0, 3, 35, 8, 1)


# production  occupations: 3.0 per week
# https://www.bls.gov/cps/cpsaat47.htm#cps_eeann_abs_ft_occu_ind.f.1
