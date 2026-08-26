# Platform compatibility

Forms Responder uses portable Agent Skills for its instructions, references, and Python study-memory helper. The same behavior is packaged for Codex, Claude Code, Gemini CLI, and Grok Build. Packaging compatibility does not create tools a host does not expose.

## Capability contract

For live form operation, the current host must provide an interactive browser or computer-control tool that can inspect visible state, click, type, scroll, and preserve the user's signed-in session. For source review, it must also expose the required media or document. For Google Drive memory, it must expose callable file search, folder creation, upload, metadata readback, and content fetch operations.

If a required capability is absent, explain exactly what is missing and stop that part of the workflow. The skill may still provide help, review user-supplied content, or use local study memory when the user requests it. Never describe a tool action as completed when only the skill instructions are installed.

## Host notes

| Host | Native package | Live form prerequisite | Google Drive prerequisite |
|---|---|---|---|
| Codex | Codex plugin and Agent Skills | Browser plugin or supported browser-control surface | Connected Google Drive plugin |
| Claude Code | Claude plugin and Agent Skills | Chrome integration, computer-use surface, or an equivalent trusted tool/MCP | Connected Drive integration or trusted MCP with the required file operations |
| Gemini CLI | Gemini extension and Agent Skills | Browser-capable extension or trusted MCP/tool | Drive-capable extension or trusted MCP/tool |
| Grok Build | Claude-compatible plugin and Agent Skills | Grok browser/computer surface or trusted tool/MCP | Connected Drive connector or trusted MCP/tool |

The ordinary Grok chat product, a model-only API call, or a plain terminal agent without browser tooling cannot operate a signed-in live form merely because the skill is present. The local memory script still requires Python 3 and filesystem permission on every host.

## Invocation

Natural-language triggering is preferred. Direct invocation syntax is host-specific: Codex may expose a skill selector, Claude and Grok plugin skills are namespaced slash commands, and Gemini activates installed skills through its skills interface. Do not require a slash command when automatic discovery already selects the skill.

The no-submission boundary, internal two-pass audit, exact handoff table, per-record save confirmation, and explicit Google Drive selection apply identically on every host.
