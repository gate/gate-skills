# Gate Info Liveroom Location (gate-info-liveroomlocation)

## Overview

An AI Agent skill that returns a filtered list of live streams and replays on Gate by business type (tag), coin, sort (hottest/newest), and count. One API call returns a list; each item is title + link. Missing parameters use defaults; do not ask the user for them.

## Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| **List by tag** | Filter by business type: Market Analysis, Hot Topics, Blockchain, Others | "Hottest market analysis live rooms" |
| **List by coin** | Filter by coin (e.g. BTC, SOL) | "5 SOL-related hottest lives" |
| **Sort and limit** | Sort by hot or new; limit 1–10 (default 10) | "Latest 5 replays" |
| **Title + link output** | Each item: title (live.name or video.title) plus Gate link; no extra fields | Single API; list only |

## Architecture

- **API**: `GET /live/gate_ai/tag_coin_live_replay` with query params: tag, coin, sort, limit.
- **Output**: List of lines: title + link (streaming: `https://www.gate.io/live/video/{id}?type=live`, video: `https://www.gate.io/live/video/{id}`).
- **Restricted regions**: Do not call the API; reply that the feature is not available.
- **No MCP**: This skill uses HTTP only; no MCP dependency.

## Source

- **Repository**: [github.com/gate/gate-skills](https://github.com/gate/gate-skills)
- **Publisher**: [Gate.com](https://www.gate.com)
