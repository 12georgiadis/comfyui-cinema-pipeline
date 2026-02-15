# Claude Code + ComfyUI Integration

How to connect Claude Code (LLM CLI agent) to ComfyUI for programmatic image/video generation.

---

## 1. MCP Servers (the direct bridge)

MCP (Model Context Protocol) lets Claude Code call ComfyUI as a tool. Multiple servers exist:

### joenorton/comfyui-mcp-server -- MOST COMPLETE
- **URL**: https://github.com/joenorton/comfyui-mcp-server
- **Transport**: Streamable HTTP on `http://127.0.0.1:9000/mcp`
- **Key feature**: Auto-discovery. Drop a JSON workflow in `workflows/`, it becomes an MCP tool. Uses placeholders `PARAM_PROMPT`, `PARAM_INT_STEPS`, `PARAM_FLOAT_CFG` that become typed arguments.
- **Tools exposed**: `generate_image`, `generate_song`, `regenerate`, `get_queue_status`, `get_job`, `list_assets`, `get_asset_metadata`, `cancel_job`, `list_models`, `get_defaults`, `set_defaults`, `list_workflows`, `run_workflow`
- **Config for Claude Code**: via `.mcp.json` in project root
- **Limit**: Asset IDs are ephemeral (session-scoped)

### IO-AtelierTech/comfyui-mcp -- 29 TOOLS
- **URL**: https://github.com/IO-AtelierTech/comfyui-mcp
- **29 tools**: System Monitoring (5), Node Discovery (7), Workflow Management (11), Execution (6)
- **Schema validation** against ComfyUI v0.4
- **Auto-layout** of nodes via NetworkX
- **Format conversion** API <-> UI/Litegraph
- **Install**: `uvx comfyui-easy-mcp` or `pip install comfyui-easy-mcp`

### alecc08/comfyui-mcp -- SIMPLE & EFFECTIVE
- **URL**: https://github.com/alecc08/comfyui-mcp
- **Node.js** (TypeScript)
- **Tools**: `generate_image`, `modify_image` (img2img), `resize_image`, `remove_background`, `get_image`, `get_request_history`, `list_workflows`
- **Built-in HTTP proxy** on port 8190 for serving images (no base64)
- **Config for Claude Desktop**:
```json
{
  "mcpServers": {
    "comfyui": {
      "command": "node",
      "args": ["/path/to/comfyui-mcp/dist/index.js"],
      "env": {
        "COMFYUI_URL": "http://127.0.0.1:8188",
        "COMFYUI_WORKFLOW_DIR": "/path/to/workflow_files"
      }
    }
  }
}
```

