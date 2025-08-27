#!/bin/bash

# OOM Platform Service Runner
# Runs all services without Docker using individual environment files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVICES_DIR="$BASE_DIR/services/core"
CONFIG_DIR="$BASE_DIR/config"
ENV_DIR="$BASE_DIR/environments"
LOG_DIR="$BASE_DIR/logs"
PID_DIR="$BASE_DIR/pids"

# Ensure directories exist
mkdir -p "$ENV_DIR" "$LOG_DIR" "$PID_DIR"

# Service configuration using backend ports (for non-Docker deployment)
SERVICES="requirement-analysis-service:8101 program-manager-service:8102 cognitive-processing-service:8103 quality-assurance-service:8104 learning-metadata-service:8105 automl-service:8106 innovation-service:8107 collaboration-service:8108 api-gateway-service:8109 control-plane-service:8110 task-manager-service:8111 finance-service:8112 feature-engineering-service:8113 tooling-service:8114 ethics-service:8115"

# Infrastructure services that need to be running
INFRASTRUCTURE_PORTS="postgres:5432 redis:6379 kafka:9092"

# Helper functions for service management
get_service_port() {
    local service_name=$1
    echo "$SERVICES" | tr ' ' '\n' | grep "^$service_name:" | cut -d: -f2
}

get_all_services() {
    echo "$SERVICES" | tr ' ' '\n' | cut -d: -f1
}

get_infrastructure_port() {
    local service_name=$1
    echo "$INFRASTRUCTURE_PORTS" | tr ' ' '\n' | grep "^$service_name:" | cut -d: -f2
}

get_all_infrastructure() {
    echo "$INFRASTRUCTURE_PORTS" | tr ' ' '\n' | cut -d: -f1
}

# Function to print colored output
print_status() {
    local color=$1
    local message=$2
    echo -e "${color}[$(date '+%Y-%m-%d %H:%M:%S')] ${message}${NC}"
}

# Function to check if port is available
check_port() {
    local port=$1
    if lsof -i :$port >/dev/null 2>&1; then
        return 1
    else
        return 0
    fi
}

# Function to wait for service to be ready
wait_for_service() {
    local host=$1
    local port=$2
    local timeout=${3:-30}
    local count=0
    
    print_status $YELLOW "Waiting for $host:$port to be ready..."
    
    while [ $count -lt $timeout ]; do
        if nc -z $host $port >/dev/null 2>&1; then
            print_status $GREEN "$host:$port is ready!"
            return 0
        fi
        sleep 1
        ((count++))
    done
    
    print_status $RED "Timeout waiting for $host:$port"
    return 1
}

# Function to create environment file for a service
create_env_file() {
    local service_name=$1
    local port=$2
    local env_file="$ENV_DIR/${service_name}.env"
    
    cat > "$env_file" << EOF
# Environment configuration for $service_name
# Generated on $(date)

# Service Configuration
SERVICE_NAME=$service_name
SERVICE_PORT=$port
SERVICE_HOST=0.0.0.0
SERVICE_ENV=development

# Database Configuration
DATABASE_URL=postgresql://oom_user:oom_password@localhost:5432/oom_platform
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=oom_platform
POSTGRES_USER=oom_user
POSTGRES_PASSWORD=oom_password

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# Kafka Configuration (if needed)
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_GROUP_ID=${service_name}_group

# Monitoring & Observability
JAEGER_ENDPOINT=http://localhost:14268/api/traces
PROMETHEUS_GATEWAY=localhost:9091
GRAFANA_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
LOG_FILE=$LOG_DIR/${service_name}.log

# Security
SECRET_KEY=${service_name}_secret_$(date +%s)
JWT_SECRET_KEY=${service_name}_jwt_secret_$(date +%s)

# API Configuration
API_VERSION=v1
API_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8080"]

# Service Discovery
CONSUL_URL=http://localhost:8500
HEALTH_CHECK_INTERVAL=30

# External Services (using backend ports)
AI_MANAGER_URL=http://localhost:8201
RAG_ENGINE_URL=http://localhost:8202
ETHICS_ENGINE_URL=http://localhost:8203

# Resource Limits
MAX_WORKERS=4
TIMEOUT_SECONDS=30
RETRY_ATTEMPTS=3

# Development Settings
DEBUG=true
RELOAD=true
HOT_RELOAD=true
DEVELOPMENT=true
EOF

    print_status $GREEN "Created environment file: $env_file"
}

