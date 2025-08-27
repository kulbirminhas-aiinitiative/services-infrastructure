#!/usr/bin/env python3
"""
Simple End-to-End Test
======================

Direct test of the persona-driven workflow to validate:
1. Requirement translation through the chain
2. Code generation matching requirements  
3. Proper persona handoffs

This bypasses some complexity to focus on core requirement fidelity.
"""

import asyncio
import json
from workflow_orchestrator import PersonaAPIClient

async def test_direct_requirement_to_code():
    """Test direct requirement to code generation"""
    
    print("🧪 SIMPLE END-TO-END TEST")
    print("=" * 50)
    
    client = PersonaAPIClient()
    
    # Simple, clear requirement
    requirement = """
    Create a user authentication page for a fitness website with:
    1. Email and password login form
    2. Google and Facebook social login buttons  
    3. "Remember me" checkbox
    4. "Forgot password" link
    5. Clean, modern design with fitness theme
    6. Mobile responsive layout
    """
    
    print("📝 Original Requirement:")
    print(requirement)
    print("\n" + "=" * 50)
    
    # Step 1: Requirement Concierge - Structure the requirement
    print("\n1️⃣ REQUIREMENT CONCIERGE - Analyzing requirement")
    
    concierge_result = await client.call_persona(
        "requirement-concierge",
        f"Analyze and structure this website requirement: {requirement}",
        {"analysis_type": "web_development", "priority": "high"}
    )
    
    concierge_response = concierge_result.get("response", "")
    print(f"📋 Concierge Analysis (preview): {concierge_response[:200]}...")
    
    # Step 2: Solution Architect - Define technical approach
    print("\n2️⃣ SOLUTION ARCHITECT - Technical approach")
    
    architect_context = {
        "requirement_analysis": concierge_response[:500],
        "project_type": "fitness_website",
        "target_platform": "web"
    }
    
    architect_result = await client.call_persona(
        "solution-architect", 
        f"Design technical solution for: {requirement}",
        architect_context
    )
    
    architect_response = architect_result.get("response", "")
    print(f"🏗️ Architecture (preview): {architect_response[:200]}...")
    
    # Step 3: Developer - Generate actual code
    print("\n3️⃣ DEVELOPER - Code generation")
    
    developer_context = {
        "requirement": requirement,
        "architecture": architect_response[:500],
        "tech_stack": ["React", "TypeScript", "Tailwind CSS"],
        "target": "authentication_page"
    }
    
    developer_result = await client.call_persona(
        "developer",
        f"Implement the authentication page based on: {requirement}",
        developer_context
    )
    
    developer_response = developer_result.get("response", "")
    print(f"💻 Code Generated: {len(developer_response)} characters")
    print(f"📝 Code Preview:")
    print("-" * 30)
    print(developer_response[:1000])
    if len(developer_response) > 1000:
        print(f"\n... ({len(developer_response) - 1000} more characters)")
    print("-" * 30)
    
    # Step 4: Analyze requirement fidelity
    print("\n📊 REQUIREMENT FIDELITY ANALYSIS")
    
    required_elements = [
        "email", "password", "login", "form",
        "google", "facebook", "social",
        "remember me", "forgot password",
        "responsive", "mobile"
    ]
    
    found_elements = []
    for element in required_elements:
        if element.lower() in developer_response.lower():
            found_elements.append(element)
    
    fidelity_score = (len(found_elements) / len(required_elements)) * 100
    
    print(f"🎯 Requirement Fidelity Score: {fidelity_score:.1f}%")
    print(f"✅ Found: {', '.join(found_elements)}")
    missing = [e for e in required_elements if e not in found_elements]
    if missing:
        print(f"❌ Missing: {', '.join(missing)}")
    
    # Step 5: Check for code quality indicators
    print("\n💡 CODE QUALITY ANALYSIS")
    
    quality_indicators = {
        "React component": "component" in developer_response.lower() or "function" in developer_response.lower(),
        "Form handling": "form" in developer_response.lower() or "input" in developer_response.lower(),
        "Event handlers": "onclick" in developer_response.lower() or "onchange" in developer_response.lower() or "handle" in developer_response.lower(),
        "CSS/Styling": "style" in developer_response.lower() or "class" in developer_response.lower() or "css" in developer_response.lower(),
        "State management": "state" in developer_response.lower() or "usestate" in developer_response.lower()
    }
    
    for indicator, found in quality_indicators.items():
        status = "✅" if found else "❌"
        print(f"{status} {indicator}")
    
    # Final assessment
    print("\n🎉 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"✅ Requirement processed through 3 personas")
    print(f"📊 Requirement fidelity: {fidelity_score:.1f}%")
    print(f"💻 Code generated: {len(developer_response)} characters")
    
    code_quality_score = sum(quality_indicators.values()) / len(quality_indicators) * 100
    print(f"🏆 Code quality indicators: {code_quality_score:.1f}%")
    
    overall_success = fidelity_score > 70 and code_quality_score > 60
    print(f"🎯 Overall Success: {'✅ PASS' if overall_success else '❌ NEEDS IMPROVEMENT'}")
    
    return {
        "requirement_fidelity": fidelity_score,
        "code_quality": code_quality_score,
        "success": overall_success,
        "generated_code": developer_response,
        "personas_used": ["requirement-concierge", "solution-architect", "developer"]
    }

async def test_specific_website_feature():
    """Test generation of a specific website feature"""
    
    print("\n\n🌐 SPECIFIC FEATURE TEST: FITNESS TRACKER COMPONENT")
    print("=" * 60)
    
    client = PersonaAPIClient()
    
    feature_requirement = """
    Create a workout logging component for the fitness website:
    - Form to log workout details (exercise name, sets, reps, weight)
    - Dropdown to select exercise from predefined list
    - Add/remove exercise rows dynamically
    - Save workout to local storage
    - Display recent workouts history
    - Progress charts showing improvement over time
    """
    
    print("📝 Feature Requirement:")
    print(feature_requirement)
    
    # Direct to developer for focused test
    result = await client.call_persona(
        "developer",
        f"Create a React component for: {feature_requirement}",
        {
            "component_type": "workout_logger",
            "framework": "React",
            "styling": "Tailwind CSS",
            "storage": "localStorage"
        }
    )
    
    response = result.get("response", "")
    print(f"\n💻 Generated Component ({len(response)} characters):")
    print("-" * 40)
    print(response)
    
    # Check for specific feature elements
    feature_elements = [
        "workout", "exercise", "sets", "reps", "weight",
        "dropdown", "form", "storage", "history", "chart"
    ]
    
    found_features = [elem for elem in feature_elements if elem.lower() in response.lower()]
    feature_score = (len(found_features) / len(feature_elements)) * 100
    
    print(f"\n📊 Feature Coverage: {feature_score:.1f}%")
    print(f"✅ Implemented: {', '.join(found_features)}")
    
    return {
        "feature_coverage": feature_score,
        "generated_code": response
    }

async def main():
    """Run all end-to-end tests"""
    
    print("🚀 STARTING COMPREHENSIVE E2E TESTS")
    print("=" * 60)
    
    # Test 1: Full requirement to code flow
    auth_test = await test_direct_requirement_to_code()
    
    # Test 2: Specific feature generation
    feature_test = await test_specific_website_feature()
    
    # Overall results
    print("\n\n📈 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    print(f"🔐 Auth Page Test:")
    print(f"   Requirement Fidelity: {auth_test['requirement_fidelity']:.1f}%")
    print(f"   Code Quality: {auth_test['code_quality']:.1f}%")
    print(f"   Success: {'✅' if auth_test['success'] else '❌'}")
    
    print(f"\n🏋️ Workout Feature Test:")
    print(f"   Feature Coverage: {feature_test['feature_coverage']:.1f}%")
    
    overall_score = (auth_test['requirement_fidelity'] + auth_test['code_quality'] + feature_test['feature_coverage']) / 3
    print(f"\n🎯 Overall System Score: {overall_score:.1f}%")
    
    if overall_score > 75:
        print("🎉 EXCELLENT: System successfully translates requirements to code!")
    elif overall_score > 50:
        print("✅ GOOD: System works but has room for improvement")
    else:
        print("⚠️ NEEDS WORK: System requires optimization")
    
    return {
        "auth_test": auth_test,
        "feature_test": feature_test,
        "overall_score": overall_score
    }

if __name__ == "__main__":
    results = asyncio.run(main())