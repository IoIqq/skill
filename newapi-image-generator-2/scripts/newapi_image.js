#!/usr/bin/env node
'use strict';

const fs = require('node:fs/promises');
const path = require('node:path');

const DEFAULT_BASE_URL = 'https://api.xstx.info';
const DEFAULT_GENERATE_MODEL = 'gpt-image-1';
const DEFAULT_EDIT_MODEL = 'gpt-image-1';
const DEFAULT_VARIATION_MODEL = 'dall-e-2';
const DEFAULT_RESPONSE_FORMAT = 'url';

function usage() {
  console.log(`Usage:
  node scripts/newapi_image.js generate --prompt "..." [options]
  node scripts/newapi_image.js edit --image input.png [--mask mask.png] --prompt "..." [options]
  node scripts/newapi_image.js variation --image input.png [options]

Options:
  --base-url <url>            API base URL (default: ${DEFAULT_BASE_URL})
  --api-key <key>             API key (default: NEWAPI_API_KEY env)
  --model <name>              Image model (default depends on action)
  --size <value>              Size, for example 1024x1024
  --n <count>                 Number of images
  --response-format <value>   url or b64_json (default: ${DEFAULT_RESPONSE_FORMAT})
  --output-dir <dir>          Write images to disk
  --output-prefix <name>      File prefix when saving images
  --prompt <text>             Prompt text
  --image <path>              Source image path
  --mask <path>               Optional mask path for edits
  --help                      Show help`);
}

function parseArgs(argv) {
  const args = {
    _: [],
    image: [],
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }

    const key = token.slice(2);
    if (key === 'help') {
      args.help = true;
      continue;
    }

    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) {
      if (key === 'image') {
        throw new Error('--image requires a value');
      }
      args[key] = true;
      continue;
    }

    i += 1;
    if (key === 'image') {
      args.image.push(next);
    } else if (key === 'n') {
      args[key] = Number(next);
    } else {
      args[key] = next;
    }
  }

  return args;
}

function normalizeBaseUrl(value) {
  const trimmed = String(value || '').trim();
  if (!trimmed) return DEFAULT_BASE_URL;
  return trimmed.replace(/\/+$/, '');
}

function ensureRequired(value, name) {
  if (value === undefined || value === null || String(value).trim() === '') {
    throw new Error(`Missing required ${name}`);
  }
  return value;
}

function resolveModel(action, args) {
  if (args.model) {
    return args.model;
  }
  if (action === 'variation') {
    return DEFAULT_VARIATION_MODEL;
  }
  if (action === 'edit') {
    return DEFAULT_EDIT_MODEL;
  }
  return DEFAULT_GENERATE_MODEL;
}

function toFormField(value) {
  if (value === undefined || value === null) return undefined;
  return String(value);
}

async function fileToBlob(filePath) {
  const bytes = await fs.readFile(filePath);
  return new Blob([bytes], { type: 'application/octet-stream' });
}

async function buildFormData(action, args) {
  const form = new FormData();
  form.set('model', toFormField(resolveModel(action, args)));

  if (args.prompt) {
    form.set('prompt', args.prompt);
  }
  if (args.size) {
    form.set('size', args.size);
  }
  if (args.n !== undefined) {
    form.set('n', String(args.n));
  }
  if (args.responseFormat || args['response-format']) {
    form.set('response_format', args.responseFormat || args['response-format']);
  } else {
    form.set('response_format', DEFAULT_RESPONSE_FORMAT);
  }
  if (args.user) {
    form.set('user', args.user);
  }

  if (action === 'generate') {
    return form;
  }

  const images = args.image || [];
  if (images.length !== 1) {
    throw new Error(`Expected exactly one --image for ${action}`);
  }

  const absolute = path.resolve(images[0]);
  const blob = await fileToBlob(absolute);
  form.append('image', blob, path.basename(absolute));

  if (action === 'edit' && args.mask) {
    const absoluteMask = path.resolve(args.mask);
    const maskBlob = await fileToBlob(absoluteMask);
    form.append('mask', maskBlob, path.basename(absoluteMask));
  }

  return form;
}

