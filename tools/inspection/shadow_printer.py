from __future__ import annotations

from .shadow_builder import build_shadow_result


def print_shadow_report(results) -> None:

    report = build_shadow_result(results)

    print("=" * 80)
    print("BLE SHADOW MODE")
    print("=" * 80)

    print(f"Players        : {report.summary.total_players}")
    print(f"Stats Compared : {report.summary.total_stats}")
    print(f"Matched        : {report.summary.matched}")
    print(f"Mismatched     : {report.summary.mismatched}")
    print(f"Match %        : {report.summary.percent_match}%")
    print()

    if report.ready_for_production:
        print("STATUS : READY FOR OPPONENT IQ")
    else:
        print("STATUS : KEEP USING LEGACY PARSER")
