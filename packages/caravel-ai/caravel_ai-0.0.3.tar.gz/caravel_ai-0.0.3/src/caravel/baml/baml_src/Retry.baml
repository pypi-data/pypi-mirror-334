
function RetryFailedAPIRequest(err: string @assert(equal_to_500, {{this == "500"}}), context: string, original_api_req: DynamicAPIRequest) -> DynamicAPIRequest {
    client "openai/gpt-4o-mini"
    prompt #"
        {{original_api_req}}
    "#

    // how do I recreate the DynamicAPIRequest
}