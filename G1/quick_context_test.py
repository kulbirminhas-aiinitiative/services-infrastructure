#!/usr/bin/env python3
"""
Quick Context Integration Test
=============================

Focused test to validate the context integration fix.
"""

import asyncio
import json
from workflow_orchestrator import WorkflowContextManager
from workflow_orchestrator import PersonaAPIClient

async def test_context_integration():
    """Test the context integration with workflow accumulation"""
    
    print("🧪 TESTING CONTEXT INTEGRATION WITH WORKFLOW ACCUMULATION")
    print("="*70)
    
    # Initialize components
    context_manager = WorkflowContextManager()
    persona_client = PersonaAPIClient()
    
    # Step 1: Get initial analysis
    print("\n1️⃣ REQUIREMENT CONCIERGE - Initial Analysis")
    concierge_result = await persona_client.call_persona(
        "requirement-concierge",
        "Analyze requirement: Build OAuth-enabled user authentication system with 6-week deadline for 3 developers",
        {"phase": "initial_analysis", "project_constraints": ["OAuth required", "6 weeks", "3 developers"]},
        context_manager
    )
    
    print(f"✅ Concierge Response: {concierge_result['response'][:150]}...")
    
    # Step 2: Program Manager with accumulated context
    print("\n2️⃣ PROGRAM MANAGER - Project Planning (WITH ACCUMULATED CONTEXT)")
    pm_result = await persona_client.call_persona(
        "program-manager", 
        "Create project plan based on the requirement analysis",
        {"phase": "project_planning", "stakeholders": ["development_team", "product_owner"]},
        context_manager
    )
    
    print(f"✅ PM Response: {pm_result['response'][:150]}...")
    
    # Step 3: Developer with full accumulated context
    print("\n3️⃣ DEVELOPER - Technical Implementation (WITH FULL CONTEXT)")
    dev_result = await persona_client.call_persona(
        "developer",
        "Design technical architecture based on previous analysis and planning",
        {"phase": "technical_design", "constraints": ["security_first", "scalable"]},
        context_manager
    )
    
    print(f"✅ Developer Response: {dev_result['response'][:150]}...")
    
    # Analyze context utilization
    print("\n🔍 CONTEXT UTILIZATION ANALYSIS")
    print("="*50)
    
    # Check if OAuth is mentioned in all responses
    oauth_mentioned = {
        "concierge": "oauth" in concierge_result['response'].lower(),
        "pm": "oauth" in pm_result['response'].lower(), 
        "developer": "oauth" in dev_result['response'].lower()
    }
    
    # Check if timeline is mentioned
    timeline_mentioned = {
        "concierge": any(term in concierge_result['response'].lower() for term in ["6", "week", "timeline"]),
        "pm": any(term in pm_result['response'].lower() for term in ["6", "week", "timeline"]),
        "developer": any(term in dev_result['response'].lower() for term in ["6", "week", "timeline"])
    }
    
    # Check if team size is mentioned
    team_mentioned = {
        "concierge": any(term in concierge_result['response'].lower() for term in ["3", "three", "developer"]),
        "pm": any(term in pm_result['response'].lower() for term in ["3", "three", "developer"]),
        "developer": any(term in dev_result['response'].lower() for term in ["3", "three", "developer"])
    }
    
    print(f"OAuth Context Utilization:")
    for persona, mentioned in oauth_mentioned.items():
        status = "✅" if mentioned else "❌"
        print(f"  {status} {persona.upper()}: {'OAuth mentioned' if mentioned else 'OAuth missing'}")
    
    print(f"\nTimeline Context Utilization:")
    for persona, mentioned in timeline_mentioned.items():
        status = "✅" if mentioned else "❌"
        print(f"  {status} {persona.upper()}: {'Timeline mentioned' if mentioned else 'Timeline missing'}")
    
    print(f"\nTeam Size Context Utilization:")
    for persona, mentioned in team_mentioned.items():
        status = "✅" if mentioned else "❌"
        print(f"  {status} {persona.upper()}: {'Team size mentioned' if mentioned else 'Team size missing'}")
    
    # Overall assessment
    total_context_items = 9  # 3 personas × 3 context elements
    utilized_items = sum(oauth_mentioned.values()) + sum(timeline_mentioned.values()) + sum(team_mentioned.values())
    utilization_rate = (utilized_items / total_context_items) * 100
    
    print(f"\n📊 OVERALL CONTEXT UTILIZATION: {utilization_rate:.1f}% ({utilized_items}/{total_context_items})")
    
    if utilization_rate >= 70:
        print("🎉 CONTEXT INTEGRATION: SUCCESS")
    elif utilization_rate >= 40:
        print("⚠️ CONTEXT INTEGRATION: PARTIAL")
    else:
        print("❌ CONTEXT INTEGRATION: FAILED")
    
    # Show accumulated context
    print(f"\n🗂️ WORKFLOW CONTEXT ACCUMULATED:")
    print(f"Personas processed: {len(context_manager.persona_outputs)}")
    for persona in context_manager.persona_outputs.keys():
        print(f"  ✓ {persona}")
    
    return {
        "oauth_utilization": oauth_mentioned,
        "timeline_utilization": timeline_mentioned,
        "team_utilization": team_mentioned,
        "overall_rate": utilization_rate,
        "personas_processed": len(context_manager.persona_outputs)
    }

if __name__ == "__main__":
    result = asyncio.run(test_context_integration())
    print(f"\nTest completed with {result['overall_rate']:.1f}% context utilization")