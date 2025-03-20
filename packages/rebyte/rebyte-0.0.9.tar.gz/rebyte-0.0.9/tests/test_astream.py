import os
import asyncio
from rebyte import RebyteAPIRequestor

async def main():
    api_key = os.getenv('REBYTE_API_KEY')
    requestor = RebyteAPIRequestor(
        key=api_key,
        api_base="https://rebyte.ai"
    )
    project_id = "a8056c9a7bac76e20087"
    agent_id = "de7d2bdf4dac96971e19"
    path = f'/api/sdk/p/{project_id}/a/{agent_id}/r'
    data = {
        "version": "latest",       
        "inputs": [{"messages": [{"role": "user","content": "My name is John"}]}],
        "config": {},
        "stream": True
    }
    res, _, _ = await requestor.arequest(
        method="POST",
        url=path,
        params=data,
        stream=True
    )
    async for msg in res:
        # print streaming output message
        stream_text = msg.get_stream_chunk()
        if msg and stream_text:
            print(stream_text)

asyncio.run(main())