from pycentral.utils import NewCentralURLs
from pycentral.exceptions import (
    GenericOperationError,
    ParameterError,
    VerificationError,
)

from copy import deepcopy
from .profiles import Profiles

urls = NewCentralURLs()

REQUIRED_ATTRIBUTES = {
    "vlan": 0,
    "description": "",
    "enable": True,
    "name": "",
}


class Vlan(Profiles):
    def __init__(
        self, vlan_id, description=None, name=None, central_conn=None, 
        config_dict={}, local={}
    ):
        """
        instantiate a VLAN Profile object

        :param vlan_id: id of the vlan profile
        :type vlan_id: int
        :param description: description of VLAN profile, defaults to None
        :type description: str, optional
        :param name: name of the VLAN profile, defaults to None
        :type name: str, optional
        :param central_conn: established Central connection object
        :type central_conn: ArubaCentralNewBase, optional
        """
        resource = "layer2-vlan"
        #  Profile Specific Attributes
        super().__init__(name=name, resource=resource,
                         central_conn=central_conn, config_dict=config_dict,
                         local=local)

        
        # VLAN Specific Attributes
        self.vlan = vlan_id
        self.description = description
        self.resource_dict['path'] = urls.fetch_url("PROFILES", "vlan",
                                                   str(self.vlan))


        if not central_conn:
            exit(
                "Unable to fetch Vlan Profile without central connection. "
                + "Please pass a central connection to Vlan Profile."
            )

        # Attribute used to know if object exists within Central or not
        self.materialized = False
        # Attribute used to know if object was changed recently
        self.__modified = False

    def apply(self):
        """
        Main method used to update or create a Vlan Profile.
            Checks whether the Vlan Profile exists in Central. Calls
            self.update() if Vlan Profile is being updated.
            Calls self.create() if a Vlan Profile is being created.
        :return: var modified - True if object was created or modified.
        :rtype: bool
        """
        modified = False
        if self.materialized:
            modified = self.update()
        else:
            modified = self.create()
        # Set internal attribute
        self.__modified = modified
        return modified


    def create(self):
        """
        Perform a POST call to create a Layer 2 Vlan Profile. Only returns if
            no exception is raised.
        :return: var vlan_creation_status - True if Vlan profile was created.
        :rtype: bool
        """
        api_method = "POST"

        if not self.vlan:
            err_str = "Missing self.vlan attribute"
            raise VerificationError(err_str, "create() failed")
        api_path = urls.fetch_url("PROFILES", "vlan", str(self.vlan))

        vlan_data = self.__setattrs__(REQUIRED_ATTRIBUTES)
        self.config_dict = vlan_data

        return super().create()

    # def get(self):
    #     """
    #     Perform a GET call to retrieve data for a Vlan profile then sets attrs
    #         on Vlan Profile Object based on data received
    #     :return: Returns JSON Data of GET call if success, else None
    #     :rtype: dict
    #     """
    #     api_method = "GET"
    #     api_path = urls.fetch_url("PROFILES", "vlan", str(self.vlan))

    #     resp = self.central_conn.command(
    #         api_method=api_method, api_path=api_path, api_params=None
    #     )
    #     if resp["code"] == 200:
    #         self.materialized = True
    #         # Sets attributes of self to what was found on Central
    #         vlan_data = resp["msg"]
    #         self.create_attrs(vlan_data)

    #         self.central_conn.logger.info(
    #             f"Successfully fetched Vlan Profile "
    #             f"{self.name} with id {self.vlan}"
    #         )

    #         return resp["msg"]
    #     else:
    #         self.central_conn.logger.error(
    #             f"Unable to fetch Vlan Profile of"
    #             f" {self.name} with id {self.vlan}"
    #         )
    #         self.materialized = False
    #         return None

    # def update(self):
    #     """
    #     Perform a POST call to apply changes to an existing Vlan Profile.
    #         Source of truth is self
    #     Perform a POST call to apply difference found in self to an existing
    #         Vlan Profile.
    #     :return: var modified: True if Object was modified and a POST request was
    #         successful.
    #     :rtype: bool
    #     """
    #     # Variable returned
    #     modified = False
    #     found_diff = False

    #     api_method = "GET"
    #     api_path = urls.fetch_url("PROFILES", "vlan", str(self.vlan))

    #     resp = self.central_conn.command(
    #         api_method=api_method, api_path=api_path, api_params=None
    #     )

    #     existing_obj = None

    #     if resp["code"] == 200:
    #         existing_obj = resp["msg"]
    #     else:
    #         # Raise exception?
    #         log_str = (
    #             f"Unable to fetch Vlan Profile of {self.name}"
    #             f" with id {self.vlan}"
    #         )
    #         self.central_conn.logger.error(log_str)
    #         self.materialized = False

    #         return False

    #     self_dict = deepcopy(self.__dict__)

    #     for key in existing_obj.keys():
    #         if key in self_dict.keys() and self_dict[key] != existing_obj[key]:
    #             found_diff = True
    #             break

    #     if found_diff:
    #         # Self is "source of truth"
    #         api_method = "POST"
    #         vlan_data = self.__setattrs__(REQUIRED_ATTRIBUTES)

    #         resp = self.central_conn.command(
    #             api_method=api_method, api_path=api_path, api_data=vlan_data
    #         )

    #         if resp["code"] == 200 and resp["msg"]["message"] == "success":
    #             self.central_conn.logger.info(
    #                 f"Successfully updated Vlan Profile "
    #                 f"{self.name} with id {self.vlan}"
    #             )
    #             modified = True
    #         else:
    #             err_str = (
    #                 f"Failure to update Vlan profile."
    #                 f" Error-message -> {resp['msg']}"
    #             )
    #             self.central_conn.logger.error(err_str)
    #             e = GenericOperationError(resp["code"], resp["msg"])
    #             e.set_response(resp)
    #             raise e
    #         # PATCH is not supported in CNX
    #         # self.patch()

    #     return modified

    # def delete(self):
    #     """
    #     Perform DELETE call to delete Vlan Profile.
    #     :return: Returns True if resource was successfully deleted
    #     :rtype: bool
    #     """
    #     api_method = "DELETE"
    #     api_path = urls.fetch_url("PROFILES", "vlan", str(self.vlan))
    #     api_data = {"vlan": self.vlan}

    #     resp = self.central_conn.command(
    #         api_method=api_method, api_path=api_path, api_data=api_data
    #     )

    #     if resp["code"] == 200 and resp["msg"]["message"] == "success":
    #         self.central_conn.logger.info(
    #             f"Successfully deleted Vlan Profile {self.vlan}"
    #         )
    #         return True
    #     else:
    #         # I Don't think we should raise exception?
    #         # This could be the resource does not exist?
    #         self.central_conn.logger.info(
    #             f"Failed to delete Vlan Profile {self.vlan} - {resp}"
    #         )
    #     return False

    def set_vlan(self, vlan_id):
        """
        Sets the attribute of self.vlan
        :return: None
        """
        if not isinstance(vlan_id, int):
            err_str = (
                f"invalid value for vlan_id - must be of type int "
                f"- found {type(vlan_id)}"
            )
            raise ParameterError(err_str)
        self.vlan = vlan_id

    def set_description(self, description):
        """
        Sets the attribute of self.description
        :return: None
        """
        if not isinstance(description, str):
            err_str = (
                f"invalid value for description - must be of type str "
                f"- found {type(description)}"
            )
            raise ParameterError(err_str)
        self.description = description

    def set_name(self, name):
        """
        Sets the attribute of self.name
        :return: None
        """
        if not isinstance(name, str):
            err_str = (
                f"invalid value for name - must be of type str "
                f"- found {type(name)}"
            )
            raise ParameterError(err_str)
        self.description = name

    def __str__(self):
        """
        String containing the Vlan ID.
        :return: This class' string representation.
        :rtype: str
        """
        return "Vlan Profile, id: '{0}'".format(self.vlan)
