#!/usr/bin/env python3
"""
Workflow Trace Test - Complete End-to-End Workflow Demonstration
================================================================

This script demonstrates a complete workflow execution with detailed
tracing of inputs and outputs from each persona in the chain.
"""

import asyncio
import json
from datetime import datetime
from workflow_orchestrator import DynamicWorkflowOrchestrator
from typing import Dict, Any
import time

class WorkflowTracer:
    """Enhanced workflow tracer to capture all persona interactions"""
    
    def __init__(self):
        self.orchestrator = DynamicWorkflowOrchestrator()
        self.trace_log = []
        
    def log_interaction(self, step_num: int, persona: str, input_data: str, 
                       output_data: str, execution_time: float):
        """Log a persona interaction with full details"""
        interaction = {
            "step": step_num,
            "persona": persona,
            "timestamp": datetime.now().isoformat(),
            "input": input_data,
            "output": output_data,
            "execution_time": execution_time
        }
        self.trace_log.append(interaction)
        
        # Print formatted output
        print(f"\n{'='*80}")
        print(f"STEP {step_num}: {persona.upper()}")
        print(f"{'='*80}")
        print(f"⏱️  Execution Time: {execution_time:.2f}s")
        print(f"\n📥 INPUT:")
        print(f"{'-'*40}")
        print(f"{input_data[:500]}..." if len(input_data) > 500 else input_data)
        print(f"\n📤 OUTPUT:")
        print(f"{'-'*40}")
        print(f"{output_data[:500]}..." if len(output_data) > 500 else output_data)
        
    async def execute_traced_workflow(self, requirement: str, context: Dict[str, Any] = None):
        """Execute workflow with detailed tracing"""
        
        print("\n" + "="*80)
        print("🚀 WORKFLOW EXECUTION TRACE")
        print("="*80)
        print(f"\n📝 INITIAL REQUIREMENT:")
        print(f"{requirement}")
        print(f"\n🎯 CONTEXT:")
        print(json.dumps(context or {}, indent=2))
        print("\n" + "="*80)
        
        # Step 1: Interface Validator (Input Validation)
        step_num = 1
        start_time = time.time()
        validator_input = json.dumps({
            "requirement": requirement,
            "priority": context.get("priority", "medium"),
            "type": context.get("type", "feature_request"),
            "requestor": context.get("requestor", "test-user")
        }, indent=2)
        
        validator_result = await self.orchestrator.persona_client.call_persona(
            "interface-validator",
            f"Validate this request for workflow processing:\n{validator_input}",
            {"validation_phase": "initial"}
        )
        
        self.log_interaction(
            step_num,
            "Interface Validator",
            validator_input,
            validator_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 2: Requirement Concierge (Analysis)
        step_num = 2
        start_time = time.time()
        concierge_input = f"""Analyze this software requirement and provide:
1. Clarified requirement statement
2. Key stakeholders identification
3. Business objectives extraction
4. Initial risk signals
5. Feasibility assessment

Requirement: {requirement}
Priority: {context.get('priority', 'medium')}
Type: {context.get('type', 'feature_request')}"""
        
        concierge_result = await self.orchestrator.persona_client.call_persona(
            "requirement-concierge",
            concierge_input,
            {"analysis_phase": "requirement_analysis"}
        )
        
        self.log_interaction(
            step_num,
            "Requirement Concierge",
            concierge_input,
            concierge_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 3: Queue Manager (Routing)
        step_num = 3
        start_time = time.time()
        queue_input = f"""Route this validated requirement to appropriate personas:
Requirement: {requirement}
Priority: {context.get('priority', 'medium')}
Workflow Type: Standard Development

Determine:
1. Processing priority
2. Optimal routing path
3. Parallel processing opportunities
4. Resource allocation strategy"""
        
        queue_result = await self.orchestrator.persona_client.call_persona(
            "queue-manager",
            queue_input,
            {"routing_phase": "workflow_routing"}
        )
        
        self.log_interaction(
            step_num,
            "Queue Manager",
            queue_input,
            queue_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 4: Program Manager (Strategic Planning)
        step_num = 4
        start_time = time.time()
        pm_input = f"""Create strategic project plan for:
Requirement: {requirement}

Provide:
1. Project timeline and milestones
2. Resource allocation plan
3. Risk mitigation strategies
4. Stakeholder communication plan
5. Success metrics definition"""
        
        pm_result = await self.orchestrator.persona_client.call_persona(
            "program-manager",
            pm_input,
            {"planning_phase": "strategic_planning"}
        )
        
        self.log_interaction(
            step_num,
            "Program Manager",
            pm_input,
            pm_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 5: Developer (Implementation)
        step_num = 5
        start_time = time.time()
        dev_input = f"""Implement technical solution for:
Requirement: {requirement}

Provide:
1. Technical architecture design
2. Implementation approach
3. Code structure and components
4. API design if applicable
5. Database schema if needed
6. Integration points"""
        
        dev_result = await self.orchestrator.persona_client.call_persona(
            "developer",
            dev_input,
            {"implementation_phase": "development"}
        )
        
        self.log_interaction(
            step_num,
            "Developer",
            dev_input,
            dev_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 6: Interface Validator (Dev->Test Transfer)
        step_num = 6
        start_time = time.time()
        transfer_input = f"""Validate data transfer from Developer to Tester:
Source: Developer
Target: Tester
Data: Implementation artifacts and test requirements
Validation Focus: Code completeness, test coverage requirements, documentation"""
        
        transfer_result = await self.orchestrator.persona_client.call_persona(
            "interface-validator",
            transfer_input,
            {"validation_phase": "dev_to_test_transfer"}
        )
        
        self.log_interaction(
            step_num,
            "Interface Validator (Dev→Test)",
            transfer_input,
            transfer_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 7: Tester (Quality Assurance)
        step_num = 7
        start_time = time.time()
        test_input = f"""Create comprehensive testing strategy for:
Requirement: {requirement}

Provide:
1. Test plan and test cases
2. Unit test scenarios
3. Integration test scenarios
4. Performance test criteria
5. Security test requirements
6. Acceptance criteria validation"""
        
        test_result = await self.orchestrator.persona_client.call_persona(
            "tester",
            test_input,
            {"testing_phase": "quality_assurance"}
        )
        
        self.log_interaction(
            step_num,
            "Tester",
            test_input,
            test_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 8: Interface Validator (Test->Ops Transfer)
        step_num = 8
        start_time = time.time()
        ops_transfer_input = f"""Validate data transfer from Tester to Operations:
Source: Tester
Target: Infrastructure Engineer
Data: Tested artifacts and deployment requirements
Validation Focus: Test results, deployment specifications, monitoring requirements"""
        
        ops_transfer_result = await self.orchestrator.persona_client.call_persona(
            "interface-validator",
            ops_transfer_input,
            {"validation_phase": "test_to_ops_transfer"}
        )
        
        self.log_interaction(
            step_num,
            "Interface Validator (Test→Ops)",
            ops_transfer_input,
            ops_transfer_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 9: Infrastructure Engineer (Deployment)
        step_num = 9
        start_time = time.time()
        infra_input = f"""Design deployment infrastructure for:
Requirement: {requirement}

Provide:
1. Infrastructure architecture
2. Container configuration (Docker/Kubernetes)
3. CI/CD pipeline setup
4. Monitoring and alerting setup
5. Security hardening measures
6. Scaling strategy"""
        
        infra_result = await self.orchestrator.persona_client.call_persona(
            "infrastructure-engineer",
            infra_input,
            {"deployment_phase": "infrastructure_setup"}
        )
        
        self.log_interaction(
            step_num,
            "Infrastructure Engineer",
            infra_input,
            infra_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Step 10: DevOps Specialist (Operations)
        step_num = 10
        start_time = time.time()
        devops_input = f"""Implement operational excellence for:
Requirement: {requirement}

Provide:
1. CI/CD automation setup
2. Monitoring dashboards configuration
3. Log aggregation strategy
4. Incident response procedures
5. Performance optimization recommendations
6. Cost optimization strategies"""
        
        devops_result = await self.orchestrator.persona_client.call_persona(
            "devops-specialist",
            devops_input,
            {"operations_phase": "operational_setup"}
        )
        
        self.log_interaction(
            step_num,
            "DevOps Specialist",
            devops_input,
            devops_result.get("response", "No response"),
            time.time() - start_time
        )
        
        # Final Summary
        print(f"\n{'='*80}")
        print("📊 WORKFLOW EXECUTION SUMMARY")
        print(f"{'='*80}")
        print(f"✅ Total Steps: {step_num}")
        print(f"⏱️  Total Execution Time: {sum(log['execution_time'] for log in self.trace_log):.2f}s")
        print(f"🎯 Personas Involved: {len(set(log['persona'] for log in self.trace_log))}")
        
        # Save trace log
        with open("workflow_trace_log.json", "w") as f:
            json.dump(self.trace_log, f, indent=2)
        print(f"\n💾 Trace log saved to: workflow_trace_log.json")
        
        return self.trace_log


async def main():
    """Execute a traced workflow demonstration"""
    
    print("\n" + "="*80)
    print("🎭 G1 WORKFLOW ORCHESTRATOR - COMPLETE TRACE DEMONSTRATION")
    print("="*80)
    print("\nThis demonstration will trace a complete workflow execution,")
    print("showing inputs and outputs from each persona in the chain.")
    print("="*80)
    
    # Simple requirement for demonstration
    requirement = """Add a user authentication feature with the following capabilities:
    1. User registration with email verification
    2. Secure login with password hashing
    3. Password reset functionality
    4. Session management with JWT tokens
    5. Role-based access control (Admin, User, Guest)"""
    
    # Context for the requirement
    context = {
        "priority": "high",
        "type": "feature_request",
        "requestor": "product-team",
        "deadline": "2024-02-15",
        "budget": "medium",
        "team_size": 4
    }
    
    # Execute traced workflow
    tracer = WorkflowTracer()
    trace_log = await tracer.execute_traced_workflow(requirement, context)
    
    print("\n" + "="*80)
    print("✅ WORKFLOW TRACE COMPLETE!")
    print("="*80)
    print("\n📈 Execution Statistics:")
    for i, log in enumerate(trace_log, 1):
        print(f"  {i}. {log['persona']}: {log['execution_time']:.2f}s")
    
    print(f"\n🎉 Demonstration completed successfully!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())