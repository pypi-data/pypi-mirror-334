import os
from rebyte import RebyteAPIRequestor

api_key = os.getenv('REBYTE_API_KEY')
requestor = RebyteAPIRequestor(
            key=api_key,
            api_base="https://rebyte.ai"
        )

# create an agent on rebyte platform and get the project_id and agent_id
# https://rebyte.ai/api/sdk/p/{test_project_id}/a/{test_agent_id}/r
project_id = "a8056c9a7bac76e20087"
agent_id = "de7d2bdf4dac96971e19"
path = f'/api/sdk/p/{project_id}/a/{agent_id}/r'

# You may use any string as thread_id and try to avoid duplicate thread_ids
# Note that you must set thread_id if you want to enable stateful actions, such as threads (aka, memory), in your agent.
# Or you can leave it as empty when the agent has no stateful actions.
data = {
    "version": "latest",       
    "inputs": [{"messages": [{"role": "user","content": "Please remember: My name is John"}]}],
    "config": {},
    "thread_id" : "ANY_STRING"
}
res, _, _ = requestor.request(
    method="POST",
    url=path,
    params=data,
    stream=False
)
print(res.data['run']['results'][0][0]["value"]["content"])

data = {
    "version": "latest",       
    "inputs": [{"messages": [{"role": "user","content": "Please answer me: What is my name?"}]}],
    "config": {},
    "thread_id" : "ANY_STRING"
}
res, _, _ = requestor.request(
    method="POST",
    url=path,
    params=data,
    stream=False
)
print(res.data['run']['results'][0][0]["value"]["content"])