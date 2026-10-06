# Evaluation report

## The five cases and the trap

| # | Ask | Expected | Recorded | Devnet | Evidence |
|---|---|---|---|---|---|
| 1 | one espresso | lands, receipt reconciles | pass | pass | `receipts/3SgWuQiD.md` |
| 2 | one general-admission ticket | refuse on `product` | pass | not run | `smoke-report.recorded.json` |
| 3 | module 3, paid in USDC | refuse on `mint` | pass | not run | `smoke-report.recorded.json` |
| 4 | tip up to 2 USDC | refuse on `price_raw` | pass | not run | `smoke-report.recorded.json` |
| 5 | two bags of beans | refuse on `quantity` | pass | not run | `smoke-report.recorded.json` |
| trap | one latte | refuse on `price_raw` | pass | not run | `smoke-report.recorded.json` |

Recorded smoke: **6/6 matches** — one landing and five refusals.

The recorded command was:

`GECKO_SOURCE=recorded uv run buyer --cases --json smoke-report.recorded.json`

The live devnet purchase was:

`uv run buyer "one espresso" --devnet`

Transaction:

`3SgWuQiDppcuM144WDsV97A2e2vEZqSYLmkMoGDvmAATM8hcUXgeiztSbgMx27smKS1VaR6ZFJQreYZ7mXEKVpUi`

## The four Friday cards

| Card | Expected | Result | Evidence |
|---|---|---|---|
| quantity | refuse on `quantity` | pass | `refusals/20261006T051807.718569-quantity.json` |
| budget | refuse on `price_raw` | pass | `refusals/20261006T051859.322730-price-raw.json` |
| tampered bytes | verify refuses, nothing submitted | pass | `refusals/20261006T051952.606572-signed-bytes.json` |
| stale bytes | signer refuses, nothing signed | pass | `refusals/20261006T052123.685782-blockhash.json` |

All four cards were run against the live devnet buyer on 2026-10-06.

## Tests

`uv run pytest -q`: **80 passed, 1 failed, 2 skipped**.

The only failure is the Windows-only mainnet wallet permission assertion:

`test_create_makes_a_600_key_outside_the_repo_and_prints_only_the_address`

The test expects mode `0600`, while Windows reports the created file as mode `0666`. The signer tests themselves pass.

## Receipts reconciled with the ledger

The committed devnet receipt records:

- buyer delta: `-1000000`
- store delta: `+1000000`
- `total_purchases`: `0 -> 1`
- explorer transaction: `3SgWuQiDppcuM144WDsV97A2e2vEZqSYLmkMoGDvmAATM8hcUXgeiztSbgMx27smKS1VaR6ZFJQreYZ7mXEKVpUi`

The purchase landed successfully and the receipt was written from the ledger read.

## What this does not prove

- This evaluation is primarily against Solana devnet, not mainnet.
- The recorded six-case suite proves the refusal logic against its fixtures, not network behavior.
- One successful purchase does not prove every possible product, quantity, or transaction shape.
- The buyer checks the request against its own pinned intent, so a wrong pin can still be followed faithfully.