async function fetchImagePayload(baseUrl, apiKey, endpoint, form) {
  const response = await fetch(`${baseUrl}${endpoint}`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${apiKey}`,
    },
    body: form,
  });

  const contentType = response.headers.get('content-type') || '';
  const text = await response.text();
  let payload;
  if (contentType.includes('application/json')) {
    payload = JSON.parse(text);
  } else {
    try {
      payload = JSON.parse(text);
    } catch {
      payload = { raw: text };
    }
  }

  if (!response.ok) {
    const message = payload?.error?.message || payload?.message || text || response.statusText;
    throw new Error(`Request failed (${response.status}): ${message}`);
  }

  return payload;
}

async function writeOutputFile(outputDir, prefix, index, source) {
  await fs.mkdir(outputDir, { recursive: true });
  const fileName = `${prefix || 'image'}-${String(index + 1).padStart(2, '0')}.png`;
  const filePath = path.join(outputDir, fileName);
  await fs.writeFile(filePath, source);
  return filePath;
}

function guessExtension(value) {
  if (!value || typeof value !== 'string') {
    return '.png';
  }
  try {
    const parsed = new URL(value);
    const ext = path.extname(parsed.pathname);
    return ext || '.png';
  } catch {
    return '.png';
  }
}

async function saveResponse(payload, args) {
  const outputDir = args.outputDir || args['output-dir'];
  const outputPrefix = args.outputPrefix || args['output-prefix'];
  const data = Array.isArray(payload?.data) ? payload.data : [];

  if (data.length === 0) {
    return { saved: [], payload };
  }

  const saved = [];
  for (let i = 0; i < data.length; i += 1) {
    const item = data[i];
    if (item.url) {
      if (!outputDir) continue;
      const response = await fetch(item.url);
      if (!response.ok) {
        throw new Error(`Failed to download image ${item.url}: ${response.status} ${response.statusText}`);
      }
      const buffer = Buffer.from(await response.arrayBuffer());
      const extension = guessExtension(item.url);
      const fileName = `${outputPrefix || 'image'}-${String(i + 1).padStart(2, '0')}${extension}`;
      const filePath = path.join(outputDir, fileName);
      await fs.mkdir(outputDir, { recursive: true });
      await fs.writeFile(filePath, buffer);
      saved.push(filePath);
      continue;
    }

    if (item.b64_json) {
      if (!outputDir) continue;
      const buffer = Buffer.from(item.b64_json, 'base64');
      saved.push(await writeOutputFile(outputDir, outputPrefix, i, buffer));
    }
  }

  return { saved, payload };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const action = args._[0];

  if (args.help || !action) {
    usage();
    process.exitCode = 0;
    return;
  }

  if (!['generate', 'edit', 'variation'].includes(action)) {
    throw new Error(`Unknown action: ${action}`);
  }

  const baseUrl = normalizeBaseUrl(args.baseUrl || args['base-url'] || process.env.NEWAPI_BASE_URL);
  const apiKey = ensureRequired(args.apiKey || args['api-key'] || process.env.NEWAPI_API_KEY, 'NEWAPI_API_KEY');

  if (action !== 'generate') {
    if ((args.image || []).length !== 1) {
      throw new Error(`Expected exactly one --image for ${action}`);
    }
  }

  if (action === 'generate') {
    ensureRequired(args.prompt, '--prompt');
  } else if (action === 'edit') {
    ensureRequired(args.prompt, '--prompt');
  }

  const form = await buildFormData(action, args);
  const endpoint = action === 'generate'
    ? '/v1/images/generations'
    : action === 'edit'
      ? '/v1/images/edits'
      : '/v1/images/variations';

  const payload = await fetchImagePayload(baseUrl, apiKey, endpoint, form);
  const result = await saveResponse(payload, args);

  console.log(JSON.stringify({
    action,
    endpoint,
    saved: result.saved,
    response: payload,
  }, null, 2));
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
});
