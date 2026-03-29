"""
Live runner — calls a real LLM API with the agent or sub-agent system prompt.

Execution is controlled by the --live pytest flag (or LIVE_LLM=true env var).
When neither is set this module is never imported at runtime, so missing API
client packages do not cause errors in stub mode.

Supported providers (auto-detected from the model name):
  - openai  : requires OPENAI_API_KEY  (gpt-*, o1-*, o3-*)
  - anthropic: requires ANTHROPIC_API_KEY (claude-*)

The agent system prompt is extracted from the body of the agent.md /
sub-agent.md file (everything after the YAML frontmatter fence).
"""
from __future__ import annotations

import os
import pathlib
import textwrap

import frontmatter  # python-frontmatter


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]


def _normalize_slug(text: str) -> str:
    """Normalize a name/ref string to a slug for comparison."""
    return text.lower().replace(" ", "-").replace(".", "")


def _load_spec(kind: str, ref: str) -> tuple[dict, str]:
    """Return (frontmatter_dict, body_text) for the named agent/sub-agent.

    Matches *ref* against both the spec folder name and the frontmatter `name`
    field so that aliases like "Velocity" (folder: scrum-master-coach) resolve
    correctly.
    """
    slug = _normalize_slug(ref)

    if kind == "agent":
        search_root = _REPO_ROOT / "agents"
        filename = "agent.md"
    else:
        search_root = _REPO_ROOT / "sub-agents"
        filename = "sub-agent.md"

    # Match by folder name first, then fall back to frontmatter `name` field
    # (same aliases accepted by the CI validator).
    for path in search_root.rglob(filename):
        folder_slug = _normalize_slug(path.parent.name)
        try:
            post = frontmatter.load(str(path))
        except Exception:  # noqa: BLE001
            continue
        fm_name_slug = _normalize_slug(post.metadata.get("name", ""))
        if folder_slug == slug or fm_name_slug == slug:
            return dict(post.metadata), post.content

    raise FileNotFoundError(
        f"Could not locate spec for {kind} {ref!r} "
        f"(searched {search_root} for slug {slug!r})"
    )


def _build_system_prompt(metadata: dict, body: str) -> str:
    """Combine frontmatter description with the markdown body."""
    description = metadata.get("description", "")
    lines = [
        "You are an AI agent. Follow the specification below exactly.",
        "",
        f"Name: {metadata.get('name', 'Assistant')}",
    ]
    if description:
        lines += ["", f"Description: {description}"]
    lines += ["", "---", "", textwrap.dedent(body).strip()]
    return "\n".join(lines)


def _pick_model(metadata: dict, case: dict) -> str:
    """Choose the model to use: case override > spec primary model > fallback."""
    override = (case.get("input") or {}).get("model")
    if override:
        return override
    # Prefer new-style specs: metadata['model_recommendations']['primary']
    model_recs = metadata.get("model_recommendations", {}) or {}
    primary = model_recs.get("primary")
    if primary:
        return primary
    # Backward compatibility: older specs may use metadata['models']['primary']
    models = metadata.get("models", {}) or {}
    return models.get("primary", "gpt-4o-mini")


# ---------------------------------------------------------------------------
# Provider clients
# ---------------------------------------------------------------------------

def _call_openai(model: str, system_prompt: str, user_message: str) -> str:
    import openai  # noqa: PLC0415  (defer import)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. "
            "Export it before running with --live."
        )
    client = openai.OpenAI(api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0,
    )
    return resp.choices[0].message.content or ""


def _call_anthropic(model: str, system_prompt: str, user_message: str) -> str:
    import anthropic  # noqa: PLC0415  (defer import)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY is not set. "
            "Export it before running with --live."
        )
    client = anthropic.Anthropic(api_key=api_key)
    resp = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return resp.content[0].text if resp.content else ""


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

def run_live(case: dict) -> str:
    """Call the LLM and return the raw response string."""
    target = case["target"]
    kind = target["kind"]
    ref = target["ref"]

    metadata, body = _load_spec(kind, ref)
    system_prompt = _build_system_prompt(metadata, body)
    model = _pick_model(metadata, case)

    input_data = case.get("input", {})
    user_text = input_data.get("user", "")
    context_text = input_data.get("context", "")
    if context_text:
        user_text = f"{user_text}\n\nContext: {context_text}"

    if model.startswith("claude"):
        return _call_anthropic(model, system_prompt, user_text)
    return _call_openai(model, system_prompt, user_text)
