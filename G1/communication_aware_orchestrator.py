#!/usr/bin/env python3
"""
Communication-Aware Workflow Orchestrator
==========================================

Enhanced orchestrator that eliminates Chinese Whispers effect using AI personas
for communication intelligence, verification, and collaborative transitions.

Key Features:
- Hub-and-spoke communication via Central Knowledge Hub persona
- Read-back verification via Verification Service persona  
- Collaborative transitions via Collaborative Transition Manager persona
- Pull-based context delivery with role-appropriate information
- Communication anti-pattern prevention
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

from workflow_orchestrator import PersonaAPIClient, WorkflowContextManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CommunicationAwareOrchestrator:
    """Enhanced orchestrator with communication intelligence"""
    
    def __init__(self):
        self.persona_client = PersonaAPIClient()
        self.context_manager = WorkflowContextManager()
        
        # Communication personas
        self.knowledge_hub = "central-knowledge-hub"
        self.verification_service = "verification-service"
        self.collaboration_manager = "collaborative-transition-manager"
        
        # Workflow personas
        self.workflow_personas = [
            "requirement-concierge",
            "program-manager", 
            "developer",
            "tester"
        ]
    
    async def store_original_requirement(self, requirement_text: str, context: Dict[str, Any]) -> str:
        """Store original requirement in knowledge hub"""
        req_id = str(uuid.uuid4())
        
        storage_request = f"""
        Please store this original requirement with complete context:
        
        REQUIREMENT: {requirement_text}
        
        CONTEXT:
        {json.dumps(context, indent=2)}
        
        Please assign requirement ID: {req_id}
        
        Ensure complete context preservation for downstream personas.
        """
        
        result = await self.persona_client.call_persona(
            self.knowledge_hub,
            storage_request,
            {"action": "store_requirement", "requirement_id": req_id}
        )
        
        logger.info(f"Stored requirement {req_id} in knowledge hub")
        return req_id
    
    async def get_context_from_hub(self, req_id: str, persona_name: str, context_scope: str = "standard") -> Dict[str, Any]:
        """Pull context from knowledge hub for specific persona"""
        
        context_request = f"""
        Please provide role-appropriate context for {persona_name} regarding requirement {req_id}.
        
        Context scope requested: {context_scope}
        
        Deliver exactly what this persona needs for their role without information loss or filtering.
        Include complete traceability to original requirement.
        """
        
        result = await self.persona_client.call_persona(
            self.knowledge_hub,
            context_request,
            {
                "action": "get_context",
                "requirement_id": req_id,
                "persona_type": persona_name,
                "context_scope": context_scope
            }
        )
        
        # Extract structured context from response
        context = {
            "requirement_id": req_id,
            "persona_context": result.get("response", ""),
            "source": "knowledge_hub",
            "pull_timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Pulled {context_scope} context for {persona_name} from knowledge hub")
        return context
    
    async def log_persona_interpretation(self, req_id: str, persona_name: str, interpretation: str):
        """Log persona interpretation back to knowledge hub"""
        
        logging_request = f"""
        Please log the following persona interpretation:
        
        REQUIREMENT ID: {req_id}
        PERSONA: {persona_name}
        INTERPRETATION: {interpretation}
        
        Track this interpretation for audit trail and communication analysis.
        """
        
        await self.persona_client.call_persona(
            self.knowledge_hub,
            logging_request,
            {
                "action": "log_interpretation",
                "requirement_id": req_id,
                "persona": persona_name,
                "interpretation": interpretation[:500]  # Truncate for context
            }
        )
        
        logger.info(f"Logged interpretation from {persona_name} for requirement {req_id}")
    
    async def verify_understanding(self, req_id: str, upstream_persona: str, downstream_persona: str, 
                                 upstream_output: str, downstream_understanding: str) -> Dict[str, Any]:
        """Verify downstream persona understands upstream output"""
        
        verification_request = f"""
        Please verify understanding between personas:
        
        REQUIREMENT ID: {req_id}
        UPSTREAM PERSONA: {upstream_persona}
        DOWNSTREAM PERSONA: {downstream_persona}
        
        UPSTREAM OUTPUT:
        {upstream_output}
        
        DOWNSTREAM UNDERSTANDING:
        {downstream_understanding}
        
        Verify accuracy and identify any gaps, assumptions, or misunderstandings.
        Provide understanding accuracy score and clarification recommendations.
        """
        
        result = await self.persona_client.call_persona(
            self.verification_service,
            verification_request,
            {
                "action": "verify_understanding",
                "requirement_id": req_id,
                "upstream_persona": upstream_persona,
                "downstream_persona": downstream_persona
            }
        )
        
        verification_result = {
            "verified": "VERIFIED" in result.get("response", "").upper(),
            "accuracy_mentioned": any(score in result.get("response", "") for score in ["0.", "1."]),
            "clarification_needed": "CLARIFICATION" in result.get("response", "").upper(),
            "verification_response": result.get("response", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Verification between {upstream_persona} → {downstream_persona}: {'PASSED' if verification_result['verified'] else 'NEEDS_CLARIFICATION'}")
        return verification_result
    
    async def facilitate_collaborative_handoff(self, req_id: str, upstream_persona: str, downstream_persona: str,
                                             upstream_output: str) -> Dict[str, Any]:
        """Facilitate collaborative handoff between personas"""
        
        handoff_request = f"""
        Please orchestrate a collaborative handoff:
        
        REQUIREMENT ID: {req_id}
        HANDOFF: {upstream_persona} → {downstream_persona}
        
        UPSTREAM OUTPUT TO TRANSFER:
        {upstream_output}
        
        Please create a collaborative transition plan with:
        1. Joint review session outcomes
        2. Knowledge transfer protocol
        3. Mentorship period coordination
        4. Quality scoring and validation
        
        Ensure no information loss during transition.
        """
        
        result = await self.persona_client.call_persona(
            self.collaboration_manager,
            handoff_request,
            {
                "action": "facilitate_handoff",
                "requirement_id": req_id,
                "upstream_persona": upstream_persona,
                "downstream_persona": downstream_persona
            }
        )
        
        handoff_result = {
            "handoff_complete": "READY" in result.get("response", "").upper(),
            "quality_score_mentioned": any(score in result.get("response", "") for score in ["0.", "1."]),
            "mentorship_planned": "mentorship" in result.get("response", "").lower(),
            "collaboration_plan": result.get("response", ""),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Collaborative handoff {upstream_persona} → {downstream_persona}: {'READY' if handoff_result['handoff_complete'] else 'IN_PROGRESS'}")
        return handoff_result
    
    async def execute_communication_aware_workflow(self, requirement_text: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute workflow with communication intelligence"""
        
        logger.info("🎯 Starting Communication-Aware Workflow Execution")
        logger.info("="*70)
        
        # Step 1: Store original requirement in knowledge hub
        req_id = await self.store_original_requirement(requirement_text, context)
        logger.info(f"✅ Requirement stored in knowledge hub: {req_id}")
        
        # Step 2: Process with each persona using pull-based context
        persona_results = {}
        previous_persona = None
        previous_output = None
        
        for i, persona in enumerate(self.workflow_personas):
            logger.info(f"\n{i+1}️⃣ Processing with {persona.upper()}")
            
            # Pull appropriate context from knowledge hub
            persona_context = await self.get_context_from_hub(req_id, persona, "standard")
            
            # Add context from context manager for workflow continuity
            if persona in self.context_manager.persona_outputs:
                workflow_context = self.context_manager.get_enriched_context(persona, persona_context)
            else:
                workflow_context = persona_context
            
            # Process with persona
            result = await self.persona_client.call_persona(
                persona,
                requirement_text,
                workflow_context,
                self.context_manager
            )
            
            persona_results[persona] = result
            persona_output = result.get("response", "")
            
            # Log interpretation back to knowledge hub
            await self.log_persona_interpretation(req_id, persona, persona_output)
            
            # Verification step (if not first persona)
            if previous_persona and previous_output:
                logger.info(f"🔍 Verifying understanding: {previous_persona} → {persona}")
                
                # Ask current persona to paraphrase their understanding
                understanding_check = await self.persona_client.call_persona(
                    persona,
                    f"Please paraphrase your understanding of the previous output from {previous_persona}: {previous_output[:300]}...",
                    {"verification_check": True}
                )
                
                # Verify understanding
                verification = await self.verify_understanding(
                    req_id, previous_persona, persona, 
                    previous_output, understanding_check.get("response", "")
                )
                
                persona_results[persona]["verification"] = verification
                
                # Collaborative handoff if verification passes
                if verification.get("verified", False):
                    logger.info(f"🤝 Facilitating collaborative handoff: {previous_persona} → {persona}")
                    handoff = await self.facilitate_collaborative_handoff(
                        req_id, previous_persona, persona, previous_output
                    )
                    persona_results[persona]["handoff"] = handoff
                else:
                    logger.warning(f"⚠️ Verification failed, clarification may be needed")
            
            previous_persona = persona
            previous_output = persona_output
            
            logger.info(f"✅ {persona} completed successfully")
        
        # Step 3: Final analysis and communication quality assessment
        logger.info(f"\n📊 Analyzing Communication Quality")
        
        communication_analysis = await self.analyze_communication_quality(req_id, persona_results)
        
        workflow_result = {
            "requirement_id": req_id,
            "original_requirement": requirement_text,
            "persona_results": persona_results,
            "communication_analysis": communication_analysis,
            "workflow_completed": True,
            "completion_timestamp": datetime.now().isoformat(),
            "personas_processed": len(persona_results),
            "verifications_passed": sum(1 for r in persona_results.values() 
                                     if r.get("verification", {}).get("verified", False)),
            "handoffs_completed": sum(1 for r in persona_results.values()
                                   if r.get("handoff", {}).get("handoff_complete", False))
        }
        
        logger.info("🎉 Communication-Aware Workflow Completed")
        logger.info(f"   Personas: {len(persona_results)}")
        logger.info(f"   Verifications: {workflow_result['verifications_passed']}")
        logger.info(f"   Handoffs: {workflow_result['handoffs_completed']}")
        
        return workflow_result
    
    async def analyze_communication_quality(self, req_id: str, persona_results: Dict) -> Dict[str, Any]:
        """Analyze overall communication quality using knowledge hub"""
        
        analysis_request = f"""
        Please analyze communication quality for requirement {req_id}:
        
        PERSONAS PROCESSED: {list(persona_results.keys())}
        
        Please provide:
        1. Overall communication fidelity score
        2. Information loss assessment  
        3. Context preservation analysis
        4. Anti-pattern detection results
        5. Communication effectiveness summary
        
        Analyze how well the original requirement was preserved through the workflow.
        """
        
        result = await self.persona_client.call_persona(
            self.knowledge_hub,
            analysis_request,
            {
                "action": "analyze_communication_quality",
                "requirement_id": req_id,
                "personas_processed": list(persona_results.keys())
            }
        )
        
        return {
            "communication_analysis": result.get("response", ""),
            "analysis_timestamp": datetime.now().isoformat(),
            "personas_analyzed": len(persona_results),
            "hub_analysis_available": True
        }


