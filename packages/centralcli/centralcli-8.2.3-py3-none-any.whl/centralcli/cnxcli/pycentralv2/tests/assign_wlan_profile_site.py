from pycentral.base import ArubaCentralNewBase
from pycentral.profiles import wlan
from pycentral.scopes import Scopes

cordelia_creds = {
    "aruba_central": {
        "access_token": "",
        "base_url": "https://apigw-cordelia.arubadev.cloud.hpe.com",
    },
    "glp": {"access_token": ""},
    "classic_aruba_central": {
        "base_url": "https://apigw-cordelia.arubadev.cloud.hpe.com",
        "token": {"access_token": ""},
    },
    "ssl_verify": True,
}


open = {
    "ssid": "sdk-test",
    "enable": True,
    "forward-mode": "FORWARD_MODE_BRIDGE",
    "dmo": {
        "enable": False,
        "channel-utilization-threshold": 90,
        "clients-threshold": 6,
    },
    "broadcast-filter-ipv4": "BCAST_FILTER_ARP",
    "ssid-utf8": False,
    "essid": {"name": "Guest-Network"},
    "allowed-5ghz-radio": "ALL_5G",
    "dtim-period": 1,
    "inactivity-timeout": 150,
    "max-clients-threshold": 64,
    "max-retries": 4,
    "rf-band": "24GHZ_5GHZ",
    "opmode": "OPEN",
    "mac-authentication": False,
    "type": "GUEST",
    "radius-interim-accounting-interval": 60,
    "pmk-cache-delete-on-leave": True,
}

psk = {
    "essid": {"name": "sdk-test-psk"},
    "ssid": "sdk-test-psk",
    "enable": True,
    "opmode": "BOTH_WPA_WPA2_PSK",
    "personal-security": {"wpa-passphrase": "password"},
    "forward-mode": "FORWARD_MODE_BRIDGE",
    "vlan-selector": "VLAN_RANGES",
    "vlan-id-range": ["1"],
    "rf-band": "24GHZ_5GHZ",
    "dtim-period": 1,
    "broadcast-filter-ipv4": "BCAST_FILTER_NONE",
    "denylist": True,
    "dmo": {"channel-utilization-threshold": 90},
    "local-probe-req-thresh": 0,
    "max-clients-threshold": 1024,
}

site_def = {
    "id": "1072080064",
    "name": "wlan-sdk-test",
    "address": "8000 Foothills",
    "city": "Roseville",
    "state": "CA",
    "country": "United States",
    "zipCode": "95816",
    "timezone": {
        "rawOffset": 19800000,
        "timezone-id": "America/Los_Angeles",
        "timezone-name": "Pacific Standard Time",
    },
}

# Example toggles
delete = False
update = False
site_exist = False

base = ArubaCentralNewBase(token_info=cordelia_creds, classic_auth=True)

wlan_open = wlan.Wlan(base, open["ssid"], open)
wlan_psk = wlan.Wlan(base, psk["ssid"], psk)

if not (delete or update):
    wlan_open.create()
    wlan_psk.create()

if not site_exist:
    print("inside site block")
    scopes = Scopes(base)
    resp = scopes.create_site(site_attributes=site_def)
    new_site = scopes.get_site(site_name=site_def["name"])

    open_profile_resource_str = f"{wlan_open.resource}/{wlan_open.name}"
    psk_profile_resource_str = f"{wlan_psk.resource}/{wlan_psk.name}"

    assign = new_site.assign_profile(
        profile_name=open_profile_resource_str, profile_persona=["CAMPUS_AP"]
    )
    assign = new_site.assign_profile(
        profile_name=psk_profile_resource_str, profile_persona=["CAMPUS_AP"]
    )

# Update example
if update:
    wlan_open.set_update_data({"enable": False})
    wlan_open.update()

# Delete example
if delete:
    wlan_open.delete()
    wlan_psk.delete()
