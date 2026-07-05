--- name: comfyui-skill-openclaw
description: |
  Run ComfyUI workflows from any AI agent (Claude Code, OpenClaw, Codex, Hermes) via a single CLI. Import workflows, manage dependencies, execute across multiple servers, and track history through shell commands.
  Use this skill when the user wants to generate an image, draw a picture, execute a ComfyUI workflow, or import and configure saved ComfyUI workflows for later reuse.
version: 1.0.0
license: Apache-2.0
platforms: [macos, linux, windows]
prerequisites:
  commands: ["comfyui-skill"]
  env_vars: []
metadata:
  requires: []
bins:
  - comfyui-skill
cliHelp: "comfyui-skill --help"
tags:
  - image-generation
  - comfyui
  - ai-art
  - workflow
  - stable-diffusion
  - flux

# ComfyUI Agent SKILL

Prerequisites: install the CLI with `pip install -U comfyui-skill-cli`.
All commands must run from this project's root directory, where this `SKILL.md` is located.

Important: the CLI reads `config.json` and `data/` from the current directory.
You must `cd` into the project root before running any command.

Quick use:
- `comfyui-skill --json list`
- `comfyui-skill --json deps check <server_id>/<workflow_id>`
- `comfyui-skill --json run <server_id>/<workflow_id> --args '{"prompt":"a white cat"}'`
- `comfyui-skill --json workflow import <path>`

Core concepts:
- Skill ID: `<server_id>/<workflow_id>` such as `local/txt2img`
- Schema: each workflow has a `schema.json` that maps business parameter names to internal ComfyUI node fields
- Server: one or more ComfyUI instances configured in `config.json`

Common commands:
- `comfyui-skill --json server status`
- `comfyui-skill --json server stats`
- `comfyui-skill --json list`
- `comfyui-skill --json info <id>`
- `comfyui-skill --json submit <id> --args '{...}'`
- `comfyui-skill --json status <prompt_id>`
- `comfyui-skill --json run <id> --args '{...}'`
- `comfyui-skill --json run <id> --validate`
- `comfyui-skill --json upload <path>`
- `comfyui-skill --json upload <path> --mask`
- `comfyui-skill --json nodes list`
- `comfyui-skill --json jobs list`
- `comfyui-skill --json deps check <id>`
- `comfyui-skill --json deps install <id> --repos '[...]'`
- `comfyui-skill --json workflow import <path>`
- `comfyui-skill --json history list <id>`

Execution flow:
1. Query available workflows with `comfyui-skill --json list`
2. Assemble parameters as valid JSON
3. Run `comfyui-skill --json deps check <id>` before first use
4. Execute with `submit` + `status`, or `run` for blocking mode
5. Present generated files to the user

Workflow import:
- Supports both API format and editor format
- Automatically generates a `schema.json`
- After import, check dependencies before first execution

Troubleshooting:
- If `list` returns `[]`, you are probably in the wrong directory
- If the server is offline, check `config.json` and start ComfyUI
- If parameters fail, ensure `--args` is valid JSON wrapped in single quotes
