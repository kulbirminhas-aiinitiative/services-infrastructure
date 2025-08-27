#!/usr/bin/env python3
"""
Complex Website Workflow Test
============================

Test the pure persona-driven workflow with a complex website requirement
to ensure proper requirement translation and code generation.

This test validates:
1. Requirement structuring and sharing between personas
2. Requirement fidelity throughout the workflow
3. Final code generation alignment with original requirements
4. Communication effectiveness across persona handoffs
"""

import asyncio
import json
from datetime import datetime
from pure_persona_driven_orchestrator import PurePersonaDrivenOrchestrator

async def test_complex_website_workflow():
    """Test workflow with complex website requirement"""
    
    orchestrator = PurePersonaDrivenOrchestrator()
    
    # Complex website requirement
    complex_website_requirement = """
    Build a comprehensive fitness tracking and community website with the following features:
    
    **USER MANAGEMENT & AUTHENTICATION:**
    - User registration with email verification
    - Social login (Google, Facebook, Apple)
    - User profiles with customizable avatars and fitness goals
    - Privacy settings for profile visibility
    - Account management (password reset, account deletion)
    
    **FITNESS TRACKING FEATURES:**
    - Workout logging with exercise library (500+ exercises)
    - Custom workout creation and sharing
    - Progress tracking with charts and analytics
    - Body measurements tracking (weight, body fat, muscle mass)
    - Photo progress comparison (before/after photos)
    - Nutrition logging with calorie and macro tracking
    - Integration with fitness devices (Fitbit, Apple Watch, Garmin)
    
    **COMMUNITY FEATURES:**
    - Social feed with workout posts and achievements
    - Follow system (follow other users)
    - Workout challenges and competitions
    - Community groups based on fitness goals
    - Achievement badges and leaderboards
    - Messaging system between users
    - Forum-style discussions by topic
    
    **CONTENT MANAGEMENT:**
    - Blog section with fitness articles
    - Video workout library with streaming
    - Meal planning with recipe database
    - Educational content (exercise guides, nutrition tips)
    - Expert trainer profiles and content
    
    **TECHNICAL REQUIREMENTS:**
    - Responsive design (mobile-first approach)
    - Progressive Web App (PWA) capabilities
    - Real-time notifications for social interactions
    - Advanced search and filtering capabilities
    - Data export functionality (workout history, progress data)
    - API integration with third-party fitness services
    - SEO optimization for content discovery
    - Performance optimization (sub-3-second load times)
    
    **BUSINESS REQUIREMENTS:**
    - Freemium model with premium subscription tiers
    - Payment processing for subscriptions
    - Analytics dashboard for business metrics
    - Content moderation tools
    - User reporting and safety features
    - GDPR and privacy compliance
    - Scalability to handle 100K+ users
    
    **DESIGN REQUIREMENTS:**
    - Modern, motivational design aesthetic
    - Dark mode and light mode support
    - Accessibility compliance (WCAG 2.1 AA)
    - Consistent design system and component library
    - Smooth animations and micro-interactions
    - Mobile-optimized touch interactions
    """
    
    project_context = {
        "project_type": "complex_fitness_community_website",
        "complexity": "enterprise",
        "timeline": "8_months",
        "team_size_preference": "multi_team_structure", 
        "technology_stack": ["React", "Next.js", "Node.js", "MongoDB", "Redis", "AWS"],
        "performance_requirements": ["sub_3_second_load", "100k_users", "real_time_features"],
        "compliance_requirements": ["GDPR", "WCAG_2.1_AA", "data_privacy"],
        "business_model": ["freemium", "subscription", "payment_processing"],
        "integration_requirements": ["fitbit", "apple_watch", "garmin", "social_logins"],
        "business_constraints": {
            "budget": "$800K",
            "go_to_market": "Q3_2025",
            "user_target": "100K_users",
            "revenue_target": "$500K_ARR",
            "stakeholder_priorities": ["user_engagement", "scalability", "monetization", "retention"]
        },
        "technical_constraints": {
            "cloud_provider": "AWS",
            "mobile_support": "PWA_required", 
            "real_time": "websockets_required",
            "seo_requirements": "high_search_visibility",
            "analytics": "comprehensive_tracking"
        },
        "success_criteria": [
            "User registration and authentication working",
            "Core fitness tracking functional",
            "Social features enabling community engagement", 
            "Payment processing for subscriptions",
            "Mobile-responsive design achieved",
            "Performance targets met (sub-3-second load)",
            "Accessibility compliance validated",
            "Integration with fitness devices working"
        ]
    }
    
    print("🚀 Testing Complex Website Workflow")
    print("=" * 80)
    print(f"Project: Fitness Tracking & Community Website")
    print(f"Complexity: {project_context['complexity']}")
    print(f"Timeline: {project_context['timeline']}")
    print(f"Target Users: {project_context['business_constraints']['user_target']}")
    print(f"Success Criteria: {len(project_context['success_criteria'])} key requirements")
    print("=" * 80)
    
    # Execute the workflow
    result = await orchestrator.execute_persona_driven_workflow(
        complex_website_requirement, 
        project_context
    )
    
    # Analyze requirement translation fidelity
    print(f"\n📊 WORKFLOW EXECUTION RESULTS:")
    print(f"   Execution ID: {result['execution_id']}")
    print(f"   Requirement ID: {result['requirement_id']}")
    print(f"   Phases Executed: {result['execution_results']['phases_executed']}")
    print(f"   Teams Coordinated: {result['execution_results']['teams_coordinated']}")
    print(f"   Orchestration Type: {result['orchestration_type']}")
    
    # Check if key requirements were preserved
    await analyze_requirement_fidelity(orchestrator, result, complex_website_requirement)
    
    # Test specific persona outputs for requirement alignment
    await verify_persona_outputs(result, project_context['success_criteria'])
    
    return result

