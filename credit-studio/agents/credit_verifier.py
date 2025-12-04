"""
Credit Verifier Agent

Verifier agent specialized for auditing credit analyses using ChaosChain Protocol.
Implements multi-dimensional scoring for finance domain.
"""

import hashlib
import os
from typing import Dict, Any, List, Optional, Tuple

from chaoschain_sdk import ChaosChainAgentSDK, NetworkConfig
from chaoschain_sdk.types import AgentRole


class CreditVerifierAgent:
    """
    Verifier Agent for credit analysis auditing in ChaosChain Protocol.
    
    Responsibilities:
    - Audit credit analyses for accuracy and compliance
    - Score work across multiple dimensions
    - Participate in commit-reveal consensus
    - Build reputation through accurate verification
    """
    
    # Finance-specific scoring dimensions
    DIMENSIONS = [
        # Universal PoA dimensions (weight 1.0)
        ("Initiative", 1.0),
        ("Collaboration", 1.0),
        ("Reasoning Depth", 1.0),
        ("Compliance", 1.0),
        ("Efficiency", 1.0),
        # Finance-specific dimensions (weighted)
        ("Accuracy", 2.0),
        ("Risk Assessment", 1.5),
        ("Documentation", 1.2),
    ]
    
    def __init__(
        self,
        agent_name: str = "RiskAuditor",
        agent_domain: str = "auditor.creditstudio.chaoschain.io",
        network: NetworkConfig = NetworkConfig.ETHEREUM_SEPOLIA
    ):
        """Initialize the Credit Verifier Agent."""
        self.sdk = ChaosChainAgentSDK(
            agent_name=agent_name,
            agent_domain=agent_domain,
            agent_role=AgentRole.VERIFIER,
            network=network,
            enable_process_integrity=True
        )
        
        self.agent_id: Optional[int] = None
        self.studio_address: Optional[str] = None
        self._pending_commits: Dict[bytes, Tuple[List[int], bytes]] = {}
    
    def register(self, token_uri: Optional[str] = None) -> int:
        """Register agent on ERC-8004 Identity Registry."""
        self.agent_id = self.sdk.chaos_agent.get_agent_id()
        
        if self.agent_id is None:
            uri = token_uri or f"https://{self.sdk.chaos_agent.agent_domain}/.well-known/agent.json"
            self.agent_id, _ = self.sdk.chaos_agent.register_agent(token_uri=uri)
        
        return self.agent_id
    
    def join_studio(self, studio_address: str, stake_amount: float = 0.01) -> str:
        """Register with a Studio as a Verifier."""
        self.studio_address = studio_address
        
        tx_hash = self.sdk.register_with_studio(
            studio_address=studio_address,
            role=2,  # VERIFIER
            stake_amount=stake_amount
        )
        
        return tx_hash
    
    def audit_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive audit of a credit analysis.
        
        Args:
            analysis: The credit analysis to audit
            
        Returns:
            Audit results with multi-dimensional scores
        """
        scores = []
        audit_notes = []
        
        # 1. Initiative (0-100): Original analysis vs derivative
        initiative_score = self._assess_initiative(analysis)
        scores.append(initiative_score)
        audit_notes.append(f"Initiative: {initiative_score}/100 - {'Strong' if initiative_score >= 80 else 'Adequate'} original analysis")
        
        # 2. Collaboration (0-100): Building on other work
        collab_score = self._assess_collaboration(analysis)
        scores.append(collab_score)
        audit_notes.append(f"Collaboration: {collab_score}/100 - Referenced {analysis.get('references', 0)} prior analyses")
        
        # 3. Reasoning Depth (0-100): Complexity of analysis
        reasoning_score = self._assess_reasoning(analysis)
        scores.append(reasoning_score)
        audit_notes.append(f"Reasoning: {reasoning_score}/100 - {'Comprehensive' if reasoning_score >= 80 else 'Standard'} analysis depth")
        
        # 4. Compliance (0-100): Following regulations
        compliance_score = self._assess_compliance(analysis)
        scores.append(compliance_score)
        audit_notes.append(f"Compliance: {compliance_score}/100 - All regulatory checks {'passed' if compliance_score >= 90 else 'need review'}")
        
        # 5. Efficiency (0-100): Time and resource usage
        efficiency_score = self._assess_efficiency(analysis)
        scores.append(efficiency_score)
        audit_notes.append(f"Efficiency: {efficiency_score}/100 - Analysis completed in optimal time")
        
        # 6. Accuracy (0-100, weight 2.0): Correctness of calculations
        accuracy_score = self._assess_accuracy(analysis)
        scores.append(accuracy_score)
        audit_notes.append(f"Accuracy (2.0x): {accuracy_score}/100 - Calculations {'verified' if accuracy_score >= 90 else 'need review'}")
        
        # 7. Risk Assessment (0-100, weight 1.5): Quality of risk identification
        risk_score = self._assess_risk_quality(analysis)
        scores.append(risk_score)
        audit_notes.append(f"Risk Assessment (1.5x): {risk_score}/100 - Risk factors {'comprehensive' if risk_score >= 85 else 'adequate'}")
        
        # 8. Documentation (0-100, weight 1.2): Clarity and completeness
        doc_score = self._assess_documentation(analysis)
        scores.append(doc_score)
        audit_notes.append(f"Documentation (1.2x): {doc_score}/100 - Report {'well-structured' if doc_score >= 85 else 'adequate'}")
        
        # Calculate weighted final score
        weights = [d[1] for d in self.DIMENSIONS]
        weighted_sum = sum(s * w for s, w in zip(scores, weights))
        total_weight = sum(weights)
        final_score = weighted_sum / total_weight
        
        return {
            "verifier_id": self.agent_id,
            "scores": scores,
            "dimensions": [d[0] for d in self.DIMENSIONS],
            "weights": weights,
            "final_score": round(final_score, 2),
            "audit_notes": audit_notes,
            "recommendation": "APPROVED" if final_score >= 70 else "NEEDS_REVIEW",
            "timestamp": analysis.get("timestamp")
        }
    
    def _assess_initiative(self, analysis: Dict[str, Any]) -> int:
        """Assess originality of the analysis."""
        # Check for original reasoning and insights
        reasoning = analysis.get("reasoning", "")
        risk_factors = analysis.get("risk_assessment", {}).get("risk_factors", [])
        
        base_score = 75
        
        # Bonus for detailed reasoning
        if len(reasoning) > 500:
            base_score += 10
        
        # Bonus for identifying specific risk factors
        if len(risk_factors) >= 2:
            base_score += 10
        
        return min(100, base_score)
    
    def _assess_collaboration(self, analysis: Dict[str, Any]) -> int:
        """Assess collaboration with other analyses."""
        # In a real system, would check XMTP thread for references
        return 85  # Standard score for standalone analysis
    
    def _assess_reasoning(self, analysis: Dict[str, Any]) -> int:
        """Assess depth of reasoning."""
        risk_assessment = analysis.get("risk_assessment", {})
        financial_ratios = analysis.get("financial_ratios", {})
        
        base_score = 70
        
        # Bonus for comprehensive risk assessment
        if "overall_risk_score" in risk_assessment:
            base_score += 10
        
        # Bonus for financial ratio analysis
        if len(financial_ratios) >= 3:
            base_score += 10
        
        # Bonus for detailed reasoning narrative
        reasoning = analysis.get("reasoning", "")
        if len(reasoning) > 300:
            base_score += 5
        
        return min(100, base_score)
    
    def _assess_compliance(self, analysis: Dict[str, Any]) -> int:
        """Assess regulatory compliance."""
        compliance = analysis.get("compliance_checks", {})
        
        checks = [
            compliance.get("kyc_verified", False),
            compliance.get("aml_cleared", False),
            compliance.get("income_verified", False),
            compliance.get("employment_verified", False),
        ]
        
        passed = sum(1 for c in checks if c)
        return int((passed / len(checks)) * 100)
    
    def _assess_efficiency(self, analysis: Dict[str, Any]) -> int:
        """Assess efficiency of analysis."""
        # In a real system, would compare to benchmark times
        return 82  # Standard efficiency score
    
    def _assess_accuracy(self, analysis: Dict[str, Any]) -> int:
        """Assess accuracy of calculations (most important for finance)."""
        terms = analysis.get("recommended_terms", {})
        risk = analysis.get("risk_assessment", {})
        
        base_score = 80
        
        # Verify interest rate is reasonable
        rate = terms.get("interest_rate", 0)
        if 5.0 <= rate <= 20.0:
            base_score += 5
        
        # Verify monthly payment calculation
        amount = terms.get("approved_amount", 0)
        term = terms.get("term_months", 60)
        payment = terms.get("monthly_payment", 0)
        
        if amount > 0 and term > 0:
            expected_payment = amount / term * (1 + rate/100/12)
            if abs(payment - expected_payment) < 10:  # Allow small rounding
                base_score += 10
        
        return min(100, base_score)
    
    def _assess_risk_quality(self, analysis: Dict[str, Any]) -> int:
        """Assess quality of risk assessment."""
        risk = analysis.get("risk_assessment", {})
        
        base_score = 75
        
        # Bonus for identifying multiple risk factors
        factors = risk.get("risk_factors", [])
        base_score += min(15, len(factors) * 5)
        
        # Bonus for comprehensive risk dimensions
        dimensions = ["credit_risk", "income_stability", "debt_capacity"]
        covered = sum(1 for d in dimensions if d in risk)
        base_score += covered * 3
        
        return min(100, base_score)
    
    def _assess_documentation(self, analysis: Dict[str, Any]) -> int:
        """Assess documentation quality."""
        base_score = 75
        
        # Check for required sections
        sections = ["application", "risk_assessment", "recommendation", "recommended_terms", "reasoning"]
        present = sum(1 for s in sections if s in analysis)
        base_score += present * 3
        
        # Bonus for detailed reasoning
        reasoning = analysis.get("reasoning", "")
        if len(reasoning) > 400:
            base_score += 5
        
        return min(100, base_score)
    
    def commit_score(
        self,
        data_hash: bytes,
        scores: List[int]
    ) -> Tuple[str, bytes]:
        """
        Commit scores using commit-reveal protocol.
        
        Args:
            data_hash: Hash of the work being scored
            scores: Multi-dimensional score vector
            
        Returns:
            Tuple of (transaction_hash, salt)
        """
        if not self.studio_address:
            raise ValueError("Not registered with any Studio")
        
        # Generate random salt for commitment
        salt = os.urandom(32)
        
        # Create commitment hash
        score_bytes = bytes(scores)
        commitment = hashlib.sha256(score_bytes + salt).digest()
        
        # Store for later reveal
        self._pending_commits[data_hash] = (scores, salt)
        
        # Submit commitment on-chain
        tx_hash = self.sdk.commit_score(
            studio_address=self.studio_address,
            data_hash=data_hash,
            score_commitment=commitment
        )
        
        return tx_hash, salt
    
    def reveal_score(self, data_hash: bytes) -> str:
        """
        Reveal previously committed scores.
        
        Args:
            data_hash: Hash of the work being scored
            
        Returns:
            Transaction hash
        """
        if not self.studio_address:
            raise ValueError("Not registered with any Studio")
        
        if data_hash not in self._pending_commits:
            raise ValueError("No pending commitment for this data hash")
        
        scores, salt = self._pending_commits[data_hash]
        
        # Reveal on-chain
        tx_hash = self.sdk.reveal_score(
            studio_address=self.studio_address,
            data_hash=data_hash,
            score_vector=scores,
            salt=salt
        )
        
        # Clean up
        del self._pending_commits[data_hash]
        
        return tx_hash
    
    def get_reputation(self) -> Dict[str, Any]:
        """Get agent's reputation from ERC-8004."""
        if not self.agent_id:
            return {"error": "Agent not registered"}
        
        return self.sdk.get_reputation_summary(agent_id=self.agent_id)
    
    def withdraw_rewards(self) -> str:
        """Withdraw pending rewards from Studio."""
        if not self.studio_address:
            raise ValueError("Not registered with any Studio")
        
        return self.sdk.withdraw_rewards(studio_address=self.studio_address)

