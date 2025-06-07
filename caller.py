import anthropic
client = anthropic.Anthropic()
response = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=2000,
    messages=[
        {
        "role": "user",
        "content": "What messages on the board",
    }],
    mcp_servers=[{
        "type": "url",
        "url": "https://mcp.andrewperkins.com.au/message_board/mcp/",
        "name": "Message Board",
    }],
    betas=["mcp-client-2025-04-04"]
)

output = '\n'.join([c.text for c in response.content if c.type=='text'])

print(output)