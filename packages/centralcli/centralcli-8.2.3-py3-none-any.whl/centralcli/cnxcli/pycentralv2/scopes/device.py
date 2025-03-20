from .scope_maps import ScopeMaps
from . import scope_utils
from ..utils import common_utils, NewCentralURLs


urls = NewCentralURLs()
scope_maps = ScopeMaps()

API_ATTRIBUTE_MAPPING = {
    "id": "id",
    "name": "name",
    "deviceGroupName": "group_name",
    "deviceGroupId": "group_id",
    "deviceType": "type",
    "scopeName": "serial",
    "deployment": "deployment",
    "siteName": "site_name",
    "siteId": "site_id",
    "mac": "mac",
    "model": "model",
    "persona": "persona",
    "ipv4": "ipv4"
}

REQUIRED_ATTRIBUTES = [
    "name"
]

OPTIONAL_ATTRIBUTES = {
    "id": None,
    "latitude": None,
    "longitude": None,
    "image": {"name": "", "contentType": ""},
    "associated_devices": 0,
    "site_collection_name": None,
    "site_collection_id": None,
    "assigned_profiles": []
}

class Device(object):
    """
    This class holds site and all of its attributes & related methods.
    """

    def __init__(self, name=None, serial=None, device_attributes=None,
                 from_api=False, central_conn=None):
        """
        Constructor for Device object

        :param device_attributes: Attributes of the Device
        :type device_attributes: dict
        :param central_conn: Instance of class:`pycentral.ArubaCentralNewBase`
        to establish connection to Central.
        :type central_conn: class:`ArubaCentralNewBase`, optional
        :param from_api: Boolean indicates if the device_attributes is from the
        Central API response.
        :type from_api: bool, optional
        """
        self.materialized = False
        self.central_conn = central_conn

        if from_api and device_attributes:
            device_attributes = scope_utils.rename_keys(device_attributes,
                                            API_ATTRIBUTE_MAPPING)
            common_utils.create_attrs(self, device_attributes)

        if name:
            self.name = name
        if serial:
            self.serial = serial

        # missing_required_attributes = [
        #     attr for attr in REQUIRED_ATTRIBUTES if attr not in site_attributes
        # ]
        # if missing_required_attributes:
        #     raise ValueError(
        #         f'Missing required attributes: {", ".join(missing_required_attributes)}'
        #     )
        # valid_attributes = REQUIRED_ATTRIBUTES + list(OPTIONAL_ATTRIBUTES.keys())
        # unexpected_attributes = [
        #     attr for attr in site_attributes if attr not in valid_attributes
        # ]
        # if unexpected_attributes:
        #     raise ValueError(
        #         f'Unexpected attributes: {", ".join(unexpected_attributes)}.\n If site is being created based off api_response ensure that the from_api flag is set to True'
        #     )
        # set_attributes(
        #     obj=self,
        #     attributes_dict=site_attributes,
        #     required_attributes=REQUIRED_ATTRIBUTES,
        #     optional_attributes=OPTIONAL_ATTRIBUTES,
        # )