from pycentral.utils import NewCentralURLs
from pycentral.exceptions import (
    GenericOperationError,
    VerificationError,
)

from copy import deepcopy
from .profiles import Profiles

urls = NewCentralURLs()

REQUIRED_ATTRIBUTES = {
    "hostname": "",
    "contact": "",
    "location": "",
}


class SystemInfo(Profiles):
    def __init__(
        self, hostname, contact, location, central_conn=None, local={},
        config_dict={}
    ):
        """
        instantiate a System Info Profile object

        :param hostname: hostname of the System Info profile
        :type hostname: str
        :param contact: description of System Info profile, defaults to None
        :type contact: str
        :param location: name of the System Info profile, defaults to None
        :type location: str
        :param central_conn: established Central connection object
        :type central_conn: ArubaCentralNewBase, optional
        """
        resource = "system-info"
        #  Profile Specific Attributes
        super().__init__(name=hostname, resource=resource,
                         central_conn=central_conn, local=local)
        
        # System Info Specific Attributes
        self.hostname = hostname
        self.contact = contact
        self.location = location

        if config_dict:
            self.config_dict = config_dict
            # Include some validation of config_dict?

        self.config_dict = dict(hostname=self.hostname,
                                contact=self.contact,
                                location=self.location)

        if not central_conn:
            exit(
                "Unable to configure SystemInfo Profile(s) without Central"
                + "connection. "
                + "Please pass a Central connection to SystemInfo Profile."
            )


        self.materialized = False

        self.__modified = False

    def apply(self):
        """
        Main method used to update or create a System Info Profile.
            Checks whether the System Info Profile exists in Central. Calls
            self.update() if System Info Profile is being updated.
            Calls self.create() if a System Info Profile is being created.
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
        Perform a POST call to create a System Info Profile. Only returns if
            no exception is raised.
        :return: var vlan_creation_status - True if System Info profile was
        created.
        :rtype: bool
        """
        api_method = "POST"

        # Need to change verification to consider config dict
        if not set(REQUIRED_ATTRIBUTES.keys()).issubset(dir(self)):
            err_str = "Missing REQUIRED attributes"
            raise VerificationError(err_str, "create() failed")
            
        api_path = urls.fetch_url("PROFILES", "SYSTEM_INFO")

        sysinfo_data = self.__setattrs__(REQUIRED_ATTRIBUTES)

        api_params = {}
        if self.local and self._local_parameters():
            api_params = self._local_parameters()

        resp = self.central_conn.command(
                api_method=api_method, api_path=api_path,
                api_data=sysinfo_data, api_params=api_params
        )

        sysinfo_creation_status = False
        if resp["code"] == 200 and resp["msg"]["message"] == "success":
            sysinfo_creation_status = True
            self.materialized = True
            self.central_conn.logger.info(
                "Successfully created SystemInfo profile "
            )
        else:
            err_str = (
                f"Failure to create SystemInfo profile."
                f" Error-message -> {resp['msg']}"
            )
            self.central_conn.logger.error(err_str)
            e = GenericOperationError(resp["code"], resp["msg"])
            e.set_response(resp)
            raise e
        return sysinfo_creation_status

    def get(self):
        """
        Perform a GET call to retrieve data for a System Info profile then sets attrs
            on System Info Profile Object based on data received
        :return: Returns JSON Data of GET call if success, else None
        :rtype: dict
        """
        api_method = "GET"
        api_path = urls.fetch_url("PROFILES", "SYSTEM_INFO")

        if self.local and self._local_parameters():
            api_params = self._local_parameters()
        else:
            api_params = None

        resp = self.central_conn.command(
            api_method=api_method, api_path=api_path, api_params=api_params
        )
        if resp["code"] == 200:
            self.materialized = True
            # Sets attributes of self to what was found on Central
            sysinfo_data = resp["msg"]

            if self.local and self._local_parameters():
                info_str = ("Successfully fetched SystemInfo Profile " +
                            f"from scope {self.local['scope_id']} with " +
                            f"{self.local['persona']} persona")
            else:
                info_str = ("Successfully fetched SystemInfo Profile " +
                            f"from scope {self.local['scope_id']} with " +
                            f"{self.local['persona']} persona")


            self.central_conn.logger.info(info_str)

            return sysinfo_data
        else:
            err_str = ("Failed to fetch SystemInfo Profile " +
                       f"from scope {self.local['scope_id']} with " +
                       f"{self.local['persona']} persona")
            self.central_conn.logger.error(err_str)
            self.materialized = False
            return None

    def update(self):
        """
        Perform a POST call to apply changes to an existing System Info Profile.
            Source of truth is self
        Perform a POST call to apply difference found in self to an existing
            System Info Profile.
        :return: var modified: True if Object was modified and a POST request
        was successful.
        :rtype: bool
        """
        # Variable returned
        modified = False
        found_diff = False

        api_method = "GET"
        api_path = urls.fetch_url("PROFILES", "SYSTEM_INFO")

        if self.local and self._local_parameters():
            api_params = self._local_parameters()
        else:
            api_params = None

        resp = self.central_conn.command(
            api_method=api_method, api_path=api_path, api_params=api_params
        )

        existing_obj = None

        if resp["code"] == 200:
            existing_obj = resp["msg"]
        else:
            # Raise exception?
            log_str = ("Failed to fetch SystemInfo Profile " +
                        f"from scope {self.local['scope_id']} with " +
                        f"{self.local['persona']} persona")
            self.central_conn.logger.error(log_str)
            self.materialized = False

            return False

        self_dict = deepcopy(self.__dict__)

        for key in existing_obj.keys():
            if key in self_dict.keys() and self_dict[key] != existing_obj[key]:
                found_diff = True
                break

        if found_diff:
            # Self is "source of truth"
            api_method = "POST"
            sysinfo_data = self.__setattrs__(REQUIRED_ATTRIBUTES)

            resp = self.central_conn.command(
                api_method=api_method, api_path=api_path,
                api_data=sysinfo_data,
                api_params=api_params
            )

            if resp["code"] == 200 and resp["msg"]["message"] == "success":
                if self.local and self._local_parameters():
                    info_str = ("Successfully updated SystemInfo Profile " +
                                f"from scope {self.local['scope_id']} with " +
                                f"{self.local['persona']} persona")
                else:
                    info_str = ("Successfully updated SystemInfo Profile " +
                                f"from scope {self.local['scope_id']} with " +
                                f"{self.local['persona']} persona")

                self.central_conn.logger.info(info_str)
                modified = True
            else:
                err_str = ("Failure to update SystemInfo Profile ")
                self.central_conn.logger.error(err_str)
                e = GenericOperationError(resp["code"], resp["msg"])
                e.set_response(resp)
                raise e

        return modified

    def delete(self):
        """
        Perform DELETE call to delete System Info Profile.
        :return: Returns True if resource was successfully deleted
        :rtype: bool
        """
        api_method = "DELETE"
        api_path = urls.fetch_url("PROFILES", "SYSTEM_INFO")

        if self.local and self._local_parameters():
            api_params = self._local_parameters()
        else:
            api_params = None

        resp = self.central_conn.command(
            api_method=api_method, api_path=api_path, api_params=api_params,
            headers={"Accept": "*/*"}
        )

        if resp["code"] == 200 and resp["msg"]["message"] == "success":
            self.central_conn.logger.info(
                "Successfully deleted SystemInfo Profile "
            )
            return True
        else:
            self.central_conn.logger.info(
                f"Failed to delete SystemInfo Profile - {resp}"
            )

        return False


    def __str__(self):
        """
        String containing the SystemInfo Profile.
        :return: This class' string representation.
        :rtype: str
        """
        return "SystemInfo Profile, hostname: '{0}'".format(self.hostname)
