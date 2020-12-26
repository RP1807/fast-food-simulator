from celery import shared_task, Celery
from celery.utils.log import get_task_logger
from .fast_food_sim import FastFoodSimulator
import os

logger = get_task_logger(__name__)

celery = Celery('fast_food_simulator', broker='amqp://localhost:5672//')

os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "fast_food_simulator.settings"


@shared_task(name="start_sim_task")
def start_simulator(**kwargs):
    logger.info("Starting simulator task...")
    sim_obj = FastFoodSimulator(customer_arrival_interval=kwargs.get('customer_arrival_interval'),
                                order_preparation_time=kwargs.get('order_preparation_time'),
                                order_taker_interval=kwargs.get('order_taker_interval'),
                                time_taken_by_server=kwargs.get('time_taken_by_server'),
                                stop_after=kwargs.get('stop_after'))
    sim_obj.run()
