from .profiles import Profiles
from pycentral.utils import NewCentralURLs

urls = NewCentralURLs()

class Wlan(Profiles):
    def __init__(self, ssid, conn, wlan_attrs={}, local={}):
        resource = "wlan-ssids"
        self.config = wlan_attrs

        super().__init__(
            ssid,
            resource,
            central_conn=conn,
            local=local,
            config_dict=wlan_attrs
        )

        self.object_data['path'] = urls.fetch_url("PROFILES", "wlan", ssid)
        self.object_data['body_key'] = "wlan-ssid"
