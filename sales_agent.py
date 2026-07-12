from __future__ import annotations

import argparse
import csv
import json
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib import error, request
from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from anthropic import Anthropic


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Novelle outreach sales agent powered by Claude."
    )
    parser.add_argument(
        "--leads",
        default="leads.sample.csv",
        help="CSV file with lead data.",
    )
    parser.add_argument(
        "--strategy-file",
        default="OUTREACH-STRATEGY.md",
        help="Path to outreach strategy markdown used as core guidance.",
    )
    parser.add_argument(
        "--output",
        default="outreach_results.json",
        help="Path to output JSON file.",
    )
    parser.add_argument(
        "--model",
        default="claude-opus-4-7",
        help="Claude model ID.",
    )
    parser.add_argument(
        "--max-leads",
        type=int,
        default=10,
        help="Maximum leads to process from the CSV.",
    )
    parser.add_argument(
        "--zapier-webhook-url",
        default=os.getenv("ZAPIER_WEBHOOK_URL", ""),
        help="Optional Zapier Catch Hook URL. If provided, each outreach record is POSTed to Zapier.",
    )
    return parser.parse_args()


def load_leads(leads_path: Path, max_leads: int) -> List[Dict[str, str]]:
    leads: List[Dict[str, str]] = []
    with leads_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(leads) >= max_leads:
                break
            leads.append({k: (v or "").strip() for k, v in row.items()})
    return leads


def build_user_prompt(lead: Dict[str, str]) -> str:
    return (
        "Create outreach for this lead:\n"
        f"- Name: {lead.get('name', '')}\n"
        f"- Role: {lead.get('role', '')}\n"
        f"- Company: {lead.get('company', '')}\n"
        f"- Company size: {lead.get('company_size', '')}\n"
        f"- Industry: {lead.get('industry', '')}\n"
        f"- Notes/signals: {lead.get('notes', '')}\n\n"
        "Return valid JSON with keys:\n"
        "- lead_score (0-100)\n"
        "- fit_tier (high_fit|qualified_with_conditions|disqualify)\n"
        "- angle (A|B|C|D)\n"
        "- subject\n"
        "- email_body\n"
        "- linkedin_connect_note\n"
        "- linkedin_first_dm\n"
        "- follow_ups (array of 2 concise follow-up messages)"
    )


def make_system_prompt(strategy_text: str) -> str:
    return (
        "You are the dedicated outreach sales agent for Novelle. "
        "Follow the strategy exactly and produce concise, practical outreach assets. "
        "Never fabricate proof or outcomes.\n\n"
        "Novelle strategy and positioning:\n"
        f"{strategy_text}\n\n"
        "Output must be strict JSON only."
    )


def generate_for_lead(
    client: "Anthropic",
    model: str,
    system_prompt: str,
    lead: Dict[str, str],
) -> Dict[str, Any]:
    response = client.messages.create(
        model=model,
        max_tokens=1600,
        thinking={"type": "adaptive"},
        cache_control={"type": "ephemeral"},
        system=system_prompt,
        messages=[{"role": "user", "content": build_user_prompt(lead)}],
    )
    text_blocks = [block.text for block in response.content if block.type == "text"]
    output_text = "\n".join(text_blocks).strip()
    parsed = json.loads(output_text)
    return {
        "lead": lead,
        "outreach": parsed,
    }

def post_to_zapier(webhook_url: str, payload: Dict[str, Any]) -> None:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        webhook_url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with request.urlopen(req, timeout=15) as response:
        status = getattr(response, "status", 200)
        if status >= 400:
            raise RuntimeError(f"Zapier webhook returned HTTP {status}")
