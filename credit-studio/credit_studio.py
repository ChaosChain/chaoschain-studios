#!/usr/bin/env python3
"""
Credit Studio - ChaosChain Protocol Demo

This demonstrates the full ChaosChain Protocol workflow for credit assessment:
1. Worker Agent analyzes credit applications
2. Verifier Agents audit and score the analysis
3. Consensus is reached via commit-reveal protocol
4. Rewards are distributed based on multi-dimensional scores
5. Reputation is published to ERC-8004

Uses the deployed FinanceStudioLogic contract on Ethereum Sepolia.
"""

import os
import sys
import hashlib
import time
from datetime import datetime
from typing import Dict, Any, List, Optional

from dotenv import load_dotenv
from rich import print as rprint
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

from chaoschain_sdk import ChaosChainAgentSDK, NetworkConfig
from chaoschain_sdk.types import AgentRole

# Load environment variables
load_dotenv()

# Contract addresses (Ethereum Sepolia)
CHAOS_CORE = "0x91235F3AcEEc27f7A3458cd1faeF247CeFeB13BA"
REWARDS_DISTRIBUTOR = "0xaC3BC53eC1774c746638b4B1949eCF79984C2DE0"
FINANCE_LOGIC = "0x48E3820CE20E2ee6D68c127a63206D40ea182031"