async def test_communication_aware_workflow():
    """Test the communication-aware workflow"""
    
    orchestrator = CommunicationAwareOrchestrator()
    
    # Test requirement
    requirement = "Build a secure user authentication system with OAuth integration, profile management, and multi-factor authentication for a web application."
    
    context = {
        "business_rationale": "Enable secure user access and personalized experiences",
        "stakeholder_priorities": ["security", "user_experience", "compliance"],
        "constraints": ["6-week timeline", "3 developers", "must integrate with existing systems"],
        "success_criteria": ["successful authentication", "secure profile management", "MFA implementation"],
        "timeline": "6 weeks",
        "resources": {"developers": 3, "budget": "$50000"},
        "dependencies": ["existing user database", "OAuth provider integration"],
        "assumptions": ["users have email addresses", "OAuth provider available"]
    }
    
    print("🚀 Testing Communication-Aware Workflow")
    print("="*70)
    
    result = await orchestrator.execute_communication_aware_workflow(requirement, context)
    
    print(f"\n📊 Final Results:")
    print(f"   Requirement ID: {result['requirement_id']}")
    print(f"   Personas Processed: {result['personas_processed']}")
    print(f"   Verifications Passed: {result['verifications_passed']}")
    print(f"   Handoffs Completed: {result['handoffs_completed']}")
    print(f"   Communication Analysis Available: {result['communication_analysis']['hub_analysis_available']}")
    
    return result


if __name__ == "__main__":
    asyncio.run(test_communication_aware_workflow())