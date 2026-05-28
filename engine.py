import json
import sys

def load_json_file(filepath):
    """Safely loads and parses a JSON file."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[ERROR] Critical file missing: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"[ERROR] Corrupt JSON formatting in: {filepath}")
        sys.exit(1)

def analyze_compliance(baseline, live_state):
    """Compares live state against baseline to detect security drift."""
    print("[INFO] Starting Multi-Cloud Compliance Scan...")
    drift_detected = False

    # Create a lookup map of baseline rules by their unique security group ID
    baseline_rules = {sg['id']: sg for sg in baseline.get('security_groups', [])}

    for live_sg in live_state.get('security_groups', []):
        sg_id = live_sg['id']
        
        # Check if the security group is recognized
        if sg_id not in baseline_rules:
            print(f"[ALERT] Rogue Security Group detected in live environment! ID: {sg_id}")
            drift_detected = True
            continue
            
        rule = baseline_rules[sg_id]
        
        # Engineering Check: Compare network access (CIDR block)
        if live_sg['allowed_cidr'] != rule['allowed_cidr']:
            print(f"\n[CRITICAL DRIFT DETECTED]")
            print(f"Resource: Security Group '{live_sg['name']}' ({sg_id})")
            print(f"Expected Network: {rule['allowed_cidr']}")
            print(f"Actual Live Network: {live_sg['allowed_cidr']}")
            print(f"Risk Assessment: EXPOSED TO INTERNET (Potential Data Exfiltration)\n")
            drift_detected = True

    if not drift_detected:
        print("[SUCCESS] Environment compliant. Zero drift detected.")

if __name__ == "__main__":
    baseline_data = load_json_file('baseline.json')
    live_state_data = load_json_file('live-state.json')
    analyze_compliance(baseline_data, live_state_data)
