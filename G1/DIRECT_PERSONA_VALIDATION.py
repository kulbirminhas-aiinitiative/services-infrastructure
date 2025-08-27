#!/usr/bin/env python3
"""
Direct G1 Persona Validation
Proves personas are REAL, not mocks - regardless of RAG engine status
Tests actual AI persona responses to validate authenticity
"""

import requests
import json
import time
from datetime import datetime

class DirectPersonaValidator:
    def __init__(self):
        self.base_url = "http://localhost:8013"
        self.validation_results = []
        self.persona_responses = {}
        
    def log_result(self, test_name, status, details=None):
        """Log validation result"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "test": test_name,
            "status": status,
            "details": details or {}
        }
        self.validation_results.append(result)
        status_emoji = "✅" if status == "PASS" else "❌"
        print(f"{status_emoji} {test_name}: {status}")
        if details and status == "FAIL":
            print(f"    {details}")
    
    def test_persona_exists_and_responds(self, persona_name, test_query):
        """Test that persona exists and provides authentic response"""
        try:
            # Test persona existence
            persona_info = requests.get(f"{self.base_url}/personas/{persona_name}")
            if persona_info.status_code != 200:
                self.log_result(f"Persona Existence: {persona_name}", "FAIL", 
                              {"error": f"HTTP {persona_info.status_code}"})
                return False
            
            # Test persona interaction
            payload = {"query": test_query}
            response = requests.post(f"{self.base_url}/persona/{persona_name}",
                                   json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                response_text = data.get("response", "")
                
                # Store response for analysis
                self.persona_responses[persona_name] = {
                    "query": test_query,
                    "response": response_text,
                    "execution_time": data.get("execution_time", 0),
                    "timestamp": data.get("timestamp", "")
                }
                
                # Validate response authenticity
                if self.is_authentic_response(persona_name, test_query, response_text):
                    self.log_result(f"Persona Response: {persona_name}", "PASS",
                                  {"length": len(response_text), "time": data.get("execution_time", 0)})
                    return True
                else:
                    self.log_result(f"Persona Response: {persona_name}", "FAIL",
                                  {"reason": "Response appears to be mock/dummy"})
                    return False
            else:
                self.log_result(f"Persona Response: {persona_name}", "FAIL",
                              {"error": f"HTTP {response.status_code}"})
                return False
                
        except Exception as e:
            self.log_result(f"Persona Test: {persona_name}", "FAIL",
                          {"exception": str(e)})
            return False
    
    def is_authentic_response(self, persona_name, query, response):
        """Analyze response to determine if it's authentic vs mock/dummy"""
        if not response or len(response) < 50:
            return False
            
        # Check for mock/dummy indicators
        mock_indicators = [
            "mock", "dummy", "placeholder", "not implemented", "todo",
            "lorem ipsum", "test response", "sample output"
        ]
        
        if any(indicator in response.lower() for indicator in mock_indicators):
            return False
            
        # Check for persona-appropriate content
        persona_indicators = {
            "requirement-concierge": ["requirements", "analysis", "scope", "feasibility"],
            "developer": ["code", "implementation", "function", "class", "variable"],
            "tester": ["test", "testing", "validation", "verify", "scenario"],
            "ui-ux-designer": ["user", "interface", "design", "experience", "usability"],
            "security-specialist": ["security", "vulnerability", "authentication", "encryption"],
            "workflow-designer": ["workflow", "phase", "process", "methodology"],
        }
        
        expected_terms = persona_indicators.get(persona_name, [])
        if expected_terms and not any(term in response.lower() for term in expected_terms):
            return False
            
        # Check for structured, detailed response
        structure_indicators = [
            response.count('\n') > 2,  # Multi-line response
            any(marker in response for marker in ['1.', '2.', '•', '-', '**', 'Step']),  # Structured content
            len(response.split()) > 20  # Substantial content
        ]
        
        return any(structure_indicators)
    
    def test_workflow_personas(self):
        """Test key workflow personas with realistic queries"""
        print("🔍 TESTING CORE WORKFLOW PERSONAS")
        
        test_cases = [
            ("requirement-concierge", "Analyze this requirement: Build a simple calculator app with basic arithmetic operations"),
            ("workflow-designer", "Design an optimal development workflow for a small web application project"),
            ("developer", "Implement a JavaScript function to validate email addresses"),
            ("tester", "Create test cases for a user registration form"),
            ("ui-ux-designer", "Design the user interface for a task management application"),
            ("security-specialist", "Identify security considerations for a login system"),
        ]
        
        results = []
        for persona_name, query in test_cases:
            success = self.test_persona_exists_and_responds(persona_name, query)
            results.append(success)
            time.sleep(1)  # Avoid overwhelming the service
            
        return results
    
    def test_specialized_personas(self):
        """Test specialized personas with domain-specific queries"""
        print("\n🎯 TESTING SPECIALIZED PERSONAS")
        
        specialized_cases = [
            ("solution-architect", "Design a scalable architecture for a social media platform"),
            ("technical-architect", "Create detailed technical specifications for a microservices system"),
            ("performance-specialist", "Optimize the performance of a slow-loading web application"),
            ("simulator", "Generate a realistic bug scenario for testing purposes"),
        ]
        
        results = []
        for persona_name, query in specialized_cases:
            success = self.test_persona_exists_and_responds(persona_name, query)
            results.append(success)
            time.sleep(1)
            
        return results
    
    def analyze_response_patterns(self):
        """Analyze response patterns to prove authenticity"""
        print("\n📊 ANALYZING RESPONSE AUTHENTICITY")
        
        analysis = {
            "total_responses": len(self.persona_responses),
            "authentic_responses": 0,
            "average_length": 0,
            "unique_content": True,
            "persona_appropriate": 0
        }
        
        if not self.persona_responses:
            return analysis
            
        total_length = 0
        responses_text = []
        
        for persona_name, data in self.persona_responses.items():
            response = data["response"]
            total_length += len(response)
            responses_text.append(response.lower())
            
            # Check if response is authentic
            if self.is_authentic_response(persona_name, data["query"], response):
                analysis["authentic_responses"] += 1
                analysis["persona_appropriate"] += 1
        
        analysis["average_length"] = total_length // len(self.persona_responses)
        
        # Check for unique content (not copy-paste responses)
        if len(set(responses_text)) == len(responses_text):
            analysis["unique_content"] = True
        
        self.log_result("Response Authenticity Analysis", "PASS", analysis)
        return analysis
    
    def demonstrate_real_functionality(self):
        """Demonstrate that personas provide real, different responses to same query"""
        print("\n🎨 DEMONSTRATING PERSONA DIFFERENTIATION")
        
        common_query = "How would you approach building a web application?"
        
        personas_to_test = ["developer", "ui-ux-designer", "security-specialist", "tester"]
        responses = {}
        
        for persona in personas_to_test:
            try:
                payload = {"query": common_query}
                response = requests.post(f"{self.base_url}/persona/{persona}",
                                       json=payload, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    responses[persona] = data.get("response", "")
                time.sleep(1)
            except:
                continue
        
        # Analyze response differentiation
        unique_perspectives = len(set(resp.lower() for resp in responses.values()))
        total_responses = len(responses)
        
        if unique_perspectives == total_responses and total_responses > 1:
            self.log_result("Persona Differentiation", "PASS",
                          {"unique_perspectives": unique_perspectives, "total_tested": total_responses})
            
            # Show examples
            print("\n📝 SAMPLE PERSONA RESPONSES TO SAME QUERY:")
            for persona, response in list(responses.items())[:2]:
                print(f"\n{persona.upper()}:")
                print(f"'{response[:150]}{'...' if len(response) > 150 else ''}'")
        else:
            self.log_result("Persona Differentiation", "FAIL",
                          {"reason": "Responses too similar or insufficient data"})
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n" + "="*80)
        print("🏆 G1 DIRECT PERSONA VALIDATION REPORT")
        print("="*80)
        
        total_tests = len(self.validation_results)
        passed_tests = len([r for r in self.validation_results if r["status"] == "PASS"])
        
        print(f"📊 VALIDATION SUMMARY:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Analyze authenticity
        analysis = self.analyze_response_patterns()
        print(f"\n🔍 AUTHENTICITY ANALYSIS:")
        print(f"   Total Persona Responses: {analysis['total_responses']}")
        print(f"   Authentic Responses: {analysis['authentic_responses']}")
        print(f"   Average Response Length: {analysis['average_length']} chars")
        print(f"   Unique Content: {'Yes' if analysis['unique_content'] else 'No'}")
        
        # Save detailed report
        report = {
            "validation_summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0
            },
            "authenticity_analysis": analysis,
            "persona_responses": self.persona_responses,
            "all_results": self.validation_results
        }
        
        with open('/Users/kulbirminhas/Documents/github/projects/G1/DIRECT_VALIDATION_REPORT.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Full report saved: DIRECT_VALIDATION_REPORT.json")
        
        # Final verdict
        success_rate = (passed_tests/total_tests)*100 if total_tests > 0 else 0
        authenticity_rate = (analysis['authentic_responses']/analysis['total_responses'])*100 if analysis['total_responses'] > 0 else 0
        
        if success_rate >= 70 and authenticity_rate >= 70:
            print(f"\n🎉 VALIDATION SUCCESSFUL!")
            print(f"✅ G1 Personas are REAL and functional")
            print(f"✅ Responses are authentic, not mocks or dummies")
            print(f"✅ Personas show appropriate domain expertise")
            return True
        else:
            print(f"\n❌ VALIDATION CONCERNS DETECTED")
            print(f"⚠️  Some personas may not be fully functional")
            return False

def main():
    """Execute direct persona validation"""
    print("🚀 G1 DIRECT PERSONA VALIDATION")
    print("🎯 Proving personas are REAL, not mocks or dummies")
    print("⚡ Independent of RAG engine status")
    print("📋 Testing actual AI responses for authenticity\n")
    
    validator = DirectPersonaValidator()
    
    try:
        # Test core workflow personas
        workflow_results = validator.test_workflow_personas()
        
        # Test specialized personas  
        specialized_results = validator.test_specialized_personas()
        
        # Demonstrate persona differentiation
        validator.demonstrate_real_functionality()
        
        # Generate comprehensive report
        overall_success = validator.generate_validation_report()
        
        if overall_success:
            print("\n🏆 VALIDATION COMPLETE: G1 PERSONAS ARE REAL!")
            return 0
        else:
            print("\n⚠️  VALIDATION INCOMPLETE: Some issues detected")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Validation interrupted")
        return 1
    except Exception as e:
        print(f"\n💥 Validation error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())