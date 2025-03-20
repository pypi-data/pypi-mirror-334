# MIT License
#
# Copyright (c) 2020 Aruba, a Hewlett Packard Enterprise company
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def urlJoin(*args):
    """
    Util for joining additional path parameters onto the end of a URL. This
    function should not be used for query parameters. URL path should be the
    first arg followed by additional path parameters to join.

    :param *args: path parameter. First arg is the URL path followed by
        additional parameters.
    :type *args: str

    :return: Joined url with additional path parameters
    :rtype: str
    """
    trailing_slash = "/" if args[-1].endswith("/") else ""
    return (
        "/" + "/".join(map(lambda x: str(x).strip("/"), args)) + trailing_slash
    )

NETWORKING_PREFIX = "network-config/v1alpha1/"

class NewCentralURLs:
    Authentication = {
        "OAUTH": "https://sso.common.cloud.hpe.com/as/token.oauth2"
    }

    GLP = {"BaseURL": "https://global.api.greenlake.hpe.com"}

    GLP_DEVICES = {
        "GET": "/devices/v1beta1/devices",
        # full url requires {id} to be passed as param:
        # /devices/v1beta1/async-operations/{id}
        "GET_ASYNC": "/devices/v1beta1/async-operations/",
        "POST": "/devices/v1beta1/devices",
        "PATCH": "/devices/v1beta1/devices",
    }

    GLP_SUBSCRIPTION = {
        "GET": "/subscriptions/v1alpha1/subscriptions",
        # full url requires {id} to be passed as param:
        # /subscriptions/v1beta1/async-operations/{id}
        "GET_ASYNC": "/subscriptions/v1beta1/async-operations/",
        "POST": "/subscriptions/v1beta1/subscriptions",
    }

    GLP_USER_MANAGEMENT = {
        "GET": "/identity/v1/users",
        # full url requires {id} to be passed as param: /identity/v1/users/{id}
        "GET_USER": "/identity/v1/users/",
        "POST": "/identity/v1/users",
        # full url requires {id} to be passed as param: /identity/v1/users/{id}
        "PUT": "/identity/v1/users/",
        # full url requires {id} to be passed as param: /identity/v1/users/{id}
        "DELETE": "/identity/v1/users/",
    }

    SCOPES = {
        "SITE": "sites",
        "SITE_COLLECTION": "site-collections",
        "DEVICE": "devices",
        "DEVICE_GROUP": "device-collections",
        "ADD_SITE_TO_COLLECTION": "site-collection-add-sites",
        "REMOVE_SITE_FROM_COLLECTION": "site-collection-remove-sites",
        "HIERARCHY": "hierarchy",
        "SCOPE-MAPS": "scope-maps"
    }

    PROFILES = {
        "SYSTEM_INFO": "system-info",
        "vlan": "layer2-vlan",
        "wlan": "wlan-ssids",
        "ntp": "ntp"
    }
    
    def fetch_url(self, api_category, api_name, resource_name=None):
        api_url = NETWORKING_PREFIX
        if hasattr(self, api_category):
            api_category = getattr(self, api_category)
            if api_name in api_category:
                api_url += api_category[api_name]

                if resource_name:
                    api_url += "/" + resource_name

        return api_url