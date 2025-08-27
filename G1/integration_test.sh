#!/usr/bin/env bash

# G1 Project Integration Test Script - External Services Mode
# Tests connectivity to existing Docker services and reports missing ones

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Default values
TEST_MODE="full"
VERBOSE=false
TIMEOUT=10

# Service definitions (service_name:port format)
# Core Infrastructure Services
EXPECTED_SERVICES="
rag-engine:8003
secrets-management:8004
port-management:8005
ai-manager:8007
personas-service:8012
personas-gateway:8013
"

# All personas are handled by personas-gateway:8013 (no individual ports)
# Personas: requirement-concierge, program-manager, quality-assurance, 
# cognitive-processing, developer, tester, infrastructure-engineer, 
# release-engineer, devops-specialist, risk-assessor, team-manager, 
# operations, mind-engine-coordinator

# Health endpoints to try
HEALTH_ENDPOINTS="/health / /api/health /ping /status"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            TEST_MODE="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --help|-h)
            echo "G1 Integration Test Script - External Services Mode"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --mode MODE     Test mode: full, connectivity, workflow, missing (default: full)"
            echo "  --verbose, -v   Enable verbose output"
            echo "  --timeout SEC   Service connection timeout in seconds (default: 10)"
            echo "  --help, -h      Show this help message"
            echo ""
            echo "Test Modes:"
            echo "  full         - Run all tests: connectivity, workflow, and integration"
            echo "  connectivity - Only test service connectivity"
            echo "  workflow     - Only test workflow orchestrator"
            echo "  missing      - Only report missing services"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Logging functions
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️  $1${NC}"
}

log_info() {
    echo -e "${CYAN}[$(date '+%Y-%m-%d %H:%M:%S')] ℹ️  $1${NC}"
}

log_section() {
    echo -e "${PURPLE}[$(date '+%Y-%m-%d %H:%M:%S')] 🔍 $1${NC}"
}

# Check if a service is accessible on a port
check_service_port() {
    local service_name=$1
    local port=$2
    
    if [ "$VERBOSE" = true ]; then
        log_info "Testing $service_name on port $port..."
    fi
    
    # Try different health endpoints
    for endpoint in $HEALTH_ENDPOINTS; do
        local url="http://localhost:$port$endpoint"
        if curl -s -f --connect-timeout $TIMEOUT "$url" >/dev/null 2>&1; then
            log_success "$service_name is accessible on port $port at $endpoint"
            return 0
        fi
    done
    
    # Try basic connection
    if timeout $TIMEOUT bash -c "echo >/dev/tcp/localhost/$port" 2>/dev/null; then
        log_warning "$service_name port $port is open but no HTTP response"
        return 2
    fi
    
    if [ "$VERBOSE" = true ]; then
        log_error "$service_name is not accessible on port $port"
    fi
    return 1
}

# Discover currently running Docker services
discover_running_services() {
    log_section "Discovering currently running Docker services..."
    
    if ! command -v docker >/dev/null 2>&1; then
        log_warning "Docker command not found"
        return
    fi
    
    local container_info=$(docker ps --format "{{.Names}}\t{{.Ports}}" 2>/dev/null || echo "")
    
    if [ -z "$container_info" ]; then
        log_warning "No running Docker containers found"
        return
    fi
    
    echo "$container_info" | while IFS=$'\t' read -r name ports; do
        if [ "$name" = "NAMES" ]; then
            continue
        fi
        if [[ $ports =~ 0\.0\.0\.0:([0-9]+) ]]; then
            local port="${BASH_REMATCH[1]}"
            log_info "Found running service: $name on port $port"
        fi
    done
}

