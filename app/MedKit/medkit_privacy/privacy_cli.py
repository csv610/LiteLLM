import argparse
import sys
import json
from pathlib import Path

# Add the project root to sys.path to support absolute imports
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

try:
    from .privacy_compliance import PrivacyManager
except (ImportError, ValueError):
    from privacy_compliance import PrivacyManager


def main():
    parser = argparse.ArgumentParser(description="MedKit Privacy & Compliance CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Consent
    subparsers.add_parser("consent", help="Display HIPAA consent form")

    # Audit
    audit_p = subparsers.add_parser("audit", help="Log an audit event")
    audit_p.add_argument("--session", required=True, help="Session ID")
    audit_p.add_argument("--action", required=True, help="Action performed")
    audit_p.add_argument("--role", default="patient", help="User role")
    audit_p.add_argument("--details", help="Event details")

    # Report
    subparsers.add_parser("report", help="Generate compliance report")

    # Mask
    mask_p = subparsers.add_parser("mask", help="Mask PII in text")
    mask_p.add_argument("text", help="Text to mask")

    # Detect
    detect_p = subparsers.add_parser("detect", help="Detect PII in text")
    detect_p.add_argument("text", help="Text to detect PII in")

    args = parser.parse_args()
    manager = PrivacyManager()

    try:
        if args.command == "consent":
            accepted = manager.display_consent_form()
            if accepted:
                print("\n✅ Consent accepted.")
            else:
                print("\n❌ Consent declined.")

        elif args.command == "audit":
            manager.log_audit_event(args.session, args.action, args.role, args.details)
            print(f"✅ Audit event logged for session {args.session}")

        elif args.command == "report":
            report = manager.generate_compliance_report()
            print(json.dumps(report, indent=2))

        elif args.command == "mask":
            masked = manager.mask_pii(args.text)
            print(masked)

        elif args.command == "detect":
            detections = manager.detect_pii(args.text)
            print(json.dumps(detections, indent=2))

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
