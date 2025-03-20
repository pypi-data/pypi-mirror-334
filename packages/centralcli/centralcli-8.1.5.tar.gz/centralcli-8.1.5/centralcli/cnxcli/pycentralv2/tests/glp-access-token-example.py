from pycentral.base import ArubaCentralNewBase
import pdb

new_creds = {
    "glp": {"access_token": "<access-token-generated-from-GLP>"},
    "aruba_central": {
        "client_id": "<central-client-id-from-glp>",
        "client_secret": "<central-client-secret-from-glp>",
    },
}

central_conn = ArubaCentralNewBase(token_info=new_creds)
# Making GLP API call with Command
resp = central_conn.command(
    api_method="GET", api_path="devices/v1beta1/devices", app_name="glp"
)

# The below call will not work since CNX doesn't support CNX Access tokens
# resp = central_conn.command(api_method="GET", api_path="<CNX-API-PATH>")
