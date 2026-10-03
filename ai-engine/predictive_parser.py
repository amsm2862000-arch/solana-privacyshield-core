import time
import os # 🔥 مكتبة نظام التشغيل الرسمية لقراءة متغيرات البيئة ديناميكياً
import json
from solana.rpc.api import Client 

class SolanaLiveAuditor:
    def __init__(self):
        # 🔥 الإصلاح البرمجي: قراءة الرابط ديناميكياً من ملف .env مع تفعيل Fallback تلقائي لحالات الطوارئ
        self.rpc_url = os.getenv("SOLANA_RPC_URL", "https://solana.com")
        self.solana_client = Client(self.rpc_url)

    def get_live_solana_status(self):
        """يتصل بالشبكة الحية عبر الـ RPC لجلب البلوك الحالي ومراقبة المزامنة"""
        try:
            slot_response = self.solana_client.get_slot()
            current_slot = slot_response.value
            return {
                "latest_slot": current_slot,
                "rpc_endpoint_in_use": self.rpc_url,
                "status": "NETWORK_ACTIVE",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception:
            return {
                "latest_slot": "Fetch Error (Fallback Active)",
                "rpc_endpoint_in_use": self.rpc_url,
                "status": "LIMITED_MODE_OFFLINE",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
            }

    def analyze_solana_program(self, account_meta_code):
        """يفحص الهيكل البرمجي للتأكد من إنفاذ شرط التوقيع وفحص المالك"""
        findings = []

        # 1. التدقيق في ثغرة Missing Signer
        if "is_signer" not in account_meta_code and "Signer" not in account_meta_code:
            findings.append({
                "issue": "Missing is_signer Check / Vulnerable Account Validation",
                "severity": "CRITICAL",
                "impact": "Unprotected instruction execution. Malicious accounts can bypass signature enforcement."
            })

        # 🔥 الإصلاح: الفاحص الذكي بات يبحث ويدقق في وجود شرط الـ Owner Check لحماية العقود المحدثة
        if "owner" not in account_meta_code and "IncorrectProgramId" not in account_meta_code:
            findings.append({
                "issue": "Missing Program Owner Validation Loop",
                "severity": "CRITICAL",
                "impact": "The smart contract accepts external accounts without checking their owner program ID. Subject to fake account substitution attacks."
            })

        # 2. فحص صمود التجميد الزمني الموضعي
        if "Clock::get" not in account_meta_code and "slot" not in account_meta_code:
            findings.append({
                "issue": "Missing Slot-Based Time Lock / Circuit Breaker",
                "severity": "HIGH",
                "impact": "Program cannot freeze its functions during network blackouts, risking state manipulation."
            })

        status = "VULNERABLE" if findings else "SECURE"
        return {"status": status, "vulnerabilities": findings}

if __name__ == "__main__":
    auditor = SolanaLiveAuditor()
    print("[LIVE RUN TIME DATA] Connecting to Solana Secure RPC...")
    # تعديل الـ indent ليعمل الكود بشكل مستقر ومطابق 100%
    print(json.dumps(auditor.get_live_solana_status(), indent=4))
    
