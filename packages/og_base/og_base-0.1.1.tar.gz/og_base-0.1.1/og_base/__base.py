import logging
import requests


class RestClient():
    def __init__(self, base_url=None, headers=None, auth_token=None, timeout=10, debug=False):

        self.base_url = base_url.rstrip('/') if base_url else None
        self.session = requests.Session()
        self.session.headers.update(headers or {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })

        if auth_token:
            self.session.headers.update({'Authorization': f'Bearer {auth_token}'})
        self.timeout = timeout

        self.logger = logging.getLogger(__name__)
        log_level = logging.DEBUG if debug else logging.WARNING
        logging.basicConfig(level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger.debug(f'Initialised REST Client with base URL: {self.base_url}')

    def _request(self, method, endpoint, **kwargs):
        url = f'{self.base_url}/{endpoint.lstrip("/")}'
        logging.debug(f'Making {method.upper()} request to {url} with kwargs: {kwargs}')

        try:
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()

            logging.debug(f'Response Status: {response.status_code}')
            if response.content:
                return response.json()

        except requests.exceptions.HTTPError:
            error_details = None
            try:
                error_details = response.json()
            except ValueError:
                error_details = response.text

            msg = f'HTTPError {response.status_code} for {method} {url}: {error_details}'
            self.logger.error(msg)
            raise requests.exceptions.HTTPError(msg)

        except requests.exceptions.Timeout:
            self.logger.error(f'Request timed out: {method} {url}')
            raise requests.exceptions.Timeout(f'Request timed out: {method} {url}')

        except requests.exceptions.ConnectionError as e:
            self.logger.error(f'Connection error: {method} {url} - {e}')
            raise requests.exceptions.ConnectionError(str(e))

        except requests.exceptions.RequestException as e:
            self.logger.error(f'Unexpected error: {method} {url} - {e}')
            raise requests.exceptions.RequestException(str(e))

    def get(self, endpoint, params=None):
        """Perform a GET request"""
        return self._request('GET', endpoint, params=params)

    def post(self, endpoint, json=None, files=None):
        """Perform a POST request"""
        return self._request('POST', endpoint, json=json, files=files)

    def put(self, endpoint, json=None):
        """Perform a PUT request"""
        return self._request('PUT', endpoint, json=json)

    def delete(self, endpoint):
        """Perform a DELETE request"""
        return self._request('DELETE', endpoint)

    def patch(self, endpoint, json=None):
        """Perform a PATCH request"""
        return self._request('PATCH', endpoint, json=json)

    def set_auth_token(self, auth_token):
        """Set the Authorization token"""
        self.session.headers.update({'Authorization': f'Bearer {auth_token}'})
        self.logger.debug('Updated Authorization token')

    def set_api_key(self, api_key, header='X-Api-Key'):
        """Set the API key"""
        self.session.headers.update({header: api_key})
        self.logger.debug('Updated API key')

    def close(self):
        """Close the session"""
        self.session.close()
        self.logger.debug('Closed the session')
