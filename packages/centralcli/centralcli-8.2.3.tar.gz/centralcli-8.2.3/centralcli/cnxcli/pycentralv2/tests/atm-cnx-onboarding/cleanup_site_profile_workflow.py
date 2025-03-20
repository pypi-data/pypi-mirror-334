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

    for ssid in ssids_dict:
        tmp_wlan_obj = wlan.Wlan(central_conn, ssid['ssid'], ssid)
        result = tmp_wlan_obj.delete()
        if not result:
            print("error in deleting site collection")

    ######################
    #####VLAN PROFILE#####
    ######################
    vlan_obj_list = []

    for vlan in vlan_profile_list:

        tmp_vlan_obj = Vlan(vlan_id=vlan['vlan_id'],
                        description=vlan['description'],
                        name=vlan['name'],
                        central_conn=central_conn)

        result = tmp_vlan_obj.delete()
        if not result:
            print("Error - delete failure")

    site_obj_list = []

    scope_global = Scopes(central_conn=central_conn)

    for site in site_dict_list:      
        site_obj = scope_global.get_site(site_name=site["name"])
        if site_obj is None:
            print("error in retrieving site")
        else:
            site_obj_list.append(site_obj)

    # Creating site collection
    for site_collection_dict in collection_dict_list:
        result = scope_global.delete_site_collection(
            site_collection_name=site_collection_dict['scope-name'],
            remove_sites=True)
        if not result:
            print("error in deleting site collection")


    for site_obj in site_obj_list:
        if site_obj.name == "Demo Town":
            # Include logic to only configure wlan for this site
            pass
        else:
            for vlan in vlan_obj_list:
                profile_resource_str = f"{vlan.resource}/{vlan.vlan}"
                result = site_obj.unassign_profile(profile_name=profile_resource_str, profile_persona=['SWITCH', 'CAMPUS_AP'])
                if not result:
                    print("error in unassigning profile to site")

        result = site_obj.delete()
        if not isinstance(result, bool):
            print(f"site {site_obj.name} delete failed")
if __name__ == "__main__":
    main()