import json
import sys
import os
import urllib.request

def load_json_file(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"[ERROR] Could not load {filepath}: {e}")
        sys.exit(1)

def send_discord_alert(message):
    """Pulls the secret Webhook URL from the environment and fires the alert."""
    webhook_url = os.environ.get('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("[WARN] No Discord Webhook URL provided in environment. Skipping chat alert.")
        return

    # Package the message into a JSON format Discord understands
    payload = {
        "content": f"🚨 **CLOUD SECURITY DRIFT DETECTED** 🚨\n```yaml\n{message}\n```"
    }
    
    # Fire the payload at Discord
    req = urllib.request.Request(
	        webhook_url, 
        data=json.dumps(payload).encode('utf-8'), 
        headers={'Content-Type': 'application/json',
		 'User-Agent': 'CloudDriftEngine/1.0'}
    )
    
    try:
        urllib.request.urlopen(req)
        print("[INFO] Webhook alert successfully dispatched to Discord!")
    except Exception as e:
        print(f"[ERROR] Failed to send Discord alert: {e}")

def analyze_compliance(baseline, live_state):
    print("[INFO] Starting Multi-Cloud Compliance Scan...")
    drift_detected = False
    baseline_rules = {sg['id']: sg for sg in baseline.get('security_groups', [])}

    for live_sg in live_state.get('security_groups', []):
        sg_id = live_sg['id']
        rule = baseline_rules.get(sg_id)
        
        if not rule:
            continue
            
        if live_sg['allowed_cidr'] != rule['allowed_cidr']:
            # Create a clean message format
            alert_msg = (
                f"Resource: {live_sg['name']} ({sg_id})\n"
                f"Expected Network: {rule['allowed_cidr']}\n"
                f"Actual Live Network: {live_sg['allowed_cidr']}\n"
                f"Risk: EXPOSED TO INTERNET (Potential Exfiltration)"
            )
            
            print(f"\n[CRITICAL DRIFT DETECTED]\n{alert_msg}\n")
            
            # Trigger the Discord webhook
            send_discord_alert(alert_msg)
            drift_detected = True

    if not drift_detected:
        print("[SUCCESS] Environment compliant. Zero drift detected.")

if __name__ == "__main__": analyze_compliance(load_json_file('baseline.json'), 
    load_json_file('live-state.json'))
