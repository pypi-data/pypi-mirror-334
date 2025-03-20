from pycentral.base import ArubaCentralNewBase
from pycentral.glp import Devices, Subscription
import json
from operator import itemgetter
from argparse import ArgumentParser
import time
from termcolor import colored
import logging
import sys

logging.disable(sys.maxsize)

d = Devices()
s = Subscription()


def onboarding():
    workflow_vars = json.load(open("workflow_vars.json"))
    credentials = json.load(open("account_credentials.json"))
    platform_conn = ArubaCentralNewBase(token_info=credentials)
    devices, application = itemgetter("Devices", "Application")(workflow_vars)
    devices = add_devices(platform_conn, devices)
    application_id = get_application_id(
        platform_conn, application["region"], application["name"]
    )
    if devices and application_id:
        assign_device_status = assign_devices_to_application(
            platform_conn, devices, application_id, application
        )
        if assign_device_status:
            assign_subscription_to_device(platform_conn, devices)


def undo_onboarding():
    workflow_vars = json.load(open("workflow_vars.json"))
    new_credentials = json.load(open("account_credentials.json"))
    old_credentials = json.load(open("reset/old_account_credentials.json"))
    platform_conn = ArubaCentralNewBase(token_info=new_credentials)
    devices = itemgetter("Devices")(workflow_vars)
    resp = unassign_devices_from_application(conn=platform_conn, devices=devices)
    if resp["code"] == 200:
        platform_conn = ArubaCentralNewBase(token_info=old_credentials)
        devices = add_devices(platform_conn, devices)
        if devices:
            print('Successfully moved devices to old account. Ready to run GLP onboarding script! :)')

def add_devices(conn, devices):
    glp_format_devices = [
        {"serialNumber": device["serial"], "macAddress": device["mac"]}
        for device in devices
    ]

    add_device_resp = d.add_devices(conn=conn, network=glp_format_devices)
    if add_device_resp["code"] == 202:
        time.sleep(1)
        get_all_devices_resp = d.get_all_devices(conn=conn, select="id,serialNumber")

        if get_all_devices_resp["code"] == 200:
            all_device_serials = [
                device["serialNumber"]
                for device in get_all_devices_resp["msg"]["items"]
            ]

            new_devices_serials = [device["serial"] for device in devices]
            if all(
                device_serial in all_device_serials
                for device_serial in new_devices_serials
            ):
                print(
                    f"Devices({colored(','.join(new_devices_serials), 'green')}) have been successfully added to GLP account"
                )
                all_device_serials_dict = format_device_dict(
                    get_all_devices_resp["msg"]["items"]
                )
                for device in devices:
                    device["id"] = all_device_serials_dict[device["serial"]]
                return devices
        else:
            print(
                "Unable to validate device addition by API. Please verify device addition to account via UI."
            )
    else:
        print(
            f"Unable to add devices to GLP account. Error code - {colored(add_device_resp['code'], 'red')}"
        )
    return None


def get_application_id(platform_conn, region, name):
    region_id = get_region_name(region)
    if region_id:
        api_method = "GET"
        api_path = f"/service-catalog/v1beta1/per-region-service-managers/{region_id}"
        resp = platform_conn.command(
            api_method=api_method, api_path=api_path, app_name="glp"
        )
        if resp["code"] == 200:
            region_services = resp["msg"]["serviceManagers"]
            for service in region_services:
                if service["name"] == name:
                    return service["id"]
    return None


def get_region_name(user_provided_region):
    region_name_mapping = json.load(open('reset/region_name_mapping.json'))
    if user_provided_region in [region["id"] for region in region_name_mapping]:
        return user_provided_region
    if user_provided_region in [region["regionName"] for region in region_name_mapping]:
        return next(
            (
                region["id"]
                for region in region_name_mapping
                if region["regionName"] == user_provided_region
            ),
            None,
        )
    print(f'Unknown region name provided - {colored(user_provided_region, "red")}')
    return None


def assign_devices_to_application(conn, devices, application_id, application):
    device_ids = [device["id"] for device in devices]
    region_id = get_region_name(application["region"])
    assign_device_status = d.assign_devices(
        conn=conn,
        devices=device_ids,
        application=application_id,
        region=region_id,
    )
    if assign_device_status["code"] == 200:
        if "succeededDevices" in assign_device_status["msg"]["result"]:
            if len(assign_device_status["msg"]["result"]["succeededDevices"]) == len(
                device_ids
            ):
                new_devices_serials = [device["serial"] for device in devices]
                print(
                    f'Successfully assigned devices({colored(",".join(new_devices_serials), "green")}) to application {colored(application["name"], "green")} in {colored(application["region"], "green")} region.'
                )
                return True
    print(
        f'Unable to assign devices to specified application. Error code - {assign_device_status["code"]}'
    )
    return False

def assign_subscription_to_device(conn, devices):
    sub_response = s.get_all_subscriptions(conn=conn, select="id,key")
    sub_dict = format_sub_dict(sub_response["msg"]["items"])
    add_sub_resp = None
    for device in devices:
        if add_sub_resp is not None:
            time.sleep(15)
        if device["subscription_key"] in sub_dict:
            subscription_id = sub_dict[device["subscription_key"]]
            add_sub_resp = d.add_sub(
                conn=conn,
                devices=[device["id"]],
                sub=subscription_id,
            )
            if "code" in add_sub_resp and add_sub_resp["code"] == 200:
                print(
                    f'Successfully assigned subscription key {colored(device["subscription_key"], "green")} to device {colored(device["serial"], "green")}'
                )


def unassign_devices_from_application(conn, devices):
    get_all_devices_resp = d.get_all_devices(conn=conn, select="id,serialNumber")
    all_device_serials_dict = format_device_dict(get_all_devices_resp["msg"]["items"])
    import pdb
    pdb.set_trace()
    for device in devices:
        if device["serial"] in all_device_serials_dict:
            device["id"] = all_device_serials_dict[device["serial"]]
    device_ids = []
    for device in devices:
        if 'id' in device:
            device_ids.append(device["id"])
    if len(device_ids) == 0:
        print('Unable to find devices in new account')
        return {'code': 200}
    unassign_resp = d.unassign_devices(conn=conn, devices=device_ids)
    if unassign_resp['code'] == 200:
        device_serials = [device["serial"] for device in devices]
        print(f'Successfully unassigned devices({colored(",".join(device_serials), "green")}) from Central application in new account.')
    return unassign_resp


def format_device_dict(device_list):
    device_serials_dict = {}
    for item in device_list:
        serialNumber = item["serialNumber"]
        device_serials_dict[serialNumber] = item["id"]
    return device_serials_dict

def format_sub_dict(sub_list):
    sub_dict = {}
    for sub in sub_list:
        sub_key = sub["key"]
        sub_dict[sub_key] = sub["id"]
    return sub_dict


def parse_arguments():
    parser = ArgumentParser(
        prog="GLP Onboarding Script",
        description="This script utilizes GLP APIs to onboard devices into GLP, assign them to Central application & add subscription keys to the devices",
        epilog="Text at the bottom of help",
    )
    parser.add_argument("--undo", action="store_true")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    if args.undo:
        undo_onboarding()
    else:
        onboarding()
