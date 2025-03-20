import pytest
from pycentral.module_helpers.scopes.site import Site
from pycentral.module_helpers.scopes.site_collection import Site_Collection
import json
from pycentral.base import ArubaCentralNewBase
import pprint
import pdb
# Pretty printing settings
pp = pprint.PrettyPrinter(indent=1)

# Global variables:

# Credentials:
central_info = {
    "aruba_central": {
        "base_url": "",
        "client_id": "",
        "client_secret": "",
        "access_token": ""
    },
    "glp": {
        "client_id": "<glp-client-id>",
        "client_secret": "<glp-client-secret>",
    },
    "classic_aruba_central": {
        "base_url": "<api-base-url>",
        "token": {
            "access_token": "<access-token>",
        }
    }
}

# Create an instance of ArubaCentralBase using API access token
# or API Gateway credentials.


vars = json.load(open("test_scopes_vars.json"))
connection = ArubaCentralNewBase(
    token_info=vars["credentials"], classic_auth=True)
scopes = connection.scopes


def test_get_scopes():
    func_vars = vars["test_get_scopes"]
    assert scopes.global_id == func_vars["global_id"]
    assert len(scopes.sites) == func_vars["sites"]
    assert len(scopes.site_collections) == func_vars["site_collections"]


def test_get_sites():
    func_vars = vars["test_get_sites"]
    resp = scopes.get_sites(
        size=func_vars["size"],
        offset=func_vars['offset']
    )
    assert resp['code'] == 200
    assert len(resp['msg']['site-info']
               ) == min(func_vars["size"], resp['msg']['total-count'])


def test_get_sites_sort_asc():
    func_vars = vars["test_get_sites_sort_asc"]
    resp = scopes.get_sites(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_by=func_vars['sort_by'],
        sort_direction=func_vars['sort_direction']
    )
    site_ids = [int(site[func_vars['sort_by']])
                for site in resp['msg']['site-info']]
    sorted_site_ids = sorted(site_ids)
    assert resp['code'] == 200
    assert len(resp['msg']['site-info']
               ) == min(func_vars["size"], resp['msg']['total-count'])
    assert site_ids == sorted_site_ids


def test_get_sites_sort_des():
    func_vars = vars["test_get_sites_sort_des"]
    resp = scopes.get_sites(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_by=func_vars['sort_by'],
        sort_direction=func_vars['sort_direction']
    )
    site_ids = [int(site[func_vars['sort_by']])
                for site in resp['msg']['site-info']]
    sorted_site_ids = sorted(site_ids, reverse=True)
    assert resp['code'] == 200
    assert len(resp['msg']['site-info']
               ) == min(func_vars["size"], resp['msg']['total-count'])
    assert site_ids == sorted_site_ids


def test_get_sites_sort_error_one():
    func_vars = vars["test_get_sites_sort_des"]
    resp = scopes.get_sites(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_by=func_vars['sort_by']
    )
    assert resp is None


def test_get_sites_sort_error_two():
    func_vars = vars["test_get_sites_sort_error"]
    resp = scopes.get_sites(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_direction=func_vars['sort_direction']
    )
    assert resp is None


def test_get_site_collections():
    func_vars = vars["test_get_site_collections"]
    resp = scopes.get_site_collections(
        size=func_vars["size"],
        offset=func_vars['offset']
    )
    assert resp['code'] == 200
    assert len(resp['msg']['site-collection-info']
               ) == min(func_vars["size"], resp['msg']['total-count'])


def test_get_site_collections_sort_asc():
    func_vars = vars["test_get_site_collections_sort_asc"]
    resp = scopes.get_site_collections(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_by=func_vars['sort_by'],
        sort_direction=func_vars['sort_direction']
    )
    collection_ids = [int(site[func_vars['sort_by']])
                      for site in resp['msg']['site-collection-info']]
    sorted_collection_ids = sorted(collection_ids)
    assert resp['code'] == 200
    assert len(resp['msg']['site-collection-info']
               ) == min(func_vars["size"], resp['msg']['total-count'])
    assert collection_ids == sorted_collection_ids


