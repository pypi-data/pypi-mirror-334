
test get_intent {
    functions [GetIntent]
    args {
        intents [
            "POST Add a new vehicle to Fleetio",
            "GET Get a vehicle from Fleetio",
            "PATCH Edit a vehicle in Fleetio" 
        ]
        intent #"upload a new vehicle to fleetio"#
    } // args
} // get_intent