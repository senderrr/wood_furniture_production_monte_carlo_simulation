## Title: Wood Furniture Production Monte Carlo Simulation

## Team Members: Alex Wieker

## Monte Carlo Simulation Summary: 
In this simulation, I will be simulating two scenarios for a small manufactory that produces wooden furniture in order to determine which of the scenarios makes the furniture available to their customers faster. Since it takes time to swap between machinary to make different items, and since  this small manufactory has limited machines and workers, orders are completed item by item. In order to prevent as many customers as possible from cancelling their orders,  the goal of this simulation is  to determine which of the scenarios will produce less waiting time between ordering and receiving their orders for their customers. In my scenarios, I am starting  day 1 as the first work day, and they begin to work on orders that were processed from the day  before.  Hence, all customers wait at least one day froms sending the other and their order being available. Lastly, the simulation will compare the same  set of orders for both scenarios. The goal is to determine which queue will result in customers receiving their orders faster because if their is a huge pipeline, orders will be cancelled.
 
Scenario 1: First Come First Queue:
In this scenario, it builds orders as they come. Order two does not start until order one is  finished. Thus, it is a  first come first serve manufactory  methodology. 

Scenario 2: Stock Inventory Queue:
In this scenario it also builds orders as they come in similar to scenario two and does not start a new order until the one that is being worked on is finished. However, in this scenario, there is the  assumption now that the manufactory maintains a small stock inventory of all of its supply based on demand. That is, there might be more of one item than another in the stock inventory. Nevertheless, in this scenario rather than build the items for each order when they come, the manufactory pulls from the inventory stock if enough is available. When there is not enough inventory stock to fulfill an order, items are built item by item as needed for each order. In other words similar to scenario one, orders will still be completed one at a time. Additionally, the stock_inventory will be restocked at the end of each set of days orders in order to maintain a full stock inventory. Hence, it comes to the last order of each day, the manufactory will go item by item and fulfill each order but also  restock the stock inventory. While it would be faster for the last customer of each day to receive his or her order if the restock is completed after their order is fulfilled, for the sake of efficiency, due to the time it takes to swap machinary, fulfilling the last order of each day and restocking the stock inventory take place simultaneously. The advantage of this simulation is that you still go order by order (the limited resources of the manufactory) but also build a larger batch of all items once a day, saving some time by swapping machinary less.

if daily orders are completed in a timely fashion for a small business that constructs custom wood furniture. The variables that I will be working with include what items were included in any received orders (some items take longer to make and some orders will have smaller or larger quantities of items ordered), and the time it takes to switch machinery between working on different items that may require different machinery. Lastly, there will be two types of simulations run. The first where orders are only worked on after a previous order has finished (first come first serve). The second being where orders that contain similar items will be worked on in tandem instead of only working on one order at a time. 

## Variables:
Scenario 1: First Come First Queue:

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
I hypothesize that the inventory stock queue will result in orders have less wait time between the order customer making the order and the order being built than the first come first servue queue.  

## Results: 

## Instructions on how to use the program:


## Github File Descriptions:
Wieker_mc_poster_1.jpg: Poster Part 1

Wieker_mc_poster_2.jpg: Poster Part 2

monte_carlo_v1.py: Initial py files of my first simulation scenario, but I have since altered it.

monte_carlo_v2.py: Updated py files of the current simulation
