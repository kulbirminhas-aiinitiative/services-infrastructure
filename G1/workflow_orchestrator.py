#!/usr/bin/env python3
"""
Enhanced Dynamic Workflow Orchestrator with Complete Persona Ecosystem

Features:
- Dynamic workflows based on requirement complexity and classification
- Interface validators and queue managers for proper data flow
- Metrics personas with rule-based calculations
- Team/Program management integration
- Full development lifecycle coverage
"""

import asyncio
import json
import uuid
import aiohttp
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RequirementType(Enum):
    BUG_FIX = "bug_fix"
    FEATURE_REQUEST = "feature_request"
    INFRASTRUCTURE = "infrastructure"
    COMPLIANCE = "compliance"
    MIGRATION = "migration"
    RESEARCH = "research"


class RequirementPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class WorkflowChannel(Enum):
    FAST_TRACK = "fast_track"        # Simple changes, 2-4 hours
    STANDARD = "standard"            # Regular features, 1-4 weeks
    MEGA = "mega"                    # Complex projects, 3-18 months
    RESEARCH = "research"            # Proof of concepts, variable


class ExecutionPhase(Enum):
    """Execution phases that run automatically for all workflows"""
    PLANNING = "planning"            # Requirement analysis and design
    DEVELOPMENT = "development"      # Core implementation
    TESTING = "testing"             # Quality assurance
    DEPLOYMENT = "deployment"       # Infrastructure and release
    MONITORING = "monitoring"       # Post-deployment validation


@dataclass
class RequirementClassification:
    """Classification of the requirement"""
    type: RequirementType
    priority: RequirementPriority
    complexity_score: float
    risk_score: float
    estimated_effort: str
    confidence: float


@dataclass
class PersonaResult:
    """Result from a persona execution"""
    persona_id: str
    persona_name: str
    success: bool
    output_data: Dict[str, Any]
    confidence: float
    processing_time: float
    metadata: Dict[str, Any]
    validated: bool = False


