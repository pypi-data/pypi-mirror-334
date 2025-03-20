from pycentral.base import ArubaCentralNewBase
from pycentral.profiles.vlan import Vlan
from pycentral.profiles import wlan
from pycentral.scopes import Scopes
import json
from operator import itemgetter


def main():

    scope_vars = json.load(open("sites_config.json"))
    profiles_vars = json.load(open("profile_config.json"))
    credentials = json.load(open("account_credentials.json"))
    central_conn = ArubaCentralNewBase(
        token_info=credentials, classic_auth=True, disable_scope=True)

    if central_conn is None:
        print("Error in central conn")
        exit()

    vlan_profile_list = itemgetter("vlan_profiles")(profiles_vars)

    ######################
    #####VLAN PROFILE#####
    ######################
    vlan_obj_list = []

    for vlan in vlan_profile_list:

        tmp_vlan_obj = Vlan(vlan_id=vlan['vlan_id'],
                        description=vlan['description'],
                        name=vlan['name'],
                        central_conn=central_conn)
        vlan_obj_list.append(tmp_vlan_obj)

        result = tmp_vlan_obj.delete()
        if not result:
            print("Error - delete failure")


if __name__ == "__main__":
    main()
