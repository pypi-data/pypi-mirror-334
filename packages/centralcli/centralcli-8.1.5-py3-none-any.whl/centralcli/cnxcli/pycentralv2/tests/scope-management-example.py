import json
from pycentral.base import ArubaCentralNewBase
import pdb

new_creds = {
    "glp": {
        'access_token': '<access-token-generated-from-GLP>'
    },
    "aruba_central": {
        "client_id": "<central-client-id-from-glp>",
        "client_secret": "<central-client-secret-from-glp>"
    },
    "classic_aruba_central": {
        "base_url": "<api-base-url>",
        "token": {
            "access_token": "<api-access-token>",
        }
    }
}


def main():
    central_conn = ArubaCentralNewBase(
        token_info=new_creds, classic_auth=True)
    scopes = central_conn.scopes
    workflow_variables = json.load(open("scope-management-vars.json"))
    site_data = workflow_variables["sites"]
    collection_data = workflow_variables["collections"]

    # Creating sites
    for site in site_data:
        scopes.create_site(site_attributes=site)

    # Creating site collection
    for collection_attributes in collection_data:
        scopes.create_site_collection(
            collection_attributes=collection_attributes)

    # Associating sites to collection
    single_collection_id_site_id(scopes)
    single_collection_id_site_ids(scopes)
    single_collection_id_site_name(scopes)
    single_collection_id_site_names(scopes)
    single_collection_name_site_id(scopes)
    single_collection_name_site_ids(scopes)
    single_collection_name_site_name(scopes)
    single_collection_name_site_names(scopes)

    single_collection_id_error_site_name(scopes)
    single_collection_id_error_site_id(scopes)
    single_collection_id_error_site_names(scopes)
    single_collection_id_error_site_ids(scopes)
    single_collection_name_error_site_name(scopes)
    single_collection_name_error_site_id(scopes)
    single_collection_name_error_site_names(scopes)
    single_collection_name_error_site_ids(scopes)

    change_single_collection_id_site_id(scopes)
    change_single_collection_id_site_ids(scopes)


def change_single_collection_id_site_id(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="api-collection-1", site_ids=231171729)
    assert resp is True


def change_single_collection_id_site_ids(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=237172016, site_ids=[243176269, 235180332])
    assert resp is True


def single_collection_id_site_id(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_ids=243148079)
    assert resp is True


def single_collection_id_site_ids(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_ids=[243176269, 231171729])
    assert resp is True


def single_collection_id_site_name(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_names='api-site-2')
    assert resp is True


def single_collection_id_site_names(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_names=['api-site-2', 'api-site-3'])
    assert resp is True


def single_collection_id_error_site_name(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_names='api-site-kk')
    assert resp is False


def single_collection_id_error_site_id(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_ids=243162600)
    assert resp is False


def single_collection_id_error_site_names(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_names=['api-site-kk', 'api-site-kk-2'])
    assert resp is False


def single_collection_id_error_site_ids(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_id=239163653, site_ids=[243162600, 243162601])
    assert resp is False


def single_collection_name_site_id(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="Ti-West-Region", site_ids=243148079)
    assert resp is True


def single_collection_name_site_ids(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="Ti-West-Region", site_ids=[243176269, 231171729])
    assert resp is True


def single_collection_name_site_name(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="Ti-West-Region", site_names='api-site-1')
    assert resp is True


def single_collection_name_site_names(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="Ti-West-Region", site_names=['api-site-2', 'api-site-3'])
    assert resp is True


def single_collection_name_error_site_name(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="error-name", site_names='api-site-2')
    assert resp is False


def single_collection_name_error_site_id(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="error-name", site_ids=243148079)
    assert resp is False


def single_collection_name_error_site_names(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="error-name", site_names=['api-site-2', 'api-site-3'])
    assert resp is False


def single_collection_name_error_site_ids(scopes):
    resp = scopes.add_sites_to_collection(
        site_collection_name="error-name", site_ids=[243162600, 243162601])
    assert resp is False


if __name__ == "__main__":
    main()
