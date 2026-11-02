# Gate CEX Bot

Source instructions for official recommendations and eight bot products. The entry point routes to action contracts, request models and shared execution rules.

Maintainers build with `python3 scripts/build_cex_bot.py --output <new-parent>/gate-cex-bot` from a checkout with scripts/requirements-cex.txt installed. This delegates to the canonical CEX validator/builder and publishes a standalone package only after source and package checks pass. Engineering provenance and integration evidence stay outside the runtime package. Existing output directories are never overwritten.
