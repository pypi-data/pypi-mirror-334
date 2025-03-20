
import json
from typing import Dict, List
from caravel.baml.baml_client.async_client import b
# from src.caravel.baml.baml_client.types import
from caravel.baml.baml_client.type_builder import TypeBuilder
from caravel.parsing import Parser
import os
import dotenv
dotenv.load_dotenv()
from caravel.baml.baml_client import reset_baml_env_vars
reset_baml_env_vars(dict(os.environ))
from datetime import datetime

class BamlRunner:

    def __init__(self, parser: Parser):
        self.parser = parser
        
    async def make_path(self, path: str, user_input: str) -> str:
        '''
        Constructs the path, filling in path params.
        '''
        response = await b.MakePath(path, user_input)
        return response
    
    
    # async def extract_req_body_format(self, req_body_json: str, required_req: List[str]) -> RequestDataStorage:
    #     response = await b.ExtractReqBodyFormat(req_body_json, required_req)
    #     return response
     
    
    # async def extract_query_params_format(self, params: List[str], required: List[str]) -> RequestDataStorage:
    #     response = await b.ExtractQueryParamsFormat(
    #         params,
    #         required
    #     )
    #     return response
        
    
    # async def get_request_body(self, raw_json: str) -> RequestBody:
    #     response = await b.ExtractRequestBodySchema(raw_json)
    #     return response

    
    # async def make_api_request_body(self, schema: RequestBody, user_prompt: str) -> APIRequest:
    #     response = await b.CreateAPIRequestBody(schema, user_prompt)
    #     return response

    
    async def get_intent(self, intents: list[str], intent) -> str:
        response = await b.GetIntent(intents, intent)
        return response

    
    async def generate_human_language_response(self, response: str, context:str):
        try:
            response = await b.GenerateHumanLanguageResponse(response, context)
            return response
        except Exception:
            raise Exception("An error occured when calling GenerateHumanLanguageResponse.")
    
    async def populate_request_body(self, fmt: str, required: list[str], context: str, date:str=str(datetime.now())) -> str:
        
        # print(fmt)
        # print(required)
        # print(context)
        # print(date)
        
        try:
            response = await b.PopulateRequestBody(fmt, required, context, date)
            return response
        except Exception:
            raise Exception("BamlRunner.populate_request_body: There was an error trying to populate request body.")
        
    
    async def populate_query_parameters(self, query_param_fmt: Dict[str, str], context: str) -> Dict[str, str]:
        try:
            response = await b.PopulateQueryParameters(query_param_fmt, context)
            return response
        except Exception:
            raise Exception("BamlRunner.populate_query_parameters: an error occurred")

    # async def construct_api_request(self, intents: list[str], user_prompt: str) -> APIRequest:
    #     intent = await self.get_intent(intents=intents, intent=user_prompt)
    #     path = self.parser.path_map[intent]
    #     formatted_path = await self.make_path(path, user_prompt)
    #     method = intent.split(" ")[0]
        
    #     qp_fmt = self.parser.extract_query_param_defaults(path, method.lower())
    #     print(qp_fmt)
    #     if len(qp_fmt.keys()) == 0:
    #         qp_map = {}
    #     else:
    #         qp_fmt_flat = self.parser.flatten_query_params(qp_fmt)
    #         qp_map = await self.populate_query_parameters(qp_fmt_flat, user_prompt)
        
        
        
    #     if method.lower() not in ["post", "put", "patch"]:
    #         # create the API request now and return it
    #         return APIRequest(path=formatted_path, params=qp_map, method=method)
    #     else:
    #         rb_fmt, required = self.parser.extract_request_body(self.parser.openapi_spec, path, method.lower())
    #         rb_fmt = json.dumps(rb_fmt)
    #         rb_json_str = await self.populate_request_body(rb_fmt, required, user_prompt, str(datetime.now()))
            
    #         return APIRequest(path=formatted_path, params=qp_map, request_body=rb_json_str, method=method)
                        
            
    #         # create the request body, add to API request, and return it.
            
    async def construct_dynamic_api_request(self, intents: list[str], context: str):
        '''
        A Python wrapper for the ConstructDynamicAPIRequest baml function in Dynamic.baml. This will eventually replace self.construct_api_request.
        '''
        tb = TypeBuilder()
        intent = await self.get_intent(intents=intents, intent=context)
        path = self.parser.path_map[intent]
        formatted_path = await self.make_path(path, context)
        method = intent.split(" ")[0]
        
        qp_fmt = self.parser.extract_query_param_defaults(path, method.lower())
        if len(qp_fmt.keys()) == 0:
            qp_map = {}
        else:
            qp_fmt_flat = self.parser.flatten_query_params(qp_fmt)
            qp_map = await self.populate_query_parameters(qp_fmt_flat, context)
        
        # we should handle the edge case where get needs a request body
        
        json_schema = self.parser.openapi_spec.get("paths", {}).get(path, {}).get(method.lower(), {}).get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {})
        # print("this method: ", self.parser.openapi_spec.get("paths").get(path).get(method.lower()))
        print("this schema: ", self.parser.openapi_spec.get("paths").get(path).get(method.lower()).get("requestBody"))
        print("This application/json: ", self.parser.openapi_spec.get("paths").get(path).get(method.lower()).get("requestBody").get("content").get("application/json").get("schema"))
        
        print(json_schema)
        
        if json_schema == {}:
            print(f"{json_schema} == '{''}' ")
            rb_map = {}
        else:
            print("json_schema is not empty")
            rb_fmt = self.parser.parse_json_schema(json_schema=json_schema, tb=tb, spec=self.parser.openapi_spec) # does variable declaration need to happen here?
            print("rb_fmt ", rb_fmt)
            tb.DynamicObject.add_property("data", rb_fmt)
            rb_map_wrapper = await b.ExtractDynamicTypes(context, {"tb": tb})
            rb_map = rb_map_wrapper.data if hasattr(rb_map_wrapper, 'data') else {}
            
        # this will need to be passed into the dynamic rb creation function
        # required = self.parser.extract_request_body(self.parser.openapi_spec, path, method.lower())[1]
        
        
        api_request = await b.ConstructDynamicAPIRequest(formatted_path, method, qp_map, rb_map, {"tb":tb})
        
        return api_request
        
            

