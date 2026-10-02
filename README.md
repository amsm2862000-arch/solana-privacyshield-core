# PrivacyShield - Resilient Solana Core Security Infrastructure

PrivacyShield is an advanced, open-source decentralized security auditing infrastructure specifically engineered to protect the Solana ecosystem against critical vulnerabilities, such as **Missing Signer Checks**, while ensuring operational resilience in extreme network-constrained environments (e.g., edge processing nodes under infrastructure blackouts).

---

## 📊 1. System & AI Architecture Block Diagram

```text
[Target Contract / Account Data] 
       |
       v
[ai-engine / predictive_parser.py]  <--- Uses `RpcClient` to trace Signatures
       |
       +---> Check: `is_signer` present?
       +---> Check: `Clock::get()?.slot` utilized?
       |
       v
[orchestrator / pipeline.py]        <--- The Integration & Workflow Hub
       |
       |==========> (Internet Check Protocol)
       |
       +---> [If Online] ----> Offload heavy compute to Cloud Hub.
       +---> [If Offline] ---> Trigger `LOCAL_GPU_FLAG = true` 
                                  |
                                  v
                               Execute locally on Edge Hardware via Mesh
                                  |
                                  v
                               Route traffic safely through [zk-privacy (SOCKS5)]
                                  |
                                  v
[programs / solana-privacy-shield] <-- Enforces On-Chain Circuit Breaker & Blinds Metadata
```

---

## 📝 2. Comprehensive Architectural & Technical Breakdown

This repository operates as a fully integrated, multi-layered security ecosystem. Below is the explicit breakdown of how each directory functions and interacts with the rest of the system:

### 1. `/programs/solana-privacy-shield/src/lib.rs` (The On-Chain Enforcer)
*   **Technical Role:** Built using pure native `solana_program` bindings in Rust to enforce strict cryptographic governance directly on the blockchain.
*   **Core Logic:** It intercepts incoming instruction accounts and parses the boolean `account_info.is_signer` trait. If a critical administrative instruction lacks a signature, it immediately halts execution and returns `ProgramError::MissingRequiredSignature`.
*   **Resilience Feature:** It tracks temporal state changes using `Clock::get()?.slot`. If external heartbeat updates cease due to localized network drops, it engages an automated circuit breaker to lock contract functions until the designated authority wallet provides an un-blinded verification signature.

### 2. `/ai-engine/predictive_parser.py` (The Intelligent Bytecode Scanner)
*   **Technical Role:** An independent automated auditing agent written in Python that leverages the official `solana.rpc.api.Client` to interact with live testnet infrastructure.
*   **Core Logic:** It fetches live state transaction matrices and runs predictive pattern matching against target smart contract bytecodes. It is specifically designed to flag programs that process state mutations without explicitly asserting signature validation patterns.

### 3. `/infra-edge/edge_gpu_sync.sh` (The Environmental Resilience Layer)
*   **Technical Role:** A shell-based automation layer engineered to combat infrastructure and power instabilities in restricted geographical regions (e.g., Gaza).
*   **Core Logic:** It runs automated network latency and health checks against remote servers. Upon identifying a complete cloud disconnection, it flips the system to an isolated environment variable (`LOCAL_GPU_FLAG=true`). This forces the auditing pipelines to spin up local hardware threads and GPU clusters, compiling and logging reports locally until a network sync becomes available.

### 4. `/zk-privacy/tor_proxy_config.sh` (Geographical Footprint Protection)
*   **Technical Role:** An infrastructure hardening script providing anonymization and operational security for edge developers.
*   **Core Logic:** It configures a localized `SOCKS5_PROXY` connection overlay (`127.0.0.1:9050`). When internet access is restored, it forces all bulk offline-compiled data packages and RPC requests to route through anonymized layers, blinding the physical node IP addresses and metadata footprint from tracking systems.

### 5. `/orchestrator/pipeline.py` (The Core System Integration Hub)
*   **Technical Role:** The centralized software nerve center that imports and wires all sub-modules into a cohesive atomic workflow.
*   **Core Logic:** It dynamically injects paths using `sys.path.append` and initializes communication loops. It invokes the python auditor to inspect contract inputs, checks environmental states from the infrastructure scripts, and prepares the structured data to be broadcasted securely to the on-chain Solana program.

### 6. `/tests/security_check.ts` (Deterministic Exploit Simulation)
*   **Technical Role:** A TypeScript-based integration testing suite utilizing Coral’s `@coral-xyz/anchor` environment.
*   **Core Logic:** It generates mock environment settings and spawns dynamic, un-signed cryptographic `Keypair` instances. It deliberately fires unauthorized instruction payloads at the Rust program to mathematically prove that the on-chain validation triggers zero-false-negatives when dealing with missing signers.

### 7. `/migrations/deploy.json` (Immutable Identity Management)
*   **Technical Role:** Configuration deployment ledger.
*   **Core Logic:** Securely anchors the target network endpoints, mapping cryptographic identities, and locking the unique program identifier compiled via the contract's `declare_id!()` macro.

---

## 🛠️ 3. Atomic Explicit Integration Workflow (How Files Call Each Other)
The ecosystem achieves absolute atomicity by enforcing strict code-level imports. The `orchestrator/pipeline.py` actively imports the AI logic via `from ai_engine.predictive_parser import SolanaLiveAuditor`. Before any connection handshake is initiated by the Python client, the underlying shell layer triggers `source ./zk-privacy/tor_proxy_config.sh` to hook the network sockets to the `SOCKS5_PROXY`. Once the network is authenticated, the structured audit results are packaged and transmitted directly into the Solana program parameters via `&[AccountInfo]`, executing an unbroken, secure cross-file dependency chain.
