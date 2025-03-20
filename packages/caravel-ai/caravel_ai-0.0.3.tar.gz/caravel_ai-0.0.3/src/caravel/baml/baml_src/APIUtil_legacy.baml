
template_string NoMarkdown() #"
    Do not use markdown.
"#

template_string NotEnoughContextError(error_message: string, required: string[]) #"
    NotEnoughContextError: {{ error_message }}, required: {{ required }}
"# 

template_string EmptyDictString() #"
    {}
"#

template_string EmptyString() #"
    
"# 



function GenerateHumanLanguageResponse(json: string, context: string) -> string {
    client "openai/gpt-4o-mini"
    prompt #"

        Describe the content within the following
        {{ json }}
        as if you are answering the prompt in
        {{ context }}
        in a single paragraph. Do not include technical details, just describe the content itself.
        
        {{ ctx.output_format }}
    "#
} // GenerateHumanLanguageResponse

test new_function {
    functions [PopulateQueryParameters]
    args {
        fmt {
            "start_cursor" ""
            "filter[acquisition_type][eq]" "loan | lease"
            "filter[reference_number][like]" ""
            "filter[vehicle_id][eq]" ""
            "filter[lender_id][eq]" ""
            "filter[vendor_id][eq]" ""
            "filter[acquisition_date][lt]" ""
            "filter[created_at][lt]" ""
            "filter[updated_at][lt]" ""
            "sort[id]" "desc"
            "sort[acquisition_date]" "asc | desc" 
            "sort[created_at]" "asc | desc"
            "sort[updated_at]" "asc | desc"
        }
        context #"
            Get all of my loan acquisitions from 2010 to 2020 sorted in chronological order.
        "#
    }
}