def test_get_site_collections_sort_des():
    func_vars = vars["test_get_site_collections_sort_des"]
    resp = scopes.get_site_collections(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_by=func_vars['sort_by'],
        sort_direction=func_vars['sort_direction']
    )
    collection_ids = [int(site[func_vars['sort_by']])
                      for site in resp['msg']['site-collection-info']]
    sorted_collection_ids = sorted(collection_ids, reverse=True)
    assert resp['code'] == 200
    assert len(resp['msg']['site-collection-info']
               ) == min(func_vars["size"], resp['msg']['total-count'])
    assert collection_ids == sorted_collection_ids


def test_get_site_collections_sort_error_one():
    func_vars = vars["test_get_site_collections_sort_error"]
    resp = scopes.get_site_collections(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_by=func_vars['sort_by']
    )
    assert resp is None


def test_get_site_collections_sort_error_two():
    func_vars = vars["test_get_site_collections_sort_error"]
    resp = scopes.get_site_collections(
        size=func_vars["size"],
        offset=func_vars['offset'],
        sort_direction=func_vars['sort_direction']
    )
    assert resp is None


def test_find_site_id():
    func_vars = vars["test_find_site"]
    site = scopes.find_site(site_ids=func_vars["site_id"])
    assert isinstance(site, Site)
    assert site.get_site_id() == func_vars["site_id"]
    assert site.get_site_name() == func_vars["site_name"]


def test_find_site_name():
    func_vars = vars["test_find_site"]
    site = scopes.find_site(site_names=func_vars["site_name"])
    assert isinstance(site, Site)
    assert site.get_site_id() == func_vars["site_id"]
    assert site.get_site_name() == func_vars["site_name"]


def test_find_sites_id():
    func_vars = vars["test_find_sites"]
    sites = scopes.find_site(
        site_ids=[func_vars["site_one_id"], func_vars["site_two_id"]])
    first_site = sites[0]
    second_site = sites[1]
    assert isinstance(first_site, Site)
    assert isinstance(second_site, Site)
    assert first_site.get_site_id() == func_vars["site_one_id"]
    assert first_site.get_site_name() == func_vars["site_one_name"]
    assert second_site.get_site_id() == func_vars["site_two_id"]
    assert second_site.get_site_name() == func_vars["site_two_name"]


def test_find_sites_name():
    func_vars = vars["test_find_sites"]
    sites = scopes.find_site(
        site_names=[func_vars["site_one_name"], func_vars["site_two_name"]])
    first_site = sites[0]
    second_site = sites[1]
    assert isinstance(first_site, Site)
    assert isinstance(second_site, Site)
    assert first_site.get_site_id() == func_vars["site_one_id"]
    assert first_site.get_site_name() == func_vars["site_one_name"]
    assert second_site.get_site_id() == func_vars["site_two_id"]
    assert second_site.get_site_name() == func_vars["site_two_name"]


def test_find_site_id_error():
    func_vars = vars["test_find_site_error"]
    site = scopes.find_site(site_ids=func_vars["site_one_id"])
    assert site is None


def test_find_site_name_error():
    func_vars = vars["test_find_site_error"]
    site = scopes.find_site(site_names=func_vars["site_one_name"])
    assert site is None


def test_find_sites_id_error():
    func_vars = vars["test_find_site_error"]
    sites = scopes.find_site(
        site_ids=[func_vars["site_one_id"], func_vars["site_two_id"]])
    first_site = sites[0]
    second_site = sites[1]
    assert first_site is None
    assert second_site is None


def test_find_sites_name_error():
    func_vars = vars["test_find_site_error"]
    sites = scopes.find_site(
        site_names=[func_vars["site_one_name"], func_vars["site_two_name"]])
    first_site = sites[0]
    second_site = sites[1]
    assert first_site is None
    assert second_site is None


