# Issues

## 2026-10-06: A requested quantity did not match the prepared purchase

- **What I saw:** `REFUSED on quantity: asked 2, prepared 1` from `uv run buyer "two espressos" --devnet`.
- **What was actually wrong:** Gecko prepared one Espresso even though the pinned intent requested two.
- **How I found it:** The `quantity` check compared the pinned intent with the prepared transaction before signing.
- **What I changed:** The check already enforced exact quantity equality; I captured the refusal in `refusals/20261006T051807.718569-quantity.json`.
- **What it cost:** No SOL or token transfer. Nothing was signed.
- **Would the checks have caught it?** Yes. The `quantity` check caught it before signing.

## 2026-10-06: The prepared price exceeded the pinned budget

- **What I saw:** `REFUSED on price_raw: asked 'at most 500000', prepared 1000000` from `uv run buyer "one espresso" --budget-raw 500000 --devnet`.
- **What was actually wrong:** The Espresso cost 1,000,000 raw units while the pinned budget was 500,000.
- **How I found it:** The `price_raw` check compared the prepared price with the pinned budget.
- **What I changed:** The existing budget check correctly refused the purchase; I captured the refusal in `refusals/20261006T051859.322730-price-raw.json`.
- **What it cost:** No SOL or token transfer. Nothing was signed.
- **Would the checks have caught it?** Yes. The `price_raw` check caught it before signing.

## 2026-10-06: Signed bytes no longer matched the checked bytes

- **What I saw:** `REFUSED on signed bytes` after the tampered card changed one byte of the signed transaction.
- **What was actually wrong:** The bytes presented to verification were different from the prepared bytes that had passed the checks.
- **How I found it:** `verify_signed_transaction` rejected the changed bytes because they no longer matched the binding.
- **What I changed:** The verification step remains mandatory before submission; the incident is recorded in `refusals/20261006T051952.606572-signed-bytes.json`.
- **What it cost:** A signature was produced for the tampered test, but nothing was submitted and no purchase landed.
- **Would the checks have caught it?** Yes. The signed-bytes verification caught it after signing and before submission.

## 2026-10-06: Prepared bytes expired before signing

- **What I saw:** `REFUSED on blockhash: asked 'height <= 495228158', signer 495228176`.
- **What was actually wrong:** The prepared transaction had passed its valid block-height window before signing.
- **How I found it:** The signer checked the current block height against the transaction's last valid block height.
- **What I changed:** The signer refuses stale bytes and requires a fresh prepare rather than re-signing expired bytes. The incident is recorded in `refusals/20261006T052123.685782-blockhash.json`.
- **What it cost:** No SOL or token transfer. Nothing was signed.
- **Would the checks have caught it?** Yes. The signer caught the expired `blockhash` before signing.
