"""
Tests for Credit Studio workflow.

Validates the complete ChaosChain Protocol workflow for credit assessment.
"""

import pytest
import hashlib
import json
from unittest.mock import MagicMock, patch

from agents.credit_worker import CreditWorkerAgent
from agents.credit_verifier import CreditVerifierAgent


class TestCreditWorkerAgent:
    """Tests for Credit Worker Agent."""
    
    def test_analyze_low_risk_application(self):
        """Test analysis of a low-risk credit application."""
        # Create agent with mocked SDK
        with patch('agents.credit_worker.ChaosChainAgentSDK'):
            worker = CreditWorkerAgent()
            worker.agent_id = 1
            
            # Low-risk application
            application = {
                "applicant_name": "John Doe",
                "credit_score": 750,
                "annual_income": 100000,
                "debt_to_income": 0.25,
                "employment_years": 7,
                "requested_amount": 50000
            }
            
            analysis = worker.analyze_credit_application(application)
            
            # Assertions
            assert analysis["recommendation"] == "APPROVE"
            assert analysis["risk_assessment"]["overall_risk_score"] <= 20
            assert analysis["risk_assessment"]["risk_level"] == "LOW"
            assert analysis["recommended_terms"]["approved_amount"] == 50000
    
    def test_analyze_high_risk_application(self):
        """Test analysis of a high-risk credit application."""
        with patch('agents.credit_worker.ChaosChainAgentSDK'):
            worker = CreditWorkerAgent()
            worker.agent_id = 1
            
            # High-risk application
            application = {
                "applicant_name": "Jane Smith",
                "credit_score": 580,
                "annual_income": 40000,
                "debt_to_income": 0.50,
                "employment_years": 1,
                "requested_amount": 30000
            }
            
            analysis = worker.analyze_credit_application(application)
            
            # Assertions
            assert analysis["recommendation"] in ["DECLINE", "CONDITIONAL"]
            assert analysis["risk_assessment"]["overall_risk_score"] > 40
            assert analysis["risk_assessment"]["risk_level"] == "HIGH"
    
    def test_analysis_includes_compliance_checks(self):
        """Test that analysis includes all compliance checks."""
        with patch('agents.credit_worker.ChaosChainAgentSDK'):
            worker = CreditWorkerAgent()
            worker.agent_id = 1
            
            application = {
                "applicant_name": "Test User",
                "credit_score": 700,
                "annual_income": 75000,
                "debt_to_income": 0.30,
                "employment_years": 3,
                "requested_amount": 25000
            }
            
            analysis = worker.analyze_credit_application(application)
            
            # Check compliance fields
            compliance = analysis["compliance_checks"]
            assert "kyc_verified" in compliance
            assert "aml_cleared" in compliance
            assert "income_verified" in compliance
            assert "employment_verified" in compliance


