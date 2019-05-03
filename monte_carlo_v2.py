"""
By Alex Wieker; Email: awieker2@illinois.edu
IS 590 PR Final Project: Wood Furniture Production Monte Carlo Simulation"
See README.md document for additional simulation information.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings



def main(num_of_samples):
    """This function runs the orders function to generate an order that is the rounded up US average work day per month,
    22 days, and then puts that set of orders into the first_come_queue and stock_inventory_que 1,000 times. After
    the simulation is run 1,000 times this function outputs aggregate statistics and two histogram distributions, one
    for each of the different type of scenarios being run in the simulation.

    :param num_of_samples: This sets how many times to run the simulation.
    """

    warnings.filterwarnings('ignore', category=RuntimeWarning)

    fcq_wait_time_list = np.array([])
    stock_wait_time_list = np.array([])

    for i in range(num_of_samples):
        print('Running sample:', i)
        generate_orders = orders(0, 2, 5, daily_count_confidence=4, order_size_confidence=4, samples=1)
        fcq = first_come_queue(generate_orders, machine_time_swap=0.5, build_confidence=4)

        stock_queue = stock_inventory_queue(generate_orders, machine_time_swap=0.5, build_confidence=4, a_stock=6,
                                            b_stock=6, c_stock=8, d_stock=6, e_stock=3)

        fcq_wait_time_list = np.append(fcq_wait_time_list, fcq['Wait Time'])

        stock_wait_time_list = np.append(stock_wait_time_list, stock_queue['Wait Time'])

    print('Median first come queue customer wait time:', np.median(fcq_wait_time_list), 'days.')
    print('Mean first come queue customer wait time:', np.around(np.mean(fcq_wait_time_list), decimals=2), 'days.')
    print('Max first come queue customer wait time:', np.max(fcq_wait_time_list), 'days.')
    print('Min first come queue customer wait time:', np.min(fcq_wait_time_list), 'days.')

    fcq_wait_time_hist = plt.hist(fcq_wait_time_list, bins=11, density=False)
    plt.xlabel('Wait Time')
    plt.ylabel('Count')
    plt.title('First Come First Serve Wait Time Queue Distribution')
    plt.show()

    print('----')

    print('Median stock inventory queue wait time customer wait time:', np.median(stock_wait_time_list), 'days.')
    print('Mean stock inventory queue come queue customer wait time:',
          np.around(np.mean(stock_wait_time_list), decimals=2), 'days.')
    print('Max stock inventory queue customer wait time:', np.max(stock_wait_time_list), 'days.')
    print('Min stock inventory queue customer wait time:', np.min(stock_wait_time_list), 'days.')

    fcq_wait_time_hist = plt.hist(stock_wait_time_list, bins=11, density=False)
    plt.xlabel('Wait Time')
    plt.ylabel('Count')
    plt.title('Stock Inventory Wait Time Queue Distribution')
    plt.show()


def pert(low, likely, high, confidence=4, samples=10000):
    """ This function creates randoms numbers via the PERT distribution.

    :param low: This is the lowest expected value.
    :param likely: This is the most likely expected value or mode
    :param high: This is the highest expected value.
    :param confidence: This is 'lambda,' or how confident one is about the input range (low, likely, high).
    :param samples: How many samples to take in the PERT distribution.
    :return beta: The random number that is returned from this function.

    I got this function from Instructor Weible's Lecture Notes:
    https://github.com/iSchool-590PR-2019-Spring/examples_from_class/blob/master/class12_Prob_Distributions.ipynb
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
    """ This function uses the PERT distribution function and
    the np.random.choice function to create a set of random orders for a rounded average US work month, and outputs it
    in the form  of a DataFrame to be called later in the simulation for both types of scenarios.

    :param low: This is the lowest expected value, and will be called for the pert function.
    :param likely: This is the most likely expected value or mode, and it will be used for the pert function.
    :param high: This is the highest expected value, and will be used for the pert function.
    :param daily_count_confidence: This is 'lambda,' or how confidence in knowing daily order count PERT range.
    :param order_size_confidence: This is 'lambda,' or how confidence in knowing order size PERT range.
    :param samples: How many samples to take in the PERT distribution.
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
            order_size = pert(1, 3, 10, confidence=order_size_confidence, samples=samples)
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

    :param item_list: This is a list of item counts.
    :param machine_time_swap: This is how long it takes to swap machines.
    :param low: This is the lowest expected value, and will be called for the pert function,
                and will be called for the pert function.
    :param likely: This is the most likely expected value or mode, and it will be used for the pert function.
    :param high: This is the highest expected value, and will be used for the pert function.
    :param confidence: This is 'lambda,' or how confidence in knowing the PERT distribution range.
    :return item_hours: This function returns a list of how long it takes to build each of the items from item_list.

    >>> test_df = pd.DataFrame({'Item A': [1, 3, 2, 2, 5, 6, 7, 10]})
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

    :param df: This is the DataFrame from the orders function, which is the set of orders being run in the simulation.
    :param machine_time_swap: This is used for the build_time function for time to swap machines.
    :param build_confidence: This is 'lambda,' or how confidence in knowing the PERT distribution range, and
                            it is passed to the build_time function to set item build confidence.
    :return first_come_df: This function returns this DataFrame, which is the completed first_come_queue.

    I adopted code from the following URL as a resource to iterate over DataFrame rows:
    https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas

    >>> test_df = pd.DataFrame({'Item A': [1, 3, 2], 'Item B': [1, 2, 4], 'Item C': [3, 0, 2],
    ...     'Item D': [2, 1, 5], 'Item E': [5, 2, 0]})
    >>> test_df
       Item A  Item B  Item C  Item D  Item E
    0       1       1       3       2       5
    1       3       2       0       1       2
    2       2       4       2       5       0
    >>> test_df = first_come_queue(test_df, machine_time_swap=0.5, build_confidence=4)
    >>> test_df.columns
    Index(['Item A', 'Item B', 'Item C', 'Item D', 'Item E', 'Build A Hours', 'Build B Hours', 'Build C Hours', 'Build D Hours', 'Build E Hours', 'Build Time', 'Pick Up Day', 'Wait Time'], dtype='object')
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

    # Build Item x: How many items needed to be built to fulfil and/or restock inventory
    first_come_df['Build Time'] = first_come_df['Build A Hours'] + first_come_df['Build B Hours'] + \
                                  first_come_df['Build C Hours'] + first_come_df['Build D Hours'] + \
                                  first_come_df['Build E Hours']
    # Applied ceil to this calculation because orders need to be processed and are available the next work day.
    first_come_df['Pick Up Day'] = np.ceil((first_come_df['Build Time'].cumsum(axis=0)) / 7.5)
    # Added plus one to account for the customer ordering one day before the order was started in the manufactory.
    first_come_df['Wait Time'] = first_come_df['Pick Up Day'] + 1

    # print(first_come_df)

    return first_come_df


def build_stock_inventory(df, stock, item_column, start_stock, surplus_stock, build_item, restock):
    """ This function takes a DataFrame  for the stock_inventory_queue and determines when or how many items need to be
    pulled from the stock inventory to fulfill an order, and it also determines when to build additional items, in order
    to fulfill an order that requires more than there are items in the stock inventory or to restock it.

    :param df: This is the DataFrame that will be used to subset each of the items and to determine how many items
            need to build and when to fulfill orders or restock the stock inventory.
    :param stock: This is how much stock the manufactory holds at the start of a day of a given item, such as a_stock.
    :param item_column: This is the column of items
    :param start_stock: This a column that will be created for each item that describes starting stock inventory quantity.
    :param surplus_stock: This a column that will be created for each item that describes how much inventory there is
                        for each item after items have been pulled to fulfill orders.
    :param build_item: This is a column that will be created for each item
                    that describes how many items need to be built and when.
    :param restock: This is a column that will be created for each item that says how many items need to be made
                    at the end of the day to restock the stock inventory.
    :return build_item_column: This is a column that will be created that describes when and how many items
                            need to be built to fulfill each order that comes in or to restock the stock inventory.

    Note on calling function:
    All parameters in the function except for the initial DataFrame and stock parameter must be strings.

    IF you want to see how this function works, but on a smaller scale, uncomment the stock_preview in the
    stock_inventory_queue function, which will give a preview on only item A.

    Note on surplus stock parameter: Surplus stock was used as a means to an end. Since I had to make negative numbers
    zero, in order to get accurate restock number. It has no negative effect on the simulation because all negative
    numbers in this column have the same value as any other negative number in the simulation.
    Additionally, I changed the value to zero after I was already using it.
    Hence, when it is turned to zero, it is only used to calculate the restock column.

    Note on restock parameter: Lastly, I am simulating that restocking take place for the last order items are build
    directly for the customer as they come, and then restocked at the end of the day

    I adopted code from the following URL's as a resource to iterate over DataFrame rows:
    https://stackoverflow.com/questions/39109045/numpy-where-with-multiple-conditions/39111919
    """
    df[start_stock] = 0
    df[surplus_stock] = stock - df.groupby('Day')[item_column].cumsum(axis=0)
    # set stock to input stock value
    df[start_stock] = df.groupby('Day')[surplus_stock].shift(1).fillna(stock).astype('int')
    # How many items needed to be built to fulfil and/or restock inventory
    df[build_item] = np.where(df[surplus_stock] >= 1, 0, np.where(df[start_stock] >= 1,
                                                                  df[item_column] - df[start_stock], df[item_column]))
    df[surplus_stock] = np.where(df[surplus_stock] < 0, 0, df[surplus_stock])
    df[restock] = df.groupby('Day')[surplus_stock].tail(1)
    df[restock] = stock - df[restock]
    df[restock] = df[restock].fillna(0)
    df[build_item] = df[build_item] + df[restock]
    build_item_column = df[build_item]
    return build_item_column


def stock_inventory_queue(df, machine_time_swap,  build_confidence, a_stock, b_stock, c_stock, d_stock, e_stock):
    """This function takes an input DataFrame (of orders), calculates how long it takes to build each of the orders, and
    then calculates how long customers are waiting for their order to be available.

    :param df: This is the DataFrame from the orders function, which is the set of orders being run in the simulation.
    :param machine_time_swap: This is used for the build_time function for time to swap machines.
    :param build_confidence: This is 'lambda,' or how confidence in knowing the PERT distribution range, and
                            it is passed to the build_time function to set item build confidence.
    :param a_stock: This sets how much Item A stock should be available before orders come in.
    :param b_stock: This sets how much Item B stock should be available before orders come in.
    :param c_stock: This sets how much Item C stock should be available before orders come in.
    :param d_stock: This sets how much Item D stock should be available before orders come in.
    :param e_stock: This sets how much Item D stock should be available before orders come in.
    :return stock_df: This function returns this DataFrame, which is the completed stock_inventory_queue.

    I adopted code from the following URL's as a resource to iterate over DataFrame rows:
    https://stackoverflow.com/questions/16476924/how-to-iterate-over-rows-in-a-dataframe-in-pandas
    """

    stock_df = df.copy(deep=True)

    stock_df['Build Item A'] = build_stock_inventory(stock_df, a_stock, 'Item A', 'Start Stock A', 'Surplus A Stock',
                                                     'Build Item A', 'Restock A')

    stock_df['Build Item B'] = build_stock_inventory(stock_df, b_stock, 'Item B', 'Start Stock B', 'Surplus B Stock',
                                                     'Build Item B', 'Restock B')

    stock_df['Build Item C'] = build_stock_inventory(stock_df, c_stock, 'Item C', 'Start Stock C', 'Surplus C Stock',
                                                     'Build Item C', 'Restock C')

    stock_df['Build Item D'] = build_stock_inventory(stock_df, d_stock, 'Item D', 'Start Stock D', 'Surplus D Stock',
                                                     'Build Item D', 'Restock D')

    stock_df['Build Item E'] = build_stock_inventory(stock_df, e_stock, 'Item E', 'Start Stock E', 'Surplus E Stock',
                                                     'Build Item E', 'Restock E')

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

    # Applied ceil to this calculation because orders need to be processed and are available the next work day.
    stock_df['Pick Up Day'] = np.ceil((stock_df['Order Build Hours'].cumsum(axis=0) / 7.5))
    # Added plus one to account for the customer ordering one day before the order was started in the manufactory.
    stock_df['Wait Time'] = stock_df['Pick Up Day'] + 1

    pd.set_option('display.expand_frame_repr', False)

    # preview the calculations that determine how much and when to build items for this queue
    stock_preview = stock_df[['Order #', 'Day', 'Item A', 'Start Stock A', 'Surplus A Stock',
                              'Build Item A', 'Restock A', 'Build A Hours']]
    print(stock_preview)
    return stock_df


main(num_of_samples=1000)
