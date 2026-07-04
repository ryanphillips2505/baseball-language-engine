from __future__ import annotations

from dataclasses import asdict, is_dataclass
from html import escape
from pprint import pformat

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

from assemblers.plate_appearance_builder import build_plate_appearance
from detectors.event_detector import detect_event_types
from aggregators.game_stat_aggregator import _effective_ball_type


app = FastAPI(title="BLE Developer Console")


def _safe(value) -> str:
    return escape(str(value))


def _event_name(event) -> str:
    if event is None:
        return "None"

    return str(getattr(event, "value", event))


def _pa_dict(pa) -> str:
    try:
        if is_dataclass(pa):
            return pformat(asdict(pa), width=100)
    except Exception:
        pass

    return pformat(pa.__dict__, width=100)


def _aggregation_reason(pa, effective_ball_type: str | None) -> str:
    original = pa.ball_type
    location = pa.location
    event = pa.baseball_event.primary_event if pa.baseball_event else None

    if original == effective_ball_type:
        return "No conversion"

    if original == "BUNT" and effective_ball_type == "GB":
        return "Legacy conversion: ordinary bunt ground out counts as GB"

    if original == "BUNT" and effective_ball_type == "FB" and location == "C":
        return "Legacy conversion: bunt out handled by catcher counts as FB-C"

    return f"Converted from {original} to {effective_ball_type} by aggregation rule"


def _stat_lines(pa) -> list[str]:
    lines = []

    effective_ball_type = _effective_ball_type(pa)

    if pa.is_bip:
        lines.append("+1 BIP")

    if effective_ball_type:
        lines.append(f"+1 {effective_ball_type}")

    if pa.location:
        lines.append(f"+1 {pa.location}")

    if effective_ball_type and pa.location:
        lines.append(f"+1 {effective_ball_type}-{pa.location}")

    for runner_event in pa.runner_events:
        lines.append(f"+1 {runner_event.event_type}-{runner_event.base}")

    return lines


def _inspect_play(raw_play: str) -> str:
    detected_events = detect_event_types(raw_play)
    pa = build_plate_appearance(raw_play)

    primary_event = pa.baseball_event.primary_event if pa.baseball_event else None
    secondary_events = pa.baseball_event.secondary_events if pa.baseball_event else []
    effective_ball_type = _effective_ball_type(pa)

    stats = _stat_lines(pa)
    reason = _aggregation_reason(pa, effective_ball_type)

    detected_html = "\n".join(
        f"- {_event_name(event.event_type)}" for event in detected_events
    ) or "None"

    secondary_html = "\n".join(
        f"- {_event_name(event.event_type)}" for event in secondary_events
    ) or "None"

    runner_html = "\n".join(
        f"- {r.event_type} {r.base} {r.runner_name or ''}".strip()
        for r in pa.runner_events
    ) or "None"

    return f"""
    <div class="play-card">
      <div class="raw">{escape(raw_play)}</div>

      <div class="grid">
        <div><b>Batter</b><span>{_safe(pa.batter_name)}</span></div>
        <div><b>Primary Event</b><span>{_safe(_event_name(primary_event))}</span></div>
        <div><b>BIP</b><span>{pa.is_bip}</span></div>
        <div><b>Original Ball Type</b><span>{_safe(pa.ball_type)}</span></div>
        <div><b>Effective Ball Type</b><span>{_safe(effective_ball_type)}</span></div>
        <div><b>Location</b><span>{_safe(pa.location)}</span></div>
      </div>

      <div class="two-col">
        <div class="panel">
          <h3>Detected Events</h3>
          <pre>{escape(detected_html)}</pre>
        </div>

        <div class="panel">
          <h3>Secondary Events</h3>
          <pre>{escape(secondary_html)}</pre>
        </div>
      </div>

      <div class="two-col">
        <div class="panel">
          <h3>Runner Events</h3>
          <pre>{escape(runner_html)}</pre>
        </div>

        <div class="panel">
          <h3>Final Stat Mapping</h3>
          <pre>{escape(chr(10).join(stats) if stats else "No stats")}</pre>
        </div>
      </div>

      <div class="panel">
        <h3>Aggregation Decision</h3>
        <pre>Original:  {escape(str(pa.ball_type))}
Effective: {escape(str(effective_ball_type))}
Reason:    {escape(reason)}</pre>
      </div>

      <details>
        <summary>Full PlateAppearance Object</summary>
        <pre>{escape(_pa_dict(pa))}</pre>
      </details>
    </div>
    """


CSS = """
<style>
  body { font-family: Arial, sans-serif; background: #f4f6f8; margin: 0; padding: 24px; color: #111827; }
  h1 { margin-top: 0; }
  textarea { width: 100%; height: 280px; font-size: 14px; padding: 12px; }
  button { margin-top: 12px; padding: 10px 18px; font-weight: 800; cursor: pointer; }
  a { font-weight: 800; color: #065f46; }
  .play-card { background: white; border: 1px solid #d1d5db; border-radius: 12px; padding: 16px; margin: 16px 0; }
  .raw { font-weight: 900; margin-bottom: 12px; font-size: 15px; }
  .grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 10px; margin-bottom: 12px; }
  .grid div, .panel { background: #f9fafb; padding: 10px; border-radius: 8px; border: 1px solid #e5e7eb; }
  .grid b { display: block; font-size: 11px; color: #6b7280; margin-bottom: 4px; text-transform: uppercase; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 12px 0; }
  h3 { margin: 0 0 8px 0; font-size: 13px; text-transform: uppercase; color: #374151; }
  pre { background: #111827; color: white; padding: 10px; border-radius: 8px; overflow-x: auto; white-space: pre-wrap; }
  summary { cursor: pointer; font-weight: 900; margin-top: 12px; }
</style>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
    <head>
      <title>BLE Developer Console</title>
      {CSS}
    </head>
    <body>
      <h1>BLE Developer Console</h1>
      <form method="post" action="/inspect">
        <textarea name="raw_text" placeholder="Paste raw plays here, one play per line..."></textarea>
        <br>
        <button type="submit">Inspect Plays</button>
      </form>
    </body>
    </html>
    """


@app.post("/inspect", response_class=HTMLResponse)
def inspect(raw_text: str = Form(...)):
    plays = [line.strip() for line in raw_text.splitlines() if line.strip()]
    cards = "\n".join(_inspect_play(play) for play in plays)

    return f"""
    <html>
    <head>
      <title>BLE Developer Console</title>
      {CSS}
    </head>
    <body>
      <a href="/">← Back</a>
      <h1>Inspection Results</h1>
      {cards}
    </body>
    </html>
    """
