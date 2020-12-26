# fast-food-simulator
A Fast Food take away restaurant simulator in Python

This app simulates customers of a take-away restaurant placing orders and and waiting for them to be prepared and delivered to a pickup counter. After placing the order the customer waits on the order to be announced before picking it up and proceeding to the dining area.

The user stories that make up this app center around four distinct roles:
 - User - the end user using the application
 - Customer - the simulated Customer
 - Order Taker - the simulated Order Taker 
 - Cook - the simulated Cook
 - Server - the simulated Server

The idea of this project was taken from [FastFood-App](https://github.com/florinpop17/app-ideas/blob/master/Projects/3-Advanced/FastFood-App.md) by changing few constraints.
This project is focused on backend application which provides simple RestAPI to trigger/start simulator with different config parameters as an input. On server, celery tasks gets triggered which executes simulator and generates log file as an output. 

## Tech Stack 
The tool requires following lib/frameworks 
 - Python (3.9.1)
 - Django (3.1.4)
 - Django Rest Framework (3.12.2)
 - Celry (5.0.5)
 - RabbitMQ 

The core functionality of this project which is simulator is implemented using Async code with `async/await`.

## How to use simulator 

1. Clone this repo 
2. Setup virtual env with Python 3.9+ 
3. Run `pip install -r requirements.txt`. This will install necessary python packages required to run this tool.
4. Start django server locally by running `python manage.py runserver` command. 

Once server is started, open another terminal window and start celery worker by running command `celery -A fast_food_simulator worker  -l INFO`. This will start celery process which will wait for new task to recieve. Celery is used to offload simulator execution and free up server CPU for handling other requests. 

After that use any Rest client like Postman or curl to run below request 

```
curl --location --request POST 'http://127.0.0.1:8000/api/run-sim/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "customer_arrival_interval": 60,
    "order_preparation_time": 5,
    "order_taker_interval": 2,
    "time_taken_by_server": 2,
    "stop_after": 300
}'
```
Server will return 201 status code as a success response and it will start simulator execution via celery task for specified amount of time. 
*Note:* All the timeouts mentioned above are in secs. 
Config params
```
customer_arrival_interval -> Simulates a customer behaviour. A new customer arrives at certain interval 
order_preparation_time -> Simulates a time taken by cook to prepare an order 
order_taker_interval -> Simulates a time taken by the order taker to take order, create unique order ticket number and place an order in kitchen.
time_taken_by_server -> Time taken by the server to served prepared order. 
stop_after -> Execution time of a tool 
```

Sample execution logs will look like this 
```
2020-12-25 14:41:01,763 - INFO - Simulation started...
2020-12-25 14:41:01,764 - INFO - Customer process started...
2020-12-25 14:41:01,764 - INFO - New customer arrived: cust_f4bac6a0
2020-12-25 14:41:01,764 - INFO - Order taker process started..
2020-12-25 14:41:01,764 - INFO - Kitchen process started..
2020-12-25 14:41:01,764 - INFO - Server process started..
2020-12-25 14:41:01,764 - INFO - Simulator polling started...
2020-12-25 14:41:06,764 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:41:06,764 - INFO - Creating new order ticket..
2020-12-25 14:41:06,766 - INFO - New order created for cust_f4bac6a0: tk_1061e127
2020-12-25 14:41:06,766 - INFO - Order created and placed in kitchen area
2020-12-25 14:41:06,766 - INFO - Preparing tk_1061e127 order wait for 30 secs...
2020-12-25 14:41:36,773 - INFO - Number of orders to be prepared 0
2020-12-25 14:41:36,773 - INFO - Order tk_1061e127 is ready to serve..
2020-12-25 14:42:01,759 - INFO - New customer arrived: cust_bb04bc45
2020-12-25 14:42:01,760 - INFO - Serving for tk_1061e127 to cust_f4bac6a0 wait for 5 secs..
2020-12-25 14:42:06,762 - INFO - Number of orders to be served 0
2020-12-25 14:42:06,763 - INFO - cust_f4bac6a0 your order ready. Enjoy your food !!
2020-12-25 14:42:11,765 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:42:11,765 - INFO - Creating new order ticket..
2020-12-25 14:42:11,765 - INFO - New order created for cust_bb04bc45: tk_832fd7d4
2020-12-25 14:42:11,765 - INFO - Order created and placed in kitchen area
2020-12-25 14:42:11,783 - INFO - Preparing tk_832fd7d4 order wait for 30 secs...
2020-12-25 14:42:41,785 - INFO - Number of orders to be prepared 0
2020-12-25 14:42:41,785 - INFO - Order tk_832fd7d4 is ready to serve..
2020-12-25 14:43:01,772 - INFO - New customer arrived: cust_f74144cd
2020-12-25 14:43:06,760 - INFO - Serving for tk_832fd7d4 to cust_bb04bc45 wait for 5 secs..
2020-12-25 14:43:11,761 - INFO - Number of orders to be served 0
2020-12-25 14:43:11,761 - INFO - cust_bb04bc45 your order ready. Enjoy your food !!
2020-12-25 14:43:16,764 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:43:16,764 - INFO - Creating new order ticket..
2020-12-25 14:43:16,765 - INFO - New order created for cust_f74144cd: tk_105b4944
2020-12-25 14:43:16,765 - INFO - Order created and placed in kitchen area
2020-12-25 14:43:16,799 - INFO - Preparing tk_105b4944 order wait for 30 secs...
2020-12-25 14:43:46,801 - INFO - Number of orders to be prepared 0
2020-12-25 14:43:46,801 - INFO - Order tk_105b4944 is ready to serve..
2020-12-25 14:44:01,772 - INFO - New customer arrived: cust_962d1555
2020-12-25 14:44:11,759 - INFO - Serving for tk_105b4944 to cust_f74144cd wait for 5 secs..
2020-12-25 14:44:16,760 - INFO - Number of orders to be served 0
2020-12-25 14:44:16,760 - INFO - cust_f74144cd your order ready. Enjoy your food !!
2020-12-25 14:44:21,763 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:44:21,763 - INFO - Creating new order ticket..
2020-12-25 14:44:21,764 - INFO - New order created for cust_962d1555: tk_e5cea61c
2020-12-25 14:44:21,764 - INFO - Order created and placed in kitchen area
2020-12-25 14:44:21,812 - INFO - Preparing tk_e5cea61c order wait for 30 secs...
2020-12-25 14:44:51,814 - INFO - Number of orders to be prepared 0
2020-12-25 14:44:51,814 - INFO - Order tk_e5cea61c is ready to serve..
2020-12-25 14:45:01,768 - INFO - New customer arrived: cust_c75cb29f
2020-12-25 14:45:16,771 - INFO - Serving for tk_e5cea61c to cust_962d1555 wait for 5 secs..
2020-12-25 14:45:21,774 - INFO - Number of orders to be served 0
2020-12-25 14:45:21,774 - INFO - cust_962d1555 your order ready. Enjoy your food !!
2020-12-25 14:45:26,776 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:45:26,776 - INFO - Creating new order ticket..
2020-12-25 14:45:26,776 - INFO - New order created for cust_c75cb29f: tk_14e46666
2020-12-25 14:45:26,776 - INFO - Order created and placed in kitchen area
2020-12-25 14:45:26,807 - INFO - Preparing tk_14e46666 order wait for 30 secs...
2020-12-25 14:45:56,809 - INFO - Number of orders to be prepared 0
2020-12-25 14:45:56,809 - INFO - Order tk_14e46666 is ready to serve..
2020-12-25 14:46:01,763 - INFO - New customer arrived: cust_770d919d
2020-12-25 14:46:21,785 - INFO - Serving for tk_14e46666 to cust_c75cb29f wait for 5 secs..
2020-12-25 14:46:26,787 - INFO - Number of orders to be served 0
2020-12-25 14:46:26,787 - INFO - cust_c75cb29f your order ready. Enjoy your food !!
2020-12-25 14:46:31,790 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:46:31,790 - INFO - Creating new order ticket..
2020-12-25 14:46:31,791 - INFO - New order created for cust_770d919d: tk_249e0d04
2020-12-25 14:46:31,791 - INFO - Order created and placed in kitchen area
2020-12-25 14:46:31,807 - INFO - Preparing tk_249e0d04 order wait for 30 secs...
2020-12-25 14:47:01,763 - INFO - New customer arrived: cust_71dbef40
2020-12-25 14:47:01,812 - INFO - Number of orders to be prepared 0
2020-12-25 14:47:01,812 - INFO - Order tk_249e0d04 is ready to serve..
2020-12-25 14:47:26,784 - INFO - Serving for tk_249e0d04 to cust_770d919d wait for 5 secs..
2020-12-25 14:47:31,787 - INFO - Number of orders to be served 0
2020-12-25 14:47:31,787 - INFO - cust_770d919d your order ready. Enjoy your food !!
2020-12-25 14:47:36,789 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:47:36,789 - INFO - Creating new order ticket..
2020-12-25 14:47:36,789 - INFO - New order created for cust_71dbef40: tk_331a227e
2020-12-25 14:47:36,790 - INFO - Order created and placed in kitchen area
2020-12-25 14:47:36,807 - INFO - Preparing tk_331a227e order wait for 30 secs...
2020-12-25 14:48:01,760 - INFO - New customer arrived: cust_25b0d146
2020-12-25 14:48:06,808 - INFO - Number of orders to be prepared 0
2020-12-25 14:48:06,808 - INFO - Order tk_331a227e is ready to serve..
2020-12-25 14:48:31,782 - INFO - Serving for tk_331a227e to cust_71dbef40 wait for 5 secs..
2020-12-25 14:48:36,786 - INFO - Number of orders to be served 0
2020-12-25 14:48:36,786 - INFO - cust_71dbef40 your order ready. Enjoy your food !!
2020-12-25 14:48:41,788 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:48:41,788 - INFO - Creating new order ticket..
2020-12-25 14:48:41,789 - INFO - New order created for cust_25b0d146: tk_15900842
2020-12-25 14:48:41,789 - INFO - Order created and placed in kitchen area
2020-12-25 14:48:41,820 - INFO - Preparing tk_15900842 order wait for 30 secs...
2020-12-25 14:49:01,758 - INFO - New customer arrived: cust_7cdbc845
2020-12-25 14:49:11,825 - INFO - Number of orders to be prepared 0
2020-12-25 14:49:11,825 - INFO - Order tk_15900842 is ready to serve..
2020-12-25 14:49:36,782 - INFO - Serving for tk_15900842 to cust_25b0d146 wait for 5 secs..
2020-12-25 14:49:41,784 - INFO - Number of orders to be served 0
2020-12-25 14:49:41,784 - INFO - cust_25b0d146 your order ready. Enjoy your food !!
2020-12-25 14:49:46,786 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:49:46,786 - INFO - Creating new order ticket..
2020-12-25 14:49:46,787 - INFO - New order created for cust_7cdbc845: tk_c4bf1663
2020-12-25 14:49:46,787 - INFO - Order created and placed in kitchen area
2020-12-25 14:49:46,836 - INFO - Preparing tk_c4bf1663 order wait for 30 secs...
2020-12-25 14:50:01,759 - INFO - New customer arrived: cust_bc84eeff
2020-12-25 14:50:16,839 - INFO - Number of orders to be prepared 0
2020-12-25 14:50:16,840 - INFO - Order tk_c4bf1663 is ready to serve..
2020-12-25 14:50:41,781 - INFO - Serving for tk_c4bf1663 to cust_7cdbc845 wait for 5 secs..
2020-12-25 14:50:46,783 - INFO - Number of orders to be served 0
2020-12-25 14:50:46,783 - INFO - cust_7cdbc845 your order ready. Enjoy your food !!
2020-12-25 14:50:51,786 - INFO - Number of customers waiting to place an order 0
2020-12-25 14:50:51,786 - INFO - Creating new order ticket..
2020-12-25 14:50:51,787 - INFO - New order created for cust_bc84eeff: tk_948f84d3
2020-12-25 14:50:51,787 - INFO - Order created and placed in kitchen area
2020-12-25 14:50:51,849 - INFO - Preparing tk_948f84d3 order wait for 30 secs...
2020-12-25 14:51:01,773 - INFO - Simulation execution time limit reached stopping...
2020-12-25 14:51:01,773 - INFO - New customer arrived: cust_67ca583a
2020-12-25 14:51:01,776 - INFO - Simulation stopped...
```

## Additional info
For more details on logical flow of the application refer [Fast Food Simulator logical flow](https://drive.google.com/file/d/1Thfm5cFDm1OjTg_0LsIt2j1uPL5fv-Dh/view)
