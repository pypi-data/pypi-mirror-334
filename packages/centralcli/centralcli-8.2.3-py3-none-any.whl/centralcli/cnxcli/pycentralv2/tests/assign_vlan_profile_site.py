from pycentral.base import ArubaCentralNewBase
from pycentral.profiles.vlan import Vlan
from pycentral.scopes.site import Site
from pycentral.scopes import Scopes

new_creds = {
    "aruba_central": {
      "base_url": "",
      "client_id": "",
      "client_secret": ""
    }
}

vlan_site_test_dict = {
                    "name": "Ti-vlan-Test",
                    "address": "8000 Foothills",
                    "city": "Roseville",
                    "state": "California",
                    "country": "United States",
                    "zipcode": "95816",
                    "timezone": "America/Los_Angeles"
                }


vlan_42_dict = {
    "vlan_id": 42,
    "description": "UPLINK_VLAN",
    "name": "UPLINK_VLAN"
}


def main():
    vlan_test = False
    central_conn = ArubaCentralNewBase(
        token_info=new_creds, disable_scope=True)

    if central_conn is None:
        print("Error in central conn")
        exit()
    # I think there's value in supporting 2 methods of
    # initialization/definition - providing a dict/JSON
    # or providing the values as a parameter
    # I'm not sure how to gracefully handle both so this
    # may be a nice to have

    
    vlan_42_obj = Vlan(vlan_id=vlan_42_dict['vlan_id'],
                    description=vlan_42_dict['description'],
                    name=vlan_42_dict['name'],
                    central_conn=central_conn)
    # or alternatively

    # vlan_42_obj = Vlan(data_dict=vlan_42_dict)

    # Will create the object if it doesn't exist or
    # will retrieve the data from Central and store in
    # object if it does exist
    # vlan_42_obj.apply()

    vlan_42_obj.create()

    if not vlan_42_obj.materialized:
        print("error in creating vlan 42")
        exit()

    if vlan_test:
        vlan_42_obj.name = "shouldn't exist"

        print(vlan_42_obj.name)
        result = vlan_42_obj.get()
        if result is not None:
            print("vlan retrieval success")
        
        print(vlan_42_obj.name)

        vlan_42_obj.name = "changed name"

        modified = vlan_42_obj.update()
        if not modified:
            print("Not modified")
        else:
            print("Modified")
        
        result = vlan_42_obj.delete()
        if result:
            print("delete success")

    # Users can either choose to call apply() or
    # create() function and handle it themselves
    scope_global = Scopes(central_conn=central_conn)
    result = scope_global.create_site(site_attributes=vlan_site_test_dict)
    if not result:
        print("error in creating site")
    
    site_obj = scope_global.find_site(site_names=vlan_site_test_dict["name"])
    if site_obj is None:
        print(False)
    else:
        print("success")
        print(site_obj)

    #site_test = Site(name="vlan-profile-test")
    
    # result = site_test.create()

    # if not site_test.materialized or not result:
    #     print("error in creating site")
    #     exit()
    
    # Assigning profiles will require the whole profile
    # object or alternatively just passing in the resource
    #result = site_obj.assign_profile(profile_obj=vlan_42_obj, device_persona=['SWITCH', 'CAMPUS_AP'])
    profile_resource_str = f"{vlan_42_obj.resource}/{vlan_42_obj.vlan}"
    result = site_obj.assign_profile(profile_name=profile_resource_str, profile_persona=['SWITCH', 'CAMPUS_AP'])

    # alternatively
    #result = site_test.assign_profile(resource="layer2-vlan/42", device_persona=['ALL'])

    if not result:
        print("error in assigning profile to site")


    unassign_profile = True

    if unassign_profile:
        profile_resource_str = f"{vlan_42_obj.resource}/{vlan_42_obj.vlan}"
        result = site_obj.unassign_profile(profile_name=profile_resource_str, profile_persona=['SWITCH', 'CAMPUS_AP'])


if __name__ == "__main__":
    main()