import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html
from openai import OpenAI
import os
import json
from tenacity import retry, wait_random_exponential, stop_after_attempt

import weather_api as weather
import google_search

GPT_MODEL = "gpt-3.5-turbo-0613"

# Dash app initialization
app = dash.Dash(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Define layout
app.layout = html.Div([
    html.H1("Ask me Anything"),
    dcc.Textarea(id='input-box', value='무엇을 도와드릴까요?', style={'width': '100%', 'height': 200}),
    html.Button('Send', id='button', n_clicks=0),
    html.Div(id='output-container-button', children=[]),
])

# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "weather_forecast",
            "description": "Use this function to answer user questions about weather of certain city. Input should be passed into the following function.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city or location name to be used as function argument to def weather_forecast"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e
# Define callback to generate response on button click
@app.callback(
    Output('output-container-button', 'children'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value')]
)
def update_output(n_clicks, input_value):
    if n_clicks > 0:
        try:
            messages = [{"role": "system", "content": "Don't make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous."}]
            
            messages.append({"role": "user", "content": input_value})
            
            response = chat_completion_request(messages, tools=tools)
            

            if 'conversation_stack' not in globals():
                global conversation_stack
                conversation_stack = []

            for choice in response.choices:
                if choice.message.role == "user":
                    conversation_stack.append(html.P(choice.message.content))
                if choice.message.tool_calls:
                    for tool_call in choice.message.tool_calls:
                        function_name = tool_call.function.name
                        function_arguments = json.loads(tool_call.function.arguments)
                        if function_name == "weather_forecast":
                            city = function_arguments["city"]
                            weather_info = weather.call_current_weather(city)
                            conversation_stack.append(html.Table([
                                html.Tr([html.Th("Location"), html.Th("Weather"), html.Th("Max Temp"), html.Th("Min Temp"), html.Th("Temp"), html.Th("Humidity"), html.Th("Wind Speed")]),
                                html.Tr([
                                    html.Td(weather_info["location"]),
                                    html.Td(weather_info["weather"]),
                                    html.Td(weather_info["temp_max"]),
                                    html.Td(weather_info["temp_min"]),
                                    html.Td(weather_info["temp"]),
                                    html.Td(weather_info["humidity"]),
                                    html.Td(weather_info["wind_speed"])
                                ])
                            ]))
                            messages.append({"role": "assistant", "content": weather_info})
                        else:
                            conversation_stack.append(html.P(f"Unsupported function: {function_name}"))
                            messages.append({"role": "assistant", "content": f"Unsupported function: {function_name}"})
                else:
                    conversation_stack.append(html.P(choice.message.content))
                    messages.append({"role": "assistant", "content": choice.message.content})

            return conversation_stack
        
        except Exception as e:
            return f"Error: {e}"
    else:
        return []


if __name__ == '__main__':
    app.run_server(debug=True)

