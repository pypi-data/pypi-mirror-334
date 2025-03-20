from pycentral.base_utils import console_logger
from pycentral.glp import devices, subscription
import time

DEVICE_LIMIT = 20
SUB_LIMIT = 5

logger = console_logger("RATE LIMIT CHECK")


def rate_limit_check(input_array, input_size_limit, rate_per_minute):
    print("Attempting to bypass rate limit")
    queue = []
    wait_time = []

    for i in range(0, len(input_array), input_size_limit):
        sub_array = input_array[i : i + input_size_limit]
        queue.append(sub_array)

    if len(queue) > rate_per_minute:
        wait_time = 60 / rate_per_minute
        print(
            "Array size exceeded,",
            wait_time,
            "second wait timer implemented per request to prevent errors",
        )
        print("Loading ...")
    else:
        wait_time = 0

    return queue, wait_time


def check_progress(conn, id, module):
    """
    check progress of async glp api.

    :param conn: new pycentral base object
    :param id: async transaction id
    :param module: module for api endpoint(devices/subscription)

    :return: tuple, (True or False for operation result, api response)
    """

    limit = None
    match module:
        case "devices":
            module = devices.Devices()
            limit = DEVICE_LIMIT
        case "subscription":
            module = subscription.Subscription()
            limit = SUB_LIMIT
        case _:
            return (False, "Invalid entry for module parameter.")

    updated = False
    while not updated:
        status = module.get_status(conn, id)
        if status["code"] != 200:
            conn.logger.error(
                f"Bad request for get async status with transaction {id}!"
            )
            return (False, status)
        elif status["msg"]["status"] == "SUCCEEDED":
            updated = True
            return (True, status)
        elif status["msg"]["status"] == "TIMEOUT":
            updated = True
            conn.logger.error(
                f"Async operation timed out for transaction {id}!"
            )
            return (False, status)
        elif status["msg"]["status"] == "FAILED":
            updated = True
            conn.logger.error(f"Async operation failed for transaction {id}!")
            return (False, status)
        else:
            # Sleep time calculated by async rate limit.
            sleep_time = 60 / limit
            time.sleep(sleep_time)
