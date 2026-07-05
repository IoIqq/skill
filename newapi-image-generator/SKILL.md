---
name: newapi-image-generator
description: Use when you need to generate, edit, or vary images through the NowCoding / New API OpenAI-compatible image endpoints, or when you need a Node.js helper for /v1/images/generations, /v1/images/edits, or /v1/images/variations.
---

# Newapi Image Generator

## Overview

Use this skill when you need to call NowCoding / New API's OpenAI-compatible image endpoints from Node.js. Keep credentials in environment variables and prefer the helper script in `scripts/` for repeatable calls.

## Quick Start

1. Set `NEWAPI_BASE_URL` to `https://nowcoding.ai/v1` or your own gateway root.
2. Set `NEWAPI_API_KEY`.
3. Run the helper:

```bash
node scripts/newapi_image.js generate --prompt "A cinematic fox in a neon city"
node scripts/newapi_image.js edit --image input.png --mask mask.png --prompt "Turn this into a watercolor poster"
node scripts/newapi_image.js variation --image input.png
```

4. Add `--output-dir ./out` when you want images written to disk.

## Use Cases

- Use `generate` for text-to-image requests.
- Use `edit` for prompt-guided image edits with an optional mask.
- Use `variation` for image-to-image variations from one source image.

## Conventions

- Prefer `response-format url` when you only need links.
- Prefer `response-format b64_json` or `--output-dir` when you need local files.
- For `edit`, pass one or more `--image` inputs and an optional `--mask`.
- Keep prompts specific: subject, style, lighting, framing, and mood.

## Reference

- See `references/newapi-image-api.md` for endpoint notes, parameter defaults, and response handling.
