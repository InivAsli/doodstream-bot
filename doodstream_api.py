import requests
from config import config

class DoodStreamAPI:
    def __init__(self):
        self.api_key = config.DOODSTREAM_API_KEY
        self.base_url = config.DOODSTREAM_BASE_URL
    
    def _make_request(self, endpoint, params=None):
        if params is None:
            params = {}
        
        params['key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = requests.get(url, params=params, timeout=30)
            return response.json()
        except Exception as e:
            return {"error": str(e), "status": "error"}
    
    def get_account_info(self):
        return self._make_request("account/info")
    
    def get_account_stats(self):
        return self._make_request("account/stats")
    
    def list_files(self, page=1):
        params = {'page': page, 'per_page': config.ITEMS_PER_PAGE}
        return self._make_request("files/list", params)
    
    def upload_from_url(self, url):
        params = {'url': url}
        response = requests.post(
            f"{self.base_url}/upload/url",
            data=params,
            timeout=60
        )
        return response.json()

dood_api = DoodStreamAPI()
