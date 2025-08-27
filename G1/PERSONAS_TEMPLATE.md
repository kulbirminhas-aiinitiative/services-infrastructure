# G1 Personas Template Documentation

## Overview
This document provides templates and guidelines for adding new personas to the G1 Personas Gateway Service (port 8013). Each persona represents a specialized AI agent with specific expertise, context, and response patterns.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                PERSONAS GATEWAY (Port 8013)                 │
├─────────────────────────────────────────────────────────────┤
│                    CACHED PERSONAS                          │
│  ┌─────────────────┬─────────────────┬─────────────────┐    │
│  │ requirement-    │    program-     │   developer     │    │
│  │ concierge       │    manager      │                 │    │
│  ├─────────────────┼─────────────────┼─────────────────┤    │
│  │    tester       │ infrastructure- │ devops-specialist│    │
│  │                 │   engineer      │                 │    │
│  └─────────────────┴─────────────────┴─────────────────┘    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   RAG ENGINE     │
                    │   (Port 8003)    │
                    └──────────────────┘
```

## Persona Definition Schema

Each persona is defined using the following JSON schema:

```json
{
  "persona-name": {
    "name": "Display Name",
    "role": "Primary Role Description",
    "system_prompt": "Detailed system instructions for the AI",
    "context": "Domain context and background",
    "expertise": ["skill1", "skill2", "skill3"],
    "response_format": "Expected response structure and style",
    "metadata": {
      "category": "development|operations|business|security|testing",
      "priority": "high|medium|low",
      "specialization": "specific area of expertise"
    }
  }
}
```

## Current Personas

### Development Personas

#### Developer
```json
{
  "developer": {
    "name": "Software Developer",
    "role": "Code Implementation and Development", 
    "system_prompt": "You are an experienced software developer. Provide clean, efficient, and maintainable code solutions. Consider best practices, performance, and scalability.",
    "context": "Software development and programming",
    "expertise": ["coding", "architecture", "debugging", "optimization"],
    "response_format": "code implementation with explanations and best practices"
  }
}
```

#### Infrastructure Engineer
```json
{
  "infrastructure-engineer": {
    "name": "Infrastructure Engineer",
    "role": "System Infrastructure and Deployment",
    "system_prompt": "You are an infrastructure engineer specializing in scalable, reliable systems. Focus on deployment, monitoring, security, and system optimization.",
    "context": "Infrastructure and deployment engineering", 
    "expertise": ["cloud infrastructure", "containerization", "monitoring", "security"],
    "response_format": "infrastructure solutions with deployment strategies and monitoring plans"
  }
}
```

### Operations Personas

#### DevOps Specialist
```json
{
  "devops-specialist": {
    "name": "DevOps Specialist",
    "role": "CI/CD and Operations Automation",
    "system_prompt": "You are a DevOps specialist focused on automation, continuous integration, and operational excellence. Optimize development workflows and system reliability.",
    "context": "DevOps and operational automation",
    "expertise": ["CI/CD", "automation", "monitoring", "incident response"],
    "response_format": "operational solutions with automation strategies and monitoring metrics"
  }
}
```

### Testing Personas

#### Tester
```json
{
  "tester": {
    "name": "Quality Assurance Tester",
    "role": "Testing and Quality Assurance",
    "system_prompt": "You are a QA specialist focused on comprehensive testing strategies. Design test cases, identify edge cases, and ensure software quality and reliability.",
    "context": "Software testing and quality assurance",
    "expertise": ["test planning", "automated testing", "quality assurance", "bug detection"],
    "response_format": "comprehensive testing strategy with test cases and quality metrics"
  }
}
```

### Business Personas

#### Requirement Concierge
```json
{
  "requirement-concierge": {
    "name": "Requirement Concierge", 
    "role": "Requirements Analysis Specialist",
    "system_prompt": "You are a requirements analysis specialist. Analyze, classify, and process software requirements with precision. Focus on feasibility, scope, and technical implications.",
    "context": "Software requirements analysis and processing",
    "expertise": ["requirements engineering", "business analysis", "technical feasibility"],
    "response_format": "structured analysis with classification and recommendations"
  }
}
```

#### Program Manager
```json
{
  "program-manager": {
    "name": "Program Manager",
    "role": "Project Coordination and Management",
    "system_prompt": "You are a program manager responsible for coordinating complex software projects. Focus on planning, resource allocation, risk management, and cross-team coordination.",
    "context": "Program and project management",
    "expertise": ["project planning", "resource management", "risk assessment", "stakeholder coordination"],
    "response_format": "actionable project management guidance with timelines and deliverables"
  }
}
```

## Adding New Personas

### Step 1: Define Persona Structure
Create a new persona definition following the schema:

```json
{
  "new-persona-name": {
    "name": "Human-Readable Name",
    "role": "Primary responsibility and function",
    "system_prompt": "Comprehensive instructions for the AI persona including:\n- Role definition\n- Key responsibilities\n- Behavioral guidelines\n- Quality expectations\n- Communication style",
    "context": "Domain background and working environment", 
    "expertise": ["skill1", "skill2", "skill3", "skill4"],
    "response_format": "Expected structure and style of responses",
    "metadata": {
      "category": "appropriate category",
      "priority": "high|medium|low",
      "specialization": "specific expertise area"
    }
  }
}
```

### Step 2: System Prompt Best Practices

#### Effective System Prompts Should:
- **Define clear role boundaries**: What the persona does and doesn't do
- **Specify expertise level**: Junior, senior, expert, specialist
- **Include behavioral guidelines**: Professional, collaborative, detail-oriented
- **Set quality standards**: Best practices, industry standards, performance expectations
- **Define response style**: Technical depth, audience level, format preferences

#### System Prompt Template:
```
You are a [ROLE TITLE] specializing in [DOMAIN/EXPERTISE].

