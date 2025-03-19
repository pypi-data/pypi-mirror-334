from pycentral.base import ArubaCentralNewBase
from pycentral.profiles.vlan import Vlan
from pycentral.profiles import wlan
from pycentral.scopes import Scopes
import json
from operator import itemgetter


def main():

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

    test_err1 = False
    test_err2 = False
    test_err3 = False

    for vlan in vlan_profile_list:

        tmp_vlan_obj = Vlan(vlan_id=vlan['vlan_id'],
                        description=vlan['description'],
                        name=vlan['name'],
                        central_conn=central_conn)
        if test_err1:
            # VerificationError due to vlan_id set to None for create()
            tmp_vlan_obj = Vlan(vlan_id=None,
                            central_conn=central_conn)
        elif test_err2:
            # GenericOperationError due to vlan_id not being a valid int
            tmp_vlan_obj = Vlan(vlan_id="dfsafjaskfld;ajsk",
                            description="CREATES GENERIC OPERATION ERROR",
                            name="CREATES GENERIC OPERATION ERROR",
                            central_conn=central_conn)        

        if test_err3:
            # ParameterError due to vlan_id not being a valid int
            tmp_vlan_obj.set_vlan("booger")

        vlan_obj_list.append(tmp_vlan_obj)

        tmp_vlan_obj.create()

        if not tmp_vlan_obj.materialized:
            print(f"error in creating vlan profile {tmp_vlan_obj.vlan}")
            exit()


if __name__ == "__main__":
    main()
