# The buyer signs only when all required fields match the pinned intent

## Status and date

accepted, 2026-10-06

## Context

My buyer holds a key that can pay. Gecko prepares the bytes; I sign them. A wrong purchase could move tokens to the wrong destination, pay the wrong amount, buy the wrong product, or use the wrong mint.

The most concrete devnet incident was the quantity card: the intent asked for 2 Espresso units while the prepared purchase contained 1. The buyer refused before signing.

## Decision

Before signing, the buyer compares these fields of the prepared transaction with the pinned intent and refuses on the first mismatch, naming the field and both values:

| Field | Compared how | Why this one |
|---|---|---|
| program | address equality and program-account structure | Prevents signing a purchase involving the wrong program |
| store | address derived from `['receipts', name]` | Prevents silently paying a different store |
| product | exact product-name equality | Prevents buying a different item |
| price_raw | integer, at or under the pinned budget | Prevents paying more than requested |
| mint | exact mint address | Prevents paying with a different token |
| quantity | exact integer equality | Prevents buying a different amount |
| destination | store authority's token account for the pinned mint | Prevents paying the wrong token account |
| signed bytes | `verify_signed_transaction` before `submit_transaction` | Prevents broadcasting bytes that differ from the checked transaction |

## What this forbids

Signing on a partial match, retrying a refusal unchanged, signing without a passed simulation, submitting bytes different from the prepared bytes, and signing expired transaction bytes.

## What I left out, and why

I do not independently check every account or instruction field that Gecko exposes. I focus the buyer's explicit checks on the fields that define the user's purchase intent and the safety boundary around signing. The risk accepted is that a field outside this set could be wrong without being identified by one of these intent checks.

## What would reverse this

If Gecko's verification or a future audited binding were proven to cryptographically and semantically cover one of these checks, with evidence that the guarantee is equivalent to the buyer's requirement, I would consider removing the duplicate check. I would not remove it based only on documentation or a single successful transaction.

## What this does not prove

That my pin was right. The buyer faithfully checks and signs the request that I pinned.
