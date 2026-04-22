import hashlib
import hmac
import time
import urllib.parse
import requests
import logging

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    """A client for the Binance Futures Testnet API."""
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        if testnet:
            self.base_url = "https://testnet.binancefuture.com"
        else:
            self.base_url = "https://fapi.binance.com"
        
        # Testnet usually uses a different sub-path than mainnet for fapi if required,
        # but https://testnet.binancefuture.com/fapi/v1/... is correct for testnet.
        logger.info(f"Initialized BinanceFuturesClient with base_url: {self.base_url}")

    def _generate_signature(self, query_string: str) -> str:
        """Generates an HMAC-SHA256 signature for the Binance API request."""
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def request(self, method: str, endpoint: str, signed: bool = False, params: dict = None) -> dict:
        """Sends an HTTP request to the Binance testnet API."""
        url = f"{self.base_url}{endpoint}"
        
        if params is None:
            params = {}
            
        params = {k: v for k, v in params.items() if v is not None}
            
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            query_string = urllib.parse.urlencode(params)
            signature = self._generate_signature(query_string)
            params['signature'] = signature

        headers = {
            'X-MBX-APIKEY': self.api_key
        }

        # Be careful not to log API keys or secrets
        log_params = params.copy()
        if 'signature' in log_params:
            log_params['signature'] = '***'
        
        logger.debug(f"API Request: {method} {url} Params: {log_params}")
        
        try:
            response = requests.request(method, url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"API Response: {response.status_code} {data}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Binance API Error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Error: {str(e)}")
            raise Exception(f"Network Error: {str(e)}")
        except ValueError:
            logger.error(f"Invalid JSON response: {response.text}")
            raise Exception("Invalid JSON response from Binance API")
