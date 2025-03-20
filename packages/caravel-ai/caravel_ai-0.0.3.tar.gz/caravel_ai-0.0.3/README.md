# Welcome to Caravel
Human-in-the-loop Agentic AI for your OpenAPI specs. Built in asynchronous Python and BAML.

![image](https://github.com/user-attachments/assets/28e57430-eeba-42b8-a120-8d0f0c3c0034)

## Getting Started

## Installation
```bash
pip install <name, hopefully caravel-ai>
```

## AI Assistant Speedrun
```python
from caravel.assistant.Assistant import Assistant
from caravel.baml.baml_client.types import Context
from caravel.http.Client import Client
from caravel.parsing.Parser import Parser

BASE_URL="env" # will be replaced with the dotenv

assistant: Assistant = Assistant(
    # finish this!
    client=Client(
        base_url=BASE_URL,
        auth_headers={}, # will be filled w auth headers
        allowed_methods=['get', 'post', 'patch', 'delete']
    ),
    spec_file="samsara.json"
) # Assistant

output_msg: str = "How can I help you today?"

while True:
    print("----------------------------------------")
    print("Assistant:")
    print(output_msg)
    print("----------------------------------------")
    user_prompt = input("$ ")
    output_msg = await assistant.assistant_call(user_prompt)

```

## 

# Overview
Caravel projects have four main parts:
1. The Parser
The Parser is a class that provides utilities for operating on OpenAPI specification files. The Parser is used to convert the OpenAPI specifications into formats that make it workable with the Client and the Runner.
2. The Runner 
The Runner is a class consisting of methods that perform legwork such as constructing API requests, checking the schema of requests, etc.
3. The Client
The Client is a class that is used to make HTTP requests to the API. Client functions recieve their parameters from the runner and return their results in JSON format or in human/LLM-readable text. In addition to the standard HTTP methods, the Client also allows users to add their own custom methods to the client.
4. The CaravelRegistry
The CaravelRegistry is a function registry class. This registry is what allows developers to call Caravel functions from their assistant. The CaravelRegistry is a singleton class.
