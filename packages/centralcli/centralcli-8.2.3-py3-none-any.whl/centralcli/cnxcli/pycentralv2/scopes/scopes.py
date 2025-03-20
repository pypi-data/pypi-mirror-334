from .scope_utils import (
    fetch_attribute,
    add_profile,
    assign_profile,
    unassign_profile,
    get_scope_elements,
    get_all_scope_elements,
    DEFAULT_LIMIT,
    SUPPORTED_SCOPES,
)
from .device import Device
from .site import Site
from .site_collection import Site_Collection
from .scope_maps import ScopeMaps
from ..utils import NewCentralURLs
from ..exceptions import ParameterError

urls = NewCentralURLs()

scope_maps = ScopeMaps()


class Scopes:
    """
    This class holds the Scopes(Global heirarchy) class & methods that can be used to manage sites & site collections within the Global Heirarchy
    """

    def __init__(self, central_conn=None):
        """
        Constructor for Scopes object. This represents

        :param central_conn: Instance of class:`pycentral.ArubaCentralNewBase` to establish connection to Central.
        :type central_conn: class:`ArubaCentralNewBase`, optional
        """
        self.site_collections = []
        self.sites = []
        self.id = None
        self.name = "Global"
        # Attribute used to know if object exists within Central or not
        self.materialized = False

        self.assigned_profiles = []
        if central_conn:
            self.central_conn = central_conn
            self.get()
        else:
            exit(
                "Unable to fetch scopes without central connection. Please pass a central connecton to scope."
            )

    def get(self):
        """
        Performs GET calls to Central to retrieve latest data of sites & site collections.

        :return: Returns True if sites & site collections are successfuly updated, else None
        :rtype: bool
        """
        self.get_all_sites()
        self.get_all_site_collections()
        self.get_all_device_groups()
        self.get_all_devices()

        if len(self.sites) > 0:
            self.get_id()
        if len(self.site_collections) > 0:
            self._correlate_scopes()
        if len(self.site_collections) > 0 and len(self.sites) > 0:
            self.get_scope_profiles()
        self.materialized = True
        self.central_conn.logger.info(
            "Successfully fetched scope(site & site collection) details from Aruba Central"
        )
        return True

    def get_all_sites(self):
        """
        Performs GET calls to retrieve all the sites from Central

        :return: Returns list of sites. Each element of this list is of type class:`Site`
        :rtype: dict
        """
        sites_response = get_all_scope_elements(obj=self, scope="SITE")
        sites_obj_list = [
            Site(central_conn=self.central_conn, site_attributes=site, from_api=True)
            for site in sites_response
        ]
        self.sites = sites_obj_list
        return sites_obj_list

    def get_all_site_collections(self):
        """
        Performs GET calls to retrieve all the site collections from Central

        :return: Returns list of site collections. Each element of this list is of type class:`Site_Collection`
        :rtype: dict
        """
        site_collections_response = get_all_scope_elements(
            obj=self, scope="SITE_COLLECTION"
        )
        site_collections_obj_list = [
            Site_Collection(
                central_conn=self.central_conn,
                collection_attributes=collection,
                from_api=True,
            )
            for collection in site_collections_response
        ]
        self.site_collections = site_collections_obj_list
        return site_collections_obj_list

    def get_all_devices(self):
        """
        Performs GET calls to retrieve all the devices from Central

        :return: Returns list of devices. Each element of this list is a dictionary with device details
        :rtype: dict
        """
        device_list = get_all_scope_elements(obj=self, scope="DEVICE")
        devices_obj_list = [
            Device(central_conn=self.central_conn, device_attributes=device,
                   from_api=True)
            for device in device_list
        ]
        self.devices = devices_obj_list
        return devices_obj_list

    def get_all_device_groups(self):
        """
        Performs GET calls to retrieve all the device groups from Central

        :return: Returns list of devices. Each element of this list is a dictionary with device group details
        :rtype: dict
        """
        device_groups_list = get_all_scope_elements(obj=self, scope="DEVICE_GROUP")
        self.device_groups = device_groups_list
        return device_groups_list

    def get_id(self):
        """
        Returns the ID of the Global scope. If the ID hasn't been set, the function will fetched the Id. Atleast 1 site has to be part of the Global scope for the API to get the ID

        :return: ID of global scope
        :rtype: int
        """
        global_scope_id = None
        if self.id is not None:
            global_scope_id = fetch_attribute(self, "id")
        if len(self.sites) > 0:
            sample_site = self.sites[0]
            heirarchy = None
            heirarchy = self.get_hierarchy(scope="SITE", id=sample_site.get_id())
            if heirarchy is not None:
                org_data = None
                heirarchy_data = heirarchy[0]["hierarchy"]
                for scope in heirarchy_data:
                    if scope["scopeType"] == "org":
                        org_data = scope
                        break
                if org_data is not None:
                    global_scope_id = int(org_data["scopeId"])
                    self.id = global_scope_id
                else:
                    self.central_conn.logger.error("Unable to get global scope ID")
        else:
            self.central_conn.logger.error(
                "Unable to get global scope ID without having 1 site in the central account."
            )
        return global_scope_id

    def get_name(self):
        """
        This function returns the name of the Global heirarchy

        :return: Name of site collection
        :rtype: str
        """
        return fetch_attribute(self, "name")

    def get_sites(self, limit=DEFAULT_LIMIT, offset=0, filter_field="", sort=""):
        """
        This function GETs the list of sites from Central based on the provided attributes.

        :param limit: Number of sites to be fetched, defaults to 100
        :type limit: int
        :param offset: Pagination start index, defaults to 1
        :type offset: int
        :param filter_field: Field that needs to be used for sorting the list of sites. Accepted values for this argument is scope-name, address, state, country, city, device-count, collection-name, zipcode, timezone
        :type filter_field: str, optional
        :param sort: Direction of sorting for the field. ASC or DESC are accepted values for this argument
        :type sort: str, optional

        :return: List of sites based on the provided arguments. If there are errors it will return None.
        :rtype: list
        """
        return get_scope_elements(
            obj=self,
            scope="SITE",
            limit=limit,
            offset=offset,
            filter_field=filter_field,
            sort=sort,
        )

    def get_site_collections(
        self,
        limit=DEFAULT_LIMIT,
        offset=0,
        filter_field="",
        sort="",
    ):
        """
        This function GETs the list of site collections from Central based on the provided attributes.

        :param limit: Number of site collections to be fetched, defaults to 100
        :type limit: int
        :param offset: Pagination start index, defaults to 1
        :type offset: int
        :param filter_field: Field that needs to be used for sorting the list of sites. Accepted values for this argument is site-count, device-count, scope-name
        :type filter_field: str, optional
        :param sort: Direction of sorting for the field. ASC or DESC are accepted values for this argument
        :type sort: str, optional

        :return: List of site collections based on the provided arguments. If there are errors it will return None.
        :rtype: list
        """
        return get_scope_elements(
            obj=self,
            scope="SITE_COLLECTION",
            limit=limit,
            offset=offset,
            filter_field=filter_field,
            sort=sort,
        )

    def _correlate_scopes(self):
        """
        Helper function that is used in __init__ class of Scope object. For sites under site collection, this function adds the site's ID to the site collection object.
        """
        for site in self.sites:
            collection_id = fetch_attribute(site, "site_collection_id")
            if collection_id:
                site_collection = self.find_site_collection(
                    site_collection_ids=collection_id
                )
                if site_collection:
                    site_collection.add_site(site.get_id())

    def find_site_collection(
        self, site_collection_ids=None, site_collection_names=None
    ):
        """
        This function returns the site collection(of type class:`Site_Collection`) based on the provided parameters. Only one of collection_name or collection_id is required to find the site collection(s).

        :param site_collection_ids: ID of site collection or list of site collection IDs
        :type site_collection_ids: int or list
        :param site_collection_names: Name of site collection or list of site collection names
        :type site_collection_names: str or list

        :return: If the site collection(s) are found, the site collection(s) is returned, else None is returned.
        :rtype: dict
        """
        site_collections = self._find_scope_elements(
            ids=site_collection_ids,
            names=site_collection_names,
            scope="SITE_COLLECTION",
        )
        if not site_collections:
            self.get_all_sites()
            site_collections = self._find_scope_elements(
                ids=site_collection_ids,
                names=site_collection_names,
                scope="SITE_COLLECTION",
            )
        return site_collections

    def find_site(self, site_ids=None, site_names=None):
        """
        This function returns the site(of type class:`Site`) based on the provided parameters. Only one of site_ids or site_names is required to find the site(s).

        :param site_ids: ID of site or list of site IDs
        :type site_ids: str or list
        :param site_names: Name of site or list of site names
        :type site_names: str or list

        :return: If the site(s) are found, the site(s) are returned, else None is returned.
        :rtype: dict
        """
        sites = self._find_scope_elements(ids=site_ids, names=site_names, scope="SITE")
        if not sites:
            self.get_all_sites()
            sites = self._find_scope_elements(
                ids=site_ids, names=site_names, scope="SITE"
            )
        return sites

    def find_device(self, device_ids=None, device_names=None,
                    device_serials=None):
        """
        This function returns the device(of type class:`Device`) based on the
        provided parameters. Only one of device_ids or device_names or
         device_serials is required to find the device(s).

        :param device_ids: ID of device or list of device IDs
        :type device_ids: str or list
        :param device_names: Name of device or list of device names
        :type device_names: str or list
        :param device_serials: Serial number of device or list of device serial
        numbers
        :type device_serials: str or list

        :return: If the device(s) are found, the device(s) are returned, else
        None is returned.
        :rtype: dict
        """
        devices = self._find_scope_elements(ids=device_ids, names=device_names,
                                            serials=device_serials,
                                            scope="DEVICE")
        if not devices:
            self.get_all_devices()
            devices = self._find_scope_elements(
                ids=device_ids, names=device_names, serials=device_serials,
                scope="DEVICE"
            )
        return devices

    def _find_scope_elements(self, ids=None, names=None, serials=None,
                             scope=""):
        """
        This is a helper function that returns the scope element or elements based on the provided parameter. The ids or names of the element(s) has to be provided and it will look for it in the specified scope levels. If the scope parameter is not specified, the function will look for the scope elements in global, site collection, and site.

        :param ids: ID of the element(s)
        :type ids: str or list
        :param names: Name of element(s)
        :type names: str or list
        :param scope: The type of the element. Global, site_collection, and site are valid parameters for this argument
        :type scope: str, optional

        :return: If the site(s) are found, the site(s) are returned, else None is returned.
        :rtype: dict
        """
        scope_elements = None
        scope = scope.lower()
        supported_scopes = [s.lower() for s in SUPPORTED_SCOPES]
        supported_scopes.append("global")
        if scope and scope not in supported_scopes:
            self.central_conn.logger.error(
                "Unknown scope provided. Please provide one of the supported scopes - "
                ", ".join(SUPPORTED_SCOPES)
            )
            return scope_elements
        if scope == "global" or (ids is not None and self.id == ids):
            return self

        if all([ids, names]):
            self.central_conn.logger.error(
                f"Please provide either {scope} ids or names."
            )
        elif not any([ids, names, serials]):
            self.central_conn.logger.error(
                f"Missing {scope} ids and names. Please provide either"
                f"{scope} ids or names."
            )
        else:
            if scope:
                scope_list = getattr(self, scope + "s")
                if names:
                    if isinstance(names, str):
                        scope_elements = next(
                            (
                                element
                                for element in scope_list
                                if element.name == names
                            ),
                            None,
                        )

                    elif isinstance(names, list):
                        scope_elements = [
                            next(
                                (
                                    element
                                    for element in scope_list
                                    if element.name == name
                                ),
                                None,
                            )
                            for name in names
                        ]
                elif ids:
                    if isinstance(ids, int) or isinstance(ids, str):
                        scope_elements = next(
                            (element for element in scope_list if element.id == ids),
                            None,
                        )
                    elif isinstance(ids, list):
                        scope_elements = [
                            next(
                                (
                                    element
                                    for element in scope_list
                                    if element.id == scope_id
                                ),
                                None,
                            )
                            for scope_id in ids
                        ]
                elif serials:
                        if isinstance(serials, str):
                            scope_elements = next(
                                (
                                    element
                                    for element in scope_list
                                    if element.serial == serials
                                ),
                                None,
                            )

                        elif isinstance(serials, list):
                            scope_elements = [
                                next(
                                    (
                                        element
                                        for element in scope_list
                                        if element.serial == serial
                                    ),
                                    None,
                                )
                                for serial in serials
                            ]
            else:
                scope_elements = self.find_site(site_ids=ids, site_names=names)
                if scope_elements:
                    return scope_elements
                scope_elements = self.find_site_collection(
                    site_collection_ids=ids, site_collection_names=names
                )
                if scope_elements:
                    return scope_elements
                self.central_conn.logger.warning(
                    f"Unable to find scope with provided scope details - {ids}"
                )
        return scope_elements

    def add_sites_to_site_collection(
        self,
        site_collection_id=None,
        site_collection_name=None,
        site_ids=None,
        site_names=None,
    ):
        """
        This method adds site(s) to a site collection.

        :param site_collection_id: ID of the site collection. Either site_collection_name or site_collection_id is required.
        :type site_collection_id: int, optional
        :param site_collection_name: Name of the site collection. Either site_collection_name or site_collection_id is required.
        :type site_collection_name: str, optional
        :param site_ids: ID of the site that needs to be associated with the site collection. If multiple sites need to be associated, a list of site IDs can be provided. Either site_ids or site_names is required.
        :type site_ids: int or list, optional
        :param site_names: Name of the site that needs to be associated with the site collection. If multiple sites need to be associated, a list of site names can be provided. Either site_ids or site_names is required.
        :type site_names: str or list, optional

        :return: True if site(s) were successfully associated with the site collection, else False
        :rtype: bool
        """
        site_collection = self.find_site_collection(
            site_collection_ids=site_collection_id,
            site_collection_names=site_collection_name,
        )
        if site_collection:
            sites = self.find_site(site_ids=site_ids, site_names=site_names)
            if isinstance(sites, Site):
                sites = [sites]
            if all(sites):
                site_association = site_collection.associate_site(sites=sites)
                if site_association:
                    return True
                else:
                    self.central_conn.logger.error(
                        "Unable to complete site association with site collection."
                    )
                    return False

            else:
                self.central_conn.logger.error(
                    "Unable to associate invalid site(s) with site collection. Please provide valid site id(s) or name(s)."
                )
                return False
        elif site_collection is None:
            self.central_conn.logger.error(
                "Unable to associate site(s) with invalid site collection. Please provide a valid site collection id or name."
            )
            return False

    def remove_sites_from_site_collection(self, site_ids=None, site_names=None):
        """
        This method removes site(s) from a site collection.

        :param site_ids: ID of the site that needs to be unassociated from site collection. If multiple sites need to be unassociated, a list of site IDs can be provided. Either site_ids or site_names is required.
        :type site_ids: int or list, optional
        :param site_names: Name of the site that needs to be unassociated from site collection. If multiple sites need to be unassociated, a list of site names can be provided. Either site_ids or site_names is required.
        :type site_names: str or list, optional

        :return: True if site(s) were successfully unassociated from the site collection(s), else False
        :rtype: bool
        """
        sites = self.find_site(site_ids=site_ids, site_names=site_names)
        if not isinstance(sites, list):
            sites = [sites]
        if all(sites):
            api_method = "DELETE"
            api_path = urls.fetch_url("SCOPES", "REMOVE_SITE_FROM_COLLECTION")
            api_params = {"siteIds": ",".join([str(site.get_id()) for site in sites])}
            resp = self.central_conn.command(
                api_method=api_method, api_path=api_path, api_params=api_params
            )
            if resp["code"] == 200:
                site_name_str = ", ".join([str(site.get_name()) for site in sites])
                self.central_conn.logger.info(
                    "Successfully removed sites "
                    + site_name_str
                    + " from site collection."
                )
                self._update_site_collection_attributes(sites=sites)
                return True
            else:
                self.central_conn.logger.error(resp["msg"])
                return False
        else:
            self.central_conn.logger.error(
                "Unable to remove invalid site(s) from site collection. Please provide valid site id(s) or name(s)."
            )
        return False

    def _update_site_collection_attributes(self, sites):
        """
        This is a helper function that helps with removing sites from site collection

        :param sites: List of sites that need to removed from site collections
        :type sites: list
        """
        for site in sites:
            old_collection_attributes = site.get_site_collection_attributes()
            if old_collection_attributes is not None:
                old_collection = self.find_site_collection(
                    site_collection_ids=old_collection_attributes["id"]
                )
                if old_collection:
                    old_collection.remove_site(site_id=site.get_id())
                site.remove_site_collection()

    def create_site(
        self, site_attributes, site_collection_id=None, site_collection_name=None
    ):
        """
        This method creates a new site in Central. Optionally, it can associate the newly created site to site collection

        :param site_attributes: Attributes of the site that needs to be created.
        :type site_attributes: dict
        :param site_collection_id: ID of the site collection. Either site_collection_name or site_collection_id is required if the site has to be associated to a site collection.
        :type site_collection_id: int, optional
        :param site_collection_name: Name of the site collection. Either site_collection_name or site_collection_id is required if the site has to be associated to a site collection.
        :type site_collection_name: str, optional

        :return: True if site creation is successful, else False
        :rtype: bool
        """
        site_obj = Site(site_attributes=site_attributes, central_conn=self.central_conn)
        site_creation_status = site_obj.create()

        if site_creation_status:
            self.sites.append(site_obj)
            if site_collection_id or site_collection_name:
                self.add_sites_to_site_collection(
                    site_collection_id=site_collection_id,
                    site_collection_name=site_collection_name,
                    site_ids=[site_obj.get_id()],
                )

        else:
            self.central_conn.logger.error(
                f"Unable to create site {site_obj.get_name()}"
            )
        return site_creation_status

    def delete_site(self, site_id=None, site_name=None):
        """
        This method deletes a site in Central.

        :param site_id: ID of the site that needs to be deleted. Either site_id or site_name is required.
        :type site_id: int, optional
        :param site_name: Name of the site that needs to be deleted. Either site_id or site_name is required.
        :type site_name: str, optional

        :return: True if site deletion is successful, else False
        :rtype: bool
        """
        site_deletion_status = False
        site = self.find_site(site_ids=site_id, site_names=site_name)
        if site:
            site_id = site.get_id()
            site_deletion_status = site.delete()
            if site_deletion_status:
                self._remove_scope_element(scope="SITE", element_id=site.get_id())
                if site.site_collection_id:
                    site_collection = self.find_site_collection(
                        site_collection_ids=site.site_collection_id
                    )
                    site_collection.remove_site(site_id)

            else:
                error_resp = site_deletion_status
                self.central_conn.logger.error(
                    "Unable to delete site. "
                    + "Error-message -> "
                    + error_resp["msg"]["message-code"][0]["code"]
                )
        else:
            self.central_conn.logger.error(
                "Please provide a valid site id or name to be deleted."
            )
        return site_deletion_status

    def _remove_scope_element(self, scope, element_id):
        """
        This helper method removes the specified scope element from self

        :param scope: The type of the element. site_collection and site are valid parameters for this argument
        :type scope: str
        :param element_id: ID of the scope element that needs to be removed
        :type element_id: int

        :return: True if the scope element has successfully removed from self, else False
        :rtype: bool
        """
        if scope not in SUPPORTED_SCOPES:
            self.central_conn.logger.error(
                "Unknown scope provided. Please provide one of the supported scopes - "
                ", ".join(SUPPORTED_SCOPES)
            )
            return False
        if scope == "SITE":
            element_list = self.sites
        elif scope == "SITE_COLLECTION":
            element_list = self.site_collections

        index = None
        for id_element, element in enumerate(element_list):
            if element.get_id() == element_id:
                index = id_element
                break
        if index is not None:
            element_list.pop(index)
            return True
        return False

    def create_site_collection(
        self, collection_attributes, site_ids=None, site_names=None
    ):
        """
        This method creates a new site collection in Central. Optionally, it can associate existing sites to this newly created site collection

        :param collection_attributes: Attributes of the site collection that needs to be created.
        :type collection_attributes: dict
        :param site_ids: ID of the site(s). If multiple sites need to be associated with the site collection, a list of site ids can be provided. Either site_ids or site_names is required if the site collection has to be associated with site(s)
        :type site_ids: int or list, optional
        :param site_names: Name of the site(s). If multiple sites need to be associated with the site collection, a list of site names can be provided. Either site_ids or site_names is required if the site collection has to be associated with site(s)
        :type site_names: str or list, optional

        :return: True if site collection creation is successful, else False
        :rtype: bool
        """

        site_collection_obj = Site_Collection(
            collection_attributes=collection_attributes,
            central_conn=self.central_conn
        )
        site_collection_creation_status = site_collection_obj.create()
        if site_collection_creation_status:
            self.site_collections.append(site_collection_obj)
            if site_ids or site_names:
                site_addition_status = self.add_sites_to_site_collection(
                    site_collection_id=site_collection_obj.get_id(),
                    site_ids=site_ids,
                    site_names=site_names,
                )
                if site_addition_status:
                    self.central_conn.logger.info(
                        f"Successfully associated sites with site collection {site_collection_obj.get_name()}"
                    )
                else:
                    self.central_conn.logger.error(
                        f"Failed to associate sites with site collection {site_collection_obj.get_name()}"
                    )
        else:
            self.central_conn.logger.error(
                f"Unable to create site collection {site_collection_obj.get_name()}"
            )
        return site_collection_creation_status

    def delete_site_collection(
        self, site_collection_id=None, site_collection_name=None, remove_sites=False
    ):
        """
        This method deletes a site collection in Central. If the remove_sites flag is set to true, the method will remove any sites that has been associated with the site collection before deleting.

        :param site_collection_id: ID of the site collection that needs to be deleted. Either site_collection_id or site_collection_name is required.
        :type site_collection_id: int, optional
        :param site_collection_name: Name of the site that needs to be deleted. Either site_collection_id or site_collection_name is required.
        :type site_collection_name: str, optional
        :param remove_sites: Boolean indicates if the method should remove sites associated with the site collection before deleting it. If set to true, it will first delete site(s) associated with the site collection & then delete it. If set to False & the site collection has site(s) associated with it, the method will not allow you to delete the site collection.
        :type remove_sites: bool, optional

        :return: True if site collection deletion is successful, else False
        :rtype: bool
        """
        site_collection_deletion_status = False
        site_collection = self.find_site_collection(
            site_collection_ids=site_collection_id,
            site_collection_names=site_collection_name,
        )
        if site_collection:
            num_associated_sites = len(site_collection.sites)
            if remove_sites is False and num_associated_sites > 0:
                self.central_conn.logger.error(
                    "Unable to delete site collection with "
                    f"{num_associated_sites} sites associated with it. "
                    "Set remove_sites argument to True to remove sites associated with site collection before deleting it."
                )
                return site_collection_deletion_status
            elif remove_sites and num_associated_sites > 0:
                self.central_conn.logger.info(
                    f"Attempting to remove {num_associated_sites} associated sites before deleting site collection "
                    + site_collection.get_name()
                )
                site_unassociated_status = self.remove_sites_from_site_collection(
                    site_ids=site_collection.sites
                )
                if site_unassociated_status is not True:
                    self.central_conn.logger.info(
                        f"Unable to remove {num_associated_sites} associated sites from site collection "
                        + f"{site_collection.get_name()}."
                    )
                    return site_unassociated_status
            site_collection_deletion_status = site_collection.delete()
            if site_collection_deletion_status:
                self._remove_scope_element(
                    scope="SITE_COLLECTION", element_id=site_collection.get_id()
                )
            else:
                error_resp = site_collection_deletion_status
                self.central_conn.logger.error(
                    "Unable to delete site collection. "
                    + "Error-message -> "
                    + error_resp["msg"]["message-code"][0]["code"]
                )
        else:
            self.central_conn.logger.error(
                "Please provide a valid site collection id or name to be deleted."
            )
        return site_collection_deletion_status

    def get_hierarchy(self, scope, id=None, name=None):
        """
        This method returns the heirarchy of the specified scope element in the global hierarchy.

        :param scope: The type of the element. site_collection and site are valid parameters for this argument
        :type scope: str
        :param id: ID of the element. Either id or name is required
        :type id: int or list, optional
        :param name: Name of the site collection. Either id or name
        :type name: str or list, optional

        :return: Dictionary with the heirarchy of the specified element in the Global scope
        :rtype: dict
        """
        if scope not in SUPPORTED_SCOPES:
            self.central_conn.logger.error(
                "Unknown scope provided. Please provide one of the supported scopes - "
                ", ".join(SUPPORTED_SCOPES)
            )
            return None

        scope_id = None
        if id:
            scope_id = id
        else:
            if scope == "SITE":
                site = self.find_site(site_names=name)
                if site is not None:
                    scope_id = site.get_id()
            elif scope == "SITE_COLLECTION":
                site_collection = self.find_site_collection(site_collection_names=name)
                if site_collection is not None:
                    scope_id = site.get_id()
            if not scope_id:
                self.central_conn.logger.error(
                    f"Unable to find id of specified scope element with name of {name}"
                )
                return None

        api_method = "GET"
        api_path = urls.fetch_url("SCOPES", "HIERARCHY")
        api_params = {"scopeId": scope_id, "scopeType": scope.lower()}
        resp = self.central_conn.command(
            api_method=api_method, api_path=api_path, api_params=api_params
        )
        if resp["code"] == 200:
            self.central_conn.logger.info(
                f"Successfully fetched scope heirarchy of " f"{scope} with id {id}"
            )
            return resp["msg"]["items"]
        else:
            self.central_conn.logger.error(
                f"Unable to fetch scope heirarchy of {scope} with id {id}"
            )
            return None

    def __str__(self):
        """
        This function returns the string containing the ID of the Global hierarchy scope.

        :return: String representation of this class
        :rtype: str
        """
        return f"Global ID - {self.id}"

    def get_scope_profiles(self):
        """
        This method fetches all the configuration profiles that are associated with different scope elements and associates these profiles to the relevant scope objects in self
        """
        scope_map_list = scope_maps.get(central_conn=self.central_conn)
        unknown_scopes = []
        for mapping in scope_map_list:
            scope_id = mapping.pop("scope-name")
            if scope_id in unknown_scopes:
                continue
            required_scope_element = self._find_scope_elements(ids=scope_id)
            if required_scope_element:
                add_profile(
                    obj=required_scope_element,
                    name=mapping["resource"],
                    persona=mapping["persona"],
                )
            else:
                unknown_scopes.append(scope_id)

    def assign_profile_to_scope(
        self,
        profile_name,
        profile_persona,
        scope=None,
        scope_name=None,
        scope_id=None,
    ):
        """
        This method assigns the specified configuration profile to the specified scope. Configuration profiles can be assigned to global, site collections, and sites

        :param profile_name: Name of the configuration profile
        :type profile_name: str
        :param profile_persona: Device persona(role) that the profile needs to perform in the scope
        :type profile_persona: str
        :param scope: The type of the element. Global, site_collection, and site are valid parameters for this argument
        :type scope: str
        :param scope_name: Name of the scope element. Either scope_name or scope_id is required
        :type scope_name: str
        :param scope_id: ID of the scope element. Either scope_name or scope_id is required
        :type scope_id: int

        :return: True if the configuration profiles was succesfully assigned to the specified scope, else False
        :rtype: bool
        """
        return self._profile_to_scope_helper(
            "assign", profile_name, profile_persona, scope, scope_name, scope_id
        )

    def unassign_profile_to_scope(
        self,
        profile_name,
        profile_persona,
        scope=None,
        scope_name=None,
        scope_id=None,
    ):
        """
        This method unassigns the specified configuration profile to the specified scope. Configuration profiles can be assigned to global, site collections, and sites

        :param profile_name: Name of the configuration profile
        :type profile_name: str
        :param profile_persona: Device persona(role) that the profile needs to perform in the scope
        :type profile_persona: str
        :param scope: The type of the element. Global, site_collection, and site are valid parameters for this argument
        :type scope: str
        :param scope_name: Name of the scope element. Either scope_name or scope_id is required
        :type scope_name: str
        :param scope_id: ID of the scope element. Either scope_name or scope_id is required
        :type scope_id: int

        :return: True if the configuration profiles was succesfully unassigned from the specified scope, else False
        :rtype: bool
        """
        return self._profile_to_scope_helper(
            "unassign", profile_name, profile_persona, scope, scope_name, scope_id
        )

    def _profile_to_scope_helper(
        self,
        operation,
        profile_name,
        profile_persona,
        scope=None,
        scope_name=None,
        scope_id=None,
    ):
        """
        This is a helper method that is used by assign_profile_to_scope() & unassign_profile_to_scope()

        :param operation: Type of operation that needs to be performed with the configuration profile. assign & unassign are valid parameters for this argument
        :type operation: str
        :param profile_name: Name of the configuration profile
        :type profile_name: str
        :param profile_persona: Device persona(role) that the profile needs to perform in the scope
        :type profile_persona: str
        :param scope: The type of the element. Global, site_collection, and site are valid parameters for this argument
        :type scope: str
        :param scope_name: Name of the scope element. Either scope_name or scope_id is required
        :type scope_name: str
        :param scope_id: ID of the scope element. Either scope_name or scope_id is required
        :type scope_id: int

        :return: True if the specified operation(assign/unassign configuration profiles to scope) is successful, else False
        :rtype: bool
        """
        required_scope_element = self._find_scope_elements(
            names=scope_name, ids=scope_id, scope=scope
        )
        if operation == "assign":
            return assign_profile(
                obj=required_scope_element,
                profile_name=profile_name,
                profile_persona=profile_persona,
            )
        elif operation == "unassign":
            return unassign_profile(
                obj=required_scope_element,
                profile_name=profile_name,
                profile_persona=profile_persona,
            )

    def move_devices_between_sites(
        self,
        current_site,
        new_site,
        device_serial,
        device_type=None,
        device_identifier=None,
        deployment_mode=None,
    ):
        """
        This is a method that is used to move devices between sites.

        :param current_site: ID or name or Site instance of the the current site of the device
        :type current_site: int or str or class:`Site`
        :param new_site: ID or name or Site instance of the the site to which the device has to be moved
        :type new_site: int or str class:`Site`
        :param device_serial: Serial number of device that has to be moved
        :type device_serial: str
        :param device_type: Type of device that will be moved. For eg. AP, SWITCH, GATEWAY
        :type device_type: str, optional
        :param device_identifier: Name of the scope element. Either scope_name or scope_id is required
        :type device_identifier: str, optional
        :param deployment_mode: Deployment type of device. For eg. Standalone, Virtual Controller
        :type deployment_mode: str, optional

        :return: True if the device was successfully moved to the new site
        :rtype: bool
        """
        print("Moving devices between sites via NBAPI is not currently supported")
        return False
        # current_site_id = None
        # new_site_id = None
        # if current_site is None:
        #     raise ParameterError(
        #         "Missing required attribute current_site. Please provide the ID or name or instance of the current site."
        #     )
        # elif isinstance(current_site, Site):
        #     current_site_id = current_site.get_id()
        # elif isinstance(current_site, int):
        #     current_site_id = str(current_site)
        # elif isinstance(current_site, str):
        #     current_site = self.find_site(site_names=current_site)
        #     if current_site is None:
        #         raise ParameterError(
        #             "Unknown site name of current_site. Please provide the ID or name or instance of the current site."
        #         )
        #     current_site_id = current_site.get_id()

        # if new_site is None:
        #     raise ParameterError(
        #         "Missing required attribute new_site. Please provide the ID or name or instance of the new site."
        #     )
        # elif isinstance(new_site, Site):
        #     new_site_id = new_site.get_id()
        # elif isinstance(new_site, int):
        #     new_site_id = str(new_site)
        # elif isinstance(new_site, str):
        #     new_site_id = self.find_site(site_names=new_site)
        #     if new_site is None:
        #         raise ParameterError(
        #             "Unknown site name of new_site. Please provide the ID or name or instance of the new site."
        #         )
        #     new_site_id = new_site_id.get_id()

        # if device_serial is None:
        #     raise ParameterError(
        #         "Missing device_serial. Please provide the serial number of the device that has to be moved to a new site."
        #     )

        # if any(
        #     attribute is None
        #     for attribute in [device_type, device_identifier, deployment_mode]
        # ):
        #     device_found = False
        #     device_list = self.get_all_devices()
        #     for device in device_list:
        #         if device["scopeName"] == device_serial:
        #             device_type = device["deviceType"]
        #             # device_identifier = device[""]
        #             deployment_mode = device["deployment"]
        #             device_found = True

        #     if device_found is False:
        #         raise ParameterError(
        #             "Unable to find a device with provided serial number(device_serial). Please provide a valid serial number of a device"
        #         )


        # api_path = urls.fetch_url("SCOPES", "DEVICES")
        # api_method = "POST"
        # api_body = {
        #     "srcScopeId": current_site_id,
        #     "desScopeId": new_site_id,
        #     "deviceSerial": device_serial,
        #     "deviceType": device_type,
        #     "deviceIdentifier": device_identifier,
        #     "deployment": deployment_mode,
        # }

        # resp = self.central_conn.command(
        #     api_method=api_method, api_path=api_path, api_body=api_body
        # )

        # return resp