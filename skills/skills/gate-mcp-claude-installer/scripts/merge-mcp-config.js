#!/usr/bin/env node
/**
 * Merge MCP server fragments (JSON objects keyed by server name) into existing config.
 * Usage: node merge-mcp-config.js <existingJsonPath> <outPath> <fragment.json> [...]
 * If env GATE_USER_API_KEY is set, overwrites Gate.env credentials (GATE_API_SECRET from GATE_USER_API_SECRET).
 */
const fs = require('fs');

function readExisting(path) {
  try {
    const raw = fs.readFileSync(path, 'utf8');
    if (!raw.trim()) return {};
    return JSON.parse(raw);
  } catch {
    return {};
  }
}

const existingPath = process.argv[2];
const outPath = process.argv[3];
const fragmentPaths = process.argv.slice(4).filter(Boolean);

if (!existingPath || !outPath) {
  console.error('Usage: node merge-mcp-config.js <existingJsonPath> <outPath> <fragment.json> [...]');
  process.exit(1);
}

const add = {};
for (const p of fragmentPaths) {
  let raw;
  try {
    raw = fs.readFileSync(p, 'utf8');
  } catch (e) {
    console.error(`merge-mcp-config: cannot read fragment: ${p}`);
    process.exit(1);
  }
  let j;
  try {
    j = JSON.parse(raw);
  } catch (e) {
    console.error(`merge-mcp-config: invalid JSON in fragment: ${p}`);
    process.exit(1);
  }
  Object.assign(add, j);
}

if (add.Gate && add.Gate.env && process.env.GATE_USER_API_KEY) {
  add.Gate.env.GATE_API_KEY = process.env.GATE_USER_API_KEY;
  add.Gate.env.GATE_API_SECRET = process.env.GATE_USER_API_SECRET || '';
}

const existing = readExisting(existingPath);
existing.mcpServers = existing.mcpServers || {};
Object.assign(existing.mcpServers, add);
fs.writeFileSync(outPath, JSON.stringify(existing, null, 2));
