<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# G1 Project - Copilot Instructions

## Project Overview

This is the **G1 Project**, a streamlined workflow orchestration and testing framework. G1 focuses on core orchestration capabilities with dynamic workflow selection, persona-based processing, and comprehensive integration testing.

## Key Architectural Principles

1. **Workflow Orchestration**: Dynamic selection of processing workflows based on requirement classification
2. **Persona-Based Processing**: Multiple AI personas handle different aspects of development
3. **Integration Testing**: Comprehensive testing framework for validating system functionality
4. **Service Communication**: RESTful APIs for inter-service communication
5. **Docker-Based Deployment**: Containerized services for easy deployment and scaling

## Component Structure

### Core Components
- **Workflow Orchestrator**: Central orchestration engine (`workflow_orchestrator.py`)
- **Integration Tests**: Comprehensive testing framework (`integration_tests.py`)
- **Requirement Concierge**: Analyzes and classifies incoming requirements
- **Developer Personas**: Handle different development aspects (bug fixes, features)
- **Testing Personas**: Quality assurance and validation
- **Infrastructure Personas**: Deployment and operations
- **Docker Services**: Containerized backend services

### Shared Infrastructure
- **Message Bus**: Redis-based component communication
- **Config Manager**: Environment-based configuration
- **Metrics Collector**: Performance measurement
- **Data Storage**: SQLite + file-based storage
- **Logging**: Comprehensive logging with loguru

## Code Guidelines

### Component Implementation
- All components must inherit from `OOMComponent` base class
- Implement required abstract methods: `initialize()`, `process()`, `get_status()`, `update_config()`
- Use the shared message bus for inter-component communication
- Record performance metrics for the Critic Engine
- Support graceful start/stop lifecycle

### Interface Patterns
- Use `LearningInterface` for components that learn from feedback
- Use `CriticalInterface` for components that measure performance
- Use `BalancingInterface` for components supporting the balancing approach
- Use `DataProcessor` for data processing components

### Communication
- Use the `Message` dataclass for all inter-component messages
- Publish/subscribe through the `MessageBus`
- Support request/response patterns for synchronous communication
- Include proper error handling and timeouts

### Configuration
- Use dataclasses for configuration structures
- Support environment variable overrides (OOM_ prefix)
- Validate configuration at startup
- Support hot-reloading where possible

### Performance & Metrics
- Record timing metrics for all operations using `TimingContext`
- Track functionality, performance/speed, stability, scalability metrics
- Use the `MetricsCollector` for centralized metrics
- Implement proper cleanup and resource management

### Error Handling
- Use comprehensive try-catch blocks
- Log errors with context information
- Implement proper fallback mechanisms
- Support graceful degradation

## Development Patterns

### Async Programming
- Use async/await for all I/O operations
- Implement proper async context managers
- Handle asyncio cancellation gracefully
- Use asyncio.timeout for operation timeouts

### Testing
- Write comprehensive unit tests for all components
- Use pytest with async support
- Mock external dependencies
- Test error conditions and edge cases

### Documentation
- Include comprehensive docstrings
- Document the Mind Engine pattern solving modes
- Explain the balancing approach implementation
- Provide examples of component interaction

## Special Considerations

### Mind Engine Implementation
- ME(x) should support multiple processing modes: simplify, divide, abstract, coordinate
- ME(o) orchestrates between ME(s) and ME(w)
- Implement problem decomposition and abstraction
- Support historical analysis and expansion (M(exp))

### Critic Engine Metrics
- Measure four core metrics: functionality, performance/speed, stability, scalability
- Implement continuous benchmarking
- Support A(N) -> A(f(x)) measurement iteration
- Track improvement over time

### Meta Engine Capabilities
- Capture all metadata for learning analysis
- Identify patterns and relationships
- Support AutoML decision making
- Enable performance model definition

### Technology Agnostic Design
- Abstract away specific ML frameworks
- Support multiple computing environments (online/edge)
- Use plugin-style architecture where possible
- Enable easy framework switching

## File Organization

