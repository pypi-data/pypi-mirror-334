from pycentral.utils import NewCentralURLs
from .profiles import Profiles

urls = NewCentralURLs()

class Ntp(Profiles):
    def __init__(self, name, conn, ntp_attrs={}, local={}):
        resource = "ntp"
        self.config = ntp_attrs
        super().__init__(
            name,
            resource,
            central_conn=conn,
            local=local,
            config_dict=ntp_attrs
            )
        
        self.object_data['path'] = urls.fetch_url("PROFILES", "ntp", name)
        self.object_data['body_key'] = "profile"
