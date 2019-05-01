import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


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
            order_items = np.random.choice(item_order_options, size=order_size, p=[0.3, 0.1, 0.3, 0.2, 0.1])
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


def build_time(array, machine_time_swap, low, likely, high, confidence):
    item_count = array
    item_hours = pert(low, likely, high, confidence=confidence, samples=item_count)
    item_hours = np.sum(item_hours)
    if item_hours != 0:
        item_hours = item_hours + machine_time_swap
    item_hours = item_hours          # change days to hours; wait time/ pick up day (floor, ceiling round; modulus); 2 shifts; first come queue with inventory
    item_hours = np.around(item_hours, decimals=1)
    return item_hours

def first_come_queue(df, machine_time_swap, build_confidence):
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

        item_a_time = build_time(item_a_count, machine_time_swap, 1, 3, 4, confidence=build_confidence)
        item_a_list.append(item_a_time)

        item_b_time = build_time(item_b_count, machine_time_swap, 0.5, 0.75, 1, confidence=build_confidence)
        item_b_list.append(item_b_time)

        item_c_time = build_time(item_c_count, machine_time_swap, 1, 1.5, 2, confidence=build_confidence)
        item_c_list.append(item_c_time)

        item_d_time = build_time(item_d_count, machine_time_swap, 2, 2.5, 3, confidence=build_confidence)
        item_d_list.append(item_d_time)

        item_e_time = build_time(item_e_count, machine_time_swap, 4, 5, 6, confidence=build_confidence)
        item_e_list.append(item_e_time)

    df['A T'] = item_a_list
    df['B T'] = item_b_list
    df['C T'] = item_c_list
    df['D T'] = item_d_list
    df['E T'] = item_e_list

    df['Build Time'] = df['A T'] + df['B T'] + df['C T'] + df['D T'] + df['E T']
    df['Pick Up Day'] = np.ceil((df['Build Time'].cumsum(axis=0)) / 7.5)
    df['Wait Time'] = df['Pick Up Day'] - df['Day'] + 1

    print(df)
    return df


def inventory_first_come_queue(df, machine_time_swap,  build_confidence, a_stock, b_stock, c_stock, d_stock, e_stock):
    stock_df = df

    # inventory_df['A Stock Needed'] = inventory_df['Item A'] - a_stock
    # inventory_df['Build Item A'] = inventory_df['A Stock Needed'] + a_stock
    # inventory_df['Current Stock A'] = inventory_df['Build Item A'] - inventory_df['A Stock Needed']

    stock_df['Surplus A Stock'] = a_stock - stock_df['Item A']
    stock_df['Build Item A'] = abs(a_stock - stock_df['Surplus A Stock'])
    stock_df['Stock A Quantity'] = stock_df['Build Item A'] + stock_df['Surplus A Stock']

    stock_df['Surplus B Stock'] = b_stock - stock_df['Item B']
    stock_df['Build Item B'] = abs(b_stock - stock_df['Surplus B Stock'])
    stock_df['Stock B Quantity'] = stock_df['Build Item B'] + stock_df['Surplus B Stock']

    stock_df['Surplus C Stock'] = c_stock - stock_df['Item C']
    stock_df['Build Item C'] = abs(c_stock - stock_df['Surplus C Stock'])
    stock_df['Stock C Quantity'] = stock_df['Build Item C'] + stock_df['Surplus C Stock']

    stock_df['Surplus D Stock'] = d_stock - stock_df['Item D']
    stock_df['Build Item D'] = abs(d_stock - stock_df['Surplus D Stock'])
    stock_df['Stock D Quantity'] = stock_df['Build Item D'] + stock_df['Surplus D Stock']

    stock_df['Surplus E Stock'] = e_stock - stock_df['Item E']
    stock_df['Build Item E'] = abs(e_stock - stock_df['Surplus E Stock'])
    stock_df['Stock E Quantity'] = stock_df['Build Item E'] + stock_df['Surplus E Stock']


    # inventory_df['A to Fulfil Order'] = a_stock - inventory_df['Item A']
    # inventory_df['Build Item A'] = inventory_df['A to Fulfil Order'] + a_stock
    # inventory_df['Current Stock A'] = inventory_df['Build Item A'] - inventory_df['A to Fulfil Order']

    item_a_list = []
    item_b_list = []
    item_c_list = []
    item_d_list = []
    item_e_list = []

    for index, row in df.iterrows():
        item_a_count = row['Item A']
        item_b_count = row['Item B']
        item_c_count = row['Item C']
        item_d_count = row['Item D']
        item_e_count = row['Item E']

        item_a_time = build_time(item_a_count, machine_time_swap, 1, 3, 4, confidence=build_confidence)
        item_a_list.append(item_a_time)

        item_b_time = build_time(item_b_count, machine_time_swap, 0.5, 0.75, 1, confidence=build_confidence)
        item_b_list.append(item_b_time)

        item_c_time = build_time(item_c_count, machine_time_swap, 1, 1.5, 2, confidence=build_confidence)
        item_c_list.append(item_c_time)

        item_d_time = build_time(item_d_count, machine_time_swap, 2, 2.5, 3, confidence=build_confidence)
        item_d_list.append(item_d_time)

        item_e_time = build_time(item_e_count, machine_time_swap, 4, 5, 6, confidence=build_confidence)
        item_e_list.append(item_e_time)

    stock_df['A T'] = item_a_list
    stock_df['B T'] = item_b_list
    stock_df['C T'] = item_c_list
    stock_df['D T'] = item_d_list
    stock_df['E T'] = item_e_list

    stock_df['Build Time'] = stock_df['A T'] + stock_df['B T'] + stock_df['C T'] + stock_df['D T'] + stock_df['E T']
    stock_df['Pick Up Day'] = np.ceil((stock_df['Build Time'].cumsum(axis=0) / 7.5))
    stock_df['Wait Time'] = stock_df['Pick Up Day'] - stock_df['Day'] + 1

    print(stock_df)
    return stock_df


desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 18)


def main():
    for s in range(10):
        
        generate_orders = orders(0, 3, 7, daily_count_confidence=4, order_size_confidence=4, samples=1)
        # first_come_queue(generate_orders, machine_time_swap=0.5, build_confidence=4)
        inventory = inventory_first_come_queue(generate_orders, machine_time_swap=0.5, build_confidence=4, a_stock=6,
                                               b_stock=6, c_stock=8, d_stock=6, e_stock=3)
        average_wait_time = inventory['Wait Time'].tail(1)
        average_wait_time = np.mean(average_wait_time)

        print(average_wait_time)


main()


# stock_inventory = {'Stock A': [2], 'Stock B': [2], 'Stock C': [3], 'Stock D': [2], 'Stock E': 1}
# inventory_df = pd.DataFrame(data=inventory, columns=['Stock A', 'Stock B', 'Stock C', 'Stock D', 'Stock E'])
# inventory_df = inventory_df.reset_index()
# inventory_df = pd.concat([inventory_df, df], axis=1)
# inventory_df = inventory_df.fillna(0)
