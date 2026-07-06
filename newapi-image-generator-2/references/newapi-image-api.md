# New API Image API Notes

This skill assumes an OpenAI-compatible image API behind `NEWAPI_BASE_URL`.

## Environment

- `NEWAPI_BASE_URL`: Base URL for the gateway, default `https://nowcoding.ai/v1`
- `NEWAPI_API_KEY`: Bearer token for authorization

## Endpoints

- `POST /v1/images/generations`
- `POST /v1/images/edits`
- `POST /v1/images/variations`

## Common Parameters

- `model`
- `prompt`
- `size`
- `n`
- `response_format`
- `user`

## Edit / Variation Inputs

- `image`: one or more source image files
- `mask`: optional mask file for edits

## Response Handling

Support both response shapes:

- `data[].url`
- `data[].b64_json`

When a URL is returned, save the remote file only if `--output-dir` is set.
When `b64_json` is returned, decode it and write the image locally if `--output-dir` is set.

## Notes

- Keep prompts concrete and visual.
- Use `response_format=url` when you only need a link.
- Use `response_format=b64_json` when you want a file artifact without relying on remote hosting.
