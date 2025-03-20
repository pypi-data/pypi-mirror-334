from pycentral.url_utils import NewCentralURLs

urls = NewCentralURLs()

class ServiceManager(object):
    def get_application_id(self, conn, application_name):
        """get service managers in glp workspace"""
        resp = self.get_service_managers(conn)

        for s in resp['msg']['items']:
            if s['name'] == application_name:
                application = (s['id'])
                exit

        if application != "":
            print("Successfully retrieved application id")
            return application
        else:
            print("Failed to retrieve application id for central application")
            exit

    def get_service_managers(self, conn, limit=2000, offset=0):
        conn.logger.info("Getting service managers in GLP workspace")
        """
        Retrieve all service managers in the workspace.

        :param limit: Specify the maximum number of entries per page. NOTE: The maximum value accepted is 2000.
        :type limit: integer (Pagination limit) [ 1 .. 2000 ]
        :param offset: Specify pagination offset. An offset argument defines how many pages to skip before returning results.
        :type offset: integer (Pagination offset) >= 0
        :return: API response
        :rtype: dict
        """
        path = urls.GLP_SERVICE_MANAGER["GET"]

        params = {
            "limit": limit,
            "offset": offset,
        }

        resp = conn.command(
            api_method="GET", api_path=path, api_params=params, app_name="glp"
        )
        return resp