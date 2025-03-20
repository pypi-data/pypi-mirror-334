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

    site_dict_list, collection_dict_list = itemgetter("sites", "collections")(scope_vars)
    vlan_profile_list, ssids_dict = itemgetter("vlan_profiles", "ssids")(profiles_vars)

    ######################
    #####WLAN PROFILE#####
    ######################
    wlan_obj_list = []

    for ssid in ssids_dict:
        tmp_wlan_obj = wlan.Wlan(central_conn, ssid['ssid'], ssid)
        result = tmp_wlan_obj.create()
        if not result:
            print("error in creating site collection")
        else:
            wlan_obj_list.append(tmp_wlan_obj)

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

        tmp_vlan_obj.create()

        if not tmp_vlan_obj.materialized:
            print(f"error in creating vlan profile {tmp_vlan_obj.vlan}")
            exit()

    site_obj_list = []

    scope_global = Scopes(central_conn=central_conn)

    for site in site_dict_list:

        result = scope_global.create_site(site_attributes=site)
        if not result:
            print("error in creating site")

        site_obj = scope_global.get_site(site_name=site["name"])
        if site_obj is None:
            print("error in retrieving site")

        site_obj_list.append(site_obj)

    # Creating site collection
    for site_collection_dict in collection_dict_list:
        result = scope_global.create_site_collection(
            collection_attributes=site_collection_dict)
        if not result:
            print(f"error in creating site collection {site_collection_dict['scope-name']}")
        
        if site_collection_dict["scope-name"] == "ATM-Discover-2024":
            tmp_site_obj = scope_global.get_site(site_name="Vegas-Demo-Site")
            result = scope_global.add_sites_to_collection(
        site_collection_name=site_collection_dict["scope-name"], site_ids=[tmp_site_obj.id])
            if not result:
                print(f"error in assigning site to site collection {site_collection_dict['scope-name']}")
            
            tmp_collection_obj = scope_global.get_site_collection(collection_name="ATM-Discover-2024")
            for ssid in wlan_obj_list:
                profile_resource_str = f"{ssid.resource}/{ssid.name}"
                tmp_collection_obj.assign_profile(profile_name=profile_resource_str, profile_persona=['BRANCH_GW','CAMPUS_AP'])
                if not result:
                    print("error in assigning profile to site collection")


    for site_obj in site_obj_list:
        for vlan in vlan_obj_list:
            profile_resource_str = f"{vlan.resource}/{vlan.vlan}"
            result = site_obj.assign_profile(profile_name=profile_resource_str, profile_persona=['SWITCH', 'CAMPUS_AP'])
            if not result:
                print("error in assigning profile to site")


if __name__ == "__main__":
    main()
