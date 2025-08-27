#!/bin/bash

# OOM (Object-Oriented Microservices) Platform Management Script
# This script provides commands to manage the entire OOM ecosystem

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="oom"

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

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose > /dev/null 2>&1; then
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
}

# Function to wait for service to be healthy
wait_for_service() {
    local service_name=$1
    local max_attempts=${2:-30}
    local attempt=1

    print_status "Waiting for $service_name to be healthy..."
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose ps $service_name | grep -q "healthy\|Up"; then
            print_success "$service_name is ready!"
            return 0
        fi
        
        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    print_error "$service_name failed to start within expected time"
    return 1
}

# Function to show service status
show_status() {
    print_status "OOM Platform Service Status:"
    echo ""
    docker-compose ps
    echo ""
    
    print_status "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
}

# Function to show logs for a specific service
show_logs() {
    local service_name=$1
    if [ -z "$service_name" ]; then
        print_error "Please specify a service name"
        echo "Available services:"
        docker-compose config --services
        return 1
    fi
    
    print_status "Showing logs for $service_name..."
    docker-compose logs -f $service_name
}

# Function to start infrastructure services
start_infrastructure() {
    print_status "Starting infrastructure services..."
    
    docker-compose up -d postgres redis zookeeper kafka kong-database
    
    wait_for_service postgres
    wait_for_service redis
    wait_for_service kafka
    
    print_status "Running Kong database migrations..."
    docker-compose up --no-deps kong-bootstrap
    
    print_status "Starting Kong API Gateway..."
    docker-compose up -d kong
    wait_for_service kong
    
    print_status "Starting monitoring services..."
    docker-compose up -d prometheus grafana jaeger
    
    print_success "Infrastructure services are running!"
}

# Function to start all core services
start_core_services() {
    print_status "Starting core business services..."
    
    docker-compose up -d \
        requirement-analysis-service \
        cognitive-processing-service \
        quality-assurance-service \
        learning-metadata-service \
        automl-service \
        innovation-service \
        collaboration-service
    
    print_success "Core services are starting up..."
}

# Function to start data services
start_data_services() {
    print_status "Starting data services..."
    
    docker-compose up -d \
        user-data-service \
        workflow-data-service \
        analytics-data-service
    
    print_success "Data services are starting up..."
}

# Function to start frontend services
start_frontend_services() {
    print_status "Starting frontend services..."
    
    docker-compose up -d \
        web-application \
        admin-dashboard
    
    print_success "Frontend services are starting up..."
}

# Function to start all services
start_all() {
    print_status "Starting complete OOM platform..."
    
    start_infrastructure
    start_core_services
    start_data_services
    start_frontend_services
    
    print_success "OOM platform is starting up!"
    print_status "Available endpoints:"
    echo "  - Web Application: http://localhost:3000"
    echo "  - Admin Dashboard: http://localhost:3001"
    echo "  - API Gateway: http://localhost:8000"
    echo "  - Grafana: http://localhost:3000 (admin/admin)"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Jaeger: http://localhost:16686"
    echo "  - Kong Admin: http://localhost:8001"
}

# Function to stop all services
stop_all() {
    print_status "Stopping OOM platform..."
    docker-compose down
    print_success "OOM platform stopped"
}

# Function to stop and remove all data
destroy_all() {
    print_warning "This will destroy all data and containers!"
    read -p "Are you sure? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_status "Destroying OOM platform..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_success "OOM platform destroyed"
    else
        print_status "Operation cancelled"
    fi
}

# Function to restart a specific service
restart_service() {
    local service_name=$1
    if [ -z "$service_name" ]; then
        print_error "Please specify a service name"
        return 1
    fi
    
    print_status "Restarting $service_name..."
    docker-compose restart $service_name
    print_success "$service_name restarted"
}

# Function to scale a service
scale_service() {
    local service_name=$1
    local replicas=$2
    
    if [ -z "$service_name" ] || [ -z "$replicas" ]; then
        print_error "Usage: $0 scale <service_name> <replicas>"
        return 1
    fi
    
    print_status "Scaling $service_name to $replicas replicas..."
    docker-compose up -d --scale $service_name=$replicas $service_name
    print_success "$service_name scaled to $replicas replicas"
}

# Function to run database migrations
run_migrations() {
    print_status "Running database migrations..."
    
    # Run migrations for each service that needs them
    services=("requirement-analysis-service" "cognitive-processing-service" "quality-assurance-service" 
              "learning-metadata-service" "automl-service" "innovation-service" "collaboration-service"
              "user-data-service" "workflow-data-service" "analytics-data-service")
    
    for service in "${services[@]}"; do
        print_status "Running migrations for $service..."
        docker-compose exec $service alembic upgrade head || print_warning "Migration failed for $service"
    done
    
    print_success "Database migrations completed"
}

# Function to backup databases
backup_databases() {
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p $backup_dir
    
    print_status "Creating database backup in $backup_dir..."
    
    docker-compose exec postgres pg_dumpall -U oom_user > $backup_dir/all_databases.sql
    
    print_success "Database backup created at $backup_dir/all_databases.sql"
}

# Function to show help
show_help() {
    echo "OOM Platform Management Script"
    echo ""
    echo "Usage: $0 <command> [options]"
    echo ""
    echo "Commands:"
    echo "  start-infra         Start infrastructure services (postgres, redis, kafka, kong)"
    echo "  start-core          Start core business services"
    echo "  start-data          Start data services"
    echo "  start-frontend      Start frontend services"
    echo "  start-all           Start all services"
    echo "  stop                Stop all services"
    echo "  destroy             Stop and remove all services and data"
    echo "  restart <service>   Restart a specific service"
    echo "  scale <service> <n> Scale a service to n replicas"
    echo "  status              Show service status"
    echo "  logs <service>      Show logs for a specific service"
    echo "  migrate             Run database migrations"
    echo "  backup              Backup all databases"
    echo "  help                Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start-all"
    echo "  $0 restart requirement-analysis-service"
    echo "  $0 scale web-application 3"
    echo "  $0 logs cognitive-processing-service"
}

# Function to check prerequisites
check_prerequisites() {
    check_docker
    check_docker_compose
    
    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        print_error "Docker Compose file not found: $COMPOSE_FILE"
        exit 1
    fi
}

# Main script logic
main() {
    local command=$1
    
    case $command in
        "start-infra")
            check_prerequisites
            start_infrastructure
            ;;
        "start-core")
            check_prerequisites
            start_core_services
            ;;
        "start-data")
            check_prerequisites
            start_data_services
            ;;
        "start-frontend")
            check_prerequisites
            start_frontend_services
            ;;
        "start-all")
            check_prerequisites
            start_all
            ;;
        "stop")
            check_prerequisites
            stop_all
            ;;
        "destroy")
            check_prerequisites
            destroy_all
            ;;
        "restart")
            check_prerequisites
            restart_service $2
            ;;
        "scale")
            check_prerequisites
            scale_service $2 $3
            ;;
        "status")
            check_prerequisites
            show_status
            ;;
        "logs")
            check_prerequisites
            show_logs $2
            ;;
        "migrate")
            check_prerequisites
            run_migrations
            ;;
        "backup")
            check_prerequisites
            backup_databases
            ;;
        "help"|"--help"|"-h"|"")
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run the main function with all arguments
main "$@"
