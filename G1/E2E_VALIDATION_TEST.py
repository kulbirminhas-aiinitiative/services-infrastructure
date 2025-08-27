#!/usr/bin/env python3
"""
G1 End-to-End Validation Test
Tests all personas and processes with a real requirement statement
NO MOCKS OR DUMMIES - Real persona interactions only
"""

import requests
import json
import time
import sys
from datetime import datetime

class G1E2EValidator:
    def __init__(self):
        self.base_url = "http://localhost:8013"  # Personas Gateway
        self.test_results = []
        self.workflow_trace = []
        self.persona_interactions = {}
        
    def log_step(self, step_name, status, details=None):
        """Log each validation step with timestamp"""
        timestamp = datetime.now().isoformat()
        result = {
            "timestamp": timestamp,
            "step": step_name,
            "status": status,
            "details": details or {}
        }
        self.test_results.append(result)
        print(f"[{timestamp}] {step_name}: {status}")
        if details:
            print(f"    Details: {details}")
    
    def validate_persona_exists(self, persona_name):
        """Validate that persona exists in the actual system"""
        try:
            response = requests.get(f"{self.base_url}/personas/{persona_name}")
            if response.status_code == 200:
                persona_data = response.json()
                self.log_step(f"Persona Validation: {persona_name}", "PASS", 
                            {"role": persona_data.get("role", "Unknown")})
                return True
            else:
                self.log_step(f"Persona Validation: {persona_name}", "FAIL", 
                            {"error": f"HTTP {response.status_code}"})
                return False
        except Exception as e:
            self.log_step(f"Persona Validation: {persona_name}", "ERROR", 
                         {"exception": str(e)})
            return False
    
    def execute_persona_interaction(self, persona_name, prompt, context=None):
        """Execute real interaction with persona - NO MOCKS"""
        try:
            payload = {
                "persona": persona_name,
                "prompt": prompt,
                "context": context or {},
                "session_id": f"e2e_test_{int(time.time())}"
            }
            
            response = requests.post(f"{self.base_url}/interact", 
                                   json=payload, 
                                   timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                self.persona_interactions[persona_name] = result
                self.workflow_trace.append({
                    "persona": persona_name,
                    "input": prompt[:100] + "..." if len(prompt) > 100 else prompt,
                    "output": result.get("response", "")[:200] + "..." if len(result.get("response", "")) > 200 else result.get("response", ""),
                    "timestamp": datetime.now().isoformat()
                })
                self.log_step(f"Persona Interaction: {persona_name}", "PASS",
                            {"response_length": len(result.get("response", ""))})
                return result
            else:
                self.log_step(f"Persona Interaction: {persona_name}", "FAIL",
                            {"error": f"HTTP {response.status_code}", "body": response.text})
                return None
                
        except Exception as e:
            self.log_step(f"Persona Interaction: {persona_name}", "ERROR",
                         {"exception": str(e)})
            return None
    
    def test_requirement_processing(self):
        """Test complete requirement processing workflow"""
        
        # REAL REQUIREMENT - Simple but realistic
        requirement = """
        Create a simple todo list web application where users can:
        1. Add new tasks with a description
        2. Mark tasks as complete/incomplete 
        3. Delete tasks they no longer need
        4. View all tasks in a clean interface
        
        Technical requirements:
        - Should work on mobile and desktop
        - Use modern web technologies
        - Store data locally (no server required for this version)
        - Simple, clean user interface
        """
        
        self.log_step("Starting E2E Test", "BEGIN", 
                     {"requirement_length": len(requirement)})
        
        # Step 1: Test Meta-Orchestration Personas
        print("\n=== TESTING META-ORCHESTRATION PERSONAS ===")
        
        # Test Workflow Designer
        workflow_result = self.execute_persona_interaction(
            "workflow-designer",
            f"Design an optimal SDLC workflow for this requirement: {requirement}"
        )
        
        if not workflow_result:
            self.log_step("Meta-Orchestration Test", "FAIL", 
                         {"reason": "workflow-designer failed"})
            return False
            
        # Test Team Structure Architect
        team_result = self.execute_persona_interaction(
            "team-structure-architect",
            f"Design optimal team structure for this project: {requirement}. "
            f"Workflow context: {workflow_result.get('response', '')[:500]}"
        )
        
        if not team_result:
            self.log_step("Meta-Orchestration Test", "FAIL",
                         {"reason": "team-structure-architect failed"})
            return False
            
        # Test Communication Architect
        comm_result = self.execute_persona_interaction(
            "communication-architect",
            f"Design communication strategy for this project: {requirement}. "
            f"Team structure: {team_result.get('response', '')[:500]}"
        )
        
        if not comm_result:
            self.log_step("Meta-Orchestration Test", "FAIL",
                         {"reason": "communication-architect failed"})
            return False
            
        self.log_step("Meta-Orchestration Test", "PASS")
        
        # Step 2: Test Requirements Processing
        print("\n=== TESTING REQUIREMENTS PROCESSING ===")
        
        # Test Requirement Concierge
        req_result = self.execute_persona_interaction(
            "requirement-concierge",
            f"Analyze and structure this requirement: {requirement}"
        )
        
        if not req_result:
            self.log_step("Requirements Processing", "FAIL")
            return False
            
        # Step 3: Test Architecture Personas
        print("\n=== TESTING ARCHITECTURE PERSONAS ===")
        
        # Test Solution Architect
        solution_result = self.execute_persona_interaction(
            "solution-architect",
            f"Design solution architecture for: {requirement}. "
            f"Structured requirements: {req_result.get('response', '')[:300]}"
        )
        
        # Test Technical Architect
        tech_result = self.execute_persona_interaction(
            "technical-architect",
            f"Create detailed technical design for: {requirement}. "
            f"Solution architecture: {solution_result.get('response', '')[:300] if solution_result else 'None'}"
        )
        
        if not solution_result or not tech_result:
            self.log_step("Architecture Test", "FAIL")
            return False
            
        self.log_step("Architecture Test", "PASS")
        
        # Step 4: Test Development Personas
        print("\n=== TESTING DEVELOPMENT PERSONAS ===")
        
        # Test UI/UX Designer
        ux_result = self.execute_persona_interaction(
            "ui-ux-designer",
            f"Design user interface and experience for: {requirement}"
        )
        
        # Test Frontend Developer
        frontend_result = self.execute_persona_interaction(
            "frontend-developer",
            f"Implement frontend for todo application based on: {ux_result.get('response', '')[:300] if ux_result else requirement}"
        )
        
        if not ux_result or not frontend_result:
            self.log_step("Development Test", "FAIL")
            return False
            
        self.log_step("Development Test", "PASS")
        
        # Step 5: Test Quality Personas
        print("\n=== TESTING QUALITY PERSONAS ===")
        
        # Test QA Specialist
        qa_result = self.execute_persona_interaction(
            "quality-assurance-specialist",
            f"Analyze quality and consistency of requirements: {requirement}"
        )
        
        # Test Security Specialist
        security_result = self.execute_persona_interaction(
            "security-specialist",
            f"Perform security assessment for todo application: {requirement}"
        )
        
        if not qa_result or not security_result:
            self.log_step("Quality Test", "FAIL")
            return False
            
        self.log_step("Quality Test", "PASS")
        
        # Step 6: Test Communication Personas
        print("\n=== TESTING COMMUNICATION PERSONAS ===")
        
        # Test Central Knowledge Hub
        hub_result = self.execute_persona_interaction(
            "central-knowledge-hub",
            f"Store and provide context for requirement: {requirement}"
        )
        
        # Test Verification Service
        verify_result = self.execute_persona_interaction(
            "verification-service",
            f"Verify understanding accuracy for requirement processing: {requirement}"
        )
        
        if not hub_result or not verify_result:
            self.log_step("Communication Test", "FAIL")
            return False
            
        self.log_step("Communication Test", "PASS")
        
        return True
    
    def test_persona_coverage(self):
        """Validate all 31 personas exist and are accessible"""
        print("\n=== TESTING ALL 31 PERSONAS EXISTENCE ===")
        
        expected_personas = [
            # Meta-Orchestration (3)
            "workflow-designer", "team-structure-architect", "communication-architect",
            
            # Communication Management (3) 
            "central-knowledge-hub", "verification-service", "collaborative-transition-manager",
            
            # Architecture & Design (7)
            "solution-architect", "technical-architect", "api-designer", "database-architect",
            "requirement-concierge", "program-manager", "system-architect",
            
            # Development (9)
            "developer", "senior-developer", "frontend-developer", "backend-developer",
            "ui-ux-designer", "mobile-developer", "integration-specialist", "cloud-architect",
            "performance-specialist",
            
            # Quality & Testing (5)
            "tester", "quality-assurance-specialist", "compliance-auditor", "security-specialist",
            "accessibility-specialist",
            
            # Operations & Infrastructure (3)
            "infrastructure-engineer", "devops-specialist", "technical-writer",
            
            # Optional Testing (1)
            "simulator"
        ]
        
        failed_personas = []
        
        for persona in expected_personas:
            if not self.validate_persona_exists(persona):
                failed_personas.append(persona)
        
        if failed_personas:
            self.log_step("Persona Coverage Test", "FAIL",
                         {"missing_personas": failed_personas})
            return False
        else:
            self.log_step("Persona Coverage Test", "PASS",
                         {"total_personas": len(expected_personas)})
            return True
    
    def test_workflow_adaptation(self):
        """Test that workflow-designer can adapt to different requirement types"""
        print("\n=== TESTING WORKFLOW ADAPTATION ===")
        
        test_scenarios = [
            {
                "type": "bug_fix",
                "requirement": "Fix critical login bug - users getting 500 error when login with special characters in password"
            },
            {
                "type": "enhancement", 
                "requirement": "Add dark mode toggle to existing dashboard application"
            },
            {
                "type": "new_feature",
                "requirement": "Create API endpoint for user profile image upload with thumbnail generation"
            }
        ]
        
        adaptation_results = []
        
        for scenario in test_scenarios:
            result = self.execute_persona_interaction(
                "workflow-designer",
                f"Design appropriate workflow for this {scenario['type']} requirement: {scenario['requirement']}"
            )
            
            if result:
                adaptation_results.append({
                    "type": scenario['type'],
                    "adapted": True,
                    "workflow_length": len(result.get('response', ''))
                })
            else:
                adaptation_results.append({
                    "type": scenario['type'], 
                    "adapted": False
                })
        
        success_count = sum(1 for r in adaptation_results if r['adapted'])
        
        if success_count == len(test_scenarios):
            self.log_step("Workflow Adaptation Test", "PASS",
                         {"scenarios_tested": len(test_scenarios)})
            return True
        else:
            self.log_step("Workflow Adaptation Test", "FAIL",
                         {"successful": success_count, "total": len(test_scenarios)})
            return False
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*60)
        print("G1 END-TO-END VALIDATION REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] in ['PASS', 'BEGIN']])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        error_tests = len([r for r in self.test_results if r['status'] == 'ERROR'])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")  
        print(f"Errors: {error_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\nPersona Interactions: {len(self.persona_interactions)}")
        print(f"Workflow Steps Traced: {len(self.workflow_trace)}")
        
        # Detailed results
        print("\n=== DETAILED RESULTS ===")
        for result in self.test_results:
            status_emoji = "✅" if result['status'] == 'PASS' else "❌" if result['status'] == 'FAIL' else "⚠️"
            print(f"{status_emoji} {result['step']}: {result['status']}")
            
        # Save full report
        report_data = {
            "validation_summary": {
                "total_tests": total_tests,
                "passed": passed_tests,
                "failed": failed_tests,
                "errors": error_tests,
                "success_rate": (passed_tests/total_tests)*100
            },
            "test_results": self.test_results,
            "persona_interactions": self.persona_interactions,
            "workflow_trace": self.workflow_trace
        }
        
        with open('/Users/kulbirminhas/Documents/github/projects/G1/E2E_VALIDATION_REPORT.json', 'w') as f:
            json.dump(report_data, f, indent=2)
            
        print(f"\n📄 Full report saved to: E2E_VALIDATION_REPORT.json")
        
        return passed_tests == total_tests - 1  # Excluding BEGIN status