class TestCreditVerifierAgent:
    """Tests for Credit Verifier Agent."""
    
    def test_audit_scores_all_dimensions(self):
        """Test that audit covers all 8 dimensions."""
        with patch('agents.credit_verifier.ChaosChainAgentSDK'):
            verifier = CreditVerifierAgent()
            verifier.agent_id = 2
            
            # Sample analysis to audit
            analysis = {
                "application": {"applicant_name": "Test"},
                "risk_assessment": {
                    "overall_risk_score": 25,
                    "risk_factors": ["Moderate credit score"],
                    "credit_risk": "LOW",
                    "income_stability": "HIGH",
                    "debt_capacity": "ADEQUATE"
                },
                "financial_ratios": {
                    "debt_to_income": 0.30,
                    "payment_to_income": 0.10,
                    "loan_to_value": 0
                },
                "recommendation": "APPROVE",
                "recommended_terms": {
                    "approved_amount": 45000,
                    "interest_rate": 8.5,
                    "term_months": 60,
                    "monthly_payment": 800
                },
                "compliance_checks": {
                    "kyc_verified": True,
                    "aml_cleared": True,
                    "income_verified": True,
                    "employment_verified": True
                },
                "reasoning": "Detailed analysis of credit application with comprehensive risk assessment."
            }
            
            audit = verifier.audit_analysis(analysis)
            
            # Check all dimensions scored
            assert len(audit["scores"]) == 8
            assert len(audit["dimensions"]) == 8
            assert len(audit["weights"]) == 8
            
            # Check dimension names
            expected_dims = [
                "Initiative", "Collaboration", "Reasoning Depth", "Compliance",
                "Efficiency", "Accuracy", "Risk Assessment", "Documentation"
            ]
            assert audit["dimensions"] == expected_dims
            
            # Check weights
            assert audit["weights"] == [1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.5, 1.2]
    
    def test_audit_compliance_scoring(self):
        """Test that compliance scoring reflects actual checks."""
        with patch('agents.credit_verifier.ChaosChainAgentSDK'):
            verifier = CreditVerifierAgent()
            verifier.agent_id = 2
            
            # Analysis with all compliance passed
            analysis_full = {
                "compliance_checks": {
                    "kyc_verified": True,
                    "aml_cleared": True,
                    "income_verified": True,
                    "employment_verified": True
                }
            }
            
            # Analysis with partial compliance
            analysis_partial = {
                "compliance_checks": {
                    "kyc_verified": True,
                    "aml_cleared": True,
                    "income_verified": False,
                    "employment_verified": False
                }
            }
            
            full_score = verifier._assess_compliance(analysis_full)
            partial_score = verifier._assess_compliance(analysis_partial)
            
            assert full_score == 100
            assert partial_score == 50
    
    def test_commit_reveal_protocol(self):
        """Test commit-reveal protocol for score submission."""
        with patch('agents.credit_verifier.ChaosChainAgentSDK') as mock_sdk:
            # Setup mock
            mock_instance = MagicMock()
            mock_sdk.return_value = mock_instance
            mock_instance.commit_score.return_value = "0xcommit123"
            mock_instance.reveal_score.return_value = "0xreveal456"
            
            verifier = CreditVerifierAgent()
            verifier.agent_id = 2
            verifier.studio_address = "0xstudio"
            
            # Data hash
            data_hash = hashlib.sha256(b"test_work").digest()
            scores = [85, 90, 88, 95, 82, 91, 87, 90]
            
            # Commit
            tx_hash, salt = verifier.commit_score(data_hash, scores)
            assert tx_hash == "0xcommit123"
            assert len(salt) == 32
            
            # Reveal
            reveal_tx = verifier.reveal_score(data_hash)
            assert reveal_tx == "0xreveal456"
            
            # Cannot reveal again
            with pytest.raises(ValueError):
                verifier.reveal_score(data_hash)


class TestCreditWorkflowIntegration:
    """Integration tests for full Credit Studio workflow."""
    
    def test_full_workflow(self):
        """Test complete worker -> verifier workflow."""
        with patch('agents.credit_worker.ChaosChainAgentSDK'), \
             patch('agents.credit_verifier.ChaosChainAgentSDK'):
            
            # Setup agents
            worker = CreditWorkerAgent()
            worker.agent_id = 1
            
            verifier = CreditVerifierAgent()
            verifier.agent_id = 2
            
            # Worker analyzes application
            application = {
                "applicant_name": "Integration Test",
                "credit_score": 720,
                "annual_income": 85000,
                "debt_to_income": 0.28,
                "employment_years": 5,
                "requested_amount": 50000
            }
            
            analysis = worker.analyze_credit_application(application)
            
            # Verifier audits analysis
            audit = verifier.audit_analysis(analysis)
            
            # Validate results
            assert analysis["recommendation"] in ["APPROVE", "APPROVE_WITH_CONDITIONS"]
            assert audit["final_score"] >= 70
            assert audit["recommendation"] == "APPROVED"
            
            # Calculate data hash
            analysis_json = json.dumps(analysis, sort_keys=True)
            data_hash = hashlib.sha256(analysis_json.encode()).digest()
            
            # Scores should be valid
            for score in audit["scores"]:
                assert 0 <= score <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

