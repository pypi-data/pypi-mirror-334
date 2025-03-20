
function GenerateIntent(intents: string[], intent: Context) -> string @description(#"
    A string formatted in the following manner: <METHOD Intent>, where METHOD is the HTTP Request that will need to be used. 
"#) {
    client "openai/gpt-4o-mini"
    prompt #"
        Using the following list of intents, 
        {{ intents }}
        and the current context of the conversation:
        {{ intent }}
        output the intent, sans quotes.
        {{ ctx.output_format }}   
    "#
} // GetIntent

function GeneratePath(path: string, context: Context) -> string @description(#"
    A string representing the altered path, filled with the path parameters based on the user input.
"#) {
    client "openai/gpt-4o-mini"
    prompt #"
        Using this path outline and extracting any path arguments ({id}, :id, etc):
        (Note: Never put query parameters into the path, only path parameters)
        {{ path }}
        Generate the path with path parameters (if any exist) filled in, using information gleaned from this input:
        {{ context }}
        If the parameter cannot be inferred, return:
        {{ NoParamProvided() }}
         If no path parameter exists within {{ path }}, return only:
        {{ path }}
        {{ ctx.output_format }}
    "#
} // MakePath

// A dynamic class that will be used for checking the schema of OpenAPI specifications
class DynamicObject {
    @@dynamic
} // DynamicObject

// A dynamic enum that will be used for constructing dynamic json objects.
enum DynamicEnum {
    @@dynamic
} // DynamicEnum

function ExtractDynamicTypes(context: Context) -> DynamicObject {
    client "openai/gpt-4o-mini"
    prompt #"
        {{ ctx.output_format }}
        {{ _.role('user') }}
        Using the context from the conversation:
        {{ context }}
        Sometimes, you may need to coerce a user provided input into the nearest allowed value for an attribute (e.g. If allowed options are `mi`, `km`, `hr`, and user supplies `miles`, coerce to `mi`)
    "#
} // ExtractDynamicTypes

enum HTTPMethod {
    GET
    DELETE
    POST
    PATCH
    PUT
}

// An API request object
class DynamicAPIRequest {
    path string
    method HTTPMethod
    params  map<string, string>? @description(#"
        Query Parameters. Will usually be null for POST and PATCH requests.
    "#)
    request_body DynamicObject? @description(#"
        A dynamically generated request body based on user input. It will be 
    "#)
} // DynamicAPIRequest 

// map<string, string> works here because query paramas are ALWAYS strs
function GenerateQueryParameters(fmt: map<string, string | int | float | bool>, context: Context) -> map<string, string> {
    client "openai/gpt-4o-mini"
    prompt #"
        DO NOT HALLUCINATE QUERY PARAMS NOT IN {{ fmt }}

        Using the following query parameter structure:
        {{ fmt }}
        And the provided context: {{ context }},
        Complete the query parameters. If the query param structure is empty, return {{ fmt }} with appropriate default values populated.
        {{ ctx.output_format }}
    "#
} // newPopulateQP


// A function for constructing a dynamic API request as specified above.
function ConstructDynamicAPIRequest(path: string, method: HTTPMethod | string, params: map<string, string>?, request_body: DynamicObject?) -> DynamicAPIRequest {
    client "openai/gpt-4o-mini"
    prompt #"
        Create an API Request with the given parameters.
        {{ ctx.output_format }}
        Path: {{ path }}
        method: {{ method }}
        query parameters: {{ params }}
        request_body: {{ request_body }}
    "#
} // ConstructDynamicAPIRequest


