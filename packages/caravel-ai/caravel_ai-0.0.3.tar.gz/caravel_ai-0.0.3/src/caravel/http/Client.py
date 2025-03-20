from typing import Callable, Dict, List, Optional
from caravel.baml.baml_client.types import DynamicAPIRequest
from caravel.utils.utils import remove_nulls
import json
import httpx

class Client:
    def __init__(self, name: str, base_url: str, auth_headers: Optional[dict]=None, auth_query_params: Optional[dict]=None, allowed_methods:List[str]=["get", "post"], restricted_routes: List[str]=[]):
        self.name = name
        self.base_url=base_url
        self.auth_headers=auth_headers
        self.auth_query_params=auth_query_params
        self.allowed_methods=allowed_methods 
        self.restricted_routes=restricted_routes
        self.functions: Dict[str, Callable] = {} # allows users to add util functions.

    def set_auth_headers(self, auth_headers:dict={}):
        self.auth_headers = auth_headers

    def set_auth_query_params(self, auth_query_params:dict):
        self.auth_query_params = auth_query_params

    def get_auth_headers(self):
        return self.auth_headers
    
    def get_base_url(self):
        return self.base_url
    
    async def make(self, api_request: DynamicAPIRequest):
        '''
        Returns the API request's response after routing the DynamicAPIRequest to the proper method. 
        ''' 
        # print("Client.make invoked")
        if self.auth_query_params is not None:
            api_request.params = {**api_request.params, **self.auth_query_params}
        
        match api_request.method: # need to add error handling here.
            case 'GET':
                # print("Inside GET control flow.")
                if "get" not in self.allowed_methods:
                    return "I am unable to make get requests."
                response = await self.get(api_request)
                # print(f"Client.make response: {response}")
                return str(response)
            case 'POST':
                if "post" not in self.allowed_methods:
                    return "I am unable to make post requests."
                response = await self.post(api_request)
                return response
            case 'PUT':
                if "put" not in self.allowed_methods:
                    return "I am unable to make put requests."
                response = await self.put(api_request)
                return response
            case 'PATCH':
                if "patch" not in self.allowed_methods:
                    return "I am unable to make patch requests."
                response = await self.patch(api_request)
                return response
            case 'DELETE':
                if "delete" not in self.allowed_methods:
                    return "I am unable to make delete requests."
                response = await self.delete(api_request)
                return response
            case _:
                raise Exception("The specified method is not allowed.")
    
    async def post(self, api_request: DynamicAPIRequest):    
        
        route, params, jsn = api_request.path, api_request.params, api_request.request_body.data
        
        if len(jsn.keys()) > 0:
            jsn = {key: val for key, val in jsn.items() if val is not None}
        
        print("INSIDE POST: ", jsn)
        print(type(jsn))

        if "post" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
        
        # jsn = json.loads(jsn.dict()) if jsn is not None else {}
        jsn = remove_nulls(jsn)
        print("The cleansed jsn", jsn)
        if params and len(params.keys()) > 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params,
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        
        elif params is None and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        elif params is None and len(jsn.keys()) == 0:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                )
                response.raise_for_status()
                return response.json()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params
                )
                response.raise_for_status()
                return response.json()
    
    

    async def patch(self, api_request: DynamicAPIRequest):
        
        route, params, jsn = api_request.path, api_request.params, api_request.request_body
        
        if "patch" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
        
        jsn = json.loads(jsn) if jsn is not None else {}
    
        if len(params.keys()) > 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params,
                    json=jsn,
                )
                response.raise_for_status()
                return str(response.json())
        
        elif len(params.keys()) == 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        elif len(params.keys()) == 0 and len(jsn.keys()) == 0:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                )
                response.raise_for_status()
                return str(response.json())
        else:
            async with httpx.AsyncClient() as client:
                response = await client.patch(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params
                )
                response.raise_for_status()
                return response.json()

    async def put(self, api_request: DynamicAPIRequest):
        
        route, params, jsn = api_request.path, api_request.params, api_request.request_body
        
        if "patch" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
        
        jsn = json.loads(jsn) if jsn is not None else {}
    
        if len(params.keys()) > 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params,
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        
        elif len(params.keys()) == 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        elif len(params.keys()) == 0 and len(jsn.keys()) == 0:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                )
                response.raise_for_status()
                return response.json()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params
                )
                response.raise_for_status()
                return response.json()
    
    async def get(self, api_request: DynamicAPIRequest):
        # print("Inside of Client.get")
        try:
            route, params, jsn = api_request.path, api_request.params, api_request.request_body
        except Exception as e:
            print(e)
        
        if "get" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
    
        jsn = json.loads(jsn) if jsn is not None else {}

        # print("Making request.")
        # print("route: ", route)
        # print("params: ", params)
        # print("jsn: ", jsn)
        
        if len(params.keys()) > 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params,
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        
        elif len(params.keys()) == 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        elif len(params.keys()) == 0 and len(jsn.keys()) == 0:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                )
                response.raise_for_status()
                return response.json()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params
                )
                response.raise_for_status()
                print(response)
                return response.json()
    
    
    async def delete(self, api_request: DynamicAPIRequest):
        
        route, params, jsn = api_request.path, api_request.params, api_request.request_body
        
        if "patch" not in self.allowed_methods:
            return
        if route in self.restricted_routes:
            return
    
        jsn = json.loads(jsn) if jsn is not None else {}
    
        if len(params.keys()) > 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params,
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        
        elif len(params.keys()) == 0 and len(jsn.keys()) > 0:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    json=jsn,
                )
                response.raise_for_status()
                return response.json()
        elif len(params.keys()) == 0 and len(jsn.keys()) == 0:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                )
                response.raise_for_status()
                return response.json()
        else:
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    url=f"{self.base_url}{route}",
                    headers=self.get_auth_headers(),
                    params=params
                )
                response.raise_for_status()
                return response.json()
             
    