# Test connectivity to expected services
test_service_connectivity() {
    log_section "Testing connectivity to expected services..."
    
    local available_services=0
    local missing_services=0
    local port_open_services=0
    local accessible_services=""
    local missing_services_list=""
    local port_open_list=""
    
    # Process each service
    for service_port in $EXPECTED_SERVICES; do
        if [ -z "$service_port" ]; then
            continue
        fi
        
        local service_name=$(echo "$service_port" | cut -d':' -f1)
        local port=$(echo "$service_port" | cut -d':' -f2)
        
        case $(check_service_port "$service_name" "$port"; echo $?) in
            0)
                available_services=$((available_services + 1))
                accessible_services="$accessible_services\n  ✅ $service_name:$port"
                ;;
            2)
                port_open_services=$((port_open_services + 1))
                port_open_list="$port_open_list\n  ⚠️  $service_name:$port"
                ;;
            *)
                missing_services=$((missing_services + 1))
                missing_services_list="$missing_services_list\n  ❌ $service_name:$port"
                ;;
        esac
    done
    
    # Summary
    echo ""
    log_section "Service Connectivity Summary:"
    log_success "Fully accessible services: $available_services"
    if [ -n "$accessible_services" ]; then
        echo -e "$accessible_services"
    fi
    
    if [ $port_open_services -gt 0 ]; then
        log_warning "Services with open ports but no HTTP response: $port_open_services"
        echo -e "$port_open_list"
    fi
    
    if [ $missing_services -gt 0 ]; then
        log_error "Missing services: $missing_services"
        echo -e "$missing_services_list"
        echo ""
        log_warning "To start missing services, you may need to run:"
        log_warning "docker-compose up -d <service-name>"
        return 1
    else
        log_success "All expected services are accessible!"
        return 0
    fi
}

# Test workflow orchestrator
test_workflow_orchestrator() {
    log_section "Testing Workflow Orchestrator..."
    
    if [ ! -f "workflow_orchestrator.py" ]; then
        log_error "workflow_orchestrator.py not found"
        return 1
    fi
    
    log_info "Running workflow orchestrator test..."
    if python3 workflow_orchestrator.py > /tmp/g1_orchestrator_test.log 2>&1; then
        log_success "Workflow orchestrator executed successfully"
        
        # Check for patterns in output
        local successful_patterns=$(grep -c "✅\|successful\|completed successfully" /tmp/g1_orchestrator_test.log 2>/dev/null || echo "0")
        local failed_patterns=$(grep -c "❌\|failed\|404\|Connection refused\|Error" /tmp/g1_orchestrator_test.log 2>/dev/null || echo "0")
        
        log_info "Orchestrator results: $successful_patterns successes, $failed_patterns failures"
        
        if [ "$VERBOSE" = true ]; then
            echo ""
            echo -e "${CYAN}--- Orchestrator Output ---${NC}"
            head -50 /tmp/g1_orchestrator_test.log
            echo -e "${CYAN}--- End Output (truncated) ---${NC}"
        fi
        return 0
    else
        log_error "Workflow orchestrator failed"
        if [ "$VERBOSE" = true ]; then
            echo ""
            echo -e "${RED}--- Error Output ---${NC}"
            cat /tmp/g1_orchestrator_test.log
            echo -e "${RED}--- End Error ---${NC}"
        fi
        return 1
    fi
}

# Test integration tests
test_integration_tests() {
    log_section "Running Integration Tests..."
    
    if [ ! -f "integration_tests.py" ]; then
        log_error "integration_tests.py not found"
        return 1
    fi
    
    log_info "Running integration test suite..."
    if python3 integration_tests.py > /tmp/g1_integration_test.log 2>&1; then
        log_success "Integration tests completed successfully"
        
        # Analyze test results
        local test_scenarios=$(grep -c "🧪 TEST:" /tmp/g1_integration_test.log 2>/dev/null || echo "0")
        local completed_workflows=$(grep -c "✅ Workflow completed" /tmp/g1_integration_test.log 2>/dev/null || echo "0")
        
        log_info "Integration test results: $test_scenarios scenarios, $completed_workflows completed workflows"
        
        if [ "$VERBOSE" = true ]; then
            echo ""
            echo -e "${CYAN}--- Integration Test Output ---${NC}"
            head -50 /tmp/g1_integration_test.log
            echo -e "${CYAN}--- End Output (truncated) ---${NC}"
        fi
        return 0
    else
        log_error "Integration tests failed"
        if [ "$VERBOSE" = true ]; then
            echo ""
            echo -e "${RED}--- Error Output ---${NC}"
            cat /tmp/g1_integration_test.log
            echo -e "${RED}--- End Error ---${NC}"
        fi
        return 1
    fi
}

