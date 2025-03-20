
function CreateDescription(current_api_description: string, descriptions: string[]) -> string {
    client "openai/gpt-4o-mini"
    prompt #"
        Using the following description:
        {{ current_api_description }}
        Output a single-sentence description that makes sense in human language. Be sure the description you create does not already exist here:
        {{ descriptions }}
        {{ ctx.output_format}}
    "#
} // CreateDescription

test create_description_test {
    functions [CreateDescription]
    args {
        current_api_description #""Cancels an Account that belongs to your organization.\n\n:::info\nThis endpoint is only usable by Fleetio partners with an Organization Token or Partner Token.\n:::","#
        descriptions []
    }
}