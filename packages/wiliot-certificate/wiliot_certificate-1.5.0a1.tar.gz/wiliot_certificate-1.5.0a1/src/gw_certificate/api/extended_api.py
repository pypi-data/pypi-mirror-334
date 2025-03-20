
from wiliot_api.edge.edge import EdgeClient


class ExtendedEdgeClient(EdgeClient):
    def __init__(self, api_key, owner_id, env='prod', region='us-east-2', cloud='',log_file=None, logger_=None):
        # Support for GCP
        region='us-central1' if cloud=='gcp' else region
        super().__init__(api_key=api_key, owner_id=owner_id, env=env, region=region, cloud=cloud, log_file=log_file, logger_=logger_)
                
    def kick_gw_from_mqtt(self, gw_id):
        path = f"gateway/{gw_id}/kick-mqtt-connection"
        response = self._post(path, None)
        return response
    
    def get_kong_logs(self, gw_id):
        """
        Only available under the certificate registration account
        """
        path = f"gateway/{gw_id}/auth-logs"

        return self._get(path)
        