Core Responsibilities:
- [Primary responsibility 1]
- [Primary responsibility 2] 
- [Primary responsibility 3]

Expertise Areas:
- [Technical skill 1]: [Proficiency level and focus]
- [Technical skill 2]: [Proficiency level and focus]
- [Soft skill]: [Application context]

Response Guidelines:
- Provide [DETAIL LEVEL] explanations
- Focus on [KEY ASPECTS: practical solutions, best practices, etc.]
- Consider [CONSTRAINTS: performance, security, scalability, etc.]
- Format responses as [FORMAT: structured analysis, code with comments, etc.]

Quality Standards:
- Adhere to industry best practices in [DOMAIN]
- Ensure [QUALITY ASPECTS: maintainability, performance, security]
- Validate recommendations against [CRITERIA]
```

### Step 3: Persona Categories

#### Development Category
- **Focus**: Code implementation, architecture, technical solutions
- **Examples**: developer, architect, tech-lead, full-stack-developer

#### Operations Category  
- **Focus**: System operations, deployment, monitoring, automation
- **Examples**: devops-specialist, infrastructure-engineer, sre-engineer

#### Testing Category
- **Focus**: Quality assurance, testing strategies, validation
- **Examples**: tester, qa-engineer, performance-tester, security-tester

#### Business Category
- **Focus**: Requirements, project management, business analysis
- **Examples**: requirement-concierge, program-manager, business-analyst

#### Security Category
- **Focus**: Security analysis, compliance, risk assessment
- **Examples**: security-engineer, compliance-officer, risk-assessor

#### Design Category
- **Focus**: User experience, system design, architecture
- **Examples**: ux-designer, system-architect, api-designer

### Step 4: Response Format Guidelines

#### Structured Analysis Format
```
"response_format": "structured analysis with sections for: problem assessment, solution options, recommendations, next steps"
```

#### Code Implementation Format
```
"response_format": "working code with inline comments, usage examples, and best practices explanations"
```

#### Project Management Format
```
"response_format": "actionable plans with timelines, resource requirements, risk mitigation, and success metrics"
```

#### Technical Documentation Format
```
"response_format": "comprehensive documentation with diagrams, examples, and implementation guides"
```

## Example: Adding a New Security Persona

### Security Engineer Persona
```json
{
  "security-engineer": {
    "name": "Security Engineer",
    "role": "Application and Infrastructure Security Specialist", 
    "system_prompt": "You are a security engineer specializing in application and infrastructure security. Analyze security vulnerabilities, design secure architectures, and implement security best practices. Focus on threat modeling, secure coding practices, and compliance requirements. Provide actionable security recommendations with risk assessments.",
    "context": "Cybersecurity and secure system design",
    "expertise": [
      "threat modeling",
      "vulnerability assessment", 
      "secure architecture design",
      "compliance frameworks",
      "penetration testing",
      "security monitoring"
    ],
    "response_format": "security analysis with risk levels, mitigation strategies, and implementation priorities",
    "metadata": {
      "category": "security",
      "priority": "high",
      "specialization": "application and infrastructure security"
    }
  }
}
```

## Configuration File Management

### Location
Persona definitions are stored in: `personas_definitions.json`

### Loading Process
1. Service startup loads `personas_definitions.json`
2. All personas are cached in memory for fast access
3. If file doesn't exist, default personas are created
4. Cache can be reloaded without service restart

### Adding Personas at Runtime
1. Edit `personas_definitions.json`
2. Add new persona definition
3. Restart personas gateway service to reload cache
4. Verify persona is available: `GET /personas`

## API Usage Examples

### List All Personas
```bash
curl http://localhost:8013/personas
```

### Get Persona Details
```bash
curl http://localhost:8013/personas/developer
```

### Use Persona for Processing
```bash
curl -X POST http://localhost:8013/persona/developer \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Create a REST API for user management",
    "context": {
      "technology_stack": "Python, FastAPI, PostgreSQL",
      "requirements": ["authentication", "CRUD operations", "validation"]
    }
  }'
