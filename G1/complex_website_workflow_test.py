#!/usr/bin/env python3
"""
Complex Website Workflow Test
=============================

This test validates that a complex website requirement is properly structured
and translated through each persona, ensuring the final code meets the original
specifications.
"""

import asyncio
import json
from datetime import datetime
from workflow_orchestrator import DynamicWorkflowOrchestrator
from typing import Dict, Any
import time
import re

class WebsiteWorkflowValidator:
    """Validates complex website workflow execution and requirement translation"""
    
    def __init__(self):
        self.orchestrator = DynamicWorkflowOrchestrator()
        self.trace_log = []
        self.requirement_validation = {}
        
    def log_interaction(self, step_num: int, persona: str, input_data: str, 
                       output_data: str, execution_time: float):
        """Log persona interaction with requirement analysis"""
        interaction = {
            "step": step_num,
            "persona": persona,
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "output": output_data,
            "execution_time": execution_time,
            "requirement_elements_captured": self.analyze_requirement_capture(output_data, persona)
        }
        self.trace_log.append(interaction)
        
        # Print formatted output with requirement analysis
        print(f"\n{'='*80}")
        print(f"STEP {step_num}: {persona.upper()}")
        print(f"{'='*80}")
        print(f"⏱️  Execution Time: {execution_time:.2f}s")
        print(f"📥 INPUT (Preview):")
        print(f"{'-'*40}")
        print(f"{input_data[:200]}..." if len(input_data) > 200 else input_data)
        print(f"\n📤 OUTPUT:")
        print(f"{'-'*40}")
        print(f"{output_data}")
        print(f"\n🎯 REQUIREMENT ELEMENTS CAPTURED:")
        print(f"{'-'*40}")
        for element in interaction["requirement_elements_captured"]:
            print(f"  ✓ {element}")
        
    def analyze_requirement_capture(self, output: str, persona: str) -> list:
        """Analyze how well the persona captured original requirements"""
        elements_found = []
        output_lower = output.lower()
        
        # Core requirement elements to track
        requirement_keywords = {
            "e-commerce platform": ["e-commerce", "ecommerce", "online store", "shopping"],
            "user authentication": ["authentication", "login", "register", "user account"],
            "product catalog": ["product", "catalog", "inventory", "items"],
            "shopping cart": ["cart", "shopping cart", "basket"],
            "payment processing": ["payment", "checkout", "billing", "stripe", "paypal"],
            "order management": ["order", "purchase", "transaction"],
            "admin dashboard": ["admin", "dashboard", "management", "backend"],
            "responsive design": ["responsive", "mobile", "device", "adaptive"],
            "search functionality": ["search", "filter", "query"],
            "customer reviews": ["review", "rating", "feedback", "comment"],
            "inventory tracking": ["inventory", "stock", "tracking"],
            "email notifications": ["email", "notification", "alert"],
            "analytics": ["analytics", "metrics", "tracking", "statistics"],
            "SEO optimization": ["seo", "optimization", "meta", "keywords"],
            "security": ["security", "ssl", "encryption", "protection"]
        }
        
        for requirement, keywords in requirement_keywords.items():
            if any(keyword in output_lower for keyword in keywords):
                elements_found.append(requirement)
        
        # Persona-specific analysis
        if persona.lower() == "developer":
            tech_elements = ["react", "node.js", "database", "api", "frontend", "backend", "mongodb", "express"]
            for tech in tech_elements:
                if tech in output_lower:
                    elements_found.append(f"technology: {tech}")
                    
        elif persona.lower() == "tester":
            test_elements = ["unit test", "integration test", "performance test", "security test", "user acceptance"]
            for test in test_elements:
                if test in output_lower:
                    elements_found.append(f"testing: {test}")
                    
        elif persona.lower() == "infrastructure engineer":
            infra_elements = ["docker", "kubernetes", "aws", "load balancer", "database", "cdn"]
            for infra in infra_elements:
                if infra in output_lower:
                    elements_found.append(f"infrastructure: {infra}")
        
        return elements_found if elements_found else ["general_response_provided"]
    
    async def execute_complex_website_workflow(self):
        """Execute workflow with complex website requirement"""
        
        # Complex e-commerce website requirement
        complex_requirement = """Build a comprehensive e-commerce platform with the following specifications:

**Core Features:**
1. User Authentication System (registration, login, password reset, OAuth integration)
2. Product Catalog with categories, filtering, search, and detailed product pages
3. Advanced Shopping Cart with save-for-later, quantity management, and cart persistence
4. Multi-step Checkout Process with guest checkout, address management, and order summary
5. Payment Processing supporting multiple methods (Credit cards, PayPal, Apple Pay, Google Pay)
6. Order Management system with order tracking, history, and status updates
7. Customer Review and Rating system with photo uploads and moderation
8. Inventory Management with real-time stock tracking and low-stock alerts
9. Admin Dashboard for product management, order processing, user management, and analytics

**Technical Requirements:**
- Responsive design supporting mobile, tablet, and desktop
- Performance optimization with page load times under 3 seconds
- SEO-friendly URLs and meta tags for search engine optimization
- Real-time features using WebSocket for cart updates and notifications
- Image optimization with multiple sizes and lazy loading
- Progressive Web App (PWA) capabilities for mobile app-like experience
- Email notification system for order confirmations, shipping updates, and marketing
- Analytics integration for user behavior tracking and conversion metrics
- Security measures including SSL, data encryption, and PCI compliance
- Multi-language support (English, Spanish, French) with currency conversion

**Business Requirements:**
- Support for 10,000+ concurrent users during peak times
- 99.9% uptime availability requirement
- GDPR compliance for European customers
- Integration with third-party services (shipping APIs, tax calculation, email marketing)
- A/B testing capability for marketing campaigns
- Social media integration for sharing and login
- Customer support chat integration
- Recommendation engine for personalized product suggestions"""
        
        context = {
            "priority": "critical",
            "type": "feature_request", 
            "requestor": "business-stakeholders",
            "deadline": "2024-06-01",
            "budget": "high",
            "team_size": 12,
            "target_users": "B2C_customers",
            "expected_traffic": "10000_concurrent_users",
            "compliance_requirements": ["GDPR", "PCI_DSS"],
            "business_goals": ["increase_online_sales", "expand_market_reach", "improve_customer_experience"]
        }
        
        print("\n" + "="*80)
        print("🌐 COMPLEX E-COMMERCE WEBSITE WORKFLOW EXECUTION")
        print("="*80)
        print(f"\n📝 COMPLEX REQUIREMENT:")
        print(f"{complex_requirement[:500]}... [TRUNCATED]")
        print(f"\n🎯 CONTEXT:")
        print(json.dumps(context, indent=2))
        print("\n" + "="*80)
        
        # Execute the workflow step by step with detailed analysis
        step_num = 1
        
        # Step 1: Interface Validator
        start_time = time.time()
        validator_input = json.dumps({
            "requirement": complex_requirement,
            "priority": context["priority"],
            "type": context["type"],
            "requestor": context["requestor"]
        }, indent=2)
        
        validator_result = await self.orchestrator.persona_client.call_persona(
            "interface-validator",
            f"Validate this complex e-commerce platform requirement for workflow processing:\n{validator_input}",
            {"validation_phase": "complex_requirement"}
        )
        
        self.log_interaction(
            step_num,
            "Interface Validator",
            validator_input,
            validator_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 2: Requirement Concierge  
        step_num = 2
        start_time = time.time()
        concierge_input = f"""Analyze this complex e-commerce platform requirement:

{complex_requirement}

Provide comprehensive analysis:
1. Requirement complexity assessment and breakdown
2. Key stakeholders and their needs identification
3. Business objectives and success criteria
4. Technical feasibility and architecture considerations
5. Risk assessment and mitigation strategies
6. Resource and timeline estimation
7. Acceptance criteria definition"""
        
        concierge_result = await self.orchestrator.persona_client.call_persona(
            "requirement-concierge",
            concierge_input,
            {"analysis_phase": "complex_ecommerce_analysis"}
        )
        
        self.log_interaction(
            step_num,
            "Requirement Concierge",
            concierge_input,
            concierge_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 3: Quality Assurance Specialist (New persona for requirement validation)
        step_num = 3
        start_time = time.time()
        qa_input = f"""Perform quality assessment of this e-commerce requirement:

{complex_requirement}

Analyze for:
1. Requirement completeness and consistency
2. Terminology standardization across all features
3. Acceptance criteria clarity and testability
4. Dependency identification and mapping
5. Scope boundary definition
6. Compliance requirement integration

Provide consistency scores and improvement recommendations."""
        
        qa_result = await self.orchestrator.persona_client.call_persona(
            "quality-assurance-specialist",
            qa_input,
            {"qa_phase": "requirement_validation"}
        )
        
        self.log_interaction(
            step_num,
            "Quality Assurance Specialist",
            qa_input,
            qa_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 4: Program Manager
        step_num = 4
        start_time = time.time()
        pm_input = f"""Create comprehensive project plan for this e-commerce platform:

{complex_requirement}

Provide detailed planning:
1. Project phases and detailed timeline (12-month project)
2. Resource allocation for 12-person team
3. Risk management and mitigation strategies
4. Stakeholder communication and governance plan
5. Budget planning and cost management
6. Quality gates and milestone definitions
7. Success metrics and KPI tracking"""
        
        pm_result = await self.orchestrator.persona_client.call_persona(
            "program-manager",
            pm_input,
            {"planning_phase": "complex_ecommerce_planning"}
        )
        
        self.log_interaction(
            step_num,
            "Program Manager", 
            pm_input,
            pm_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 5: Developer (Critical step - code generation)
        step_num = 5
        start_time = time.time()
        dev_input = f"""Implement comprehensive technical solution for:

{complex_requirement}

Provide complete implementation:
1. Technical architecture (frontend, backend, database, services)
2. Technology stack selection and justification
3. Database schema design for all entities
4. API design with detailed endpoints
5. Frontend component structure (React/Vue/Angular)
6. Backend service architecture (microservices/monolith)
7. Integration patterns for third-party services
8. Code examples for critical features (authentication, cart, payment)
9. Performance optimization strategies
10. Security implementation details"""
        
        dev_result = await self.orchestrator.persona_client.call_persona(
            "developer",
            dev_input,
            {"implementation_phase": "complex_ecommerce_development"}
        )
        
        self.log_interaction(
            step_num,
            "Developer",
            dev_input,
            dev_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 6: Tester
        step_num = 6
        start_time = time.time()
        tester_input = f"""Create comprehensive testing strategy for:

{complex_requirement}

Design complete testing approach:
1. Test strategy for all 9 core features
2. Performance testing for 10,000+ concurrent users
3. Security testing for PCI compliance
4. Compatibility testing across devices and browsers  
5. Integration testing for all third-party services
6. User acceptance testing scenarios
7. Load testing and stress testing plans
8. Automated testing framework design"""
        
        tester_result = await self.orchestrator.persona_client.call_persona(
            "tester",
            tester_input,
            {"testing_phase": "complex_ecommerce_testing"}
        )
        
        self.log_interaction(
            step_num,
            "Tester",
            tester_input,
            tester_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 7: Infrastructure Engineer
        step_num = 7
        start_time = time.time()
        infra_input = f"""Design production infrastructure for:

{complex_requirement}

Create enterprise-grade deployment:
1. Cloud architecture for high availability (99.9% uptime)
2. Auto-scaling for 10,000+ concurrent users
3. CDN setup for global performance
4. Database cluster design with replication
5. Security infrastructure (SSL, firewalls, DDoS protection)
6. Monitoring and alerting systems
7. Backup and disaster recovery
8. CI/CD pipeline for 12-person development team"""
        
        infra_result = await self.orchestrator.persona_client.call_persona(
            "infrastructure-engineer",
            infra_input,
            {"infrastructure_phase": "complex_ecommerce_infrastructure"}
        )
        
        self.log_interaction(
            step_num,
            "Infrastructure Engineer",
            infra_input,
            infra_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 8: Compliance Auditor (New persona for compliance validation)
        step_num = 8
        start_time = time.time()
        compliance_input = f"""Audit compliance requirements for:

{complex_requirement}

Perform comprehensive compliance assessment:
1. GDPR compliance analysis and implementation requirements
2. PCI DSS compliance for payment processing
3. Accessibility compliance (WCAG 2.1)
4. Security standards and data protection measures
5. Privacy policy and terms of service requirements
6. Audit trail and logging requirements
7. Compliance monitoring and reporting framework"""
        
        compliance_result = await self.orchestrator.persona_client.call_persona(
            "compliance-auditor",
            compliance_input,
            {"compliance_phase": "ecommerce_compliance_audit"}
        )
        
        self.log_interaction(
            step_num,
            "Compliance Auditor",
            compliance_input,
            compliance_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Final Analysis
        print(f"\n{'='*80}")
        print("🎯 WORKFLOW EXECUTION COMPLETE - REQUIREMENT TRANSLATION ANALYSIS")
        print(f"{'='*80}")
        
        # Analyze requirement translation through the workflow
        self.analyze_requirement_translation()
        
        # Save detailed trace
        with open("complex_website_workflow_trace.json", "w") as f:
            json.dump(self.trace_log, f, indent=2)
        print(f"\n💾 Detailed trace saved to: complex_website_workflow_trace.json")
        
        return self.trace_log
    
    def analyze_requirement_translation(self):
        """Analyze how well requirements were translated through the workflow"""
        
        print(f"\n📊 REQUIREMENT TRANSLATION ANALYSIS:")
        print(f"{'='*60}")
        
        # Count requirement elements captured by each persona
        all_elements = {}
        for interaction in self.trace_log:
            persona = interaction["persona"]
            elements = interaction["requirement_elements_captured"]
            all_elements[persona] = elements
            
            print(f"\n🎭 {persona}:")
            print(f"   Elements Captured: {len(elements)}")
            for element in elements[:5]:  # Show top 5
                print(f"     ✓ {element}")
            if len(elements) > 5:
                print(f"     ... and {len(elements) - 5} more")
        
        # Check if critical features were addressed by Developer
        dev_response = ""
        for interaction in self.trace_log:
            if interaction["persona"] == "Developer":
                dev_response = interaction["output"].lower()
                break
        
        critical_features = {
            "Authentication": ["authentication", "login", "oauth", "jwt"],
            "Product Catalog": ["product", "catalog", "inventory"],
            "Shopping Cart": ["cart", "shopping"],
            "Payment Processing": ["payment", "checkout", "stripe", "paypal"],
            "Database Design": ["database", "schema", "mongodb", "sql"],
            "API Design": ["api", "endpoint", "rest", "graphql"],
            "Frontend Framework": ["react", "vue", "angular", "frontend"],
            "Security": ["security", "ssl", "encryption"]
        }
        
        print(f"\n🔍 DEVELOPER CODE COVERAGE ANALYSIS:")
        print(f"{'='*40}")
        for feature, keywords in critical_features.items():
            covered = any(keyword in dev_response for keyword in keywords)
            status = "✅ COVERED" if covered else "❌ MISSING"
            print(f"  {status}: {feature}")
        
        print(f"\n⏱️ EXECUTION PERFORMANCE:")
        print(f"{'='*40}")
        total_time = sum(interaction["execution_time"] for interaction in self.trace_log)
        print(f"  Total Execution Time: {total_time:.2f} seconds")
        print(f"  Average Per Persona: {total_time/len(self.trace_log):.2f} seconds")
        print(f"  Personas Involved: {len(self.trace_log)}")


async def main():
    """Execute complex website workflow validation"""
    
    print("\n" + "="*80)
    print("🌐 COMPLEX WEBSITE WORKFLOW VALIDATION")
    print("="*80)
    print("Testing requirement translation through complete persona chain")
    print("Focus: E-commerce platform with 15+ features and compliance requirements")
    print("="*80)
    
    validator = WebsiteWorkflowValidator()
    trace_log = await validator.execute_complex_website_workflow()
    
    print(f"\n✅ Complex website workflow validation completed!")
    print(f"🎯 Validated requirement translation through {len(trace_log)} personas")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())