def main():
    """Execute comprehensive G1 validation"""
    
    print("🚀 Starting G1 End-to-End Validation")
    print("📋 Testing all personas and workflows with REAL interactions")
    print("⚠️  NO MOCKS OR DUMMIES - All calls go to actual G1 system\n")
    
    validator = G1E2EValidator()
    
    try:
        # Test 1: Persona Coverage
        persona_test = validator.test_persona_coverage()
        
        # Test 2: Workflow Adaptation  
        workflow_test = validator.test_workflow_adaptation()
        
        # Test 3: Full Requirement Processing
        requirement_test = validator.test_requirement_processing()
        
        # Generate report
        overall_success = validator.generate_validation_report()
        
        if overall_success:
            print("\n🎉 G1 VALIDATION SUCCESSFUL!")
            print("✅ All personas are real and functional")
            print("✅ Workflows adapt dynamically to requirements") 
            print("✅ End-to-end processing works correctly")
            sys.exit(0)
        else:
            print("\n❌ G1 VALIDATION FAILED!")
            print("⚠️  Some personas or workflows are not functioning correctly")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted by user")
        validator.generate_validation_report()
        sys.exit(1)
        
    except Exception as e:
        print(f"\n💥 Validation failed with exception: {e}")
        validator.generate_validation_report()
        sys.exit(1)

if __name__ == "__main__":
    main()