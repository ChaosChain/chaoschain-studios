"""
Credit Worker Agent

Worker agent specialized for credit analysis using ChaosChain Protocol.
Demonstrates multi-dimensional Proof of Agency for finance domain.
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional

from chaoschain_sdk import ChaosChainAgentSDK, NetworkConfig
from chaoschain_sdk.types import AgentRole


class CreditWorkerAgent:
    """
    Worker Agent for credit assessment in ChaosChain Protocol.
    
    Responsibilities:
    - Analyze credit applications
    - Generate risk assessments
    - Submit work with evidence to Studio
    - Build reputation through verified work
    """
    
    def __init__(
        self,
        agent_name: str = "CreditAnalyst",
        agent_domain: str = "analyst.creditstudio.chaoschain.io",
        network: NetworkConfig = NetworkConfig.ETHEREUM_SEPOLIA
    ):
        """Initialize the Credit Worker Agent."""
        self.sdk = ChaosChainAgentSDK(
            agent_name=agent_name,
            agent_domain=agent_domain,
            agent_role=AgentRole.WORKER,
            network=network,
            enable_process_integrity=True
        )
        
        self.agent_id: Optional[int] = None
        self.studio_address: Optional[str] = None
    
    def register(self, token_uri: Optional[str] = None) -> int:
        """Register agent on ERC-8004 Identity Registry."""
        self.agent_id = self.sdk.chaos_agent.get_agent_id()
        
        if self.agent_id is None:
            uri = token_uri or f"https://{self.sdk.chaos_agent.agent_domain}/.well-known/agent.json"
            self.agent_id, _ = self.sdk.chaos_agent.register_agent(token_uri=uri)
        
        return self.agent_id
    
    def join_studio(self, studio_address: str, stake_amount: float = 0.01) -> str:
        """Register with a Studio as a Worker."""
        self.studio_address = studio_address
        
        tx_hash = self.sdk.register_with_studio(
            studio_address=studio_address,
            role=1,  # WORKER
            stake_amount=stake_amount
        )
        
        return tx_hash
    
    def analyze_credit_application(self, application: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform credit analysis on an application.
        
        Args:
            application: Credit application data
            
        Returns:
            Complete analysis with recommendation
        """
        # Extract application details
        credit_score = application.get("credit_score", 650)
        income = application.get("annual_income", 50000)
        debt_to_income = application.get("debt_to_income", 0.35)
        employment_years = application.get("employment_years", 2)
        requested_amount = application.get("requested_amount", 25000)
        
        # Calculate risk factors
        risk_factors = []
        risk_score = 0
        
        # Credit score assessment
        if credit_score >= 750:
            risk_score += 0
        elif credit_score >= 700:
            risk_score += 10
        elif credit_score >= 650:
            risk_score += 25
            risk_factors.append("Moderate credit score")
        else:
            risk_score += 40
            risk_factors.append("Low credit score")
        
        # Debt-to-income assessment
        if debt_to_income <= 0.28:
            risk_score += 0
        elif debt_to_income <= 0.36:
            risk_score += 10
        elif debt_to_income <= 0.43:
            risk_score += 20
            risk_factors.append("High debt-to-income ratio")
        else:
            risk_score += 35
            risk_factors.append("Very high debt-to-income ratio")
        
        # Employment stability
        if employment_years >= 5:
            risk_score += 0
        elif employment_years >= 2:
            risk_score += 10
        else:
            risk_score += 20
            risk_factors.append("Limited employment history")
        
        # Determine recommendation
        if risk_score <= 20:
            recommendation = "APPROVE"
            approved_amount = requested_amount
            interest_rate = 6.5 + (risk_score * 0.1)
        elif risk_score <= 40:
            recommendation = "APPROVE_WITH_CONDITIONS"
            approved_amount = int(requested_amount * 0.9)
            interest_rate = 8.0 + (risk_score * 0.1)
        elif risk_score <= 60:
            recommendation = "CONDITIONAL"
            approved_amount = int(requested_amount * 0.75)
            interest_rate = 10.0 + (risk_score * 0.1)
        else:
            recommendation = "DECLINE"
            approved_amount = 0
            interest_rate = 0
        
        # Build analysis report
        analysis = {
            "application": application,
            "analyst_id": self.agent_id,
            "timestamp": datetime.now().isoformat(),
            "risk_assessment": {
                "overall_risk_score": risk_score,
                "risk_level": "LOW" if risk_score <= 20 else "MEDIUM" if risk_score <= 40 else "HIGH",
                "risk_factors": risk_factors,
                "credit_risk": "LOW" if credit_score >= 700 else "MEDIUM" if credit_score >= 650 else "HIGH",
                "income_stability": "HIGH" if employment_years >= 5 else "MEDIUM" if employment_years >= 2 else "LOW",
                "debt_capacity": "ADEQUATE" if debt_to_income <= 0.36 else "STRAINED"
            },
            "financial_ratios": {
                "debt_to_income": debt_to_income,
                "payment_to_income": (approved_amount / 60 * (1 + interest_rate/100)) / (income / 12) if approved_amount > 0 else 0,
                "loan_to_value": 0  # No collateral assumed
            },
            "recommendation": recommendation,
            "recommended_terms": {
                "approved_amount": approved_amount,
                "interest_rate": round(interest_rate, 2),
                "term_months": 60,
                "monthly_payment": round(approved_amount / 60 * (1 + interest_rate/100/12), 2) if approved_amount > 0 else 0
            },
            "compliance_checks": {
                "kyc_verified": True,
                "aml_cleared": True,
                "income_verified": True,
                "employment_verified": True
            },
            "reasoning": self._generate_reasoning(application, risk_score, recommendation, risk_factors)
        }
        
        return analysis
    
    def _generate_reasoning(
        self,
        application: Dict[str, Any],
        risk_score: int,
        recommendation: str,
        risk_factors: list
    ) -> str:
        """Generate detailed reasoning for the credit decision."""
        applicant = application.get("applicant_name", "Applicant")
        credit_score = application.get("credit_score", 650)
        income = application.get("annual_income", 50000)
        employment = application.get("employment_years", 2)
        
        reasoning = f"""
Credit Analysis Report for {applicant}
==========================================

Summary:
The application has been evaluated based on multiple risk dimensions 
including creditworthiness, income stability, and debt capacity.

Key Findings:
- Credit Score: {credit_score} ({self._score_category(credit_score)})
- Employment: {employment} years ({self._employment_category(employment)})
- Annual Income: ${income:,}
- Overall Risk Score: {risk_score}/100

"""
        
        if risk_factors:
            reasoning += "Risk Factors Identified:\n"
            for factor in risk_factors:
                reasoning += f"  • {factor}\n"
            reasoning += "\n"
        
        reasoning += f"""Recommendation: {recommendation}

This recommendation is based on a comprehensive analysis of the applicant's
financial profile, credit history, and ability to service the proposed debt.
"""
        
        return reasoning.strip()
    
    def _score_category(self, score: int) -> str:
        if score >= 750:
            return "Excellent"
        elif score >= 700:
            return "Good"
        elif score >= 650:
            return "Fair"
        else:
            return "Poor"
    
    def _employment_category(self, years: int) -> str:
        if years >= 5:
            return "Stable"
        elif years >= 2:
            return "Moderate"
        else:
            return "Limited"
    
    def submit_work(
        self,
        analysis: Dict[str, Any],
        thread_id: str = "credit_thread_001",
        evidence_id: str = "credit_evidence_001"
    ) -> str:
        """
        Submit completed analysis to Studio.
        
        Args:
            analysis: The credit analysis to submit
            thread_id: XMTP thread identifier
            evidence_id: IPFS evidence identifier
            
        Returns:
            Transaction hash
        """
        if not self.studio_address:
            raise ValueError("Not registered with any Studio")
        
        # Create hashes
        analysis_json = json.dumps(analysis, sort_keys=True)
        data_hash = hashlib.sha256(analysis_json.encode()).digest()
        thread_root = hashlib.sha256(f"xmtp_{thread_id}".encode()).digest()
        evidence_root = hashlib.sha256(f"ipfs_{evidence_id}".encode()).digest()
        
        # Submit to Studio
        tx_hash = self.sdk.submit_work(
            studio_address=self.studio_address,
            data_hash=data_hash,
            thread_root=thread_root,
            evidence_root=evidence_root
        )
        
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