def build_zapier_payload(record: Dict[str, Any]) -> Dict[str, Any]:
    lead = record.get("lead", {})
    outreach = record.get("outreach", {})

    now = datetime.now(timezone.utc)
    follow_ups_raw = outreach.get("follow_ups", [])
    follow_ups_normalized: List[Dict[str, Any]] = []
    default_day_offsets = [4, 10]

    for i, follow_up in enumerate(follow_ups_raw):
        day_offset = default_day_offsets[i] if i < len(default_day_offsets) else 10 + ((i - 1) * 7)
        scheduled_at = (now + timedelta(days=day_offset)).isoformat()
        if isinstance(follow_up, dict):
            follow_ups_normalized.append(
                {
                    "sequence": i + 1,
                    "day_offset": day_offset,
                    "scheduled_at": scheduled_at,
                    "subject": follow_up.get("subject", f"Follow-up {i + 1}: {outreach.get('subject', '')}"),
                    "body": follow_up.get("body", follow_up.get("message", "")),
                }
            )
        else:
            follow_ups_normalized.append(
                {
                    "sequence": i + 1,
                    "day_offset": day_offset,
                    "scheduled_at": scheduled_at,
                    "subject": f"Follow-up {i + 1}: {outreach.get('subject', '')}",
                    "body": str(follow_up),
                }
            )

    follow_up_1 = follow_ups_normalized[0] if len(follow_ups_normalized) > 0 else {}
    follow_up_2 = follow_ups_normalized[1] if len(follow_ups_normalized) > 1 else {}

    return {
        "source": "novelle-outreach-agent",
        "created_at": now.isoformat(),
        "zapier_event": "outreach_generated",
        "zapier_version": "v1",
        "lead_name": lead.get("name", ""),
        "lead_email": lead.get("email", ""),
        "lead_role": lead.get("role", ""),
        "lead_company": lead.get("company", ""),
        "lead_company_size": lead.get("company_size", ""),
        "lead_industry": lead.get("industry", ""),
        "lead_notes": lead.get("notes", ""),
        "lead_score": outreach.get("lead_score", ""),
        "fit_tier": outreach.get("fit_tier", ""),
        "outreach_angle": outreach.get("angle", ""),
        "outlook_to_email": lead.get("email", ""),
        "outlook_to_name": lead.get("name", ""),
        "outlook_subject": outreach.get("subject", ""),
        "outlook_body": outreach.get("email_body", ""),
        "linkedin_connect_note": outreach.get("linkedin_connect_note", ""),
        "linkedin_first_dm": outreach.get("linkedin_first_dm", ""),
        "followup_1_day_offset": follow_up_1.get("day_offset", ""),
        "followup_1_scheduled_at": follow_up_1.get("scheduled_at", ""),
        "followup_1_subject": follow_up_1.get("subject", ""),
        "followup_1_body": follow_up_1.get("body", ""),
        "followup_2_day_offset": follow_up_2.get("day_offset", ""),
        "followup_2_scheduled_at": follow_up_2.get("scheduled_at", ""),
        "followup_2_subject": follow_up_2.get("subject", ""),
        "followup_2_body": follow_up_2.get("body", ""),
        "lead": lead,
        "outreach": outreach,
        "outlook_draft": {
            "to_email": lead.get("email", ""),
            "to_name": lead.get("name", ""),
            "company": lead.get("company", ""),
            "subject": outreach.get("subject", ""),
            "body": outreach.get("email_body", ""),
        },
        "follow_up_plan": follow_ups_normalized,
    }


def main() -> None:
    args = parse_args()
    try:
        from anthropic import Anthropic
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Anthropic SDK is not installed. Run: python3 -m pip install -r requirements-agent.txt"
        ) from exc
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set.")

    leads_path = Path(args.leads)
    strategy_path = Path(args.strategy_file)
    output_path = Path(args.output)

    if not leads_path.exists():
        raise FileNotFoundError(f"Leads file not found: {leads_path}")
    if not strategy_path.exists():
        raise FileNotFoundError(f"Strategy file not found: {strategy_path}")

    strategy_text = strategy_path.read_text(encoding="utf-8")
    leads = load_leads(leads_path, max_leads=args.max_leads)

    client = Anthropic(api_key=api_key)
    results: List[Dict[str, Any]] = []
    webhook_url = args.zapier_webhook_url.strip()
    zapier_success = 0
    zapier_failed = 0
    for lead in leads:
        record = generate_for_lead(client, args.model, make_system_prompt(strategy_text), lead)
        results.append(record)

        if webhook_url:
            payload = build_zapier_payload(record)
            try:
                post_to_zapier(webhook_url, payload)
                zapier_success += 1
            except (error.URLError, RuntimeError) as exc:
                zapier_failed += 1
                print(f"Zapier delivery failed for {lead.get('name', 'unknown lead')}: {exc}")

    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Processed {len(results)} leads")
    print(f"Saved outreach output to {output_path}")
    if webhook_url:
        print(f"Zapier deliveries: success={zapier_success}, failed={zapier_failed}")


if __name__ == "__main__":
    main()