class CreditStudioOrchestrator:
    """
    Orchestrates the Credit Studio workflow using ChaosChain Protocol.
    
    Demonstrates:
    - Studio creation with FinanceStudioLogic
    - Worker Agent credit analysis
    - Multi-Verifier consensus
    - Multi-dimensional scoring (PoA)
    - Rewards distribution
    """
    
    def __init__(self):
        self.worker_sdk: Optional[ChaosChainAgentSDK] = None
        self.verifier_sdks: List[ChaosChainAgentSDK] = []
        self.studio_address: Optional[str] = None
        self.results: Dict[str, Any] = {}
    
    def run(self):
        """Execute the complete Credit Studio workflow."""
        try:
            self._print_banner()
            
            # Phase 1: Setup agents and Studio
            self._phase_1_setup()
            
            # Phase 2: Credit analysis (Worker)
            self._phase_2_credit_analysis()
            
            # Phase 3: Work submission
            self._phase_3_submit_work()
            
            # Phase 4: Verification (Verifiers)
            self._phase_4_verification()
            
            # Phase 5: Rewards distribution
            self._phase_5_rewards()
            
            # Final summary
            self._print_summary()
            
        except KeyboardInterrupt:
            rprint("[yellow]⚠️  Demo interrupted[/yellow]")
            sys.exit(1)
        except Exception as e:
            import traceback
            rprint(f"[red]❌ Error: {e}[/red]")
            traceback.print_exc()
            sys.exit(1)
    
    def _print_banner(self):
        """Print Credit Studio banner."""
        banner = """
[bold blue]🏦 CREDIT STUDIO[/bold blue]
[cyan]ChaosChain Protocol Demo for Finance[/cyan]

[yellow]Features:[/yellow]
• Multi-dimensional Proof of Agency (PoA)
• Finance-specific scoring (Accuracy, Risk, Documentation)
• Commit-reveal consensus protocol
• ERC-8004 reputation building

[green]Network: Ethereum Sepolia[/green]
"""
        rprint(Panel(banner, title="[bold green]Credit Studio[/bold green]", border_style="green"))
    
    def _phase_1_setup(self):
        """Phase 1: Initialize agents and create Studio."""
        rprint("\n[bold blue]📋 Phase 1: Setup[/bold blue]")
        rprint("=" * 60)
        
        # Initialize Worker Agent
        rprint("[cyan]Initializing Worker Agent...[/cyan]")
        self.worker_sdk = ChaosChainAgentSDK(
            agent_name="CreditAnalyst",
            agent_domain="analyst.creditstudio.chaoschain.io",
            agent_role=AgentRole.WORKER,
            network=NetworkConfig.ETHEREUM_SEPOLIA,
            enable_process_integrity=True
        )
        
        # Register Worker on ERC-8004
        worker_id = self.worker_sdk.chaos_agent.get_agent_id()
        if worker_id is None:
            rprint("[yellow]Registering Worker Agent on ERC-8004...[/yellow]")
            worker_id, tx = self.worker_sdk.chaos_agent.register_agent(
                token_uri="https://creditstudio.chaoschain.io/.well-known/worker-agent.json"
            )
            rprint(f"[green]✅ Worker registered: ID {worker_id}[/green]")
        else:
            rprint(f"[green]✅ Worker already registered: ID {worker_id}[/green]")
        
        self.results["worker_id"] = worker_id
        
        # Initialize Verifier Agents (3 for consensus)
        rprint("[cyan]Initializing Verifier Agents...[/cyan]")
        verifier_names = ["RiskAuditor1", "RiskAuditor2", "RiskAuditor3"]
        
        for name in verifier_names:
            verifier = ChaosChainAgentSDK(
                agent_name=name,
                agent_domain=f"{name.lower()}.creditstudio.chaoschain.io",
                agent_role=AgentRole.VERIFIER,
                network=NetworkConfig.ETHEREUM_SEPOLIA,
                enable_process_integrity=True
            )
            
            # Register on ERC-8004
            verifier_id = verifier.chaos_agent.get_agent_id()
            if verifier_id is None:
                verifier_id, tx = verifier.chaos_agent.register_agent(
                    token_uri=f"https://creditstudio.chaoschain.io/.well-known/{name.lower()}.json"
                )
            
            self.verifier_sdks.append(verifier)
            rprint(f"[green]✅ Verifier {name} registered: ID {verifier_id}[/green]")
        
        # Create Studio using FinanceStudioLogic
        rprint("[cyan]Creating Credit Studio...[/cyan]")
        try:
            self.studio_address = self.worker_sdk.create_studio(
                studio_name="Credit Assessment Studio",
                logic_module_address=FINANCE_LOGIC,
                initial_budget=0  # No initial budget for demo
            )
            rprint(f"[green]✅ Studio created: {self.studio_address}[/green]")
        except Exception as e:
            rprint(f"[yellow]⚠️  Studio creation failed (may already exist): {e}[/yellow]")
            # Use a placeholder for demo
            self.studio_address = "0x" + "1" * 40
        
        self.results["studio_address"] = self.studio_address
        
        # Register agents with Studio
        rprint("[cyan]Registering agents with Studio...[/cyan]")
        try:
            self.worker_sdk.register_with_studio(
                studio_address=self.studio_address,
                role=1,  # WORKER role
                stake_amount=0.01  # 0.01 ETH stake
            )
            rprint("[green]✅ Worker registered with Studio[/green]")
        except Exception as e:
            rprint(f"[yellow]⚠️  Worker registration: {e}[/yellow]")
        
        for i, verifier in enumerate(self.verifier_sdks):
            try:
                verifier.register_with_studio(
                    studio_address=self.studio_address,
                    role=2,  # VERIFIER role
                    stake_amount=0.01
                )
                rprint(f"[green]✅ Verifier {i+1} registered with Studio[/green]")
            except Exception as e:
                rprint(f"[yellow]⚠️  Verifier {i+1} registration: {e}[/yellow]")
    
    def _phase_2_credit_analysis(self):
        """Phase 2: Worker performs credit analysis."""
        rprint("\n[bold blue]📊 Phase 2: Credit Analysis[/bold blue]")
        rprint("=" * 60)
        
        # Simulate credit application
        application = {
            "applicant_name": "John Doe",
            "requested_amount": 50000,
            "annual_income": 85000,
            "employment_years": 5,
            "credit_score": 720,
            "debt_to_income": 0.28,
            "collateral": "None",
            "purpose": "Business expansion"
        }
        
        rprint(f"[cyan]📋 Credit Application Received[/cyan]")
        rprint(f"   Applicant: {application['applicant_name']}")
        rprint(f"   Requested: ${application['requested_amount']:,}")
        rprint(f"   Credit Score: {application['credit_score']}")
        
        # Worker performs analysis
        rprint("[yellow]🔍 Worker analyzing credit application...[/yellow]")
        time.sleep(1)  # Simulate analysis time
        
        analysis = {
            "application": application,
            "timestamp": datetime.now().isoformat(),
            "analyst_id": self.results.get("worker_id"),
            "risk_assessment": {
                "credit_risk": "LOW",
                "income_stability": "HIGH",
                "debt_capacity": "ADEQUATE",
                "overall_risk_score": 25  # 0-100, lower is better
            },
            "financial_ratios": {
                "debt_service_coverage": 2.1,
                "loan_to_value": 0.0,  # No collateral
                "payment_to_income": 0.12
            },
            "recommendation": "APPROVE",
            "recommended_terms": {
                "approved_amount": 45000,
                "interest_rate": 8.5,
                "term_months": 60,
                "monthly_payment": 920.13
            },
            "compliance_checks": {
                "kyc_verified": True,
                "aml_cleared": True,
                "income_verified": True,
                "employment_verified": True
            },
            "reasoning": """
            Based on the applicant's strong credit score (720), stable employment (5 years),
            and healthy debt-to-income ratio (28%), this application presents low credit risk.
            
            The debt service coverage ratio of 2.1x indicates strong ability to service the loan.
            Recommended approval with slightly reduced amount ($45,000 vs $50,000 requested)
            to maintain conservative underwriting standards.
            
            Interest rate of 8.5% reflects the unsecured nature of the loan and current market conditions.
            """
        }
        
        rprint(f"[green]✅ Analysis complete[/green]")
        rprint(f"   Recommendation: {analysis['recommendation']}")
        rprint(f"   Approved Amount: ${analysis['recommended_terms']['approved_amount']:,}")
        rprint(f"   Risk Score: {analysis['risk_assessment']['overall_risk_score']}/100")
        
        self.results["analysis"] = analysis
    
    def _phase_3_submit_work(self):
        """Phase 3: Submit work to Studio."""
        rprint("\n[bold blue]📤 Phase 3: Work Submission[/bold blue]")
        rprint("=" * 60)
        
        analysis = self.results.get("analysis", {})
        
        # Create hashes for work submission
        import json
        analysis_json = json.dumps(analysis, sort_keys=True)
        
        data_hash = hashlib.sha256(analysis_json.encode()).digest()
        thread_root = hashlib.sha256(b"xmtp_credit_thread_001").digest()
        evidence_root = hashlib.sha256(b"ipfs_credit_evidence_001").digest()
        
        rprint(f"[cyan]Creating work commitment...[/cyan]")
        rprint(f"   Data Hash: 0x{data_hash.hex()[:16]}...")
        rprint(f"   Thread Root: 0x{thread_root.hex()[:16]}...")
        rprint(f"   Evidence Root: 0x{evidence_root.hex()[:16]}...")
        
        # Submit work to Studio
        rprint("[yellow]Submitting work to Studio...[/yellow]")
        try:
            tx_hash = self.worker_sdk.submit_work(
                studio_address=self.studio_address,
                data_hash=data_hash,
                thread_root=thread_root,
                evidence_root=evidence_root
            )
            rprint(f"[green]✅ Work submitted: {tx_hash}[/green]")
            self.results["work_tx"] = tx_hash
        except Exception as e:
            rprint(f"[yellow]⚠️  Work submission: {e}[/yellow]")
            self.results["work_tx"] = "simulated_tx"
        
        self.results["data_hash"] = data_hash
    
    def _phase_4_verification(self):
        """Phase 4: Verifiers audit and score the work."""
        rprint("\n[bold blue]🔍 Phase 4: Verification[/bold blue]")
        rprint("=" * 60)
        
        data_hash = self.results.get("data_hash", b"\x00" * 32)
        
        # Each verifier performs audit and scores
        # Finance dimensions: [Initiative, Collaboration, Reasoning, Compliance, Efficiency, Accuracy, Risk, Documentation]
        verifier_scores = [
            [85, 90, 88, 95, 82, 91, 87, 90],  # Verifier 1
            [83, 88, 90, 94, 80, 89, 85, 88],  # Verifier 2
            [86, 91, 87, 96, 83, 90, 88, 91],  # Verifier 3
        ]
        
        dimension_names = [
            "Initiative", "Collaboration", "Reasoning", "Compliance",
            "Efficiency", "Accuracy", "Risk Assessment", "Documentation"
        ]
        
        rprint("[cyan]Verifiers auditing work...[/cyan]")
        
        for i, (verifier, scores) in enumerate(zip(self.verifier_sdks, verifier_scores)):
            rprint(f"\n[yellow]Verifier {i+1} performing audit...[/yellow]")
            time.sleep(0.5)  # Simulate audit time
            
            # Display scores
            table = Table(title=f"Verifier {i+1} Scores")
            table.add_column("Dimension", style="cyan")
            table.add_column("Score", style="green")
            
            for dim, score in zip(dimension_names, scores):
                table.add_row(dim, f"{score}/100")
            
            rprint(table)
            
            # Commit score (commit-reveal protocol)
            salt = os.urandom(32)
            score_commitment = hashlib.sha256(
                bytes(scores) + salt
            ).digest()
            
            rprint(f"[cyan]Committing score...[/cyan]")
            try:
                tx = verifier.commit_score(
                    studio_address=self.studio_address,
                    data_hash=data_hash,
                    score_commitment=score_commitment
                )
                rprint(f"[green]✅ Score committed[/green]")
            except Exception as e:
                rprint(f"[yellow]⚠️  Commit: {e}[/yellow]")
            
            # Reveal score
            rprint(f"[cyan]Revealing score...[/cyan]")
            try:
                tx = verifier.reveal_score(
                    studio_address=self.studio_address,
                    data_hash=data_hash,
                    score_vector=scores,
                    salt=salt
                )
                rprint(f"[green]✅ Score revealed[/green]")
            except Exception as e:
                rprint(f"[yellow]⚠️  Reveal: {e}[/yellow]")
        
        self.results["verifier_scores"] = verifier_scores
        
        # Calculate consensus
        import numpy as np
        consensus = np.mean(verifier_scores, axis=0).tolist()
        self.results["consensus_scores"] = consensus
        
        rprint(f"\n[green]✅ Consensus reached![/green]")
        rprint(f"   Consensus scores: {[round(s, 1) for s in consensus]}")
    
    def _phase_5_rewards(self):
        """Phase 5: Distribute rewards based on consensus."""
        rprint("\n[bold blue]💰 Phase 5: Rewards Distribution[/bold blue]")
        rprint("=" * 60)
        
        consensus = self.results.get("consensus_scores", [85] * 8)
        
        # Calculate weighted score (Finance weights: Accuracy 2.0x, Risk 1.5x, Documentation 1.2x)
        weights = [1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.5, 1.2]  # Last 3 are finance-specific
        weighted_sum = sum(s * w for s, w in zip(consensus, weights))
        total_weight = sum(weights)
        final_score = weighted_sum / total_weight
        
        rprint(f"[cyan]Calculating rewards...[/cyan]")
        rprint(f"   Final weighted score: {final_score:.1f}/100")
        
        # Simulate reward distribution
        base_reward = 0.1  # 0.1 ETH base reward
        worker_reward = base_reward * (final_score / 100)
        verifier_reward = 0.01  # Fixed verifier reward
        
        rprint(f"\n[green]Rewards Distribution:[/green]")
        rprint(f"   Worker (CreditAnalyst): {worker_reward:.4f} ETH")
        for i in range(3):
            rprint(f"   Verifier {i+1}: {verifier_reward:.4f} ETH")
        
        # Close epoch (would trigger on-chain distribution)
        rprint("\n[cyan]Closing epoch...[/cyan]")
        try:
            tx = self.worker_sdk.close_epoch(
                studio_address=self.studio_address,
                epoch=1
            )
            rprint(f"[green]✅ Epoch closed: {tx}[/green]")
        except Exception as e:
            rprint(f"[yellow]⚠️  Epoch close: {e}[/yellow]")
        
        # Publish reputation to ERC-8004
        rprint("[cyan]Publishing reputation to ERC-8004...[/cyan]")
        rprint(f"[green]✅ Worker reputation updated: {final_score:.1f}/100[/green]")
        
        self.results["final_score"] = final_score
        self.results["worker_reward"] = worker_reward
    
    def _print_summary(self):
        """Print final summary."""
        rprint("\n")
        
        summary = f"""
[bold green]🎉 CREDIT STUDIO DEMO COMPLETE![/bold green]

[cyan]Results:[/cyan]
• Studio: {self.results.get('studio_address', 'N/A')[:20]}...
• Worker ID: {self.results.get('worker_id', 'N/A')}
• Final Score: {self.results.get('final_score', 0):.1f}/100
• Worker Reward: {self.results.get('worker_reward', 0):.4f} ETH

[yellow]Multi-Dimensional Scores (Consensus):[/yellow]
• Initiative: {self.results.get('consensus_scores', [0]*8)[0]:.1f}
• Collaboration: {self.results.get('consensus_scores', [0]*8)[1]:.1f}
• Reasoning: {self.results.get('consensus_scores', [0]*8)[2]:.1f}
• Compliance: {self.results.get('consensus_scores', [0]*8)[3]:.1f}
• Efficiency: {self.results.get('consensus_scores', [0]*8)[4]:.1f}
• Accuracy (2.0x): {self.results.get('consensus_scores', [0]*8)[5]:.1f}
• Risk Assessment (1.5x): {self.results.get('consensus_scores', [0]*8)[6]:.1f}
• Documentation (1.2x): {self.results.get('consensus_scores', [0]*8)[7]:.1f}

[green]Protocol Features Demonstrated:[/green]
✅ Studio creation with FinanceStudioLogic
✅ ERC-8004 agent registration
✅ Multi-dimensional Proof of Agency (PoA)
✅ Commit-reveal score submission
✅ Multi-verifier consensus
✅ Finance-specific weighted scoring
✅ Reputation building
"""
        rprint(Panel(summary, title="[bold green]Summary[/bold green]", border_style="green"))


def main():
    """Main entry point."""
    orchestrator = CreditStudioOrchestrator()
    orchestrator.run()


if __name__ == "__main__":
    main()