# Report missing services with suggestions
report_missing_services() {
    log_section "Analyzing missing services and providing recommendations..."
    
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}                     G1 SERVICE STATUS REPORT                        ${NC}"
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════════${NC}"
    
    # Currently running services
    echo ""
    log_info "Currently Running Docker Services:"
    if command -v docker >/dev/null 2>&1; then
        local running_containers=$(docker ps --format "{{.Names}}" 2>/dev/null || echo "")
        if [ -n "$running_containers" ]; then
            echo "$running_containers" | while IFS= read -r container; do
                local ports=$(docker port "$container" 2>/dev/null | head -1 | cut -d':' -f2 | cut -d'-' -f1 2>/dev/null || echo "unknown")
                echo -e "  ${GREEN}🟢${NC} $container ${CYAN}(port: $ports)${NC}"
            done
        else
            echo -e "  ${YELLOW}No Docker containers are currently running${NC}"
        fi
    else
        echo -e "  ${RED}Docker command not available${NC}"
    fi
    
    # Expected vs Available services
    echo ""
    log_info "Expected Services Analysis:"
    for service_port in $EXPECTED_SERVICES; do
        if [ -z "$service_port" ]; then
            continue
        fi
        
        local service_name=$(echo "$service_port" | cut -d':' -f1)
        local port=$(echo "$service_port" | cut -d':' -f2)
        
        if check_service_port "$service_name" "$port" >/dev/null 2>&1; then
            echo -e "  ${GREEN}✅${NC} $service_name:$port - Available"
        else
            echo -e "  ${RED}❌${NC} $service_name:$port - Missing"
        fi
    done
    
    echo ""
    echo -e "${PURPLE}════════════════════════════════════════════════════════════════════${NC}"
}

# Cleanup function
cleanup() {
    if [ "$VERBOSE" = true ]; then
        log_info "Cleaning up temporary files..."
    fi
    rm -f /tmp/g1_orchestrator_test.log /tmp/g1_integration_test.log
}

# Main test execution
main() {
    echo -e "${PURPLE}"
    echo "🚀 G1 Project Integration Tests - External Services Mode"
    echo "============================================================"
    echo -e "${NC}"
    log_info "Test Mode: $TEST_MODE"
    log_info "Timeout: ${TIMEOUT}s"
    echo ""
    
    # Trap cleanup on exit
    trap cleanup EXIT
    
    local exit_code=0
    
    case $TEST_MODE in
        "connectivity")
            discover_running_services
            if ! test_service_connectivity; then
                exit_code=1
            fi
            ;;
        "workflow")
            if ! test_workflow_orchestrator; then
                exit_code=1
            fi
            ;;
        "missing")
            report_missing_services
            ;;
        "full")
            discover_running_services
            echo ""
            if ! test_service_connectivity; then
                exit_code=1
            fi
            echo ""
            if ! test_workflow_orchestrator; then
                exit_code=1
            fi
            echo ""
            if ! test_integration_tests; then
                exit_code=1
            fi
            echo ""
            report_missing_services
            ;;
        *)
            log_error "Unknown test mode: $TEST_MODE"
            exit 1
            ;;
    esac
    
    echo ""
    if [[ $exit_code -eq 0 ]]; then
        log_success "🎉 All requested tests completed successfully!"
    else
        log_warning "⚠️ Some tests had issues. Check the output above for details."
    fi
    
    exit $exit_code
}

# Run main function
main "$@"