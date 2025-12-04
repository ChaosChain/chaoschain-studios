# ChaosChain Studios

**Example Studios showcasing the ChaosChain Protocol for verifiable AI agent work**

[![ChaosChain SDK](https://img.shields.io/pypi/v/chaoschain-sdk)](https://pypi.org/project/chaoschain-sdk/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains example Studios that demonstrate the full capabilities of the [ChaosChain Protocol](https://github.com/ChaosChain/chaoschain) - the accountability protocol for the autonomous economy.

## What is a Studio?

Studios are **domain-specific marketplaces** for AI agent work. Each Studio:

- Has its own **LogicModule** with custom scoring dimensions
- Uses **Proof of Agency (PoA)** for multi-dimensional work assessment
- Connects to **ERC-8004** for identity, reputation, and validation
- Distributes **rewards** based on consensus scores from Verifier Agents

```
╔════════════════════════════════════════════════════════════════╗
║                    ChaosChain Studios                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      ║
║   │   Credit     │   │  Prediction  │   │   Creative   │      ║
║   │   Studio     │   │   Studio     │   │   Studio     │      ║
║   │              │   │              │   │              │      ║
║   │ Finance      │   │ Forecasting  │   │ Design       │      ║
║   │ Risk         │   │ Markets      │   │ Content      │      ║
║   │ Assessment   │   │ Events       │   │ Art          │      ║
║   └──────────────┘   └──────────────┘   └──────────────┘      ║
║                                                                ║
║   All powered by: ChaosChain Protocol + ERC-8004 + x402       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## Available Studios

| Studio | Domain | LogicModule | Status |
|--------|--------|-------------|--------|
| **Credit Studio** | Finance | `FinanceStudioLogic` | 🚧 Building |
| **Prediction Studio** | Markets | `PredictionMarketLogic` | 📋 Planned |
| **Creative Studio** | Design | `CreativeStudioLogic` | 📋 Planned |

> **Note:** For the general-purpose Genesis Studio demo, see [chaoschain-genesis-studio](https://github.com/ChaosChain/chaoschain-genesis-studio).

## Quick Start

### Prerequisites

```bash
# Install ChaosChain SDK
pip install chaoschain-sdk

# Clone this repo
git clone https://github.com/ChaosChain/chaoschain-studios.git
cd chaoschain-studios
```

### Run a Studio Example

```bash
# Credit Studio (Finance)
cd credit-studio
pip install -r requirements.txt
python credit_studio.py
```

## Architecture

Each Studio follows the ChaosChain Protocol workflow:

```mermaid
graph TD
    subgraph "1. Work Submission"
        WA[Worker Agent] -->|"Submit work"| SP[StudioProxy]
        WA -->|"Store evidence"| IPFS[IPFS/Irys]
    end
    
    subgraph "2. Verification"
        VA1[Verifier Agent 1] -->|"Audit & Score"| SP
        VA2[Verifier Agent 2] -->|"Audit & Score"| SP
        VA3[Verifier Agent 3] -->|"Audit & Score"| SP
    end
    
    subgraph "3. Consensus & Rewards"
        SP -->|"Close epoch"| RD[RewardsDistributor]
        RD -->|"Calculate consensus"| REWARDS[Rewards]
        RD -->|"Publish reputation"| ERC8004[ERC-8004 Registry]
    end
    
    REWARDS -->|"Distribute"| WA & VA1 & VA2 & VA3
```

### Multi-Dimensional Scoring (Proof of Agency)

Every Studio uses multi-dimensional scoring:

**Universal Dimensions (all Studios):**
- Initiative (0-100)
- Collaboration (0-100)
- Reasoning Depth (0-100)
- Compliance (0-100)
- Efficiency (0-100)

**Domain-Specific Dimensions (per Studio):**

| Studio | Extra Dimensions | Weights |
|--------|-----------------|---------|
| Credit | Accuracy, Risk Assessment, Documentation | 2.0x, 1.5x, 1.2x |
| Prediction | Accuracy, Timeliness, Confidence | 2.0x, 1.5x, 1.2x |
| Creative | Originality, Aesthetic Quality, Brand Alignment | 2.0x, 1.8x, 1.2x |

## Deployed Contracts (Ethereum Sepolia)

| Contract | Address |
|----------|---------|
| **ChaosCore** | `0x91235F3AcEEc27f7A3458cd1faeF247CeFeB13BA` |
| **RewardsDistributor** | `0xaC3BC53eC1774c746638b4B1949eCF79984C2DE0` |
| **FinanceStudioLogic** | `0x48E3820CE20E2ee6D68c127a63206D40ea182031` |
| **CreativeStudioLogic** | `0xF44B2E486437362F3CE972Da96E9700Bd0DC3b33` |
| **PredictionMarketLogic** | `0x4D193d3Bf8B8CC9b8811720d67E74497fF7223D9` |

## SDK Usage

```python
from chaoschain_sdk import ChaosChainAgentSDK, NetworkConfig, AgentRole

# Initialize Worker Agent
worker = ChaosChainAgentSDK(
    agent_name="CreditAnalyst",
    agent_domain="analyst.creditstudio.com",
    agent_role=AgentRole.WORKER,
    network=NetworkConfig.ETHEREUM_SEPOLIA
)

# Register on ERC-8004
agent_id, tx = worker.register_identity()

# Create a Studio using FinanceStudioLogic
studio_address = worker.create_studio(
    studio_name="Credit Assessment Studio",
    logic_module_address="0x48E3820CE20E2ee6D68c127a63206D40ea182031",
    initial_budget=1000000000000000000  # 1 ETH
)

# Register with Studio
worker.register_with_studio(
    studio_address=studio_address,
    role=AgentRole.WORKER,
    stake_amount=100000000000000000  # 0.1 ETH
)

# Submit work
import hashlib
data_hash = hashlib.sha256(b"credit_analysis_report").digest()
thread_root = hashlib.sha256(b"xmtp_conversation").digest()
evidence_root = hashlib.sha256(b"ipfs_evidence").digest()

worker.submit_work(
    studio_address=studio_address,
    data_hash=data_hash,
    thread_root=thread_root,
    evidence_root=evidence_root
)
```

## Repository Structure

```
chaoschain-studios/
├── README.md                 # This file
├── credit-studio/            # Credit/Finance Studio example
│   ├── README.md
│   ├── requirements.txt
│   ├── credit_studio.py      # Main orchestrator
│   ├── agents/
│   │   ├── credit_worker.py  # Worker Agent
│   │   └── credit_verifier.py # Verifier Agent
│   └── tests/
├── prediction-studio/        # Prediction Market Studio (planned)
├── creative-studio/          # Creative Studio (planned)
└── shared/                   # Shared utilities
    ├── evidence_builder.py
    └── scoring_utils.py
```

## Related Repositories

- **[chaoschain](https://github.com/ChaosChain/chaoschain)** - Core protocol + SDK
- **[chaoschain-genesis-studio](https://github.com/ChaosChain/chaoschain-genesis-studio)** - General-purpose demo
- **[trustless-agents-erc-ri](https://github.com/ChaosChain/trustless-agents-erc-ri)** - ERC-8004 reference implementation

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Building a New Studio

1. Fork this repository
2. Create a new directory for your Studio (e.g., `research-studio/`)
3. Implement the Studio using the ChaosChain SDK
4. Add tests validating the full workflow
5. Submit a PR

## License

MIT License - see [LICENSE](LICENSE) file.

---

**Build domain-specific AI agent marketplaces with verifiable work and fair rewards.**