def test_find_site_collection_id():
    func_vars = vars["test_find_site_collection"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    assert isinstance(site_collection, Site_Collection)
    assert site_collection.get_collection_id() == func_vars["collection_id"]
    assert site_collection.get_collection_name(
    ) == func_vars["collection_name"]


def test_find_site_collection_name():
    func_vars = vars["test_find_site_collection"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    assert isinstance(site_collection, Site_Collection)
    assert site_collection.get_collection_id() == func_vars["collection_id"]
    assert site_collection.get_collection_name(
    ) == func_vars["collection_name"]


def test_find_site_collections_id():
    func_vars = vars["test_find_site_collections"]
    site_collections = scopes.find_site_collection(
        site_collection_ids=[func_vars["collection_one_id"], func_vars["collection_two_id"]])
    first_collection = site_collections[0]
    second_collection = site_collections[1]
    assert isinstance(first_collection, Site_Collection)
    assert isinstance(second_collection, Site_Collection)
    assert first_collection.get_collection_id(
    ) == func_vars["collection_one_id"]
    assert first_collection.get_collection_name(
    ) == func_vars["collection_one_name"]
    assert second_collection.get_collection_id(
    ) == func_vars["collection_two_id"]
    assert second_collection.get_collection_name(
    ) == func_vars["collection_two_name"]


def test_find_site_collections_name():
    func_vars = vars["test_find_site_collections"]
    site_collections = scopes.find_site_collection(
        site_collection_names=[func_vars["collection_one_name"], func_vars["collection_two_name"]])
    first_collection = site_collections[0]
    second_collection = site_collections[1]
    assert isinstance(first_collection, Site_Collection)
    assert isinstance(second_collection, Site_Collection)
    assert first_collection.get_collection_id(
    ) == func_vars["collection_one_id"]
    assert first_collection.get_collection_name(
    ) == func_vars["collection_one_name"]
    assert second_collection.get_collection_id(
    ) == func_vars["collection_two_id"]
    assert second_collection.get_collection_name(
    ) == func_vars["collection_two_name"]


def test_find_site_collection_id_error():
    func_vars = vars["test_find_site_collection_error"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_one_id"])
    assert site_collection is None


def test_find_site_collection_name_error():
    func_vars = vars["test_find_site_collection_error"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_one_name"])
    assert site_collection is None


def test_find_site_collections_id_error():
    func_vars = vars["test_find_site_collection_error"]
    site_collections = scopes.find_site_collection(
        site_collection_ids=[func_vars["collection_one_id"], func_vars["collection_two_id"]])
    first_site_collection = site_collections[0]
    second_site_collection = site_collections[1]
    assert first_site_collection is None
    assert second_site_collection is None


def test_find_site_collections_name_error():
    func_vars = vars["test_find_site_collection_error"]
    collections = scopes.find_site_collection(
        site_collection_names=[func_vars["collection_one_name"], func_vars["collection_two_name"]])
    first_site_collection = collections[0]
    second_site_collection = collections[1]
    assert first_site_collection is None
    assert second_site_collection is None


def test_add_site_sc_id_site_id():
    func_vars = vars["test_add_site_sc_id_site_id"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_ids=func_vars["site_id"])
    site = scopes.find_site(site_ids=func_vars["site_id"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    assert func_vars["site_id"] in site_collection.sites
    assert site_collection.associated_sites == (old_associated_sites_num+1)
    assert site.site_collection_id == func_vars["collection_id"]
    assert resp is True


def test_add_site_sc_id_site_ids():
    func_vars = vars["test_add_site_sc_id_site_ids"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_ids=func_vars["site_ids"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    first_site = scopes.find_site(site_ids=func_vars["site_ids"][0])
    second_site = scopes.find_site(site_ids=func_vars["site_ids"][1])
    assert first_site.site_collection_id == func_vars["collection_id"]
    assert second_site.site_collection_id == func_vars["collection_id"]
    assert site_collection.associated_sites == (old_associated_sites_num+2)
    assert resp is True


def test_add_site_sc_id_site_name():
    func_vars = vars["test_add_site_sc_id_site_name"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_names=func_vars["site_name"])
    site = scopes.find_site(site_names=func_vars["site_name"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    assert site_collection.associated_sites == (old_associated_sites_num+1)
    assert site.site_collection_id == func_vars["collection_id"]
    assert resp is True


def test_add_site_sc_id_site_names():
    func_vars = vars["test_add_site_sc_id_site_names"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_names=func_vars["site_names"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    first_site = scopes.find_site(site_names=func_vars["site_names"][0])
    second_site = scopes.find_site(site_names=func_vars["site_names"][1])
    assert first_site.site_collection_id == func_vars["collection_id"]
    assert second_site.site_collection_id == func_vars["collection_id"]
    assert site_collection.associated_sites == (old_associated_sites_num+2)
    assert resp is True


def test_add_site_sc_name_site_id():
    func_vars = vars["test_add_site_sc_name_site_id"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_ids=func_vars["site_id"])
    site = scopes.find_site(site_ids=func_vars["site_id"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    assert func_vars["site_id"] in site_collection.sites
    assert site_collection.associated_sites == (old_associated_sites_num+1)
    assert site.site_collection_name == func_vars["collection_name"]
    assert resp is True


def test_add_site_sc_name_site_ids():
    func_vars = vars["test_add_site_sc_name_site_ids"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_ids=func_vars["site_ids"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    first_site = scopes.find_site(site_ids=func_vars["site_ids"][0])
    second_site = scopes.find_site(site_ids=func_vars["site_ids"][1])
    assert first_site.site_collection_name == func_vars["collection_name"]
    assert second_site.site_collection_name == func_vars["collection_name"]
    assert site_collection.associated_sites == (old_associated_sites_num+2)
    assert resp is True


def test_add_site_sc_name_site_name():
    func_vars = vars["test_add_site_sc_name_site_name"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_names=func_vars["site_name"])
    site = scopes.find_site(site_names=func_vars["site_name"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    assert site_collection.associated_sites == (old_associated_sites_num+1)
    assert site.site_collection_name == func_vars["collection_name"]
    assert resp is True


def test_add_site_sc_name_site_names():
    func_vars = vars["test_add_site_sc_name_site_names"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_names=func_vars["site_names"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    first_site = scopes.find_site(site_names=func_vars["site_names"][0])
    second_site = scopes.find_site(site_names=func_vars["site_names"][1])
    assert first_site.site_collection_name == func_vars["collection_name"]
    assert second_site.site_collection_name == func_vars["collection_name"]
    assert site_collection.associated_sites == (old_associated_sites_num+2)
    assert resp is True


def test_add_site_sc_already_associated_site():
    func_vars = vars["test_add_site_sc_already_associated_site"]
    new_site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["new_collection_name"])
    old_associated_sites_num = new_site_collection.associated_sites
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["new_collection_name"], site_names=func_vars["site_names"])
    old_collection_name = scopes.find_site_collection(
        site_collection_names=func_vars["old_collection_name"])
    new_site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["new_collection_name"])
    first_site = scopes.find_site(site_names=func_vars["site_names"][0])
    second_site = scopes.find_site(site_names=func_vars["site_names"][1])
    assert first_site.get_site_id() not in old_collection_name.sites
    assert second_site.get_site_id() not in old_collection_name.sites
    assert first_site.site_collection_name == func_vars["new_collection_name"]
    assert second_site.site_collection_name == func_vars["new_collection_name"]
    assert new_site_collection.associated_sites == (old_associated_sites_num+2)
    assert resp is True


def test_add_site_to_sc_id_site_id_error():
    func_vars = vars["test_add_site_sc_error"]
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_ids=func_vars["site_id"])
    assert resp is False


def test_add_site_to_sc_id_site_name_error():
    func_vars = vars["test_add_site_sc_error"]
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_names=func_vars["site_name"])
    assert resp is False


def test_add_site_to_sc_name_site_id_error():
    func_vars = vars["test_add_site_sc_error"]
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_ids=func_vars["site_id"])
    assert resp is False


def test_add_site_to_sc_name_site_name_error():
    func_vars = vars["test_add_site_sc_error"]
    resp = scopes.add_sites_to_collection(
        site_collection_id=func_vars["collection_id"], site_names=func_vars["site_name"])
    assert resp is False


def test_add_site_to_sc_name_site_names_error():
    func_vars = vars["test_add_site_sc_error"]
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_names=func_vars["site_names"])
    assert resp is False


def test_add_site_to_sc_name_site_ids_error():
    func_vars = vars["test_add_site_sc_error"]
    resp = scopes.add_sites_to_collection(
        site_collection_name=func_vars["collection_name"], site_ids=func_vars["site_ids"])
    assert resp is False


def test_remove_site_sc_id_site_id():
    func_vars = vars["test_remove_site_sc_id_site_id"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    pdb.set_trace()
    resp = scopes.remove_sites_from_site_collection(
        site_ids=func_vars["site_id"])
    site = scopes.find_site(site_ids=func_vars["site_id"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    assert func_vars["site_id"] not in site_collection.sites
    assert site_collection.associated_sites == (old_associated_sites_num-1)
    assert site.site_collection_id is None
    assert resp is True


def test_remove_site_sc_id_site_ids():
    func_vars = vars["test_remove_site_sc_id_site_ids"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_ids=func_vars["site_ids"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    first_site = scopes.find_site(site_ids=func_vars["site_ids"][0])
    second_site = scopes.find_site(site_ids=func_vars["site_ids"][1])
    assert first_site.site_collection_id is None
    assert second_site.site_collection_id is None
    assert site_collection.associated_sites == (old_associated_sites_num-2)
    assert resp is True


def test_remove_site_sc_id_site_name():
    func_vars = vars["test_remove_site_sc_id_site_name"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["site_name"])
    site = scopes.find_site(site_names=func_vars["site_name"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    assert site_collection.associated_sites == (old_associated_sites_num-1)
    assert site.site_collection_id is None
    assert resp is True


def test_remove_site_sc_id_site_names():
    func_vars = vars["test_add_site_sc_id_site_names"]
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["site_names"])
    site_collection = scopes.find_site_collection(
        site_collection_ids=func_vars["collection_id"])
    first_site = scopes.find_site(site_names=func_vars["site_names"][0])
    second_site = scopes.find_site(site_names=func_vars["site_names"][1])
    assert first_site.site_collection_id is None
    assert second_site.site_collection_id is None
    assert site_collection.associated_sites == (old_associated_sites_num-2)
    assert resp is True


def test_remove_site_sc_name_site_id():
    func_vars = vars["test_remove_site_sc_name_site_id"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_ids=func_vars["site_id"])
    site = scopes.find_site(site_ids=func_vars["site_id"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    assert func_vars["site_id"] not in site_collection.sites
    assert site_collection.associated_sites == (old_associated_sites_num-1)
    assert site.site_collection_name is None
    assert resp is True


def test_remove_site_sc_name_site_ids():
    func_vars = vars["test_remove_site_sc_name_site_ids"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_ids=func_vars["site_ids"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    first_site = scopes.find_site(site_ids=func_vars["site_ids"][0])
    second_site = scopes.find_site(site_ids=func_vars["site_ids"][1])
    assert first_site.site_collection_name is None
    assert second_site.site_collection_name is None
    assert site_collection.associated_sites == (old_associated_sites_num-2)
    assert resp is True


def test_remove_site_sc_name_site_name():
    func_vars = vars["test_remove_site_sc_name_site_name"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["site_name"])
    site = scopes.find_site(site_names=func_vars["site_name"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    assert site_collection.associated_sites == (old_associated_sites_num-1)
    assert site.site_collection_name is None
    assert resp is True


def test_remove_site_sc_name_site_names():
    func_vars = vars["test_remove_site_sc_name_site_names"]
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    old_associated_sites_num = site_collection.associated_sites
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["site_names"])
    site_collection = scopes.find_site_collection(
        site_collection_names=func_vars["collection_name"])
    first_site = scopes.find_site(site_names=func_vars["site_names"][0])
    second_site = scopes.find_site(site_names=func_vars["site_names"][1])
    assert first_site.site_collection_name is None
    assert second_site.site_collection_name is None
    assert site_collection.associated_sites == (old_associated_sites_num-2)
    assert resp is True


def test_remove_unassociated_site():
    func_vars = vars["test_remove_site_sc_error"]
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["unassociated_site"])
    assert resp is False


def test_remove_site_id_error():
    func_vars = vars["test_remove_site_sc_error"]
    resp = scopes.remove_sites_from_site_collection(
        site_ids=func_vars["site_id"])
    assert resp is False


def test_remove_site_ids_error():
    func_vars = vars["test_remove_site_sc_error"]
    resp = scopes.remove_sites_from_site_collection(
        site_ids=func_vars["site_id"])
    assert resp is False


def test_remove_site_name_error():
    func_vars = vars["test_remove_site_sc_error"]
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["site_name"])
    assert resp is False


def test_remove_site_names_error():
    func_vars = vars["test_remove_site_sc_error"]
    resp = scopes.remove_sites_from_site_collection(
        site_names=func_vars["site_names"])
    assert resp is False


if __name__ == "__main__":
    pytest.main()