class WorkflowContextManager:
    """Manages context accumulation through workflow execution"""
    
    def __init__(self):
        self.workflow_context = {}
        self.persona_outputs = {}
        self.context_history = []
    
    def add_persona_output(self, persona_name: str, output: str, metadata: Dict[str, Any] = None):
        """Add persona output to accumulated context"""
        self.persona_outputs[persona_name] = {
            "output": output,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self.workflow_context[f"{persona_name}_output"] = output
        self.context_history.append({
            "persona": persona_name,
            "output": output[:200] + "..." if len(output) > 200 else output,
            "timestamp": datetime.now().isoformat()
        })
    
    def get_enriched_context(self, current_persona: str, base_context: dict) -> dict:
        """Get enriched context with accumulated workflow history"""
        enriched_context = base_context.copy()
        enriched_context["workflow_history"] = self.persona_outputs
        enriched_context["previous_outputs"] = list(self.persona_outputs.keys())
        enriched_context["context_summary"] = self.format_context_summary(current_persona)
        return enriched_context
    
    def format_context_summary(self, current_persona: str) -> str:
        """Format context for better persona understanding"""
        if not self.persona_outputs:
            return "No previous persona outputs available."
        
        summary = f"=== WORKFLOW CONTEXT FOR {current_persona.upper().replace('-', ' ')} ===\n\n"
        summary += "Previous Persona Contributions:\n"
        
        for persona, data in self.persona_outputs.items():
            summary += f"\n--- {persona.upper().replace('-', ' ')} ---\n"
            output = data["output"]
            # Truncate long outputs but keep key information
            if len(output) > 400:
                summary += f"{output[:400]}...\n"
            else:
                summary += f"{output}\n"
        
        summary += f"\n=== CURRENT CONTEXT FOR {current_persona.upper().replace('-', ' ')} ===\n"
        return summary


@dataclass
class WorkflowContext:
    """Context passed through the workflow"""
    workflow_id: str
    user_input: str
    timestamp: datetime
    classification: Optional[RequirementClassification] = None
    metadata: Dict[str, Any] = None
    context_manager: Optional[WorkflowContextManager] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.context_manager is None:
            self.context_manager = WorkflowContextManager()


class PersonaAPIClient:
    """Enhanced client for calling personas via API with validation"""
    
    def __init__(self, base_url: str = "http://localhost:8003", personas_gateway_url: str = "http://localhost:8013"):
        self.base_url = base_url
        self.personas_gateway_url = personas_gateway_url
        
        # Load extended persona mapping
        try:
            with open("/Users/kulbirminhas/Documents/github/projects/oom/extended_persona_mapping.json", "r") as f:
                extended_mapping = json.load(f)
        except FileNotFoundError:
            extended_mapping = {}
        
        # Complete persona mapping with proper agent IDs
        self.persona_mapping = {
            # Core workflow personas
            "requirement_concierge": "requirement_concierge",
            "risk_assessor": "risk_assessor",
            "complexity_estimator": "complexity_estimator", 
            "mind_engine_coordinator": "mind_engine_coordinator",
            "workflow_router": "workflow_router",
            "gatekeeper": "gatekeeper",
            
            # Management personas
            "team_manager": "team_manager",
            "program_manager": "program_manager",
            
            # Development lifecycle personas
            "developer": "developer",
            "tester": "tester", 
            "operations": "operations",
            
            # Enhanced Deployment Engineering Personas
            "infrastructure_engineer": "infrastructure_engineer",
            "release_engineer": "release_engineer",
            "devops_specialist": "devops_specialist",
            "github_integration_specialist": "github_integration_specialist",
            
            # Interface/Queue management personas
            "interface_validator": "interface_validator",
            "queue_manager": "queue_manager",
            
            # Metrics calculation personas
            "functionality_metrics": "functionality_metrics",
            "performance_metrics": "performance_metrics",
            "stability_metrics": "stability_metrics",
            "scalability_metrics": "scalability_metrics"
        }
    
    async def validate_and_route_request(self, persona_name: str, user_message: str, 
                                       context: Dict[str, Any], context_manager: Optional[WorkflowContextManager] = None) -> Dict[str, Any]:
        """Validate request format and route through queue manager"""
        
        # First validate the request format
        validation_result = await self.call_persona(
            "interface_validator",
            f"""Please validate this request format for persona communication:

Target Persona: {persona_name}
Message: {user_message}
Context: {json.dumps(context, indent=2)}

Validate:
1. Message structure and clarity
2. Required context completeness
3. Data format compliance
4. Routing appropriateness

Provide validation status and any corrections needed.""",
            {"validation_target": persona_name, "request_type": "validation"},
            context_manager
        )
        
        if not validation_result["success"]:
            return validation_result
        
        # Route through queue manager
        routing_result = await self.call_persona(
            "queue_manager",
            f"""Please route this validated request to the appropriate persona:

Target Persona: {persona_name}
Validated Message: {user_message}
Context: {json.dumps(context, indent=2)}
Validation Result: {validation_result.get('response', '')}

Determine:
1. Optimal routing strategy
2. Processing priority
3. Workload considerations
4. Any parallel processing opportunities

Provide routing decision and processing workflow.""",
            {"routing_target": persona_name, "request_type": "routing"},
            context_manager
        )
        
        # Execute the actual persona call
        return await self.call_persona(persona_name, user_message, context, context_manager)
    
    async def call_persona(self, persona_name: str, user_message: str, 
                          context: Dict[str, Any], context_manager: Optional[WorkflowContextManager] = None) -> Dict[str, Any]:
        """Call a persona via Personas Gateway API (port 8013) with context accumulation"""
        
        # Enrich context with accumulated workflow history if context manager provided
        final_context = context
        if context_manager:
            final_context = context_manager.get_enriched_context(persona_name, context)
        
        # Personas Gateway payload format
        query_payload = {
            "query": user_message,
            "context": final_context,
            "parameters": {
                "max_tokens": 2000,
                "temperature": 0.7
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.personas_gateway_url}/persona/{persona_name}",
                    json=query_payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get("response", "")
                        
                        # Add this persona's output to context manager if provided
                        if context_manager:
                            context_manager.add_persona_output(
                                persona_name, 
                                response_text,
                                {
                                    "execution_time": result.get("execution_time", 0),
                                    "timestamp": datetime.now().isoformat()
                                }
                            )
                        
                        return {
                            "success": True,
                            "response": response_text,
                            "persona": result.get("persona", persona_name),
                            "execution_time": result.get("execution_time", 0),
                            "raw_result": result
                        }
                    else:
                        error_text = await response.text()
                        return {
                            "success": False,
                            "error": f"HTTP {response.status}: {error_text}",
                            "persona": persona_name
                        }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "persona": persona_name
            }


class MetricsCalculator:
    """Calculates metrics using rule-based personas"""
    
    def __init__(self, persona_client: PersonaAPIClient):
        self.persona_client = persona_client
    
    async def calculate_all_metrics(self, workflow_results: List[PersonaResult], 
                                  context: WorkflowContext) -> Dict[str, Any]:
        """Calculate all four core metrics using personas"""
        
        metrics = {}
        
        # Prepare results summary for metrics calculation
        results_summary = {
            "workflow_id": context.workflow_id,
            "requirement": context.user_input,
            "classification": {
                "type": context.classification.type.value if context.classification else "unknown",
                "priority": context.classification.priority.value if context.classification else "unknown",
                "complexity_score": context.classification.complexity_score if context.classification else 0,
                "risk_score": context.classification.risk_score if context.classification else 0,
                "estimated_effort": context.classification.estimated_effort if context.classification else "unknown",
                "confidence": context.classification.confidence if context.classification else 0
            },
            "results": [
                {
                    "persona": result.persona_name,
                    "success": result.success,
                    "confidence": result.confidence,
                    "processing_time": result.processing_time,
                    "key_outputs": result.output_data
                }
                for result in workflow_results
            ]
        }
        
        # Calculate Functionality Metrics
        func_result = await self.persona_client.call_persona(
            "functionality_metrics",
            f"""Calculate functionality metrics for this workflow execution:

{json.dumps(results_summary, indent=2)}

Apply functionality measurement rules to assess:
1. Feature completeness score (0-10)
2. Acceptance criteria fulfillment
3. Business value delivery assessment
4. Functional quality indicators
5. User experience impact

Provide structured metrics with scores and analysis.""",
            {"metric_type": "functionality", "workflow_id": context.workflow_id}
        )
        
        if func_result["success"]:
            metrics["functionality"] = self._parse_metric_response(func_result["response"], "functionality")
        
        # Calculate Performance Metrics
        perf_result = await self.persona_client.call_persona(
            "performance_metrics",
            f"""Calculate performance metrics for this workflow execution:

{json.dumps(results_summary, indent=2)}

Apply performance measurement rules to assess:
1. Processing speed and efficiency (0-10)
2. Response time characteristics
3. Throughput and capacity utilization
4. Performance optimization opportunities
5. SLA compliance indicators

Provide structured metrics with measurements and analysis.""",
            {"metric_type": "performance", "workflow_id": context.workflow_id}
        )
        
        if perf_result["success"]:
            metrics["performance"] = self._parse_metric_response(perf_result["response"], "performance")
        
        # Calculate Stability Metrics
        stab_result = await self.persona_client.call_persona(
            "stability_metrics",
            f"""Calculate stability metrics for this workflow execution:

{json.dumps(results_summary, indent=2)}

Apply stability measurement rules to assess:
1. Reliability and error handling (0-10)
2. System resilience indicators
3. Failure recovery capabilities
4. Stability trend analysis
5. Incident prevention measures

Provide structured metrics with reliability scores and analysis.""",
            {"metric_type": "stability", "workflow_id": context.workflow_id}
        )
        
        if stab_result["success"]:
            metrics["stability"] = self._parse_metric_response(stab_result["response"], "stability")
        
        # Calculate Scalability Metrics
        scale_result = await self.persona_client.call_persona(
            "scalability_metrics",
            f"""Calculate scalability metrics for this workflow execution:

{json.dumps(results_summary, indent=2)}

Apply scalability measurement rules to assess:
1. Scaling capability and flexibility (0-10)
2. Capacity growth potential
3. Resource utilization efficiency
4. Bottleneck identification
5. Architecture scalability assessment

Provide structured metrics with capacity analysis and recommendations.""",
            {"metric_type": "scalability", "workflow_id": context.workflow_id}
        )
        
        if scale_result["success"]:
            metrics["scalability"] = self._parse_metric_response(scale_result["response"], "scalability")
        
        return metrics
    
    def _parse_metric_response(self, response: str, metric_type: str) -> Dict[str, Any]:
        """Parse metric response into structured data"""
        import re
        
        # Extract score
        score_match = re.search(r'(?:score|rating)[:\s]+([0-9]+\.?[0-9]*)', response, re.IGNORECASE)
        score = float(score_match.group(1)) if score_match else 5.0
        
        # Extract key insights
        insights = []
        if "improvement" in response.lower():
            insights.append("improvement_opportunities_identified")
        if "excellent" in response.lower() or "high" in response.lower():
            insights.append("strong_performance_indicators")
        if "concern" in response.lower() or "risk" in response.lower():
            insights.append("attention_required")
        
        return {
            "score": min(score, 10.0),
            "assessment": response[:200] + "..." if len(response) > 200 else response,
            "insights": insights,
            "calculated_at": datetime.now().isoformat(),
            "metric_type": metric_type
        }


class DynamicWorkflowOrchestrator:
    """Enhanced orchestrator with complete persona ecosystem"""
    
    def __init__(self):
        self.persona_client = PersonaAPIClient()
        self.metrics_calculator = MetricsCalculator(self.persona_client)
        self.execution_history = []
    
    async def process_requirement(self, user_input: str, 
                                context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process requirement with dynamic workflow selection"""
        
        workflow_id = str(uuid.uuid4())
        start_time = datetime.now()
        
        if context is None:
            context = {}
        
        workflow_context = WorkflowContext(
            workflow_id=workflow_id,
            user_input=user_input,
            timestamp=start_time,
            metadata=context
        )
        
        print(f"🚀 Enhanced Dynamic Workflow Processing")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"📝 Requirement: {user_input}")
        print("=" * 60)
        
        try:
            results = []
            
            # Phase 1: Requirement Classification & Analysis
            print("\n📋 Phase 1: Requirement Analysis & Classification")
            classification = await self._classify_requirement(user_input, workflow_context)
            workflow_context.classification = classification
            
            concierge_result = await self._call_persona_with_validation(
                "requirement_concierge", user_input, workflow_context, "requirement_analysis"
            )
            results.append(concierge_result)
            
            # Phase 2: Dynamic Workflow Selection
            print("\n🔀 Phase 2: Dynamic Workflow Selection")
            workflow_channel = await self._select_workflow_channel(classification, workflow_context)
            print(f"  🛣️ Selected Channel: {workflow_channel.value}")
            
            # Phase 3: Execute Selected Workflow with Integrated Execution Phases
            workflow_results = await self._execute_workflow_with_phases(workflow_channel, workflow_context)
            results.extend(workflow_results)
            
            # Phase 4: Metrics Calculation
            print("\n📊 Phase 4: Metrics Calculation")
            metrics = await self.metrics_calculator.calculate_all_metrics(results, workflow_context)
            
            total_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                "workflow_id": workflow_id,
                "input": user_input,
                "context": context,
                "classification": {
                    "type": classification.type.value if classification else "unknown",
                    "priority": classification.priority.value if classification else "unknown",
                    "complexity_score": classification.complexity_score if classification else 0,
                    "risk_score": classification.risk_score if classification else 0,
                    "estimated_effort": classification.estimated_effort if classification else "unknown",
                    "confidence": classification.confidence if classification else 0
                },
                "selected_channel": workflow_channel.value,
                "results": [self._serialize_result(r) for r in results],
                "metrics": metrics,
                "total_time": total_time,
                "success": True,
                "execution_method": "dynamic_workflow_with_complete_personas"
            }
            
            self.execution_history.append(result)
            
            print(f"\n✅ Workflow completed successfully in {total_time:.2f} seconds")
            print(f"📊 Overall metrics calculated: {len(metrics)} categories")
            
            return result
            
        except Exception as e:
            total_time = (datetime.now() - start_time).total_seconds()
            print(f"\n❌ Workflow failed: {str(e)}")
            
            return {
                "workflow_id": workflow_id,
                "input": user_input,
                "context": context,
                "error": str(e),
                "total_time": total_time,
                "success": False,
                "execution_method": "dynamic_workflow_with_complete_personas"
            }
    
    async def _classify_requirement(self, user_input: str, 
                                  context: WorkflowContext) -> RequirementClassification:
        """Classify requirement using requirement concierge"""
        
        # Use a simple classification based on keywords for now
        # In a real system, this would be more sophisticated
        
        input_lower = user_input.lower()
        
        # Determine type
        if any(word in input_lower for word in ["fix", "bug", "error", "broken"]):
            req_type = RequirementType.BUG_FIX
        elif any(word in input_lower for word in ["compliance", "hipaa", "gdpr", "audit"]):
            req_type = RequirementType.COMPLIANCE
        elif any(word in input_lower for word in ["migrate", "migration", "upgrade"]):
            req_type = RequirementType.MIGRATION
        elif any(word in input_lower for word in ["infrastructure", "deployment", "server"]):
            req_type = RequirementType.INFRASTRUCTURE
        elif any(word in input_lower for word in ["research", "poc", "investigate"]):
            req_type = RequirementType.RESEARCH
        else:
            req_type = RequirementType.FEATURE_REQUEST
        
        # Determine priority
        if any(word in input_lower for word in ["critical", "urgent", "emergency"]):
            priority = RequirementPriority.CRITICAL
        elif any(word in input_lower for word in ["high", "important", "soon"]):
            priority = RequirementPriority.HIGH
        elif any(word in input_lower for word in ["low", "nice", "future"]):
            priority = RequirementPriority.LOW
        else:
            priority = RequirementPriority.MEDIUM
        
        # Simple complexity scoring
        complexity_score = 3.0  # Default
        if any(word in input_lower for word in ["simple", "quick", "small"]):
            complexity_score = 2.0
        elif any(word in input_lower for word in ["complex", "large", "enterprise", "platform"]):
            complexity_score = 8.0
        elif any(word in input_lower for word in ["microservices", "migration", "architecture"]):
            complexity_score = 9.0
        
        # Simple risk scoring
        risk_score = 3.0  # Default
        if req_type == RequirementType.COMPLIANCE:
            risk_score = 8.0
        elif any(word in input_lower for word in ["patient", "financial", "security"]):
            risk_score = 7.0
        elif req_type == RequirementType.BUG_FIX:
            risk_score = 2.0
        
        return RequirementClassification(
            type=req_type,
            priority=priority,
            complexity_score=complexity_score,
            risk_score=risk_score,
            estimated_effort="auto-calculated",
            confidence=0.8
        )
    
    async def _select_workflow_channel(self, classification: RequirementClassification,
                                     context: WorkflowContext) -> WorkflowChannel:
        """Select workflow channel based on classification"""
        
        # Research projects
        if classification.type == RequirementType.RESEARCH:
            return WorkflowChannel.RESEARCH
        
        # Fast track for simple, low-risk items
        if (classification.complexity_score <= 3.0 and 
            classification.risk_score <= 3.0 and
            classification.type == RequirementType.BUG_FIX):
            return WorkflowChannel.FAST_TRACK
        
        # Mega projects for high complexity
        if (classification.complexity_score >= 7.0 or
            classification.type in [RequirementType.MIGRATION, RequirementType.INFRASTRUCTURE]):
            return WorkflowChannel.MEGA
        
        # Standard for everything else
        return WorkflowChannel.STANDARD
    
    async def _execute_workflow_with_phases(self, workflow_channel: WorkflowChannel, 
                                          context: WorkflowContext) -> List[PersonaResult]:
        """Execute workflow with integrated execution phases for deployment and CI/CD"""
        print(f"  🔄 Executing {workflow_channel.value.title()} Workflow with Integrated Phases")
        
        all_results = []
        
        # Phase 1: Core Workflow Execution (based on channel)
        print(f"\n  📝 Core Development Phase ({workflow_channel.value})")
        if workflow_channel == WorkflowChannel.FAST_TRACK:
            core_results = await self._execute_fast_track_workflow(context)
        elif workflow_channel == WorkflowChannel.STANDARD:
            core_results = await self._execute_standard_workflow(context)
        elif workflow_channel == WorkflowChannel.MEGA:
            core_results = await self._execute_mega_workflow(context)
        else:  # RESEARCH
            core_results = await self._execute_research_workflow(context)
        
        all_results.extend(core_results)
        
        # Phase 2: Automated Testing & Quality Assurance
        print(f"\n  🧪 Testing & Quality Assurance Phase")
        testing_results = await self._execute_testing_phase(context)
        all_results.extend(testing_results)
        
        # Phase 3: Automated Deployment & Infrastructure
        print(f"\n  🚀 Deployment & Infrastructure Phase")
        deployment_results = await self._execute_deployment_phase(context)
        all_results.extend(deployment_results)
        
        # Phase 4: Monitoring & Validation
        print(f"\n  📊 Monitoring & Validation Phase")
        monitoring_results = await self._execute_monitoring_phase(context)
        all_results.extend(monitoring_results)
        
        return all_results
    
    async def _execute_testing_phase(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute automated testing and quality assurance phase"""
        results = []
        
        # Testing specialist for comprehensive QA
        testing_result = await self._call_persona_with_validation(
            "tester",
            f"""Comprehensive testing strategy for: {context.user_input}

            Implement complete testing framework:
            1. Unit testing strategy and implementation
            2. Integration testing with external systems
            3. End-to-end testing scenarios
            4. Performance and load testing
            5. Security testing and vulnerability assessment
            6. Accessibility and usability testing
            7. Browser/device compatibility testing
            8. Automated testing pipeline integration

            Quality assurance includes:
            - Code quality analysis and linting
            - Test coverage reporting
            - Performance benchmarking
            - Security scanning automation
            - Continuous testing in CI/CD pipeline""",
            context, "quality_assurance"
        )
        results.append(testing_result)
        
        return results
    
    async def _execute_deployment_phase(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute deployment and infrastructure phase automatically"""
        results = []
        
        # Infrastructure setup
        infra_result = await self._call_persona_with_validation(
            "infrastructure_engineer",
            f"""Infrastructure setup and deployment for: {context.user_input}

            Automate infrastructure provisioning:
            1. Cloud infrastructure setup (IaC with Terraform/CloudFormation)
            2. Container orchestration (Docker + Kubernetes)
            3. CI/CD pipeline automation (GitHub Actions)
            4. Security hardening and compliance
            5. Monitoring and logging infrastructure
            6. Backup and disaster recovery setup
            7. Auto-scaling and load balancing
            8. Cost optimization and resource management

            Generate deployment artifacts:
            - Dockerfile and docker-compose.yml
            - Kubernetes manifests (deployment, service, ingress)
            - GitHub Actions workflows (.github/workflows/)
            - Infrastructure as Code templates
            - Monitoring and alerting configurations""",
            context, "infrastructure_automation"
        )
        results.append(infra_result)
        
        # Release engineering for CI/CD
        release_result = await self._call_persona_with_validation(
            "release_engineer",
            f"""Release engineering and CI/CD automation for: {context.user_input}

            Implement automated release pipeline:
            1. Source code management and branching strategy
            2. Automated build and testing pipeline
            3. Deployment automation with rollback capabilities
            4. Environment promotion (dev → staging → prod)
            5. Blue-green and canary deployment strategies
            6. Security scanning and compliance checks
            7. Performance monitoring and alerts
            8. Release management and change tracking

            CI/CD pipeline includes:
            - Automated testing on every commit
            - Security vulnerability scanning
            - Performance regression testing
            - Automated deployment approvals
            - Rollback mechanisms and health checks""",
            context, "cicd_automation"
        )
        results.append(release_result)
        
        return results
    
    async def _execute_monitoring_phase(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute monitoring and validation phase"""
        results = []
        
        # DevOps monitoring and operations
        monitoring_result = await self._call_persona_with_validation(
            "devops_specialist",
            f"""Monitoring and operational validation for: {context.user_input}

            Implement comprehensive monitoring:
            1. Application performance monitoring (APM)
            2. Infrastructure monitoring and alerting
            3. Log aggregation and analysis
            4. Security monitoring and threat detection
            5. Business metrics and KPI tracking
            6. Incident response and escalation
            7. Capacity planning and optimization
            8. SLA monitoring and reporting

            Operational excellence:
            - Real-time dashboards and visualizations
            - Automated alerting and notifications
            - Health checks and synthetic monitoring
            - Performance optimization recommendations
            - Cost monitoring and optimization alerts""",
            context, "monitoring_operations"
        )
        results.append(monitoring_result)
        
        return results
    
    async def _execute_fast_track_workflow(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute fast track workflow - minimal personas"""
        print("  🏃‍♂️ Executing Fast Track Workflow")
        
        results = []
        
        # Quick development assessment
        dev_result = await self._call_persona_with_validation(
            "developer", 
            f"Quick technical assessment for: {context.user_input}",
            context, "fast_track_development"
        )
        results.append(dev_result)
        
        # Basic testing
        test_result = await self._call_persona_with_validation(
            "tester",
            f"Quick test strategy for: {context.user_input}",
            context, "fast_track_testing"
        )
        results.append(test_result)
        
        return results
    
    async def _execute_standard_workflow(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute standard workflow - full lifecycle"""
        print("  🚀 Executing Standard Workflow")
        
        results = []
        
        # Risk assessment
        risk_result = await self._call_persona_with_validation(
            "risk_assessor",
            f"Risk assessment for: {context.user_input}",
            context, "risk_assessment"
        )
        results.append(risk_result)
        
        # Team management
        team_result = await self._call_persona_with_validation(
            "team_manager",
            f"Team capacity and resource assessment for: {context.user_input}",
            context, "team_management"
        )
        results.append(team_result)
        
        # Development
        dev_result = await self._call_persona_with_validation(
            "developer",
            f"Technical implementation plan for: {context.user_input}",
            context, "development"
        )
        results.append(dev_result)
        
        # Testing
        test_result = await self._call_persona_with_validation(
            "tester",
            f"Comprehensive test strategy for: {context.user_input}",
            context, "testing"
        )
        results.append(test_result)
        
        # Operations
        ops_result = await self._call_persona_with_validation(
            "operations",
            f"Deployment and operational readiness for: {context.user_input}",
            context, "operations"
        )
        results.append(ops_result)
        
        return results
    
    async def _execute_mega_workflow(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute mega workflow - full enterprise governance"""
        print("  🏢 Executing Mega Project Workflow")
        
        results = []
        
        # Program management
        program_result = await self._call_persona_with_validation(
            "program_manager",
            f"Program coordination and strategic alignment for: {context.user_input}",
            context, "program_management"
        )
        results.append(program_result)
        
        # Mind engine for complex decomposition
        mind_result = await self._call_persona_with_validation(
            "mind_engine_coordinator",
            f"Complex problem decomposition for: {context.user_input}",
            context, "mind_engine"
        )
        results.append(mind_result)
        
        # All standard workflow personas
        standard_results = await self._execute_standard_workflow(context)
        results.extend(standard_results)
        
        return results
    
    async def _execute_research_workflow(self, context: WorkflowContext) -> List[PersonaResult]:
        """Execute research workflow - investigation focused"""
        print("  🔬 Executing Research Workflow")
        
        results = []
        
        # Research-focused development
        dev_result = await self._call_persona_with_validation(
            "developer",
            f"Technical research and feasibility analysis for: {context.user_input}",
            context, "research_development"
        )
        results.append(dev_result)
        
        # Mind engine for research methodology
        mind_result = await self._call_persona_with_validation(
            "mind_engine_coordinator",
            f"Research methodology and approach for: {context.user_input}",
            context, "research_methodology"
        )
        results.append(mind_result)
        
        return results
    
    async def _call_persona_with_validation(self, persona_name: str, message: str,
                                          context: WorkflowContext, phase: str) -> PersonaResult:
        """Call persona with validation and routing"""
        start_time = datetime.now()
        
        api_context = {
            "workflow_id": context.workflow_id,
            "phase": phase,
            "classification": {
                "type": context.classification.type.value if context.classification else "unknown",
                "priority": context.classification.priority.value if context.classification else "unknown",
                "complexity_score": context.classification.complexity_score if context.classification else 0,
                "risk_score": context.classification.risk_score if context.classification else 0
            }
        }
        
        # Use validation and routing for non-interface personas
        if persona_name not in ["interface_validator", "queue_manager"]:
            api_result = await self.persona_client.validate_and_route_request(
                persona_name, message, api_context
            )
        else:
            api_result = await self.persona_client.call_persona(
                persona_name, message, api_context
            )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        if api_result["success"]:
            print(f"  ✅ {persona_name} completed ({processing_time:.1f}s)")
            
            return PersonaResult(
                persona_id=api_result["persona_id"],
                persona_name=persona_name,
                success=True,
                output_data={"response": api_result["response"]},
                confidence=0.8,
                processing_time=processing_time,
                metadata={"phase": phase, "validated": True},
                validated=True
            )
        else:
            print(f"  ❌ {persona_name} failed: {api_result['error']}")
            return PersonaResult(
                persona_id=api_result.get("persona_id", "unknown"),
                persona_name=persona_name,
                success=False,
                output_data={"error": api_result["error"]},
                confidence=0.0,
                processing_time=processing_time,
                metadata={"phase": phase, "validated": False},
                validated=False
            )
    
    def _serialize_result(self, result: PersonaResult) -> Dict[str, Any]:
        """Serialize PersonaResult for JSON output"""
        return {
            "persona_id": result.persona_id,
            "persona_name": result.persona_name,
            "success": result.success,
            "output_data": result.output_data,
            "confidence": result.confidence,
            "processing_time": result.processing_time,
            "metadata": result.metadata,
            "validated": result.validated
        }


async def main():
    """Demonstrate the enhanced dynamic workflow orchestrator"""
    
    print("🚀 Enhanced Dynamic Workflow Orchestrator")
    print("=" * 60)
    print("Complete persona ecosystem with dynamic workflows!")
    print("Interface validation, queue management, and metrics calculation\n")
    
    orchestrator = DynamicWorkflowOrchestrator()
    
    # Test scenarios covering different workflow channels
    scenarios = [
        {
            "name": "Fast Track - Simple Bug Fix",
            "input": "Fix mobile checkout button not responding to taps",
            "context": {"urgency": "high", "user_impact": "medium"}
        },
        {
            "name": "Standard - Feature Request",
            "input": "Add user preference dashboard with notification settings",
            "context": {"business_value": "high", "complexity": "moderate"}
        },
        {
            "name": "Mega Project - Platform Migration",
            "input": "Migrate monolithic platform to microservices with event-driven architecture across 12 services",
            "context": {"scope": "enterprise", "teams": 8, "timeline": "18_months"}
        },
        {
            "name": "Compliance - HIPAA Implementation",
            "input": "Implement HIPAA-compliant patient data export with audit logging",
            "context": {"compliance": ["hipaa"], "data_type": "phi", "regulatory": True}
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*80}")
        print(f"🧪 Scenario {i}/{len(scenarios)}: {scenario['name']}")
        print("="*80)
        
        result = await orchestrator.process_requirement(scenario["input"], scenario["context"])
        
        if result["success"]:
            print(f"\n📊 Execution Summary:")
            print(f"  • Classification: {result['classification'].get('type', 'unknown')}")
            print(f"  • Selected Channel: {result['selected_channel']}")
            print(f"  • Total Time: {result['total_time']:.2f}s")
            print(f"  • Personas Used: {len(result['results'])}")
            print(f"  • Success Rate: {sum(1 for r in result['results'] if r['success'])}/{len(result['results'])}")
            print(f"  • Metrics Calculated: {len(result.get('metrics', {}))}")
            
            # Show metrics summary
            if result.get('metrics'):
                print(f"\n📈 Metrics Summary:")
                for metric_name, metric_data in result['metrics'].items():
                    score = metric_data.get('score', 0)
                    print(f"  • {metric_name.title()}: {score:.1f}/10")
        
        print("\n" + "."*80)
        await asyncio.sleep(2)  # Pause between scenarios
    
    print(f"\n🎉 Enhanced Dynamic Workflow Demonstration Completed!")
    print(f"All workflows executed with complete persona ecosystem!")


if __name__ == "__main__":
    asyncio.run(main())