# Function to start a service
start_service() {
    local service_name=$1
    local port=$2
    local service_dir="$SERVICES_DIR/$service_name"
    local env_file="$ENV_DIR/${service_name}.env"
    local log_file="$LOG_DIR/${service_name}.log"
    local pid_file="$PID_DIR/${service_name}.pid"
    local error_log="$LOG_DIR/${service_name}_error.log"
    
    if [ -d "$service_dir" ]; then
        :
    else
        print_status $RED "Service directory not found: $service_dir"
        return 1
    fi
    
    if [ -f "$service_dir/main.py" ]; then
        :
    else
        print_status $RED "Service main.py not found: $service_dir/main.py"
        return 1
    fi
    
    # Check if port is available
    if check_port $port; then
        :
    else
        print_status $RED "Port $port is already in use for $service_name"
        return 1
    fi
    
    # Create environment file if it doesn't exist
    if [ -f "$env_file" ]; then
        :
    else
        create_env_file "$service_name" "$port"
    fi
    
    print_status $BLUE "Starting $service_name on port $port..."
    
    # Change to service directory and start the service
    cd "$service_dir"
    
    # Set environment variables from file
    set -a
    source "$env_file"
    set +a
    
    # Start the service in background
    nohup $BASE_DIR/.venv/bin/python main.py \
        --host 0.0.0.0 \
        --port $port \
        --env-file "$env_file" \
        > "$log_file" 2> "$error_log" &
    
    local pid=$!
    echo $pid > "$pid_file"
    
    # Wait a moment for service to start
    sleep 2
    
    # Check if service is still running
    if kill -0 $pid 2>/dev/null; then
        print_status $GREEN "$service_name started successfully (PID: $pid)"
        echo "  Log file: $log_file"
        echo "  Error log: $error_log"
        echo "  PID file: $pid_file"
        echo "  Environment: $env_file"
        echo "  URL: http://localhost:$port"
        return 0
    else
        print_status $RED "Failed to start $service_name"
        cat "$error_log"
        return 1
    fi
}

# Function to stop a service
stop_service() {
    local service_name=$1
    local pid_file="$PID_DIR/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 $pid 2>/dev/null; then
            print_status $YELLOW "Stopping $service_name (PID: $pid)..."
            kill $pid
            sleep 2
            if kill -0 $pid 2>/dev/null; then
                print_status $YELLOW "Force killing $service_name..."
                kill -9 $pid
            fi
            rm -f "$pid_file"
            print_status $GREEN "$service_name stopped"
        else
            print_status $YELLOW "$service_name was not running"
            rm -f "$pid_file"
        fi
    else
        print_status $YELLOW "No PID file found for $service_name"
    fi
}

# Function to check service status
check_service_status() {
    local service_name=$1
    local port=$2
    local pid_file="$PID_DIR/${service_name}.pid"
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if kill -0 $pid 2>/dev/null; then
            if nc -z localhost $port >/dev/null 2>&1; then
                print_status $GREEN "$service_name is RUNNING (PID: $pid, Port: $port)"
                return 0
            else
                print_status $YELLOW "$service_name process exists but port $port is not accessible"
                return 1
            fi
        else
            print_status $RED "$service_name is STOPPED (stale PID file)"
            rm -f "$pid_file"
            return 1
        fi
    else
        print_status $RED "$service_name is STOPPED"
        return 1
    fi
}

# Function to check infrastructure dependencies
check_infrastructure() {
    local all_ready=true
    
    print_status $BLUE "Checking infrastructure dependencies..."
    
    for service_port in $INFRASTRUCTURE_PORTS; do
        local service=$(echo "$service_port" | cut -d: -f1)
        local port=$(echo "$service_port" | cut -d: -f2)
        if nc -z localhost $port >/dev/null 2>&1; then
            print_status $GREEN "$service is available on port $port"
        else
            print_status $RED "$service is NOT available on port $port"
            all_ready=false
        fi
    done
    
    if [ "$all_ready" = true ]; then
        print_status $GREEN "All infrastructure dependencies are ready"
        return 0
    else
        print_status $RED "Some infrastructure dependencies are not available"
        return 1
    fi
}

# Function to display service status
status() {
    print_status $BLUE "=== OOM Platform Service Status ==="
    
    local running_count=0
    local total_count=0
    
    for service_port in $SERVICES; do
        local service=$(echo "$service_port" | cut -d: -f1)
        local port=$(echo "$service_port" | cut -d: -f2)
        total_count=$((total_count + 1))
        if check_service_status "$service" "$port"; then
            running_count=$((running_count + 1))
        fi
    done
    
    echo ""
    print_status $BLUE "Summary: $running_count/$total_count services running"
    
    # Check infrastructure
    echo ""
    check_infrastructure
}