### lalanikarim/comfy-mcp-server -- FastMCP
- **URL**: https://github.com/lalanikarim/comfy-mcp-server
- Uses FastMCP framework
- Configured via env vars (`COMFY_URL`, `COMFY_WORKFLOW_JSON_FILE`, `PROMPT_NODE_ID`, `OUTPUT_NODE_ID`)
- Also has an [Open WebUI pipeline wrapper](https://github.com/lalanikarim/comfy-mcp-pipeline)

### Nikolaibibo/claude-comfyui-mcp -- CLAUDE DESKTOP SPECIFIC
- **URL**: https://github.com/Nikolaibibo/claude-comfyui-mcp
- **Tools**: `comfy_submit_workflow`, `comfy_generate_simple`, `comfy_get_status`, `comfy_wait_for_completion`, `comfy_list_models`
- Built-in templates (e.g. `flux_txt2img`)

### SamuraiBuddha/mcp-comfyui -- Enhanced Edition
- **URL**: https://lobehub.com/mcp/samuraibuddha-mcp-comfyui
- Full control: `prompt`, `negative_prompt`, `width`, `height`, `steps`, `cfg_scale`, `seed`, `model`, `sampler`, `scheduler`
- WebSocket communication

### jau123/MeiGen-Art -- MULTI-BACKEND
- **URL**: https://github.com/jau123/MeiGen-Art
- **3 backends**: ComfyUI local, MeiGen Cloud, OpenAI-compatible
- **1300+ prompts** in built-in library
- Auto-detection of KSampler, CLIPTextEncode, EmptyLatentImage, LoadImage nodes
- Install: `npx -y meigen@latest`

### jonpojonpo/comfy-ui-mcp-server
- **URL**: https://github.com/jonpojonpo/comfy-ui-mcp-server
- The first historically, more basic
- Config: `claude mcp add-json "comfy-ui-mcp-server" '{"command":"uvx","args":["comfy-ui-mcp-server"]}'`

---

## 2. Claude inside ComfyUI (reverse direction)

### christian-byrne/claude-code-comfyui-nodes
- **URL**: https://github.com/christian-byrne/claude-code-comfyui-nodes
- Puts Claude Code **inside** ComfyUI as nodes. 8 nodes:
  1. **Claude Code Execute**: runs Claude commands as a node
  2. **Claude Code Reader**: reads files with glob patterns
  3. **Claude Context Builder**: converts outputs to reusable memory
  4. **Claude Memory Builder**: builds multi-source context
  5. **Claude Arguments Builder**: `${VAR}` substitution
  6. **Claude Tools Config**: fine-grained permissions (read-only, file-ops, web, etc.)
  7. **Claude MCP Manager**: configures MCP servers from ComfyUI
  8. **Claude Reddit Scraper**: scrapes Reddit from a ComfyUI node
- **Use case for filmmakers**: Scrape discussions, transform into video scripts, chain generation steps.

### Comfy-Org/comfy-claude-prompt-library -- OFFICIAL
- **URL**: https://github.com/Comfy-Org/comfy-claude-prompt-library
- Official Claude Code commands from the Comfy-Org team
- Includes commands like `/user:STUDY-comfyui-custom-nodes-ecosystem` and `/user:AGENT-playbook-to-automated-agent-workflow`

### AIDC-AI/ComfyUI-Copilot -- AI COPILOT
- **URL**: https://github.com/AIDC-AI/ComfyUI-Copilot
- 1.6K+ stars, 85K queries, 19K users, 22 countries
- Multi-agent: generation, debugging, rewriting, parameter tuning
- Knowledge base: 7K nodes, 62K models, 9K workflows
- [Paper (arXiv)](https://arxiv.org/html/2506.05010v1)

---

## 3. ComfyUI API Reference

### REST Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/prompt` | POST | Submit workflow, returns `prompt_id` |
| `/prompt` | GET | Queue status |
| `/queue` | GET | Queue state (running + pending) |
| `/queue` | POST | Delete queue items |
| `/history/{prompt_id}` | GET | Results of a prompt |
| `/view` | GET | Retrieve image (`filename`, `subfolder`, `type`) |
| `/upload/image` | POST | Upload image |
| `/upload/mask` | POST | Upload mask |
| `/interrupt` | POST | Interrupt current execution |
| `/free` | POST | Unload models from VRAM |
| `/object_info` | GET | Metadata of all available nodes |
| `/system_stats` | GET | System stats (Python, OS, GPU, VRAM) |
| `/embeddings` | GET | List embeddings |
| `/models` | GET | Available model types |
| `/models/{folder}` | GET | Models in specific folder |

### WebSocket `/ws`
- Connection: `ws://{server}:8188/ws?clientId={uuid}`
- Messages: `status`, `execution_start`, `execution_cached`, `executing`, `progress`, `executed`
- Real-time generation tracking

### Standard Python Pattern
```python
import websocket, uuid, json, requests

server = "127.0.0.1:8188"
client_id = str(uuid.uuid4())

# 1. Connect WebSocket
ws = websocket.WebSocket()
ws.connect(f"ws://{server}/ws?clientId={client_id}")

# 2. Load and modify workflow
workflow = json.load(open("workflow_api.json"))
workflow["6"]["inputs"]["text"] = "my prompt"

# 3. Submit
result = requests.post(f"http://{server}/prompt",
    json={"prompt": workflow, "client_id": client_id}).json()
prompt_id = result["prompt_id"]

# 4. Wait (via WebSocket or polling)
# 5. Retrieve results
history = requests.get(f"http://{server}/history/{prompt_id}").json()
for node_id in history[prompt_id]["outputs"]:
    for img in history[prompt_id]["outputs"][node_id].get("images", []):
        data = requests.get(f"http://{server}/view",
            params={"filename": img["filename"],
                    "subfolder": img["subfolder"],
                    "type": img["type"]}).content
```

### Comfy Cloud API (official)
- **URL**: `https://cloud.comfy.org/api/prompt`
- **Auth**: Header `X-API-Key: $COMFY_CLOUD_API_KEY`
- **Compatible** with local API (same endpoints, same format)
- **Outputs**: via `/api/view` returning 302 redirect to signed temporary URL
- **API Keys for paid nodes**: via `extra_data.api_key_comfy_org` in payload
- **Key generation**: https://platform.comfy.org/profile/api-keys
- **Official docs**: https://docs.comfy.org/development/cloud/overview

---

## 4. Transpilers (Workflow <-> Code)

### ComfyScript -- KEY FOR LLM USAGE
- **URL**: https://github.com/Chaoses-Ib/ComfyScript (also https://github.com/comfyorg/comfyscript)
- **Transpiler**: Automatically converts ComfyUI JSON workflow to Python script
- **Library**: Use ComfyUI nodes as Python functions
- **Type hints and enums**: Models, samplers, etc. exposed as Python enums (e.g., `Checkpoints.model_name`) -- reduces LLM hallucinations
- **PyPI**: `pip install comfy-script`
- **Why ideal for LLM**: Python > JSON for an LLM, type hints = fewer errors, readable and self-documenting
- Can run in remote mode (connected to a remote ComfyUI)

### ComfyUI-to-Python-Extension
- **URL**: https://github.com/pydn/ComfyUI-to-Python-Extension
- Custom ComfyUI node that translates workflows to standalone Python scripts
- Requires Dev Mode enabled in ComfyUI

### ComfyUI-SaveAsScript
- **URL**: https://github.com/atmaranto/ComfyUI-SaveAsScript
- "Save as Script" button in ComfyUI UI
- Generates Python scripts with CLI arguments

---

## 5. LLM-Driven Workflow Generation

### ComfyUI-WorkflowGenerator
- **URL**: https://github.com/DanielPFlorian/ComfyUI-WorkflowGenerator
- Natural language -> ComfyUI node graph
- 3-stage pipeline: Generator (LLM), Validator (checks nodes), Builder (compiles to executable JSON)
- Based on Qwen2.5-14B fine-tuned

### ComfyGPT (research)
- **Paper**: https://arxiv.org/html/2503.17671v1
- 4 agents: ReformatAgent, FlowAgent, RefineAgent, ExecuteAgent
- Innovation: generates individual links between nodes (not entire workflow)
- SFT + RL for autonomous error correction

### ComfyUI-R1 (research, June 2025)
- **Paper**: https://arxiv.org/html/2506.09790v1
- Chain-of-thought reasoning for workflow code generation
- 2-stage training: CoT fine-tuning + RL

### ComfyBench (CVPR 2025)
- **Paper**: https://openaccess.thecvf.com/content/CVPR2025/papers/Xue_ComfyBench_Benchmarking_LLM-based_Agents_in_ComfyUI_for_Autonomously_Designing_Collaborative_CVPR_2025_paper.pdf
- Benchmark for LLM agents in ComfyUI
- **Sobering result**: best agent solves only 15% of creative tasks

### comfyui_LLM_party
- **URL**: https://github.com/heshengtao/comfyui_LLM_party
- Complete LLM agent framework inside ComfyUI
- Includes MCP server, Omost, GPT-sovits, ChatTTS, FLUX prompt nodes
- Compatible: o1, ollama, gemini, grok, qwen, deepseek, etc.
- "Matryoshka" feature: one LLM as a tool for another LLM

---

## Sources

- [ComfyUI Server Routes (official)](https://docs.comfy.org/development/comfyui-server/comms_routes)
- [DeepWiki - Prompt Server](https://deepwiki.com/hiddenswitch/ComfyUI/4.1-prompt-server-and-rest-api)
- [9elements API tutorial](https://9elements.com/blog/hosting-a-comfyui-workflow-via-api/)
- [LearnCodeCamp API guide](https://learncodecamp.net/comfyui-api-endpoints-complete-guide/)
- [Comfy Cloud API overview](https://docs.comfy.org/development/cloud/overview)
