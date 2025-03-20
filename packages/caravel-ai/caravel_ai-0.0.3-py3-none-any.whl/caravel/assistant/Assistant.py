
from typing import Any, Dict, List, Optional
from caravel.baml.baml_client.async_client import b
from caravel.baml.baml_client.type_builder import TypeBuilder
from baml_py.errors import BamlError, BamlInvalidArgumentError, BamlClientError, BamlClientHttpError, BamlValidationError
from caravel.baml.baml_client.types import Context, DynamicAPIRequest, Message, Role, State
from caravel.http.Client import Client
from caravel.parsing.Parser import Parser

class Assistant:
    
    '''
    A class implementing the ability to make function calls.
    '''
    def __init__(self, system_prompt:str, limit:int, spec_file: str, client:Client, debug:bool=False) -> None:
        # context management
        self.context = Context(state='INITIAL', limit=limit if limit > 1 else ValueError("Limit must be greater than 1"), messages=[])
        # self.context.state = 'INITIAL'
        # self.context.limit = limit if limit > 1 else ValueError("Limit must be greater than 1")
        # self.context.messages = []
        self._add_message(
            Message(role='SYSTEM', context_state='INITIAL', content=system_prompt)
        )
        self.client = client
        self.parser = Parser(file=spec_file)
        self.tb = TypeBuilder()
        self.debug = debug
        
    # def __init__(self, context:Optional[Context]=None, client:Optional[Client]=None, spec_file: Optional[str]=None) -> None:
    #     '''
    #     Constructor for the Assistant Class.
    #     '''
    #     self.context = None
    #     self.client = None
    #     self.parser = None
    #     self.tb = TypeBuilder() # a reusable typebuilder.
    #     if spec_file is not None:
    #         self.Parser = Parser(spec_file)
    #     if context is not None:
    #         self.context = context 
    #         if context.limit <= 1:
    #             raise ValueError("Assistant Context message limits must be greater than 1.")
    #     if client is not None:
    #         self.client = client    
            
    def reset_type_builder(self) -> None:
        '''
        Resets the Assistant's TypeBuilder to an empty TypeBuilder instance to allow for reuse.
        '''
        self.tb = TypeBuilder
    
    def update_context(self,
                       state:Optional[State],
                       messages:Optional[List[Message]],
                       limit: Optional[int] = None
                       ) -> None:
        '''
        Updates the attributes of the context attribute.
        '''
        self.context.state = state if state is not None else self.context.state
        self.context.messages = messages if messages is not None else self.context.messages
        self.context.limit = limit if limit is not None else self.context.limit
    
    
    def _add_message(self, message: Message) -> None:
        '''
        Adds a Message to the Message List in the Context attribute.
        '''
        if len(self.context.messages) >= self.context.limit:
            self.context.messages.pop(1)
        
        self.context.messages.append(message)
        
    def add_message(self, role: Role, content: str, context_state:State='INITIAL') -> None:
        '''
        A user-friendly function call that prevents the need for importing the Message class.
        '''
        self._add_message(
            Message(role=role, context_state=context_state, content=content)
        )

    
    def update_state(self, state: State) -> None:
        '''
        Changes the State of the Assistant's Context attribute.
        '''
        self.context.state = state
    
    def update_client(self,
                        name:Optional[str]=None,
                        base_url:Optional[str]=None,
                        auth_headers:Optional[dict]=None,
                        auth_query_params:Optional[dict]=None,
                        allowed_methods:List[str]=None,
                        restricted_routes:List[str]=None,
                    ) -> None:
        '''
        Updates the Client attribute of the Assistant.
        '''
        if name is not None:
            self.client.name = name
        if base_url is not None:
            self.client.base_url = base_url
        if auth_headers is not None:
            self.client.auth_headers = auth_headers
        if auth_query_params is not None:
            self.client.auth_query_params = auth_query_params
        if allowed_methods is not None:
            self.client.allowed_methods = allowed_methods
        if restricted_routes is not None:
            self.client.restricted_routes = restricted_routes
    
    def state(self) -> State:
        '''
        Returns the State of the Assistant's Context attribute.
        '''
        return self.context.state
    
    def messages(self) -> List[Message]:
        '''
        Returns the Message List of the Assistant's Context attribute.
        '''
        return self.context.messages 
    
    def poll_messages(self) -> Message:
        '''
        Returns the most previous Message appended to the Message list.
        '''
        if len(self.context.messages) == 0:
            raise ValueError("Cannot poll empty Message list.")
        else: 
            return self.context.messages[-1]
            
    async def assistant_call(self) -> None:
        '''
        Performs the function calling based on the information provided in the Context attribute.
        
        The State of the Context attribute should always be 'AWAITING_USER' when this function is invoked.
        '''
        while True:
            # print("You are inside of the assistant call loop.")
            
            if self.state() == 'INITIAL':
                # estimate the state based on the context
                # update the state
                state_estimate = await b.EstimateState(self.context.messages)
                self.update_state(state_estimate)    
                continue
            elif self.state() == 'MAKE_REQUEST':
                # get the structured request using the tb parser.
                # call the function to construct it
                # call the function to place it
                # add the response to messages, change state to NATURALLANGUAGE               
                # reset tb to TypeBuilder()
                # print("Inside MAKE_REQUEST control flow")
                api_request = await self.construct_api_request()
                # print("API Request awaited, calling the function.")
                response = await self.client.make(api_request)
                # print("response got.")
                # print(f"API RESPONSE: {response}")
                self._add_message(
                    Message(
                        role='BOT',
                        context_state=self.state(),
                        content=response
                    )
                )
                self.tb = TypeBuilder()
                self.update_state('NATURAL_LANGUAGE')
                continue
            elif self.state() == 'EXPLAIN_REQUEST':
                # print("Inside EXPLAIN_REQUEST control flow")
                # explain the request
                # get the structured request using the tb parser
                # add description to messages, set state to NATURALLANGUAGE.
                # self.
                api_request: DynamicAPIRequest = await self.construct_api_request()
                rb_map = api_request.request_body
                if rb_map is None:
                    self._add_message(
                        Message(
                            role='TOOL',
                            context_state=self.state(),
                            content=str(api_request)
                        )
                    )
                else:
                    self._add_message(
                        Message(
                            role='TOOL',
                            context_state=self.state(),
                            content=str(rb_map)
                        )
                    )
                self.update_state('NATURAL_LANGUAGE')
                self.tb = TypeBuilder()
                continue
            
            elif self.state() == 'NATURAL_LANGUAGE':
                # pass context to GenerateNaturalLanguage fn
                # append result to messages, set state to AWAITING_USER
                natural_lang_response = await self.generate_natural_language()
                self._add_message(
                    Message(
                        role='BOT',
                        context_state=self.state(),
                        content=natural_lang_response
                    )
                )
                self.update_state('AWAITING_USER')
                continue
            elif self.state() == 'AWAITING_USER':
                self.context.state = await b.EstimateState(self.context.messages)
                break
            # consider a VERIFY_REQUEST state here to allow for better HIL functionality.
        
    ###
    ### The functions below call baml functions. Functions that begin with 
    ### `generate` simply wrap BAML functions. Functions that begin with 
    ### `construct` do at least one of the following:
    ### 1 - wrap multiple BAML fns
    ### 2 - perform some sort of internal computation prior to or following the  ### BAML call.
    ### 
    
    async def generate_path(self, path: str) -> str:
        '''
        Generates a path using the Assistant's Context and the path found in the Assistant's Parser's path map.
        '''
        try:
            response = await b.GeneratePath(path, self.context)
            return response
        except BamlInvalidArgumentError as biae:
            print(biae)
        except BamlClientHttpError as bche:
            print(bche)
        except BamlValidationError as bve:
            print(bve)
        except BamlClientError as bce:
            print(bce)
        except Exception:
            raise Exception("An error occured trying to generate the path. This does not appear to be an error with BAML.")
    
    async def generate_intent(self) -> str:
        try:
            response = await b.GenerateIntent(list(self.parser.path_map.keys()), self.context)
            return response
        except BamlInvalidArgumentError as biae:
            print(biae)
        except BamlClientHttpError as bche:
            print(bche)
        except BamlValidationError as bve:
            print(bve)
        except BamlClientError as bce:
            print(bce)
        except Exception:
            raise Exception("An error occured trying to generate the path. This does not appear to be an error with BAML.")
    
    async def generate_natural_language(self) -> str:
        try:
            response = await b.GenerateNaturalLanguageResponse(self.context)
            return response
        except BamlInvalidArgumentError as biae:
            print(biae)
        except BamlClientHttpError as bche:
            print(bche)
        except BamlValidationError as bve:
            print(bve)
        except BamlClientError as bce:
            print(bce)
        except Exception:
            raise Exception("An error occured trying to generate the natural language response. This does not appear to be an error with BAML.")
        
    async def generate_query_parameters(self, query_param_fmt: Dict[str, str]) -> Dict[str, str]:
        '''
        Generates the query parameters. 
        '''
        try:
            response = await b.GenerateQueryParameters(query_param_fmt, self.context)
            return response
        except Exception:
            raise Exception("Issue trying to generate query parameters.")
        
    async def construct_api_request(self) -> DynamicAPIRequest: # could exception handling be done more gracefully here?
        intent = await self.generate_intent()
        path = self.parser.path_map[intent]
        formatted_path = await self.generate_path(path)
        method = intent.split(" ")[0]
        
        qp_fmt = self.parser.extract_query_param_defaults(path, method.lower())
        if qp_fmt is None:
            qp_map = {}
        else:
            qp_fmt_flat = self.parser.flatten_query_params(qp_fmt)
            qp_map = await self.generate_query_parameters(qp_fmt_flat)
        
        json_schema = (
            self.parser.openapi_spec
                .get("paths", {}).get(path, {})
                .get(method.lower(), {})
                .get("requestBody", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema", {})
        )

        if json_schema == {}:
            rb_map = {}
        else:
            # rb_fmt = self.parser.parse_json_schema(json_schema=json_schema, tb=self.tb, spec=self.parser.openapi_spec)
            # self.tb.DynamicObject.add_property("data", rb_fmt) # could we fix this to make it more intuitive?
            # rb_map_wrapper = await b.ExtractDynamicTypes(self.context, {"tb": self.tb})
            # rb_map = rb_map_wrapper.data if hasattr(rb_map_wrapper, 'data') else {}
            
            rb_map = await self.construct_dynamic_type(json_schema=json_schema)
        api_request = await b.ConstructDynamicAPIRequest(
            formatted_path, 
            method, 
            qp_map, 
            rb_map, 
            {"tb": self.tb}
        )
        
        return api_request  

    async def construct_dynamic_type(self, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        '''
        A function for constructing dynamic types, applicable to the request bodies of API requests.
        '''
        rb_fmt = self.parser.parse_json_schema(json_schema=json_schema, tb=self.tb, spec=self.parser.openapi_spec)
        self.tb.DynamicObject.add_property("data", rb_fmt)
        rb_map_wrapper = await b.ExtractDynamicTypes(self.context, {"tb": self.tb})
        rb_map = rb_map_wrapper.data if hasattr(rb_map_wrapper, 'data') else {}          
        return rb_map
        