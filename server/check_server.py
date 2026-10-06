"""MCP server that checks a prepared purchase against a pinned intent."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from mcp.server.mcpserver import MCPServer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from buyer.check import check_all
from buyer.intent import IntentRecord
from buyer.prepared import Prepared
from server.guard import is_public_url


server = MCPServer("gecko-check-server")


@server.tool()
def check_purchase(
    intent: dict[str, Any],
    prepared_answer: dict[str, Any],
    rpc_url: str | None = None,
) -> dict[str, Any]:
    """Check a prepared purchase against the buyer's pinned intent."""

    if rpc_url is not None and not is_public_url(rpc_url):
        return {
            "passed": False,
            "refused": True,
            "field": "rpc_url",
            "asked": "public HTTPS URL",
            "prepared": rpc_url,
            "stage": "guard",
            "note": "rpc_url is not a public HTTPS URL",
        }

    pinned = IntentRecord(**intent)
    prepared = Prepared.from_answer(prepared_answer)
    verdict = check_all(pinned, prepared)

    return {
        "passed": verdict.passed,
        "refused": not verdict.passed,
        "results": [
            {
                "field": result.field,
                "passed": result.passed,
                "expected": result.expected,
                "actual": result.actual,
                "stage": result.stage,
                "note": result.note,
            }
            for result in verdict.results
        ],
    }


if __name__ == "__main__":
    server.run()