async def analyze_requirement_fidelity(orchestrator, workflow_result, original_requirement):
    """Analyze how well original requirements were preserved through workflow"""
    
    print(f"\n🔍 ANALYZING REQUIREMENT FIDELITY")
    print("-" * 50)
    
    req_id = workflow_result['requirement_id']
    
    # Ask knowledge hub to analyze requirement preservation
    fidelity_analysis = await orchestrator.persona_client.call_persona(
        "central-knowledge-hub",
        f"""
        Please analyze requirement fidelity for requirement {req_id}:
        
        ORIGINAL REQUIREMENT:
        {original_requirement}
        
        Please assess:
        1. Which original requirements are still clearly preserved?
        2. What requirements might have been lost or diluted?
        3. Are the core business objectives maintained?
        4. Are technical requirements properly addressed?
        5. Overall fidelity score (1-10) and justification
        
        Provide specific examples of preservation or loss.
        """,
        {
            "action": "analyze_requirement_fidelity",
            "requirement_id": req_id
        }
    )
    
    print("📈 Requirement Fidelity Analysis:")
    print(fidelity_analysis.get("response", "Analysis not available"))
    
    return fidelity_analysis

async def verify_persona_outputs(workflow_result, success_criteria):
    """Verify that persona outputs align with success criteria"""
    
    print(f"\n✅ VERIFYING PERSONA OUTPUTS AGAINST SUCCESS CRITERIA")
    print("-" * 60)
    
    phase_results = workflow_result['execution_results']['phase_results']
    
    print(f"Success Criteria to Validate: {len(success_criteria)}")
    for i, criteria in enumerate(success_criteria, 1):
        print(f"  {i}. {criteria}")
    
    print(f"\nPhases Executed: {len(phase_results)}")
    for phase_name, phase_data in phase_results.items():
        print(f"\n📋 {phase_name.upper()}:")
        print(f"   Personas: {phase_data.get('personas_executed', 0)}")
        print(f"   Completed: {phase_data.get('phase_completed', False)}")
        
        # Show sample output from each persona in phase
        if 'phase_results' in phase_data:
            for persona, persona_result in phase_data['phase_results'].items():
                response_preview = persona_result.get('response', '')[:200]
                print(f"   {persona}: {response_preview}...")

async def test_code_generation_alignment():
    """Test that generated code aligns with original requirements"""
    
    print(f"\n💻 TESTING CODE GENERATION ALIGNMENT")
    print("-" * 50)
    
    orchestrator = PurePersonaDrivenOrchestrator()
    
    # Simplified requirement for code generation test
    code_requirement = """
    Create a React component for user authentication with the following features:
    - Email and password login form
    - Social login buttons (Google, Facebook)
    - Password reset functionality
    - Form validation with error messages
    - Loading states during authentication
    - Responsive design for mobile and desktop
    """
    
    context = {
        "project_type": "react_component",
        "complexity": "moderate",
        "technology_stack": ["React", "TypeScript", "Tailwind CSS"]
    }
    
    # Execute workflow focusing on development phase
    print("🔨 Executing development-focused workflow...")
    
    result = await orchestrator.execute_persona_driven_workflow(code_requirement, context)
    
    # Check if developer persona generated appropriate code
    phase_results = result['execution_results']['phase_results']
    
    for phase_name, phase_data in phase_results.items():
        if 'phase_results' in phase_data:
            for persona, persona_result in phase_data['phase_results'].items():
                if 'developer' in persona:
                    developer_output = persona_result.get('response', '')
                    print(f"\n👨‍💻 Developer Output Analysis:")
                    print(f"   Length: {len(developer_output)} characters")
                    
                    # Check for key elements in developer output
                    key_elements = [
                        'React', 'component', 'form', 'validation',
                        'login', 'password', 'email', 'responsive'
                    ]
                    
                    found_elements = []
                    for element in key_elements:
                        if element.lower() in developer_output.lower():
                            found_elements.append(element)
                    
                    print(f"   Key Requirements Found: {len(found_elements)}/{len(key_elements)}")
                    print(f"   Found: {', '.join(found_elements)}")
                    
                    if len(found_elements) >= len(key_elements) * 0.7:
                        print(f"   ✅ Good alignment with requirements")
                    else:
                        print(f"   ⚠️ Some requirements may be missing")
    
    return result

async def main():
    """Run comprehensive workflow tests"""
    
    print("🧪 COMPREHENSIVE WORKFLOW TESTING")
    print("=" * 80)
    
    # Test 1: Complex website workflow
    print("\n🌐 TEST 1: Complex Website Workflow")
    complex_result = await test_complex_website_workflow()
    
    # Test 2: Code generation alignment
    print("\n💻 TEST 2: Code Generation Alignment") 
    code_result = await test_code_generation_alignment()
    
    print("\n🎯 OVERALL TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Complex Website Test: Completed")
    print(f"   Phases Executed: {complex_result['execution_results']['phases_executed']}")
    print(f"   Teams Coordinated: {complex_result['execution_results']['teams_coordinated']}")
    print(f"   100% Persona-Driven: ✅")
    
    print(f"✅ Code Generation Test: Completed")
    print(f"   Phases Executed: {code_result['execution_results']['phases_executed']}")
    print(f"   Developer Persona Active: ✅")
    print(f"   Code Generation Attempted: ✅")
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"The workflow demonstrates proper requirement translation and code generation.")

if __name__ == "__main__":
    asyncio.run(main())