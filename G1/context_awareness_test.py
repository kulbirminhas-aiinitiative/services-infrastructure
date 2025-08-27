#!/usr/bin/env python3
"""
Context Awareness Test
=====================

Test to verify if personas are truly context-aware and can build upon
previous persona outputs in the workflow.
"""

import asyncio
import json
from datetime import datetime
from workflow_orchestrator import DynamicWorkflowOrchestrator
import time

class ContextAwarenessValidator:
    """Test and validate context awareness between personas"""
    
    def __init__(self):
        self.orchestrator = DynamicWorkflowOrchestrator()
        self.context_flow_test = []
        
    async def test_context_awareness_chain(self):
        """Test context awareness through a sequential persona chain"""
        
        print("\n" + "="*80)
        print("🧠 CONTEXT AWARENESS TEST")
        print("="*80)
        print("Testing if personas can build upon previous persona outputs")
        print("="*80)
        
        # Initial requirement
        initial_requirement = "Build a simple user management system with login, registration, and profile management"
        
        # Step 1: Requirement Concierge Analysis
        print(f"\n1️⃣ REQUIREMENT CONCIERGE - Initial Analysis")
        print(f"Input: {initial_requirement}")
        
        concierge_result = await self.orchestrator.persona_client.call_persona(
            "requirement-concierge",
            f"Analyze this requirement: {initial_requirement}. Provide detailed business analysis, stakeholder identification, and acceptance criteria.",
            {"phase": "initial_analysis", "requirement_id": "REQ-001"}
        )
        
        concierge_output = concierge_result.get("response", "No response")
        print(f"Output: {concierge_output[:200]}...")
        
        # Step 2: Program Manager - Should reference concierge analysis
        print(f"\n2️⃣ PROGRAM MANAGER - Project Planning (CONTEXT AWARE TEST)")
        print("Input: Should reference and build upon the requirement concierge analysis")
        
        pm_input = f"""Based on the requirement analysis provided by the requirement concierge:
        
REQUIREMENT CONCIERGE ANALYSIS:
{concierge_output}

Create a detailed project plan that builds upon this analysis. Reference specific elements from the analysis above and create:
1. Project timeline based on the identified complexity
2. Resource allocation considering the stakeholders mentioned
3. Risk mitigation for the risks identified in the analysis
4. Success metrics based on the business objectives outlined

Show explicit references to the concierge analysis in your response."""
        
        pm_result = await self.orchestrator.persona_client.call_persona(
            "program-manager", 
            pm_input,
            {
                "phase": "project_planning",
                "requirement_id": "REQ-001",
                "previous_persona": "requirement-concierge",
                "previous_output": concierge_output[:500]  # Include context
            }
        )
        
        pm_output = pm_result.get("response", "No response")
        print(f"Output: {pm_output[:200]}...")
        
        # Step 3: Developer - Should reference both previous outputs
        print(f"\n3️⃣ DEVELOPER - Technical Implementation (CONTEXT AWARE TEST)")
        print("Input: Should reference both concierge analysis AND program manager plan")
        
        dev_input = f"""Based on the requirement analysis and project plan from previous personas:

REQUIREMENT CONCIERGE ANALYSIS:
{concierge_output[:300]}...

PROGRAM MANAGER PROJECT PLAN:
{pm_output[:300]}...

Create a technical implementation that addresses:
1. The specific requirements identified by the concierge
2. The timeline constraints from the project manager
3. The technical architecture for the user management system

Explicitly reference elements from both previous analyses and show how they influence your technical decisions."""
        
        dev_result = await self.orchestrator.persona_client.call_persona(
            "developer",
            dev_input,
            {
                "phase": "technical_implementation", 
                "requirement_id": "REQ-001",
                "previous_personas": ["requirement-concierge", "program-manager"],
                "concierge_analysis": concierge_output[:200],
                "pm_plan": pm_output[:200]
            }
        )
        
        dev_output = dev_result.get("response", "No response")
        print(f"Output: {dev_output[:200]}...")
        
        # Analyze context awareness
        print(f"\n" + "="*80)
        print("🔍 CONTEXT AWARENESS ANALYSIS")
        print("="*80)
        
        context_analysis = self.analyze_context_awareness(
            concierge_output, pm_output, dev_output
        )
        
        for analysis in context_analysis:
            print(f"{analysis['status']} {analysis['test']}: {analysis['result']}")
        
        return {
            "concierge_output": concierge_output,
            "pm_output": pm_output,
            "dev_output": dev_output,
            "context_analysis": context_analysis
        }
    
    def analyze_context_awareness(self, concierge_output: str, pm_output: str, dev_output: str):
        """Analyze if personas referenced previous outputs"""
        
        analysis_results = []
        
        # Test 1: Does PM reference concierge analysis?
        pm_references_concierge = self.check_cross_references(concierge_output, pm_output)
        analysis_results.append({
            "test": "Program Manager references Requirement Concierge",
            "result": f"Found {len(pm_references_concierge)} potential references",
            "status": "✅" if len(pm_references_concierge) > 0 else "❌",
            "references": pm_references_concierge
        })
        
        # Test 2: Does Developer reference PM plan?
        dev_references_pm = self.check_cross_references(pm_output, dev_output)
        analysis_results.append({
            "test": "Developer references Program Manager plan", 
            "result": f"Found {len(dev_references_pm)} potential references",
            "status": "✅" if len(dev_references_pm) > 0 else "❌",
            "references": dev_references_pm
        })
        
        # Test 3: Does Developer reference original concierge analysis?
        dev_references_concierge = self.check_cross_references(concierge_output, dev_output)
        analysis_results.append({
            "test": "Developer references original Requirement analysis",
            "result": f"Found {len(dev_references_concierge)} potential references", 
            "status": "✅" if len(dev_references_concierge) > 0 else "❌",
            "references": dev_references_concierge
        })
        
        # Test 4: Context accumulation - Does each persona build upon previous?
        context_building = self.analyze_context_building(concierge_output, pm_output, dev_output)
        analysis_results.append({
            "test": "Context accumulation and building",
            "result": context_building["assessment"],
            "status": "✅" if context_building["is_building"] else "❌",
            "details": context_building
        })
        
        return analysis_results
    
    def check_cross_references(self, source_output: str, target_output: str) -> list:
        """Check if target output references concepts from source output"""
        
        # Extract key concepts from source (simplified approach)
        source_words = source_output.lower().split()
        target_words = target_output.lower().split()
        
        # Look for shared conceptual terms (simplified analysis)
        shared_concepts = []
        key_terms = ["stakeholder", "risk", "timeline", "requirement", "business", "technical", 
                    "security", "user", "management", "system", "analysis", "planning"]
        
        for term in key_terms:
            if term in source_words and term in target_words:
                # Find context around the term in both
                source_context = self.get_word_context(source_output.lower(), term, 3)
                target_context = self.get_word_context(target_output.lower(), term, 3)
                shared_concepts.append({
                    "term": term,
                    "source_context": source_context,
                    "target_context": target_context
                })
        
        return shared_concepts
    
    def get_word_context(self, text: str, word: str, context_words: int = 3) -> str:
        """Get context around a word"""
        words = text.split()
        try:
            word_index = words.index(word)
            start = max(0, word_index - context_words)
            end = min(len(words), word_index + context_words + 1)
            return " ".join(words[start:end])
        except ValueError:
            return ""
    
    def analyze_context_building(self, concierge: str, pm: str, dev: str) -> dict:
        """Analyze if context is building through the workflow"""
        
        # Simple metrics for context building
        concierge_concepts = len(set(concierge.lower().split()))
        pm_concepts = len(set(pm.lower().split()))
        dev_concepts = len(set(dev.lower().split()))
        
        # Check if content is expanding and building
        is_building = pm_concepts > concierge_concepts * 0.5 and dev_concepts > pm_concepts * 0.5
        
        # Check for specific indicators of context awareness
        context_indicators = {
            "pm_has_based_on": "based on" in pm.lower() or "according to" in pm.lower(),
            "dev_has_references": "analysis" in dev.lower() and "plan" in dev.lower(),
            "dev_has_technical_depth": len([w for w in dev.lower().split() if w in ["api", "database", "code", "implementation", "architecture"]]) > 3
        }
        
        assessment = "Building context" if is_building and any(context_indicators.values()) else "Limited context building"
        
        return {
            "is_building": is_building and any(context_indicators.values()),
            "assessment": assessment,
            "concept_counts": {
                "concierge": concierge_concepts,
                "pm": pm_concepts, 
                "dev": dev_concepts
            },
            "context_indicators": context_indicators
        }

    async def test_context_preservation_mechanism(self):
        """Test if the current system preserves context between calls"""
        
        print(f"\n" + "="*80)
        print("🔄 CONTEXT PRESERVATION MECHANISM TEST")
        print("="*80)
        
        # Test the workflow orchestrator's context handling
        test_context = {
            "workflow_id": "TEST-001",
            "previous_outputs": {
                "requirement-concierge": "User authentication system with OAuth integration",
                "program-manager": "6-week timeline, 3 developers allocated"
            },
            "accumulated_requirements": [
                "OAuth integration required",
                "3-developer team constraint", 
                "6-week delivery timeline"
            ]
        }
        
        # Call developer with rich context
        print(f"Testing with rich context: {len(test_context)} context elements")
        
        dev_result = await self.orchestrator.persona_client.call_persona(
            "developer",
            "Design the technical architecture for the user authentication system based on the previous analysis and planning.",
            test_context
        )
        
        dev_response = dev_result.get("response", "")
        
        # Analyze if context was utilized
        context_utilization = self.analyze_context_utilization(test_context, dev_response)
        
        print(f"Context Utilization Analysis:")
        for key, result in context_utilization.items():
            status = "✅" if result else "❌" 
            print(f"  {status} {key}")
        
        return context_utilization

    def analyze_context_utilization(self, provided_context: dict, response: str) -> dict:
        """Analyze if provided context was utilized in the response"""
        
        response_lower = response.lower()
        
        return {
            "references_oauth": "oauth" in response_lower,
            "references_timeline": any(word in response_lower for word in ["6", "week", "timeline", "schedule"]),
            "references_team_size": any(word in response_lower for word in ["3", "three", "team", "developer"]),
            "has_technical_depth": any(word in response_lower for word in ["architecture", "api", "database", "security"]),
            "acknowledges_constraints": any(word in response_lower for word in ["constraint", "requirement", "based on"]),
        }


