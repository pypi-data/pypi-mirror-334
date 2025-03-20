import json
import pprint
import pytest
import time
from pycentral.glp.devices import Devices
from pycentral.glp.subscription import Subscription
from pycentral.glp.user_management import UserMgmt
from pycentral.base import ArubaCentralNewBase

# Global variables:
with open("test_glp_vars.json", "r") as file:
    vars = json.load(file)

# Credentials:
central_info = vars["credentials"]

# Create an instance of ArubaCentralBase using API access token
# or API Gateway credentials.
connection = ArubaCentralNewBase(central_info, classic_auth=True)

# Pretty printing settings
pp = pprint.PrettyPrinter(indent=1)

# Shorthand for file access within glp module that contains useful functions
d = Devices()
s = Subscription()
u = UserMgmt()


def test_get_device():
    print("\nTesting GET DEVICE")

    data = vars["test_get_device"]

    print("\n - test get_device function with limit and offset set to 0")
    resp = d.get_device(conn=connection, limit=0, offset=0)
    assert resp["code"] == 200

    print("\n - test get_device function with limit set to max value of 2000")
    resp = d.get_device(conn=connection, limit=2000, offset=0)
    assert resp["code"] == 200

    print("\n - test get_device function using filter api parameter")
    resp = d.get_device(conn=connection, filter=data["filter_model"])
    assert resp["code"] == 200

    print("\n - test get_device function using select api parameter")
    resp = d.get_device(
        conn=connection, limit=2000, offset=0, select=data["select"]
    )
    assert resp["code"] == 200

    print("\n - test get_device function using sort api parameter")
    resp = d.get_device(
        conn=connection, limit=2000, offset=0, sort=data["sort"]
    )
    assert resp["code"] == 200

    print("\n - test get_device function with a bad filter")
    resp = d.get_device(connection, filter="nonsense stuff")
    print(resp)
    assert resp["code"] == 400


def test_get_all_devices():
    print("\nTesting GET ALL DEVICES")

    print("\n - test get_all_devices function")
    resp = d.get_all_devices(conn=connection)
    assert resp["code"] == 200

    print("\n - test get_all_devices function using select variable")
    resp = d.get_all_devices(
        conn=connection, select=vars["test_get_all_devices"]["select"]
    )
    assert resp["code"] == 200


def test_get_device_id():
    print("\nTesting GET DEVICE ID")

    data = vars["test_get_device_id"]

    print("\n - test with serial")
    resp = d.get_device_id(conn=connection, serial=data["serial"])
    assert resp[0] is True and resp[1] == data["id"]

    print("\n - test with bad request")
    resp = d.get_device_id(conn=connection, serial={"id": 2314234})
    assert resp[0]["code"] == 400

    print("\n - test with serial not on account")
    resp = d.get_device_id(conn=connection, serial="awdadawda")
    assert resp[0] is False and resp[1] == "Serial not found"


def test_get_dev_status():
    print("\n Testing GET STATUS - DEVICES")

    data = vars["test_get_dev_status"]

    print("\n - test with successful transaction")
    resp = d.get_status(connection, data["transaction"])
    assert resp["code"] == 200

    print("\n - test with bad transaction")
    resp = d.get_status(connection, "ffawawf")
    assert resp["code"] == 404


def test_add_devices():
    print("\n Testing ADD DEVICES")

    data = vars["test_add_devices"]
    network = [data["network1"], data["network2"]]
    compute = []
    storage = []

    print("\n - testing with valid devices")
    resp_list = d.add_devices(connection, network, compute, storage)
    for resp in resp_list:
        assert resp["code"] == 202


def test_device_subscription():
    print("\n Testing DEVICE SUBSCRIPTIONS")

    data = vars["test_device_subscription"]

    serials = [data["serial1"], data["serial2"]]
    ids = [data["dev_id1"], data["dev_id2"]]
    sub_key = data["sub_key"]
    sub_id = data["sub_id"]

    print("\n Testing add_sub with serial")
    resp_list = d.add_sub(connection, serials, sub_id, serial=True)
    for resp in resp_list:
        assert resp["msg"]["status"] == "SUCCEEDED"

    print("\n Testing remove_sub with serial")
    resp_list = d.remove_sub(connection, serials, serial=True)
    for resp in resp_list:
        assert resp["msg"]["status"] == "SUCCEEDED"

    print("\n Testing add_sub with id")
    resp_list = d.add_sub(connection, ids, sub_id)
    for resp in resp_list:
        assert resp["msg"]["status"] == "SUCCEEDED"

    print("\n Testing remove_sub with id")
    resp_list = d.remove_sub(connection, ids)
    for resp in resp_list:
        assert resp["msg"]["status"] == "SUCCEEDED"

    print("\n Testing add_sub with dev ids and sub key")
    resp_list = d.add_sub(connection, ids, sub_key, key=True)
    for resp in resp_list:
        assert resp["msg"]["status"] == "SUCCEEDED"

    # Sleep to avoid breaching rate limit.
    time.sleep(60)


