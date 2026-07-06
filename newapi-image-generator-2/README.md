# Newapi Image Generator

A skill for generating, editing, and varying images through the NowCoding / New API OpenAI-compatible image endpoints.

## Overview

This skill provides a Node.js helper script for calling NowCoding / New API's image endpoints from Claude Code or Codex. It supports:

- **Generate**: Text-to-image generation
- **Edit**: Prompt-guided image edits with optional mask support
- **Variation**: Image-to-image variations from a source image

## Quick Start

1. Set environment variables:
   `ash
   export NEWAPI_BASE_URL=https://nowcoding.ai/v1
   export NEWAPI_API_KEY=your_api_key_here
   `

2. Run the helper script:
   `ash
   # Generate an image
   node scripts/newapi_image.js generate --prompt "A cinematic fox in a neon city"
   
   # Edit an image
   node scripts/newapi_image.js edit --image input.png --mask mask.png --prompt "Turn this into a watercolor poster"
   
   # Create variations
   node scripts/newapi_image.js variation --image input.png
   `

3. Save images to disk:
   `ash
   node scripts/newapi_image.js generate --prompt "..." --output-dir ./out --output-prefix my-image
   `

## Usage

### Generate
`ash
node scripts/newapi_image.js generate \
  --prompt "A serene landscape with mountains at sunset" \
  --size 1024x1024 \
  --n 2 \
  --output-dir ./images
`

### Edit
`ash
node scripts/newapi_image.js edit \
  --image source.png \
  --mask mask.png \
  --prompt "Add a castle in the background" \
  --output-dir ./edited
`

### Variation
`ash
node scripts/newapi_image.js variation \
  --image input.png \
  --n 4 \
  --output-dir ./variations
`

## Options

- `--base-url <url>`: API base URL (default: NEWAPI_BASE_URL env or https://nowcoding.ai/v1)
- `--api-key <key>`: API key (default: NEWAPI_API_KEY env)
- `--model <name>`: Image model (default: gpt-image-1 for generate/edit, dall-e-2 for variation)
- `--size <value>`: Image size (e.g., 1024x1024, 1024x1536)
- `--n <count>`: Number of images to generate
- `--response-format <value>`: url or b64_json (default: b64_json)
- `--output-dir <dir>`: Directory to save generated images
- `--output-prefix <name>`: Filename prefix for saved images
- `--prompt <text>`: Prompt text (required for generate/edit)
- `--image <path>`: Source image path (can specify multiple times for edit)
- `--mask <path>`: Optional mask path for edits

## Response Formats

- **url**: Returns remote URLs (use when you only need links)
- **b64_json**: Returns base64-encoded data (use with --output-dir to save locally)

## Conventions

- Keep prompts specific: include subject, style, lighting, framing, and mood
- Use `response_format=url` when you only need links
- Use `response_format=b64_json` or `--output-dir` when you need local files
- For edit, pass one or more `--image` inputs and an optional `--mask`

## Environment Variables

- `NEWAPI_BASE_URL`: Base URL for the API gateway (default: https://nowcoding.ai/v1)
- `NEWAPI_API_KEY`: Bearer token for authorization (required)

## Project Structure

`
newapi-image-generator/
├── SKILL.md                          # Skill definition and usage
├── agents/
│   └── openai.yaml                   # Agent interface config
├── references/
│   └── newapi-image-api.md           # API endpoint notes
├── scripts/
│   └── newapi_image.js               # Helper script
└── README.md                         # This file
`

## License

MIT