async def main():
    """Execute context awareness validation"""
    
    validator = ContextAwarenessValidator()
    
    # Test 1: Sequential context building
    print("STARTING CONTEXT AWARENESS VALIDATION")
    sequential_results = await validator.test_context_awareness_chain()
    
    # Test 2: Context preservation mechanism
    preservation_results = await validator.test_context_preservation_mechanism()
    
    # Final assessment
    print(f"\n" + "="*80)
    print("📋 FINAL CONTEXT AWARENESS ASSESSMENT")
    print("="*80)
    
    sequential_passed = sum(1 for analysis in sequential_results["context_analysis"] if analysis["status"] == "✅")
    preservation_passed = sum(1 for result in preservation_results.values() if result)
    
    print(f"Sequential Context Tests: {sequential_passed}/4 passed")
    print(f"Context Preservation Tests: {preservation_passed}/{len(preservation_results)} passed") 
    
    overall_status = "✅ CONTEXT AWARE" if (sequential_passed >= 2 and preservation_passed >= 3) else "❌ LIMITED CONTEXT AWARENESS"
    print(f"\nOverall Assessment: {overall_status}")
    
    if "❌" in overall_status:
        print("\n🚨 CONTEXT AWARENESS ISSUES IDENTIFIED:")
        print("- Personas may not be referencing previous outputs")
        print("- Context preservation mechanism needs improvement") 
        print("- RAG engine may not be utilizing provided context")
    
    # Save detailed results
    with open("context_awareness_test_results.json", "w") as f:
        json.dump({
            "sequential_results": sequential_results,
            "preservation_results": preservation_results,
            "assessment": {
                "sequential_passed": sequential_passed,
                "preservation_passed": preservation_passed,
                "overall_status": overall_status
            }
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: context_awareness_test_results.json")


if __name__ == "__main__":
    asyncio.run(main())