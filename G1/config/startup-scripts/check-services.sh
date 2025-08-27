#!/bin/bash

# OOM Services Status Checker
# Checks the status of all running OOM services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PID_DIR="$BASE_DIR/pids"
LOG_DIR="$BASE_DIR/logs/services"

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

# Function to check if service is running
check_service() {
    local service_name=$1
    local pid_file="$PID_DIR/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 "$pid" 2>/dev/null; then
            print_success "$service_name is running (PID: $pid)"
            return 0
        else
            print_error "$service_name is not running (stale PID file)"
            rm -f "$pid_file"
            return 1
        fi
    else
        print_warning "$service_name PID file not found"
        return 1
    fi
}

# Function to check service health endpoint
check_health() {
    local service_name=$1
    local port=$2
    
    if curl -s "http://localhost:$port/health" >/dev/null 2>&1; then
        print_success "$service_name health check passed (port $port)"
        return 0
    else
        print_warning "$service_name health check failed (port $port)"
        return 1
    fi
}

print_status "Checking OOM Services Status..."
echo "================================="

# Check PID files for running services
if [ -d "$PID_DIR" ]; then
    for pid_file in "$PID_DIR"/*.pid; do
        if [ -f "$pid_file" ]; then
            service_name=$(basename "$pid_file" .pid)
            check_service "$service_name"
        fi
    done
else
    print_warning "No PID directory found. Services may not be running."
fi

echo ""
print_status "Port Allocations:"
cd "$BASE_DIR"
python3 src/port_allocation_cli.py list

echo ""
print_status "Health Check Summary:"

# Try to check health of known services
declare -A SERVICES=(
    ["ai-manager"]="8002"
    ["port-management"]=""
    ["database-service"]=""
    ["rag-engine"]=""
    ["ethics-engine"]=""
    ["requirement-analysis"]=""
    ["program-manager"]=""
    ["task-manager"]=""
    ["api-gateway"]=""
)

for service in "${!SERVICES[@]}"; do
    port="${SERVICES[$service]}"
    if [ ! -z "$port" ]; then
        check_health "$service" "$port"
    fi
done

echo ""
print_status "Log files available in: $LOG_DIR"
if [ -d "$LOG_DIR" ]; then
    ls -la "$LOG_DIR"
fi
