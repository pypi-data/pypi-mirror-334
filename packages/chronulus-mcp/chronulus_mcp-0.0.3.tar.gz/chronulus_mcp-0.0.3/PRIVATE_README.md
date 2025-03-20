choronulus-agents server provides access to the Chronulus AI platform of forecasting and prediction agents.

- Sessions capture an overall use case that is described by a situation and task.
- Agents created for a given session and are reusable across multiple different forecasting inputs.

For example, in a retail forecasting workflow, 
    - The situation might include information about the business, location, demographics of customers, and motivation for forecasting
    - The task would include specifics about what to forecast like the demand, share of foot traffic, probability of the item going out of stock, etc.
    - The agent could be used for multiple different types of items with a single data model.  For example a data model with brand and price feature could
    be used to predict over multiple items with their own values for brand and price.


```bash 
aws sso login --profile CentralArtifacts
```

```bash
bash get-index-url.sh
```



```bash
npx dotenv npx @modelcontextprotocol/inspector \
  uv run \
  --with-requirements /Users/theoldfather/Projects/chronulus/chronulus-mcp/requirements.txt  \
  --prerelease=allow \
  mcp run /Users/theoldfather/Projects/chronulus/chronulus-mcp/src/chronulus_mcp
  
```


## Claude Desktop Config
`~/Library/Application Support/Claude/claude_desktop_config.json`

```json 
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/theoldfather/Desktop/AIWorkspace/ncaa-matchups"
      ]
    },
    "chronulus-agents-dev": {
      "command": "/Users/theoldfather/.local/bin/uv",
      "args": [
        "run",
        "--prerelease=allow",
        "--with-requirements",
        "/Users/theoldfather/Projects/chronulus/chronulus-mcp/requirements.txt",
        "mcp",
        "run",
        "/Users/theoldfather/Projects/chronulus/chronulus-mcp/src/server.py"
      ],
      "env": {
        "CHRONULUS_API_KEY": "a6dfdcce-6116-4039-a3fc-00e79f650efa",
        "API_URI": "https://core-dev.api.chronulus.com/v1",
        "UV_EXTRA_INDEX_URL": ""
    },
    "fetch": {
      "command": "/Users/theoldfather/.local/bin/uvx",
      "args": ["mcp-server-fetch"]
    }
   
  }
}
```