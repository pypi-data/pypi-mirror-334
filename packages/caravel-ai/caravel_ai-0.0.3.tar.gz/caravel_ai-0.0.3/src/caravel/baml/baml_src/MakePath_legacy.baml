
template_string NoParamProvided() #"
    NoParamProvidedError
"# // NoParamProbided

test make_path_param_given {
    functions [MakePath]
    args {
        path #"/v1/vehicles/{id}"#
        user_input #"Get vehicle with id 1234"#
    }
}

test make_path_param_not_given {
    functions [MakePath]
    args {
        path #"/v1/vehicles/{id}"#
        user_input #"Can you get my dad's truck from fleetio? "#
    }
}

test make_path_no_path_param_present {
    functions [MakePath]
    args {
        path #"/v1/vehicles/"#
        user_input #"Can you give me all of my vehicles in fleetio?"#
    }
}

test make_path_no_path_param_present_but_some_given {
    functions [MakePath]
    args {
        path "/pet"
        user_input "Add a new pet to the store named blue. It is a 2 year old dog!"
    }
}