# Function to start all services
start_all() {
    print_status $BLUE "=== Starting OOM Platform Services ==="
    
    # Check infrastructure first
    if check_infrastructure; then
        :
    else
        print_status $RED "Infrastructure dependencies not met. Please start required services first."
        echo ""
        echo "To start infrastructure with Docker:"
        echo "  docker run -d --name postgres -p 5432:5432 -e POSTGRES_DB=oom_platform -e POSTGRES_USER=oom_user -e POSTGRES_PASSWORD=oom_password postgres:15-alpine"
        echo "  docker run -d --name redis -p 6379:6379 redis:7-alpine"
        echo "  docker run -d --name kafka -p 9092:9092 confluentinc/cp-kafka:latest"
        return 1
    fi
    
    local started_count=0
    local failed_count=0
    
    for service_port in $SERVICES; do
        local service=$(echo "$service_port" | cut -d: -f1)
        local port=$(echo "$service_port" | cut -d: -f2)
        if start_service "$service" "$port"; then
            started_count=$((started_count + 1))
        else
            failed_count=$((failed_count + 1))
        fi
        echo ""
    done
    
    print_status $BLUE "=== Start Summary ==="
    print_status $GREEN "Started: $started_count services"
    if [ $failed_count -gt 0 ]; then
        print_status $RED "Failed: $failed_count services"
    fi
    
    # Show status after starting
    echo ""
    status
}

# Function to stop all services
stop_all() {
    print_status $BLUE "=== Stopping OOM Platform Services ==="
    
    for service_port in $SERVICES; do
        local service=$(echo "$service_port" | cut -d: -f1)
        stop_service "$service"
    done
    
    print_status $GREEN "All services stopped"
}

# Function to restart all services
restart_all() {
    print_status $BLUE "=== Restarting OOM Platform Services ==="
    stop_all
    sleep 3
    start_all
}

# Function to show service logs
logs() {
    local service_name=$1
    local log_file="$LOG_DIR/${service_name}.log"
    local error_log="$LOG_DIR/${service_name}_error.log"
    
    if [ -z "$service_name" ]; then
        print_status $RED "Please specify a service name"
        echo "Available services: ${!SERVICES[@]}"
        return 1
    fi
    
    if [ -f "$log_file" ]; then
        :
    else
        print_status $RED "Log file not found: $log_file"
        return 1
    fi
    
    print_status $BLUE "=== Logs for $service_name ==="
    echo "Standard output:"
    tail -f "$log_file" &
    local tail_pid=$!
    
    if [ -f "$error_log" ]; then
        echo ""
        echo "Error output:"
        tail -f "$error_log" &
        local tail_error_pid=$!
    fi
    
    # Wait for Ctrl+C
    trap "kill $tail_pid 2>/dev/null; [ -n '$tail_error_pid' ] && kill $tail_error_pid 2>/dev/null; exit 0" INT
    wait
}

# Function to show help
show_help() {
    echo "OOM Platform Service Runner"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  start [service]     Start all services or a specific service"
    echo "  stop [service]      Stop all services or a specific service"
    echo "  restart [service]   Restart all services or a specific service"
    echo "  status              Show status of all services"
    echo "  logs [service]      Show logs for a specific service"
    echo "  infrastructure      Check infrastructure dependencies"
    echo "  create-env [service] Create environment file for a service"
    echo "  help                Show this help message"
    echo ""
    echo "Available services:"
    for service_port in $SERVICES; do
        local service=$(echo "$service_port" | cut -d: -f1)
        local port=$(echo "$service_port" | cut -d: -f2)
        echo "  $service (port $port)"
    done
    echo ""
    echo "Examples:"
    echo "  $0 start                              # Start all services"
    echo "  $0 start requirement-analysis-service # Start specific service"
    echo "  $0 stop                               # Stop all services"
    echo "  $0 status                             # Show service status"
    echo "  $0 logs requirement-analysis-service  # Show service logs"
}

# Main command handling
case "${1:-help}" in
    start)
        if [ -n "$2" ]; then
            local port=$(get_service_port "$2")
            if [ -n "$port" ]; then
                start_service "$2" "$port"
            else
                print_status $RED "Unknown service: $2"
                echo "Available services:"
                get_all_services
                exit 1
            fi
        else
            start_all
        fi
        ;;
    stop)
        if [ -n "$2" ]; then
            local port=$(get_service_port "$2")
            if [ -n "$port" ]; then
                stop_service "$2"
            else
                print_status $RED "Unknown service: $2"
                echo "Available services:"
                get_all_services
                exit 1
            fi
        else
            stop_all
        fi
        ;;
    restart)
        if [ -n "$2" ]; then
            local port=$(get_service_port "$2")
            if [ -n "$port" ]; then
                stop_service "$2"
                sleep 2
                start_service "$2" "$port"
            else
                print_status $RED "Unknown service: $2"
                echo "Available services:"
                get_all_services
                exit 1
            fi
        else
            restart_all
        fi
        ;;
    status)
        status
        ;;
    logs)
        logs "$2"
        ;;
    infrastructure)
        check_infrastructure
        ;;
    create-env)
        if [ -n "$2" ]; then
            local port=$(get_service_port "$2")
            if [ -n "$port" ]; then
                create_env_file "$2" "$port"
            else
                print_status $RED "Unknown service: $2"
                echo "Available services:"
                get_all_services
                exit 1
            fi
        else
            print_status $RED "Please specify a service name"
            exit 1
        fi
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_status $RED "Unknown command: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
