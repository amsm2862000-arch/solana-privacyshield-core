import sys
import os

# الإجراء الفني الصحيح: استدعاء المجلدات الأخرى وحقن مساراتها برمجياً
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استدعاء عميل الـ AI من مجلد ai-engine
from ai_engine.predictive_parser import SolanaLiveAuditor

def run_integrated_security_pipeline():
    print("[ORCHESTRATOR] Booting Integration Pipeline...")
    
    # تفعيل عميل فحص الأمان
    auditor = SolanaLiveAuditor()
    
    # محاكاة كود عقد ذكي قادم من مجلد /programs لفحصه
    sample_solana_program_code = """
    pub fn process_instruction(accounts: &[AccountInfo]) -> ProgramResult {
        let account = &accounts[0];
        // ثغرة: المطور لم يفحص التوقيع عبر account.is_signer!
        msg!("Executing unsafe balance transfer...");
        Ok(())
    }
    """
    
    print("[ORCHESTRATOR] Step 1: Fetching live Solana Slot metadata...")
    network_status = auditor.get_live_solana_status()
    print(f"Network Status Context: {network_status['status']}")
    
    print("[ORCHESTRATOR] Step 2: Passing program to AI Audit engine...")
    audit_results = auditor.analyze_solana_program(sample_solana_program_code)
    
    print("\n[AUTOMATED AI AUDIT REPORT FOR SOLANA PROGRAM]:")
    print(f"OVERALL STATUS: {audit_results['status']}")
    for vuln in audit_results['vulnerabilities']:
        print(f" -> [{vuln['severity']}] {vuln['issue']}")
        print(f"    Impact: {vuln['impact']}")

if __name__ == "__main__":
    run_integrated_security_pipeline()
