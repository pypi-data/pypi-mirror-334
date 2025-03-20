import json
import os
from rebyte import RebyteAPIRequestor

api_key = os.getenv('REBYTE_API_KEY')
requestor = RebyteAPIRequestor(
            key=api_key,
            api_base="https://rebyte.ai"
        )

# create a workflow on rebyte platform and get the project_id and agent_id
project_id = "a8056c9a7bac76e20087"
agent_id = "de7d2bdf4dac96971e19"
path = f'/api/sdk/p/{project_id}/a/{agent_id}/r'
data = {
    "version": "live",       
    "contentOnly": False,
    "inputs": [{"messages": [{"role": "user","content": "how many rows in the table?"}]},],
    "config": {}
}
res, _, _ = requestor.request(
    method="POST",
    url=path,
    params=data,
    stream=False
)
print(json.dumps(res.data, indent=2))