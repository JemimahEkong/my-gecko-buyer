# The defence: Friday 2 October, six minutes

One design rule: everything I show ends in a **receipt** (it landed, and this is what moved) or a **refusal** (it did not sign, and this is the field that disagreed).

## The six minutes

| Min | On screen | Backed by | What I say |
|---|---|---|---|
| 0:00 | README first lines and explorer link | `README.md` | This buyer pins the request before Gecko prepares bytes, checks the prepared purchase field by field, signs only after the checks pass, and reconciles the landing from the ledger. |
| 0:45 | My Gecko store and store config | `store/store.json` | This is my own devnet store, `dev3jemimahekong`. The store address is derived from the program and store name rather than hard-coded. |
| 1:30 | Live buy | `uv run buyer "one espresso" --devnet` | The buyer pins one Espresso with a 2,000,000 raw-unit budget, prepares and simulates the purchase, checks every required field, signs, verifies, submits, and reads the receipt. |
| 2:30 | Explorer and committed receipt | `receipts/3SgWuQiD.md` | The transaction landed. The receipt shows the buyer moved 1,000,000 raw units, the store received 1,000,000, and `total_purchases` changed from 0 to 1. |
| 3:15 | Injected failure card | `refusals/` | The important part is not only that a purchase can land. These cards prove the buyer can refuse. Quantity, budget, tampered bytes, and stale bytes all refused before an invalid submission. |
| 4:30 | Tests and evaluation table | `docs/EVAL_REPORT.md` | The recorded six-case suite is 6/6. The four injected devnet cards also passed. There is one known Windows permission-test failure, which is documented rather than hidden. |
| 5:15 | ADR | `docs/adr/0001-refusals-before-signing.md` | The design decision is to refuse before signing whenever a required purchase field disagrees with the pinned intent, and to verify the exact signed bytes before submission. |

## The four cards

| Card | Command | Expected result | Evidence |
|---|---|---|---|
| **Quantity** | `uv run buyer "two espressos" --devnet` | `quantity`: asked 2, prepared 1 | `refusals/20261006T051807.718569-quantity.json` |
| **Budget** | `uv run buyer "one espresso" --budget-raw 500000 --devnet` | `price_raw`: asked at most 500000, prepared 1000000 | `refusals/20261006T051859.322730-price-raw.json` |
| **Tampered bytes** | `uv run buyer "one espresso" --devnet --card tampered` | `signed bytes` verification refuses; nothing submitted | `refusals/20261006T051952.606572-signed-bytes.json` |
| **Stale bytes** | `uv run buyer "one espresso" --devnet --card stale` | `blockhash` refuses; nothing signed | `refusals/20261006T052123.685782-blockhash.json` |

## If the network is down

Use the recorded lane:

```bash
GECKO_SOURCE=recorded uv run buyer "one espresso" --devnet
I would say clearly that this is a recorded fallback, not a live transaction.

Questions I should be ready for
How do you know the purchase landed?

The receipt was read from the ledger after submission. It records the transaction signature, explorer link, buyer and store deltas, and total_purchases moving from 0 to 1.

What does the receipt not prove?

It proves what moved on-chain. It does not prove that the original request was correct. That is why the intent is pinned before preparation and compared field by field.

Why does Gecko not hold the key?

The signing key stays on my machine. Gecko prepares and verifies transaction bytes, but the buyer signs locally.

Which check would you drop first?

I would not drop one just because it has not failed yet. I would remove a duplicate only if Gecko provided an independently verified guarantee equivalent to that check.

What would change your ADR?

Evidence that a particular field is already cryptographically and semantically bound by a stronger verified guarantee could justify removing a duplicate check.

What breaks it?

A wrong pinned intent can still be faithfully executed. The buyer protects the boundary between the pinned request and prepared bytes; it cannot know that the human's original request was sensible.

Before the defence
 One devnet receipt is committed.
 Recorded six-case suite is 6/6.
 Four live devnet failure cards were exercised.
 Four refusal artifacts are present.
 Mainnet key material is outside the repository.What would change your ADR?

Evidence that a particular field is already cryptographically and semantically bound by a stronger verified guarantee could justify removing a duplicate check.

What breaks it?

A wrong pinned intent can still be faithfully executed. The buyer protects the boundary between the pinned request and prepared bytes; it cannot know that the human's original request was sensible.

Before the defence
 One devnet receipt is committed.
 Recorded six-case suite is 6/6.
 Four live devnet failure cards were exercised.
 Four refusal artifacts are present.
 Mainnet key material is outside the repository.
 Rehearse the six-minute script once with a timer.
