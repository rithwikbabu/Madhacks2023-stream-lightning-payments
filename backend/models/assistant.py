from openai import OpenAI
import json


def show_json(obj):
    print(json.loads(obj.model_dump_json()))

client = OpenAI()

assistant = client.beta.assistants.create(
    name="BitRoute Assistant",
    instructions="You are the help assistant for a bitcoin routing service called BitRoute. Help users with their problems and questions.",
    model="gpt-4-1106-preview"
)

thread = client.beta.threads.create()
show_json(thread)

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)
show_json(message)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
show_json(run)