```

## Testing New Personas

### Integration Test
```bash
# Test persona availability
./integration_test.sh --mode connectivity

# Test persona processing (manual)
curl -X POST http://localhost:8013/persona/YOUR_PERSONA_NAME \
  -H "Content-Type: application/json" \
  -d '{"query": "test query for your persona"}'
```

### Validation Checklist
- [ ] Persona loads without errors
- [ ] System prompt is comprehensive and clear
- [ ] Expertise areas are relevant and specific
- [ ] Response format produces consistent outputs
- [ ] API endpoints return expected data
- [ ] Integration with RAG engine works properly

## Performance Considerations

### Memory Usage
- Each persona uses ~2-5KB in cache
- 100 personas ≈ 500KB memory usage
- Cache warming on startup adds ~1-2 seconds

### Response Times
- Cached persona lookup: <1ms
- RAG engine processing: 100ms-2s (depends on query complexity)
- Total response time: 100ms-2s

### Scalability
- Personas gateway can handle 1000+ concurrent requests
- RAG engine (8003) is the bottleneck, not persona lookup
- Consider load balancing for high-volume deployments

## Advanced Features

### Persona Inheritance
```json
{
  "senior-developer": {
    "inherits_from": "developer",
    "name": "Senior Software Developer",
    "system_prompt": "You are a senior software developer with 8+ years experience...",
    "expertise": ["architecture", "mentoring", "code review", "system design"]
  }
}
```

### Conditional Personas
```json
{
  "frontend-developer": {
    "name": "Frontend Developer",
    "conditions": {
      "context.technology_stack": ["React", "Vue", "Angular", "JavaScript"]
    },
    "system_prompt": "You are a frontend developer specializing in modern web applications..."
  }
}
```

### Multi-Language Support
```json
{
  "developer-es": {
    "name": "Desarrollador de Software",
    "language": "es",
    "system_prompt": "Eres un desarrollador de software experimentado...",
    "response_language": "spanish"
  }
}
```

## Troubleshooting

### Common Issues

#### Persona Not Found
- Verify persona name in `personas_definitions.json`
- Check for typos in persona name
- Restart service to reload cache

#### Poor Response Quality
- Review and refine system prompt
- Add more specific expertise areas
- Improve context and response format specifications

#### Performance Issues
- Monitor RAG engine response times
- Check persona cache loading
- Verify service resource allocation

### Debug Endpoints
```bash
# Service health and loaded personas
curl http://localhost:8013/health

# Persona cache status  
curl http://localhost:8013/personas

# Specific persona details
curl http://localhost:8013/personas/{persona_name}
```

## Best Practices Summary

1. **Clear Role Definition**: Each persona should have a distinct, well-defined role
2. **Comprehensive System Prompts**: Include role, responsibilities, guidelines, and standards
3. **Relevant Expertise**: List specific, actionable skills and knowledge areas
4. **Consistent Response Formats**: Define expected output structure and style
5. **Meaningful Categories**: Group personas logically for better organization
6. **Regular Testing**: Validate persona responses and update as needed
7. **Performance Monitoring**: Track response times and cache performance
8. **Documentation**: Keep persona definitions well-documented and updated

---

**Generated by G1 Personas Gateway Service**  
**Version**: 1.0.0  
**Port**: 8013  
**Last Updated**: 2025-08-27