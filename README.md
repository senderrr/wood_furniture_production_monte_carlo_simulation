## Title: Wood Furniture Production Monte Carlo Simulation

## Team Members: Alex Wieker

## Monte Carlo Simulation Summary: 
In this simulation, I will be simulating two scenarios for a small manufactory that produces wooden furniture in order to determine which of the scenarios makes the furniture available to their customers faster. Since it takes time to swap between machinary to make different items, and since  this small manufactory has limited machines and workers, orders are completed item by item. In order to prevent as many customers as possible from cancelling their orders,  the goal of this simulation is  to determine which of the scenarios will produce less waiting time between ordering and receiving their orders for their customers. In my scenarios, I am starting  day 1 as the first work day, and they begin to work on orders that were processed from the day  before.  Hence, all customers wait at least one day froms sending the other and their order being available. Lastly, the simulation will compare the same  set of orders for both scenarios. The goal is to determine which queue will result in customers receiving their orders faster because if their is a huge pipeline, orders will be cancelled.
 
Scenario 1: First Come First Serve Queue:
In this scenario, it builds orders as they come. A new order not start until order the previous one is  finished. Thus, it is a first come first serve manufactory  methodology. 

Scenario 2: Stock Inventory Queue:
In this scenario it also builds orders as they come in similar to scenario two and does not start a new order until the one that is being worked on is finished. However, in this scenario, there is the  assumption now that the manufactory maintains a small stock inventory of all of its supply based on demand. That is, there might be more of one item than another in the stock inventory. Nevertheless, in this scenario rather than build the items for each order when they come, the manufactory pulls from the inventory stock if enough is available. When there is not enough inventory stock to fulfill an order, items are built item by item as needed for each order. In other words similar to scenario one, orders will still be completed one at a time. Additionally, the stock_inventory will be restocked at the end of each set of days orders in order to maintain a full stock inventory. Hence, when it comes to the last order of each day, the manufactory will go item by item and fulfill each order but also restock the stock inventory. While it would be faster for the last customer of each day to receive his or her order if the restock is completed after their order is fulfilled, for the sake of efficiency, due to the time it takes to swap machinary, fulfilling the last order of each day and restocking the stock inventory take place simultaneously. The advantage of this simulation is that you still go order by order (due to the limited resources of the manufactory) but also build one larger batch of all items once a day, saving some time by swapping machinary less.

## Variables:
Scenario 1: First Come First Serve Queue:

• How many work days are we simulating: 22, rounded up the average US work days in a month. 

• How many orders are received each day: PERT distribution 

• Order size: PERT distribution 

• What items are in orders: NP.random.choice

• Time to build item in order: PERT distributition

• How long it takes to swap between machinary: static variable (Machinary Swap time)

Scenario 2: Stock Inventory Queue:

• How many work days are we simulating: 22, rounded up the average US work days in a month. 

• How many orders are received each day: PERT distribution 

• Order size: PERT distribution 

• What items are in orders: NP.random.choice

• Time to build item in order: PERT distributition

• How long it takes to swap between machinary: static variable (Machinary Swap time)

• How much stock inventory should be available at the start of each day for each item: static variable based on user input in the form of a_stock, b_stock, c_stock,  d_stock, and e_stock.

## Hypothesis: 
I hypothesize that the inventory stock queue will result in orders have less wait time between the order customer making the order and the order being built than the first come first serve queue.  

## Results: 

After running my simulation 1,000 times, I found that my hypothesis is true because the median wait time in the second scenario, stock inventory queue, is 32 whereas the first scenario, the first come first serve queue, is 35. In addition, the second scenario had a mean of 32.88 days while the first scenario had a mean of 35.49 days. This suggests in the second scenario in comparison to the first secenario that it took less time to build the orders and more customers had less of a delay between making an order and receiving their order.  Additionally, the second scenario has a min wait time of 1 days, whereas the first scenario has a min wait time of 2 days. This also suggests that in the second scenario many orders were already made, due to the stock inventory, when the order came in, and  were just needing to be prepared for the customer to receive them. Lastly, the second scenario had a max wait time of 91 days, whereas the first scenario had a max wait time of 95 days, which suggests that more customers in the first scenario had to wait longer than the second scenario.

## Instructions on how to use the program:
main function: 

For the generate orders variable, set order PERT distribution range, PERT confidence, and leave sample at one. In the fcq varaible, set machine_time_swap to desired swapping time and set build_confidence to desired confidence.
In the  stock_queue variable, set machine_time_swap to desired swapping time and set build_confidence to desired confidence but also set how much inventory_stock should be available for  a_stock, b_stock, c_stock, d_stock, and e_stock. Lastly, when the function is called set how many simulations to run.

orders function: 

Set how many work days that you would like to similar in the first range loop. 
In the inner range loop, set the PERT distribution for how many items per order and set the probabilities in the order_items variable. Change the item_order_options as needed, but make sure that you change the item_order_options, and the return dataframe variable.

when_to_build_stock_inventory function:

All parameters in the function except for the initial DataFrame and stock parameter must be strings.


## Github File Descriptions:

monte_carlo_v1.py: Initial py files of my first simulation scenario, but I have since altered it (out of date).

monte_carlo_v2.py: Updated py files of the current simulation.

old_stock_inventory_code.py: This file contains old code that I used to create my build_stock_inventory function.


Serve Wait Time Queue Distribution.png: Scenario 1 First Come First Queue Simulation Distribution Histogram

Stock Inventory Wait Time Queue Distribution.png: Scenario 2 Stock Inventory Queue Distribution Histogram

Wieker_mc_poster_1.pdf: Poster Part 1

Wieker_mc_poster_2.pdf: Poster Part 2
