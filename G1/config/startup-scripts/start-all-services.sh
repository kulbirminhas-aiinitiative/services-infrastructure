#!/bin/bash

# OOM Services Startup Script (Non-Docker)
# Starts all OOM services without Docker using the services directory structure

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SERVICES_DIR="$BASE_DIR/services"
LOG_DIR="$BASE_DIR/logs/services"
PID_DIR="$BASE_DIR/pids"

# Create necessary directories
mkdir -p "$LOG_DIR" "$PID_DIR"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[OOM]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Function to start a service
start_service() {
    local service_name=$1
    local service_path=$2
    local port=$3
    local log_file="$LOG_DIR/${service_name}.log"
    local pid_file="$PID_DIR/${service_name}.pid"
    
    print_status "Starting $service_name on port $port..."
    
    # Check if port is available
    if ! check_port $port; then
        print_warning "Port $port is already in use for $service_name"
        return 1
    fi
    
    # Check if service directory exists
    if [ ! -d "$service_path" ]; then
        print_error "Service directory not found: $service_path"
        return 1
    fi
    
    cd "$service_path"
    
    # Check for main.py or app.py
    if [ -f "main.py" ]; then
        PORT=$port python3 main.py > "$log_file" 2>&1 &
        local service_pid=$!
    elif [ -f "app.py" ]; then
        PORT=$port python3 app.py > "$log_file" 2>&1 &
        local service_pid=$!
    elif [ -f "server.py" ]; then
        PORT=$port python3 server.py > "$log_file" 2>&1 &
        local service_pid=$!
    else
        print_error "No entry point found for $service_name (looking for main.py, app.py, or server.py)"
        return 1
    fi
    
    echo $service_pid > "$pid_file"
    print_success "$service_name started (PID: $service_pid)"
    
    # Wait a moment for service to start
    sleep 2
    
    # Check if service is still running
    if ! kill -0 $service_pid 2>/dev/null; then
        print_error "$service_name failed to start. Check log: $log_file"
        return 1
    fi
    
    return 0
}

# Function to allocate port for service
allocate_port() {
    local service_name=$1
    local category=$2
    local description=$3
    
    cd "$BASE_DIR"
    python3 src/port_allocation_cli.py quick "$service_name" \
        --port-type http \
        --scope external \
        --category "$category" \
        --description "$description" 2>/dev/null | grep "port" | grep -o '[0-9]*' | tail -1
}

print_status "Starting OOM Services Infrastructure..."
echo "========================================"

# Start infrastructure services first
print_status "Starting Infrastructure Services..."

# 1. Port Management Service
PORT_MGMT_PORT=$(allocate_port "port-management-service" "infrastructure" "Port allocation and management")
if [ ! -z "$PORT_MGMT_PORT" ]; then
    start_service "port-management" "$SERVICES_DIR/infrastructure/port-management" "$PORT_MGMT_PORT"
fi

# 2. Database Service
DB_SERVICE_PORT=$(allocate_port "database-service" "infrastructure" "Database management service")
if [ ! -z "$DB_SERVICE_PORT" ]; then
    start_service "database-service" "$SERVICES_DIR/infrastructure/database-service" "$DB_SERVICE_PORT"
fi

# Start AI Services
print_status "Starting AI Services..."

# 3. AI Manager (if not already running on port 8002)
if check_port 8002; then
    start_service "ai-manager" "$SERVICES_DIR/ai-services/ai-manager" "8002"
else
    print_warning "AI Manager port 8002 already in use"
fi

# 4. RAG Engine
RAG_ENGINE_PORT=$(allocate_port "rag-engine-service" "backend" "RAG engine for knowledge retrieval")
if [ ! -z "$RAG_ENGINE_PORT" ]; then
    start_service "rag-engine" "$SERVICES_DIR/ai-services/rag-engine" "$RAG_ENGINE_PORT"
fi

# 5. Ethics Engine
ETHICS_ENGINE_PORT=$(allocate_port "ethics-engine-service" "backend" "Ethics and compliance engine")
if [ ! -z "$ETHICS_ENGINE_PORT" ]; then
    start_service "ethics-engine" "$SERVICES_DIR/ai-services/ethics-engine" "$ETHICS_ENGINE_PORT"
fi

# Start Core Services
print_status "Starting Core Services..."

# 6. Requirement Analysis Service
REQ_ANALYSIS_PORT=$(allocate_port "requirement-analysis-service" "core" "Requirement analysis and processing")
if [ ! -z "$REQ_ANALYSIS_PORT" ]; then
    start_service "requirement-analysis" "$SERVICES_DIR/core/requirement-analysis-service" "$REQ_ANALYSIS_PORT"
fi

# 7. Program Manager Service
PROG_MGR_PORT=$(allocate_port "program-manager-service" "core" "Program management and coordination")
if [ ! -z "$PROG_MGR_PORT" ]; then
    start_service "program-manager" "$SERVICES_DIR/core/program-manager-service" "$PROG_MGR_PORT"
fi

# 8. Task Manager Service
TASK_MGR_PORT=$(allocate_port "task-manager-service" "core" "Task management and scheduling")
if [ ! -z "$TASK_MGR_PORT" ]; then
    start_service "task-manager" "$SERVICES_DIR/core/task-manager-service" "$TASK_MGR_PORT"
fi

# Start API Gateway last
print_status "Starting API Gateway..."

# 9. API Gateway
API_GATEWAY_PORT=$(allocate_port "api-gateway-service" "core" "API gateway and routing")
if [ ! -z "$API_GATEWAY_PORT" ]; then
    start_service "api-gateway" "$SERVICES_DIR/core/api-gateway" "$API_GATEWAY_PORT"
fi

print_success "All services startup attempted!"
print_status "Check service status with: ./config/startup-scripts/check-services.sh"
print_status "Stop all services with: ./config/startup-scripts/stop-services.sh"
print_status "View logs in: $LOG_DIR"

# Show running services
print_status "Current port allocations:"
cd "$BASE_DIR"
python3 src/port_allocation_cli.py list
