from pycentral.exceptions import ParameterError
from copy import deepcopy


class Profiles:
    def __init__(
        self, name, resource, central_conn=None, 
        config_dict={}, local={}
    ):
        self.name = name
        self.resource = resource
        # Initialize attrs that will be later defined by child
        self.config_dict = config_dict
        self.object_data = dict()

        self.__modified = False
        self.materialized = False

        if central_conn:
            self.central_conn = central_conn
        if local:
            # Sample Local Data {"scope_id": 12345, "persona": "CAMPUS_AP"}
            required_local_keys = ["scope_id", "persona"]
            if all(key in local for key in required_local_keys):
                self.local = local
            else:
                err_info = ", ".join(required_local_keys)
                err_str = f"Missing required local profile attributes. Please\
                    provide both these values - {err_info} for the local\
                    attribute."
                raise ParameterError(err_str)
        else:
            self.local = local

    def resource_str(self):
        return f"{self.resource}/{self.name}"

    def _local_parameters(self):
        local_attributes = None
        if self.local:
            local_attributes = {
                "object_type": "LOCAL"
            }
            local_attributes.update(self.local)
        return local_attributes
    
    def __setattrs__(self, config_attrs):
        """
        Utility function to dynamically set attributes of an object based on
            the provided dictionary
        :param config_attrs: dict whose keys will be added as attributes to
            the provided object with the value set to the value in config_attrs
        :type config_attrs: dict
        """
        attr_data_dict = dict()
        for key, value in config_attrs.items():
            if hasattr(self, key):
                attr_data_dict[key] = getattr(self, key)
            else:
                attr_data_dict[key] = value

        return attr_data_dict
    
    def create_attrs(obj, data_dictionary):
        """
        Given a dictionary object creates class attributes. The methods
            implements setattr() which sets the value of the specified
            attribute of the specified object. If the attribute is already
            created within the object. It's state changes only if the current
            value is not None. Otherwise it keeps the previous value.
        :param obj: Object instance to create/set attributes
        :type obj: PYCENTRAL object
        :param data_dictionary: dictionary containing keys that will be attrs
        :type data_dictionary: dict
        """

        # Used to create a deep copy of the dictionary
        dictionary_var = deepcopy(data_dictionary)

        # K is the argument and V is the value of the given argument
        for k, v in dictionary_var.items():
            # In case a key has '-' inside it's name.
            k = k.replace("-", "_")

            obj.__dict__[k] = v

    def create(self):
        result = False
        body = self.config_dict

        params = {}
        resource = self.resource
        name = self.name
        path = self.object_data['path']
        if self.local and self._local_parameters():
            params = self._local_parameters()

        resp = self.central_conn.command("POST", path, api_data=body,
                                         api_params=params)
        if resp["code"] == 200:
            self.materialized = True
            result = True
            self.central_conn.logger.info(f"{resource} {name} "
                                          "successfully created!")
        else:
            error = resp["msg"]
            err_str = f"Error-message -> {error}"
            self.central_conn.logger.error(
                f"Failed to create {resource} {name}. {err_str}"
            )

        return result

    def get(self):
        """
        Get existing Profile from Aruba Central.

        :return: response object as provided by 'command' function in
            class: `pycentral.ArubaCentralBase`
        :rtype: dict
        """
        # This GET path logic may not be the same for everything?
        path = self.object_data['path']
        params = None

        if self.local:
            params = {
                "view_type": "LOCAL",
                "scope_id": self.local["scope_id"],
                "persona": self.local["persona"]
            }
                        
        resp = self.central_conn.command(
            "GET", path, api_params=params
        )
        return resp

    def update(self, update_data=None):
        """
        Updates NTP profile with values from update_data if provided. If no
        update_data provided the function will check for a diff from the
        Central profile. If a diff is found object config will be pushed to
        Central. Invalid configurations in update_data results in a failed
        update. Individual NTP servers cannot be edited. Additional servers
        can only be added to a profile.

        :param update_data: values for updating ntp profile
        :type update_data: dict
        :return result: result of WLAN update attempt
        :rtype: Bool
        """
        result = False
        found_diff = False
        params = None
        body = None
        path = self.object_data['path']
        new_config = dict(self.config_dict)
        if update_data:
            new_config.update(update_data)

        # Check for Central profile
        central_obj = self.get()
        if central_obj["code"] == 200:
            central_obj = central_obj["msg"]
        else:
            self.materialized = False
            self.central_conn.logger.error(
                f"{self.resource} profile {self.name} not materialized. Please create\
                profile before updating"
            )
            return result

        # Check for local/central config diff
        for key in new_config.keys():
            if key not in central_obj:
                found_diff = True
                break
        for key in central_obj.keys():
            if central_obj[key] != new_config[key]:
                found_diff = True
                break

        # Update profile if diff found
        if found_diff:
            if self.local:
                params = self._local_parameters()
            body = new_config

            resp = self.central_conn.command(
                "POST", path, api_data=body, api_params=params
                )
            
            if resp["code"] == 200:
                self.central_conn.logger.info(
                    f"Successfully updated {self.resource} {self.name}!"
                    )
                self._modified = True
                result = True
                # update object with with new config
                new_config = self.get()
                self.config = new_config
            else:
                result = False
                error = resp["msg"]
                err_str = f"Error-message -> {error}"
                self.central_conn.logger.info(
                    f"Failed to update {self.resource} {self.name}. {err_str}!"
                )

        return result

    def delete(self):
        """
        Delete NTP profile from Central.

        :return result: result of NTP delete attempt
        :rtype: Bool
        """
        path = self.object_data['path']
        params = self._local_parameters()

        resp = self.central_conn.command(
            "DELETE", path, api_params=params, headers={"Accept": "*/*"}
            )
        if resp["code"] == 200:
            self.central_conn.logger.info(
                f"{self.resource} {self.name} successfully deleted!"
                )
            return True
        else:
            self.central_conn.logger.error(
                f"Failed to delete {self.resource} {self.name}!"
                )
            return False
