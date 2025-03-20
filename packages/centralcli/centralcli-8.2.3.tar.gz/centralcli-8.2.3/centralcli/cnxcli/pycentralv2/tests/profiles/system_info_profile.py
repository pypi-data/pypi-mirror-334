from pycentral.base import ArubaCentralNewBase
from pycentral.profiles import SystemInfo
from pycentral.scopes import Scopes
import json
from operator import itemgetter


def main():

    profiles_vars = json.load(open("profile_config.json"))
    credentials = json.load(open("account_credentials.json"))
    central_conn = ArubaCentralNewBase(
        token_info=credentials, disable_scope=True)

    if central_conn is None:
        print("Error in central conn, None provided")
        exit()

    scope_global = Scopes(central_conn=central_conn)        

    global_info, sites, devices = itemgetter("global",
                                             "sites",
                                             "devices")(profiles_vars)

    # Configure a Library level System Info profile
    sysinfo_global = SystemInfo(hostname=global_info["hostname"],
                                contact=global_info["contact"],
                                location=global_info["location"],
                                central_conn=central_conn)
    
    sysinfo_global.create()

    if not sysinfo_global.materialized:
            print("error in creating Library system information profile")
            exit()
    
    # Configure a Site level System Info profile
    for site, sysinfo in sites.items():
        tmp_site = scope_global.find_site(site_names=site)
        tmp_local = {
            "scope_id": tmp_site.id,
            "persona": "SWITCH"
        }

        tmp_sysinfo = SystemInfo(hostname=sysinfo["hostname"],
                                contact=sysinfo["contact"],
                                location=sysinfo["location"],
                                local=tmp_local,
                                central_conn=central_conn)
        
        tmp_sysinfo.create()

        if not tmp_sysinfo.materialized:
            print("error in creating Site system information profile " +
                  f"{tmp_site.name}")
            exit()
    
    # Configure a Device level System Info profile
    for device, sysinfo in devices.items():
        tmp_device = scope_global.find_device(device_serials=device)
        tmp_local = {
            "scope_id": tmp_device.id,
            "persona": "SWITCH"
        }

        tmp_sysinfo = SystemInfo(hostname=sysinfo["hostname"],
                                contact=sysinfo["contact"],
                                location=sysinfo["location"],
                                local=tmp_local,
                                central_conn=central_conn)
        
        tmp_sysinfo.create()

        if not tmp_sysinfo.materialized:
            print("error in creating Site system information profile " +
                  f"{tmp_site.name}")
            exit()
    
    # Include a workflow that takes Library level profile & apply to 
    # site/device?

if __name__ == "__main__":
    main()
