"""
By Alex Wieker; Email: awieker2@illinois.edu
IS 590 PR Final Project: Wood Furniture Production Monte Carlo Simulation"
See assignment instructions in the README.md document.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings


desired_width = 500
pd.set_option('display.width', desired_width)
pd.set_option('display.max_columns', 30)


def main(num_of_samples):
    """This function runs the orders function to generate an order that is the rounded up US average work day per month,
    22 days, and then puts that set of orders into the first_come_queue and stock_inventory_que 10,000 times. After
    the simulation is run 10,000 times this function outputs aggregate statistics and two histogram distributions, one
    for each of the different type of scenarios being run in the simulation.
    :param num_of_samples: This is an input parameter to set how many times to run the simulation.
    """

    warnings.filterwarnings('ignore', category=RuntimeWarning)

    fcq_wait_time_list = np.array([])
    stock_wait_time_list = np.array([])

    for i in range(num_of_samples):
        print('Running sample:', i)
        generate_orders = orders(0, 3, 7, daily_count_confidence=4, order_size_confidence=4, samples=1)
        fcq = first_come_queue(generate_orders, machine_time_swap=0.5, build_confidence=4)

        stock_queue = stock_inventory_queue(generate_orders, machine_time_swap=0.5, build_confidence=4, a_stock=6,
                                            b_stock=6, c_stock=8, d_stock=6, e_stock=3)

        fcq_wait_time_list = np.append(fcq_wait_time_list, fcq['Wait Time'])

        stock_wait_time_list = np.append(stock_wait_time_list, stock_queue['Wait Time'])

    print('Median first come queue customer wait time:', np.median(fcq_wait_time_list))
    print('Mean first come queue customer wait time:', np.around(np.mean(fcq_wait_time_list), decimals=2))
    print('Max first come queue customer wait time:', np.max(fcq_wait_time_list))
    print('Min first come queue customer wait time:', np.min(fcq_wait_time_list))

    fcq_wait_time_hist = plt.hist(fcq_wait_time_list, bins=25, density=False)
    plt.xlabel('Wait Time')
    plt.ylabel('Count')
    plt.title('First Come First Serve Time Queue Distribution')
    #plt.savefig('First Come First Serve Time Queue Distribution.png')
    plt.show()

    print('----')

    print('Median stock inventory queue wait time customer wait time:', np.median(stock_wait_time_list))
    print('Mean stock inventory queue come queue customer wait time:', np.around(np.mean(stock_wait_time_list), decimals=2))
    print('Max stock inventory queue customer wait time:', np.max(stock_wait_time_list))
    print('Min stock inventory queue customer wait time:', np.min(stock_wait_time_list))

    fcq_wait_time_hist = plt.hist(stock_wait_time_list, bins=25, density=False)
    plt.xlabel('Wait Time')
    plt.ylabel('Count')
    plt.title('Stock Inventory Wait Time Queue Distribution')
    #plt.savefig('Stock Inventory Wait Time Queue Distribution.png')
    plt.show()


def pert(low, likely, high, confidence=4, samples=10000):
    """
    I got this function from Instructor Weible's Lecture Notes

    :param low: This input parameter is the lowest expected value.
    :param likely: This input parameter is the most likely expected value or mode
    :param high: This input parameter is the highest expectedvalue.
    :param confidence:
    :param samples:
    :return beta:
    """

    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta


def orders(low, likely, high, daily_count_confidence, order_size_confidence, samples):
    """
    :param low: This input variable is the lowest expected value, and will be called for the pert function.
    :param likely: This input variable is the most likely expected value or mode, and it will be used for the pert function.
    :param high: This input variable is the highest expected value, and will be used for the pert function.
    :param daily_count_confidence: This is an input parameter for setting confidence in knowing daily order count.
    :param order_size_confidence: This is an input parameter for setting confidence in knowing order size.
    :param samples: This is an input parameter for setting how many samples to run in the PERT function.
    :return df: This function returns a DataFrame, which will be called in later functions
    >>> generate_test_orders = orders(0, 3, 7, daily_count_confidence=4, order_size_confidence=4, samples=1)
    >>> type(generate_test_orders)
    <class 'pandas.core.frame.DataFrame'>
    >>> list(generate_test_orders)
    ['Order #', 'Day', 'Item A', 'Item B', 'Item C', 'Item D', 'Item E']
    """

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
        #print('daily order count:', daily_order_count)

        for j in range(daily_order_count[0]):
            order_size = pert(1, 8, 15, confidence=order_size_confidence, samples=samples)
            order_size = np.around(order_size).astype(int)
            order_items = np.random.choice(item_order_options, size=order_size, p=[0.3, 0.1, 0.3, 0.2, 0.1])
            #print(order_items, 'day:', day_counter, 'order:', j + 1)

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
    df = pd.DataFrame({'Order #': order_len, 'Day': column_day, 'Item A': column_a, 'Item B': column_b,
                       'Item C': column_c, 'Item D': column_d, 'Item E': column_e})
    df['Order #'] = df['Order #'] + 1
    return df


def build_time(item_list, machine_time_swap, low, likely, high, confidence):
    """This function takes an input list, calls the pert function that list to calculate how long it takes to build
    all of the items in the list, and then returns the calculated series.
    :param item_list: This input variable is a list of item counts.
    :param machine_time_swap: This input variable is how long it takes to swap machines.
    :param low: This input variable is the lowest expected value, and will be called for the pert function.
    :param likely: This input variable is the most likely expected value or mode, and it will be used for the pert function.
    :param high: This input variable is the expected highest, and will be used for the pert function.
    :param confidence: This is an input parameter for setting confidence in knowing the PERT distribution range.
    :return item_hours: This function returns a list of how long it takes to build each of the items from item_list.
    >>> test_df = pd.DataFrame({'Item A': [1, 3, 2, 2, 5, 6, 7, 10]})
    >>> test_df = (generate_orders, machine_time_swap=0.5, build_confidence=4)
       Item A
    0       1
    1       3
    2       2
    3       2
    4       5
    5       6
    6       7
    7      10
    >>> item_list = test_df['Item A']
    >>> type(item_list)
    <class 'pandas.core.series.Series'>
    >>> test_df_build_time = build_time(item_list, 0.5, 1, 1.5, 2, confidence=4)
    >>> type(test_df_build_time)
    <class 'numpy.float64'>
    """

    item_count = item_list.astype('int')
    item_hours = pert(low, likely, high, confidence=confidence, samples=item_count)
    item_hours = np.sum(item_hours)
    if item_hours != 0:
        item_hours = item_hours + machine_time_swap
    item_hours = item_hours
    item_hours = np.around(item_hours, decimals=1)
    return item_hours


def first_come_queue(df, machine_time_swap, build_confidence):
    """This function takes an input DataFrame (of orders), calculates how long it takes to build each of the orders, and
    then calculates how long customers are waiting for their order to  be available.
    :param df: This is an input DataFrame from the orders function, which is the set of orders being run in the simulation.
    :param machine_time_swap: This is an input parameter to pass to the build_time function for time to swap machines.
    :param build_confidence: This is an input parameter to pass to the build_time function to set item build confidence.
    :return first_come_df: This function returns this DataFrame, which is the completed first_come_queue.

    I adopted code from the following URL as a resource to iterate over DataFrame rows:
    https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
     """

    first_come_df = df.copy(deep=True)

    item_a_list = []
    item_b_list = []
    item_c_list = []
    item_d_list = []
    item_e_list = []

    for index, row in first_come_df.iterrows():
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

    first_come_df['Build A Hours'] = item_a_list
    first_come_df['Build B Hours'] = item_b_list
    first_come_df['Build C Hours'] = item_c_list
    first_come_df['Build D Hours'] = item_d_list
    first_come_df['Build E Hours'] = item_e_list

    first_come_df['Build Time'] = first_come_df['Build A Hours'] + first_come_df['Build B Hours'] + \
                                  first_come_df['Build C Hours'] + first_come_df['Build D Hours'] + \
                                  first_come_df['Build E Hours']
    first_come_df['Pick Up Day'] = np.ceil((first_come_df['Build Time'].cumsum(axis=0)) / 7.5)
    first_come_df['Wait Time'] = first_come_df['Pick Up Day'] + 1

    # print(first_come_df)
    return first_come_df


def stock_inventory_queue(df, machine_time_swap,  build_confidence, a_stock, b_stock, c_stock, d_stock, e_stock):
    """This function takes an input DataFrame (of orders), calculates how long it takes to build each of the orders, and
    then calculates how long customers are waiting for their order to  be available.
    Variables:
    Order #: order id
    Day: Day that work was started on order--customer orders come in the day before
    Item x: How many items were ordered per order
    Start Stock x: How much inventory the manufactory has of the item
    Surplus Stock: How much stock there is after taking items to fulfill order from inventory
    Build Item x: How many items needed to be built to fulfil and/or restock inventory
    Pick Up Day: The day in the work cycle that the item will be ready for the customer.Applied ceil to this calculation
    because orders need to be packaged after being made, which means that they will be available the next work day.
    Wait Time: How much time the customer waits from ordering the item and it being built. Calculated as Pick Up Day
    plus 1 because there is a one day lapse betweeen sending a receiving an order

    :param df: This is an input DataFrame from the orders function, which is the set of orders being run in the simulation.
    :param machine_time_swap: This is an input parameter to pass to the build_time function for time to swap machines.
    :param build_confidence: This is an input parameter to pass to the build_time function to set item build confidence
    :param a_stock: This input parameter for sets how much Item A stock should be available before orders come in.
    :param b_stock: This input parameter for sets how much Item B stock should be available before orders come in.
    :param c_stock: This input parameter for sets how much Item C stock should be available before orders come in.
    :param d_stock: This input parameter for sets how much Item D stock should be available before orders come in.
    :param e_stock: This input parameter for sets how much Item D stock should be available before orders come in.
    :return stock_df: This function returns this DataFrame, which is the completed stock_inventory_queue.

    https: // stackoverflow.com / questions / 16476924 / how - to - iterate - over - rows - in -a - dataframe - in -pandas
    """

    stock_df = df.copy(deep=True)

    stock_df['Start Stock A'] = 0
    stock_df['Surplus A Stock'] = a_stock - stock_df.groupby('Day')['Item A'].cumsum(axis=0)
    stock_df['Start Stock A'] = stock_df.groupby('Day')['Surplus A Stock'].shift(1).fillna(a_stock).astype('int')
    stock_df['Build Item A'] = np.where(stock_df['Surplus A Stock'] >= 1, 0,
                                        np.where(stock_df['Start Stock A'] >= 1,
                                                 stock_df['Item A'] - stock_df['Start Stock A'], stock_df['Item A']))

    # Take note that Surplus x stock was used as a means to an end. Since I had to make negative numbers zero,
    # in order to get accurate restock num. It has no negative effect on the simulation because all negative numbers
    # in the simulation have the same value as any other negative number. Additionally, I changed the value to zero
    # after I was already using it. Hence, when it is turned to zero, it is only used to calculate the restock column.
    # Lastly, I am simulating that restocking take place for the last order  items are build directly for the customer as they come, and then
    # restocked at the end of the day
    stock_df['Surplus A Stock'] = np.where(stock_df['Surplus A Stock'] < 0, 0, stock_df['Surplus A Stock'])
    stock_df['Restock A'] = stock_df.groupby('Day')['Surplus A Stock'].tail(1)
    stock_df['Restock A'] = a_stock - stock_df['Restock A']
    stock_df['Restock A'] = stock_df['Restock A'].fillna(0)
    # apply restock to next day order; Even though the restock is done after each day, the last day customer is able
    # to get their order before the restocking is completed, and the next day orders do not start until restock is done

    stock_df['Build Item A'] = stock_df['Build Item A'] + stock_df['Restock A']

    stock_df['Start Stock B'] = 0
    stock_df['Surplus B Stock'] = b_stock - stock_df.groupby('Day')['Item B'].cumsum(axis=0)
    stock_df['Start Stock B'] = stock_df.groupby('Day')['Surplus B Stock'].shift(1).fillna(b_stock).astype('int')
    stock_df['Build Item B'] = np.where(stock_df['Surplus B Stock'] >= 1, 0,
                                        np.where(stock_df['Start Stock B'] >= 1,
                                                 stock_df['Item B'] - stock_df['Start Stock B'], stock_df['Item B']))
    stock_df['Surplus B Stock'] = np.where(stock_df['Surplus B Stock'] < 0, 0, stock_df['Surplus B Stock'])
    stock_df['Restock B'] = stock_df.groupby('Day')['Surplus B Stock'].tail(1)
    stock_df['Restock B'] = b_stock - stock_df['Restock B']
    stock_df['Restock B'] = stock_df['Restock B'].fillna(0)
    stock_df['Build Item B'] = stock_df['Build Item B'] + stock_df['Restock B']

    stock_df['Start Stock C'] = 0
    stock_df['Surplus C Stock'] = c_stock - stock_df.groupby('Day')['Item C'].cumsum(axis=0)
    stock_df['Start Stock C'] = stock_df.groupby('Day')['Surplus C Stock'].shift(1).fillna(c_stock).astype('int')
    stock_df['Build Item C'] = np.where(stock_df['Surplus C Stock'] >= 1, 0,
                                        np.where(stock_df['Start Stock C'] >= 1,
                                                 stock_df['Item C'] - stock_df['Start Stock C'], stock_df['Item C']))
    stock_df['Surplus C Stock'] = np.where(stock_df['Surplus C Stock'] < 0, 0, stock_df['Surplus C Stock'])
    stock_df['Restock C'] = stock_df.groupby('Day')['Surplus C Stock'].tail(1)
    stock_df['Restock C'] = c_stock - stock_df['Restock C']
    stock_df['Restock C'] = stock_df['Restock C'].fillna(0)
    stock_df['Build Item C'] = stock_df['Build Item C'] + stock_df['Restock C']

    stock_df['Start Stock D'] = 0
    stock_df['Surplus D Stock'] = d_stock - stock_df.groupby('Day')['Item D'].cumsum(axis=0)
    stock_df['Start Stock D'] = stock_df.groupby('Day')['Surplus D Stock'].shift(1).fillna(d_stock).astype('int')
    stock_df['Build Item D'] = np.where(stock_df['Surplus D Stock'] >= 1, 0,
                                        np.where(stock_df['Start Stock D'] >= 1,
                                                 stock_df['Item D'] - stock_df['Start Stock D'], stock_df['Item D']))
    stock_df['Surplus D Stock'] = np.where(stock_df['Surplus D Stock'] < 0, 0, stock_df['Surplus D Stock'])
    stock_df['Restock D'] = stock_df.groupby('Day')['Surplus D Stock'].tail(1)
    stock_df['Restock D'] = d_stock - stock_df['Restock D']
    stock_df['Restock D'] = stock_df['Restock D'].fillna(0)
    stock_df['Build Item D'] = stock_df['Build Item D'] + stock_df['Restock D']

    stock_df['Start Stock E'] = 0
    stock_df['Surplus E Stock'] = e_stock - stock_df.groupby('Day')['Item E'].cumsum(axis=0)
    stock_df['Start Stock E'] = stock_df.groupby('Day')['Surplus E Stock'].shift(1).fillna(e_stock).astype('int')
    stock_df['Build Item E'] = np.where(stock_df['Surplus E Stock'] >= 1, 0,
                                        np.where(stock_df['Start Stock E'] >= 1,
                                                 stock_df['Item E'] - stock_df['Start Stock E'], stock_df['Item E']))
    stock_df['Surplus E Stock'] = np.where(stock_df['Surplus E Stock'] < 0, 0, stock_df['Surplus E Stock'])
    stock_df['Restock E'] = stock_df.groupby('Day')['Surplus E Stock'].tail(1)
    stock_df['Restock E'] = e_stock - stock_df['Restock E']
    stock_df['Restock E'] = stock_df['Restock E'].fillna(0)
    stock_df['Build Item E'] = stock_df['Build Item E'] + stock_df['Restock E']

    item_a_list = []
    item_b_list = []
    item_c_list = []
    item_d_list = []
    item_e_list = []

    for index, row in stock_df.iterrows():

        item_a_count = row['Build Item A']
        item_b_count = row['Build Item B']
        item_c_count = row['Build Item C']
        item_d_count = row['Build Item D']
        item_e_count = row['Build Item E']

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

    stock_df['Build A Hours'] = item_a_list
    stock_df['Build B Hours'] = item_b_list
    stock_df['Build C Hours'] = item_c_list
    stock_df['Build D Hours'] = item_d_list
    stock_df['Build E Hours'] = item_e_list

    stock_df['Order Build Hours'] = stock_df['Build A Hours'] + stock_df['Build B Hours'] + stock_df['Build C Hours'] \
                             + stock_df['Build D Hours'] + stock_df['Build E Hours']
    stock_df['Pick Up Day'] = np.ceil((stock_df['Order Build Hours'].cumsum(axis=0) / 7.5))
    stock_df['Wait Time'] = stock_df['Pick Up Day'] + 1

    stock_df_preview = stock_df[['Order #', 'Day', 'Item A', 'Item B', 'Item C', 'Item D', 'Item E', 'Build A Hours',
                                 'Build B Hours', 'Build C Hours', 'Build D Hours', 'Build E Hours',
                                 'Order Build Hours', 'Pick Up Day', 'Wait Time']]
    #print(stock_df_preview)

    item_a_preview = stock_df[['Order #', 'Item A', 'Start Stock A', 'Surplus A Stock', 'Restock A', 'Build Item A',
                               'Build A Hours']]
    #print(item_a_preview)
    return stock_df


main(num_of_samples=1000)
