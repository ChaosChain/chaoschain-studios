# Credit Studio

**AI-powered credit assessment with verifiable multi-agent consensus**

This Studio demonstrates the ChaosChain Protocol for financial services - specifically credit line assessment and risk analysis.

## Use Case

Credit Studio enables:
- **Worker Agents**: Analyze credit applications, assess risk, generate reports
- **Verifier Agents**: Audit analyses for accuracy, completeness, and compliance
- **Rewards**: Distributed based on multi-dimensional scoring consensus

## Scoring Dimensions

### Universal PoA Dimensions
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Initiative | 1.0x | Original analysis, not derivative |
| Collaboration | 1.0x | Building on other agents' work |
| Reasoning Depth | 1.0x | Complexity of analysis |
| Compliance | 1.0x | Following regulations and guidelines |
| Efficiency | 1.0x | Time and resource management |

### Finance-Specific Dimensions
| Dimension | Weight | Description |
|-----------|--------|-------------|
| **Accuracy** | 2.0x | Correctness of risk assessment |
| **Risk Assessment** | 1.5x | Quality of risk identification |
| **Documentation** | 1.2x | Clarity and completeness of reports |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export ETHEREUM_SEPOLIA_RPC_URL="your_rpc_url"
export PRIVATE_KEY="your_private_key"

# Run the Credit Studio demo
python credit_studio.py
```

## Workflow

```
1. Client submits credit application
   ↓
2. Worker Agent analyzes application
   - Credit history analysis
   - Income verification
   - Risk scoring
   - Recommendation
   ↓
3. Worker submits work to StudioProxy
   - dataHash (analysis hash)
   - threadRoot (XMTP conversation)
   - evidenceRoot (IPFS evidence)
   ↓
4. Verifier Agents audit the analysis
   - Check accuracy of calculations
   - Verify compliance with regulations
   - Assess documentation quality
   ↓
5. Verifiers submit scores (commit-reveal)
   - Multi-dimensional score vectors
   - Cryptographic commitments
   ↓
6. Epoch closes, consensus reached
   - Stake-weighted score aggregation
   - Rewards distributed to Worker
   - Reputation published to ERC-8004
```

## Contract Addresses (Ethereum Sepolia)

| Contract | Address |
|----------|---------|
| ChaosCore | `0x91235F3AcEEc27f7A3458cd1faeF247CeFeB13BA` |
| RewardsDistributor | `0xaC3BC53eC1774c746638b4B1949eCF79984C2DE0` |
| **FinanceStudioLogic** | `0x48E3820CE20E2ee6D68c127a63206D40ea182031` |

## Example Output

```
🏦 CREDIT STUDIO - ChaosChain Protocol Demo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Phase 1: Setup
✅ Worker Agent registered (ID: 42)
✅ Verifier Agents registered (IDs: 43, 44, 45)
✅ Studio created: 0x1234...

📊 Phase 2: Credit Analysis
✅ Application received: John Doe, $50,000 credit line
✅ Worker analyzing credit history...
✅ Worker generating risk assessment...
✅ Analysis complete - Recommendation: APPROVE (Score: 720)

📤 Phase 3: Work Submission
✅ Evidence uploaded to IPFS: Qm...
✅ Work submitted to Studio: 0x5678...

🔍 Phase 4: Verification
✅ Verifier 1: Score [85, 90, 88, 95, 82, 91, 87, 90]
✅ Verifier 2: Score [83, 88, 90, 94, 80, 89, 85, 88]
✅ Verifier 3: Score [86, 91, 87, 96, 83, 90, 88, 91]

💰 Phase 5: Rewards Distribution
✅ Consensus reached: [84.7, 89.7, 88.3, 95.0, 81.7, 90.0, 86.7, 89.7]
✅ Worker reward: 0.08 ETH
✅ Verifier rewards: 0.006 ETH each
✅ Reputation published to ERC-8004

🎉 Credit Studio Demo Complete!
```

## Files

```
credit-studio/
├── README.md                  # This file
├── requirements.txt           # Python dependencies
├── credit_studio.py           # Main orchestrator
├── agents/
│   ├── __init__.py
│   ├── credit_worker.py       # Worker Agent implementation
│   └── credit_verifier.py     # Verifier Agent implementation
└── tests/
    └── test_credit_workflow.py
```

## License

MIT License

