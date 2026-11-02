# Portfolio request models

Read the selected product reference before forming a request. Fields here are business JSON fields for --json, not a body string wrapper. Amounts, prices and weights retain their decimal strings. Product minimums, leverage eligibility and available balances are backend constraints, not inferred defaults.

<a id="model-smartpositioncreaterequest"></a>
### SmartPositionCreateRequest

`strategy_type`: smart_position; `create_params`: object with `begin_money_amount`: positive string; `begin_money_currency`: USDT; `asset_info`: 2–10 unique entries of `asset`: string and `rate`: string totaling 1; exactly one of `period`: supported interval string or `threshold`: decimal ratio string. Optional `stop_profit`, `stop_loss`, `is_use_base`, `close_flag` follow [smart-position rules](../smart-position-commands.md). Do not add a top-level market to identify a multi-asset portfolio.

<a id="model-futurescombocreaterequest"></a>
### FuturesComboCreateRequest

`strategy_type`: futures_combo; `create_params`: object with `begin_money_amount`: positive string; `begin_money_currency`: USDT; `asset_info`: 2–10 unique entries of `market`: string, `side`: buy/sell and `rate`: string totaling 1; `leverage`: integer; exactly one of `period`: supported interval string or `threshold`: ratio string. Optional stop_profit/stop_loss, omission and explicit null semantics follow [futures-combo rules](../futures-combo-commands.md). Preserve every leg and its direction.

<a id="model-stopoptions"></a>
### StopOptions

For smart_position stop_mode=limit only: `price`: string price or supported expression; `expiration`: positive integer seconds; optional `slip`: decimal string ratio 0.001–0.05, at most six decimals. Modes market/no_close omit stop_options. Futures_combo uses the whole-portfolio stop and does not accept smart-position options.