def test_unassign_devices():
    print("\nTesting UNASSIGN DEVICES")

    print("\n - test unassign_devices function")
    resp = d.unassign_devices(
        conn=connection, devices=vars["test_unassign_devices"]["id"]
    )
    assert resp["code"] == 200

    print(
        "\n - test unassign_devices function using serial numbers list for devices variable"
    )
    resp = d.unassign_devices(
        conn=connection,
        devices=vars["test_unassign_devices"]["devices"],
        serial=True,
    )
    assert resp["code"] == 200


def test_assign_devices():
    print("\nTesting ASSIGN DEVICES")

    print("\n - test assign_devices function")
    resp = d.assign_devices(
        conn=connection,
        application=vars["test_assign_devices"]["application"],
        region=vars["test_assign_devices"]["region"],
        devices=vars["test_assign_devices"]["id"],
    )
    assert resp["code"] == 200

    print("\n - test assign_devices function")
    resp = d.assign_devices(
        conn=connection,
        application=vars["test_assign_devices"]["application"],
        region=vars["test_assign_devices"]["region"],
        devices=vars["test_assign_devices"]["devices"],
        serial=True,
    )
    assert resp["code"] == 200


def test_get_subscription():
    print("\nTesting GET SUBSCRIPTION")

    print("\n - test get_subscription function")
    resp = s.get_subscription(
        conn=connection,
        filter=vars["test_get_subscription"]["subscription_filter"],
        limit=1,
        offset=0,
    )
    assert resp["code"] == 200


def test_get_all_subscriptions():
    print("\nTesting GET ALL SUBSCRIPTIONS")

    print("\n - test get_all_subscriptions function")

    resp = s.get_all_subscriptions(conn=connection)
    assert resp["code"] == 200

    print("\n - test get_all_subscriptions function using select variable")

    resp = s.get_all_subscriptions(
        conn=connection, select=vars["test_get_all_subscriptions"]["select"]
    )
    assert resp["code"] == 200


def test_get_sub_id():
    print("\nTesting GET SUB ID")

    data = vars["test_get_sub_id"]

    print("\n - test with key")
    resp = s.get_sub_id(connection, data["key"])
    assert resp[0] is True and resp[1] == data["id"]

    print("\n - test with bad request")
    resp = s.get_sub_id(conn=connection, key={"id": 2314234})
    assert resp[0]["code"] == 400

    print("\n - test with key not on account")
    resp = s.get_sub_id(conn=connection, key="awdadawda")
    assert resp[0] is False and resp[1] == "Key not found"


def test_get_sub_status():
    print("\n Testing GET STATUS - SUBSCRIPTION")

    data = vars["test_get_dev_status"]

    print("\n - test with successful transaction")
    resp = s.get_status(connection, data["transaction"])
    assert resp["code"] == 200

    print("\n - test with bad transaction")
    resp = s.get_status(connection, "adakdadkakd")
    assert resp["code"] == 404


def test_add_subscription():
    print("\nTesting ADD SUBSCRIPTION")

    # Need to have a valid sub to add for req to be successful.
    print("\n - test add_subscription function")
    resp = s.add_subscription(
        conn=connection,
        subscriptions=vars["test_add_subscription"]["subscriptions"],
        limit=0,
        offset=0,
    )
    assert resp["code"] == 404


def test_get_users():
    print("\nTesting GET USERS")

    print("\n - test get_users function")
    resp = u.get_users(conn=connection, limit=300, offset=0)
    assert resp["code"] == 200

    print("\n - test get_users function using filter variable")
    resp = u.get_users(
        conn=connection,
        filter=vars["test_get_users"]["filter"],
        limit=300,
        offset=0,
    )
    assert resp["code"] == 200


def test_get_user():
    print("\nTesting GET USER")

    print("\n - test get_user function success")
    resp = u.get_user(connection, id=vars["test_get_user"]["user_id"])
    assert resp["code"] == 200

    print(
        "\n - test get_user function success using email instead of user_id variable"
    )
    resp = u.get_user(connection, email=vars["test_get_user"]["email"])
    assert resp["code"] == 200

    print("\n - test get_user function fail")
    resp = u.get_user(connection, id=vars["test_get_user"]["user_id_fail"])
    assert resp["code"] == 403


# Use different emails for each test.
def test_invite_user():
    print("\nTesting INVITE USER")

    print("\n - test inv_user function success")
    resp = u.inv_user(
        connection, email=vars["test_invite_user"]["email"], send_link=True
    )
    assert resp["code"] == 201

    print("\n - test inv_user function fail")
    resp = u.inv_user(
        connection,
        email=vars["test_invite_user"]["email_fail"],
        send_link=True,
    )
    assert resp["code"] == 400


# Use seperate user accounts for user_id + email.
def test_delete_user():
    print("\nTesting DELETE USER")

    print("\n - test delete_user function success")
    resp = u.delete_user(
        conn=connection, email=vars["test_delete_user"]["email"]
    )
    assert resp["code"] == 204

    print("\n - test delete_user function fail")
    resp = u.delete_user(
        conn=connection, user_id=vars["test_delete_user"]["user_id_fail"]
    )
    assert resp["code"] == 400


if __name__ == "__main__":
    pytest.main()
