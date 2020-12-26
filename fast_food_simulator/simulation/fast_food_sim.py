import logging
import asyncio
import sys
from argparse import ArgumentParser
from collections import deque
from .models import Customer, OrderTicket

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO,
                    filename="../../simulator.log", filemode='w')


class FastFoodSimulator:
    CUSTOMER_ARRIVAL_INTERVAL = 60
    ORDER_PREPARATION_TIME = 10
    ORDER_TAKER_INTERVAL = 10
    SERVER_INTERVAL = 10

    def __init__(self, customer_arrival_interval, order_preparation_time, order_taker_interval, time_taken_by_server,
                 stop_after):
        self.kitchen_queue = deque([])
        self.server_queue = deque([])
        self.customer_waiting_line = {}
        self.customer_queue = deque([])
        self.stop_after = stop_after
        self.loop = None
        self.__set_time_interval_settings(customer_arrival_interval=customer_arrival_interval,
                                          order_preparation_time=order_preparation_time,
                                          order_taker_interval=order_taker_interval,
                                          time_taken_by_server=time_taken_by_server)
            

    def __set_time_interval_settings(self, customer_arrival_interval, order_preparation_time, order_taker_interval,
                                     time_taken_by_server):
        self.CUSTOMER_ARRIVAL_INTERVAL = customer_arrival_interval
        self.ORDER_PREPARATION_TIME = order_preparation_time
        self.ORDER_TAKER_INTERVAL = order_taker_interval
        self.SERVER_INTERVAL = time_taken_by_server

    async def order_taker_process(self) -> None:
        logger.info("Order taker process started..")
        while True:
            if len(self.customer_queue) > 0:
                customer = self.customer_queue.popleft()
                await asyncio.sleep(self.ORDER_TAKER_INTERVAL)

                logger.info(f"Number of customers waiting to place an order {len(self.customer_queue)}")
                logger.info("Creating new order ticket..")
                order_ticket = OrderTicket()
                logger.info(f"New order created for {customer}: {order_ticket}")
                self.kitchen_queue.append(order_ticket)
                logger.info("Order created and placed in kitchen area")

                self.customer_waiting_line[order_ticket] = customer
            else:
                await asyncio.sleep(self.CUSTOMER_ARRIVAL_INTERVAL)

    async def kitchen_process(self) -> None:
        logger.info("Kitchen process started..")
        while True:
            if len(self.kitchen_queue) > 0:
                current_order = self.kitchen_queue.popleft()

                logger.info(f"Preparing {current_order} order wait for {self.ORDER_PREPARATION_TIME} secs...")
                await asyncio.sleep(self.ORDER_PREPARATION_TIME)

                logger.info(f"Number of orders to be prepared {len(self.kitchen_queue)}")
                logger.info(f"Order {current_order} is ready to serve..")
                self.server_queue.append(current_order)
            else:
                await asyncio.sleep(self.ORDER_TAKER_INTERVAL)

    async def server_process(self) -> None:
        logger.info("Server process started..")
        while True:
            if len(self.server_queue) > 0:
                current_order = self.server_queue.popleft()
                customer = self.customer_waiting_line.get(current_order, None)

                logger.info(f"Serving for {current_order} to {customer} wait for {self.SERVER_INTERVAL} secs..")
                await asyncio.sleep(self.SERVER_INTERVAL)

                logger.info(f"Number of orders to be served {len(self.server_queue)}")
                if customer:
                    logger.info(f"{customer} your order ready. Enjoy your food !!")
                else:
                    logger.info(f"Order {current_order} does not associated to any customer {customer}")
            else:
                await asyncio.sleep(self.ORDER_PREPARATION_TIME)

    async def customer_process(self) -> None:
        logger.info("Customer process started...")
        while True:
            customer = Customer()
            logger.info(f"New customer arrived: {customer}")

            self.customer_queue.append(customer)
            await asyncio.sleep(self.CUSTOMER_ARRIVAL_INTERVAL)

    async def poll_for_simulator(self) -> None:
        logger.info("Simulator polling started...")
        await asyncio.sleep(self.stop_after)

        logger.info("Simulation execution time limit reached stopping...")
        self.loop = asyncio.get_running_loop()
        self.loop.stop()

    async def start_simulator(self):
        logger.info("Simulation started...")
        await asyncio.gather(self.customer_process(), self.order_taker_process(), self.kitchen_process(),
                             self.server_process(), self.poll_for_simulator())

    def run(self):
        try:
            asyncio.run(self.start_simulator())
        except RuntimeError:
            logger.info("Simulation stopped...")
            # sys.exit(0)


def main():
    parser_obj = ArgumentParser(description="A simple fast food simulator implemented using async/await")
    parser_obj.add_argument('stop_after', type=int, help="Enter execution time of simulator once started")
    parser_obj.add_argument('-customer_arrival_interval', type=int,
                            help="Enter time interval to simulate new customer arrival", default=300)
    parser_obj.add_argument('-order_preparation_time', type=int,
                            help="Enter time interval to simulate time taken to cook an order", default=300)
    parser_obj.add_argument('-order_taker_time_interval', type=int,
                            help="Enter time to simulate time taken by order taker to create order", default=120)
    parser_obj.add_argument('-time_taken_by_server', type=int,
                            help="Enter time to simulate time taken by server to serve order once prepared",
                            default=60)

    args = parser_obj.parse_args()

    sim_obj = FastFoodSimulator(customer_arrival_interval=args.customer_arrival_interval,
                                order_preparation_time=args.order_preparation_time,
                                order_taker_interval=args.order_taker_time_interval,
                                time_taken_by_server=args.time_taken_by_server, stop_after=args.stop_after)

    try:
        asyncio.run(sim_obj.start_simulator())
    except RuntimeError:
        logger.info("Simulation stopped...")
        sys.exit(0)


if __name__ == '__main__':
    main()
