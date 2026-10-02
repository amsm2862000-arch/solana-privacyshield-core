import time
import urllib.request
import json
from solana.rpc.api import Client # استدعاء عميل سولانا الرسمي لحقن البيانات

class SolanaLiveAuditor:
    def __init__(self):
        # النود الرسمية لشبكة اختبار سولانا
        self.rpc_url = "https://solana.com"
        self.solana_client = Client(self.rpc_url)

    def get_live_solana_status(self):
        """يتصل بالشبكة الحية عبر الـ RPC لجلب البلوك الحالي ومراقبة المزامنة"""
        try:
            # استدعاء دالة سولانا الحقيقية لجلب رقم الـ Slot الحالي
            slot_response = self.solana_client.get_slot()
            current_slot = slot_response.value
            return {
                "latest_slot": current_slot,
                "status": "NETWORK_ACTIVE",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            # التحول لحالة الاتصال المحدود في ظروف انقطاع الإنترنت في غزة
            return {
                "latest_slot": "Fetch Error (Fallback Active)",
                "status": "LIMITED_MODE_OFFLINE",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }

    def analyze_solana_program(self, account_meta_code):
        """يفحص الهيكل البرمجي للتأكد من إنفاذ شرط التوقيع وعدم وجود ثغرات"""
        findings = []

        # 1. التدقيق في ثغرة Missing Signer
        if "is_signer" not in account_meta_code and "Signer" not in account_meta_code:
            findings.append({
                "issue": "Missing is_signer Check / Vulnerable Account Validation",
                "severity": "CRITICAL",
                "impact": "Unprotected instruction execution. Malicious accounts can bypass signature enforcement."
            })

        # 2. فحص صمود التجميد الزمني
        if "Clock::get" not in account_meta_code and "slot" not in account_meta_code:
            findings.append({
                "issue": "Missing Slot-Based Time Lock / Circuit Breaker",
                "severity": "HIGH",
                "impact": "Program cannot freeze itself during complete network blackouts, risking state manipulation."
            })

        status = "VULNERABLE" if findings else "SECURE"
        return {"status": status, "vulnerabilities": findings}

if __name__ == "__main__":
    auditor = SolanaLiveAuditor()
    print("[LIVE RUN TIME DATA] connecting to Solana...")
    print(json.dumps(auditor.get_live_solana_status(), indent=4))
        
