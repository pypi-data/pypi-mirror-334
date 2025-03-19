#  Copyright (c) 2020. WebShotApi All right reserved
from gawsoft.api_client import Request, Response

from .client_exception import WebshotapiClientError
from .types import ScreenshotJsonResponse, ExtractResponse
from .version import __version__
import os

class Client(Request):
    """
    Client for webshotapi server
    """

    def __init__(
        self,
        api_key: str = "",
        api_version: str ='v1',
        api_host: str = '',
        user_agent: str = f"Webshotapi Python client {__version__}"
     ):
        if (not api_key or len(api_key)==0) and 'WEBSHOTAPI_API_KEY' in os.environ:
            api_key = os.environ['WEBSHOTAPI_API_KEY']

        if (not api_host or len(api_host)==0) and 'WEBSHOTAPI_ENDPOINT' in os.environ:
            api_host = os.environ['WEBSHOTAPI_ENDPOINT']
        elif api_host:
            pass
        else:
            api_host = "https://api.webshotapi.com"

        super().__init__(api_key, api_version, api_host, user_agent)

    def screenshot(self, url:str, params:dict) -> Response:
       '''
           Take screenshot and return image

           :param url:
                link to website to take screenshot
           :param params:
                dict with parameters check available parameters in https://webshotapi.com/docs/rest/
           :return:
                Response object
        Example:
            >>> client = Client()
            >>> client.screenshot("https://example.com", {
                "image_type": "webp"
            })

       '''

       params['url'] = url
       return self.request(f'/screenshot/image','POST', params)


    def screenshot_json(self, url: str, params: dict) -> ScreenshotJsonResponse:
        '''
        Take screenshot and return url to image

        :param url:
             link to website to take screenshot
        :param params:
             dict with parameters check available parameters in https://webshotapi.com/docs/rest/
        :return:
             Response object
        '''

        params['url'] = url
        response = self.request(f'/screenshot/json', 'POST', params)
        if response.status_code != 200:
            raise WebshotapiClientError(f"Response return status code: {response.status_code}")

        parsed_data = response.data()

        return ScreenshotJsonResponse(
            url = parsed_data['url'],
            expire_sec = parsed_data['expire_sec']
        )

    def pdf(self, url:str, params:dict) -> Response:
        '''
        Take screenshot and return pdf file

        :param url:
            link to website to take screenshot
        :param params:
            dict with parameters check available parameters in https://webshotapi.com/docs/rest/
        :return:
            Response object
        '''

        params['url'] = url
        params['image_type'] = 'pdf'
        return self.request('/screenshot/image','POST', params)

    def extract(self,url:str, params:dict) -> ExtractResponse:
        """
        Extract html selectors with css styles, words with coordinates(x,y,width,height).
        You can also extract html of rendered page and clean text

        @param url: url
            link to website to take screenshot
        @param params: dict with params
            dict with parameters check available parameters in https://webshotapi.com/docs/rest/

        @return: ExtractResponse
        """
        params['url'] = url
        response = self.request('/extract', 'POST', params)
        if response.status_code != 200:
            raise WebshotapiClientError(f"Response return status code: {response.status_code}")

        parsed_data = response.data()

        return ExtractResponse(
            status_code=parsed_data["status_code"],
            html=parsed_data["html"],
            text=parsed_data["text"],
            elements=parsed_data["elements"],
            words=parsed_data["words"],
            page_properties=parsed_data["page_properties"],
            saved_in_cloud=parsed_data["saved_in_cloud"]
        )

