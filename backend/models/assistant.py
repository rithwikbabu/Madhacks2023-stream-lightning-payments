from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="BitRoute Assistant",
    instructions="You are the help assistant for a bitcoin routing service called BitRoute. Help users with their problems and questions.",
    model="gpt-4-1106-preview"
)