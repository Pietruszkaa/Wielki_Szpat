# Wielki_Szpat 🤖

Discord bot project — from learning playground to full-featured, production-ready monster.

Projekt rozwijany etapami, z naciskiem na czystą architekturę, skalowalność i naukę poprzez praktykę.

## 🇵🇱 Opis projektu

Wielki_Szpąt to bot Discord tworzony w Pythonie (discord.py), który powstaje krok po kroku — od prostych eventów i komend, aż po w pełni konfigurowalny, multi-serwerowy system z panelem webowym.

Projekt nie jest „gotowym botem” — to świadomie rozwijany system, który:

rośnie wersja po wersji

zmienia architekturę w trakcie rozwoju

służy jako narzędzie do nauki (reverse engineering + refactor)

Celem jest dojście do V1.0, gdzie bot będzie:

stabilny

modularny

konfigurowalny per-serwer

gotowy pod Docker + hosting produkcyjny

## 🇬🇧 Project overview

Wielki_Szpąt is a Discord bot written in Python (discord.py), developed incrementally — from simple event handlers to a fully modular, multi-guild, production-ready system.

This is not a plug-and-play bot.
It is a long-term learning project focused on:

clean architecture

scalability

real-world Discord API constraints

learning by refactoring and rebuilding

The end goal is V1.0, where the bot will be:

stable

modular

per-guild configurable

Docker-ready and production-friendly

## Current direction ("Road to V1")

Architecture goals

Multi-guild (per Discord server)

Config-driven behavior (JSON)

Hot-reloadable configuration

Modular Cogs

Separation of concerns (core / cogs / utils)

## Planned features

Welcome / Goodbye system (GIFs, embeds)

Member counter (Discord API–safe)

Minecraft server status (live embed)

Moderation tools (later versions)

Slash commands

Web dashboard (FastAPI + OAuth2)

## Configuration philosophy

The bot uses a single JSON config file with:

global defaults

per-guild overrides

### Example concept:

{
  "defaults": { ... },
  "guilds": {
    "123456789": { ... }
  }
}

Every guild automatically gets a config entry on join

Defaults are inherited dynamically

Only overrides are stored per guild

This makes the system:

easy to extend

safe to reload

future-proof for databases and dashboards

## Development philosophy

This project embraces:

refactoring over rewriting

learning by breaking things

gradual improvement instead of premature perfection

# Expect:

breaking changes between versions

architecture changes

rewritten systems

That is intentional.

## Status

### In active development

Current focus:

Multi-guild refactor

Config validation

Hot reload system

## Docker Deployment (planned)

Docker-ready image

.env for secrets

JSON / DB for config

Ubuntu Server hosting

## License

MIT — do whatever you want, but don’t blame the bot if it becomes a monster.

❤️ Author notes

This project is built as much for learning as for functionality.
If you’re reading this while learning Python, Discord bots, or system design — you’re exactly the target audience.

From chaos to architecture.