# OOM Services Startup Configuration Guide

This directory contains all the scripts and configuration files needed to start and manage the OOM (Object-Oriented Microservices) platform services.

## 🚀 Quick Start

### Option 1: Start All Services (Recommended)
```bash
# From the project root directory
./config/startup-scripts/start-all-services.sh
```

### Option 2: Use the Main OOM Management Script
```bash
# From the project root directory
./config/startup-scripts/oom.sh start
```

### Option 3: Start Individual Components
```bash
# Start TAO AI System
./config/startup-scripts/start-tao-system.sh

# Start microservices without Docker
./config/startup-scripts/run-services.sh
```

## 📁 Script Descriptions

### Core Management Scripts

#### `start-all-services.sh` (⭐ Recommended)
- **Purpose**: Comprehensive service startup script for non-Docker deployment
- **Features**:
  - Automatically allocates ports using the port allocation system
  - Starts services in correct dependency order
  - Creates log files for each service
  - Tracks PIDs for service management
  - Comprehensive error handling and status reporting

#### `oom.sh`
- **Purpose**: Main OOM platform management script
- **Commands**:
  - `start` - Start the platform
  - `stop` - Stop all services
  - `restart` - Restart the platform
  - `status` - Check service status
  - `logs` - View service logs

#### `check-services.sh`
- **Purpose**: Check status of all running services
- **Features**:
  - Validates PIDs and service health
  - Tests health endpoints
  - Shows port allocations
  - Lists log files

#### `stop-services.sh`
- **Purpose**: Stop all running OOM services
- **Features**:
  - Graceful shutdown with fallback to force kill
  - Cleanup of PID files
  - Port allocation status update

### Legacy Scripts

#### `start-tao-system.sh`
- **Purpose**: Start the original TAO AI system
- **Use Case**: When you need the classic TAO interface with dedicated ports

#### `run-services.sh`
- **Purpose**: Advanced service runner with extensive configuration
- **Use Case**: When you need fine-grained control over service startup

## 🔧 Configuration

### Port Management
The startup scripts use the integrated port allocation system:
- Ports are automatically allocated to avoid conflicts
- Use `python3 src/port_allocation_cli.py list` to see current allocations
- Use `python3 src/port_allocation_cli.py quick <service-name>` to manually allocate

### Service Discovery
Services are started in this order:
1. **Infrastructure**: Port management, database services
2. **AI Services**: AI Manager, RAG Engine, Ethics Engine
3. **Core Services**: Requirement analysis, program manager, task manager
4. **API Gateway**: Last to ensure all backend services are available

### Logging
- All service logs are stored in `logs/services/`
- Each service has its own log file: `logs/services/<service-name>.log`
- Use `tail -f logs/services/<service-name>.log` to monitor a specific service

### Process Management
- PIDs are stored in `pids/<service-name>.pid`
- Services can be individually stopped using the PID files
- The stop script handles cleanup automatically

## 🛠 Service Architecture

### Infrastructure Services
- **Port Management**: Dynamic port allocation and conflict resolution
- **Database Service**: Data persistence and management
- **Secrets Management**: API key and configuration management

### AI Services
- **AI Manager** (Port 8002): LLM connectivity and RAG backend
- **RAG Engine**: Knowledge retrieval and semantic search
- **Ethics Engine**: Compliance and ethical AI validation

### Core Services
- **Requirement Analysis**: Requirement processing and validation
- **Program Manager**: Project coordination and management
- **Task Manager**: Task scheduling and execution
- **API Gateway**: Request routing and load balancing

## 📋 Usage Examples

### Start the Platform
```bash
# Start all services
./config/startup-scripts/start-all-services.sh

# Check if everything is running
./config/startup-scripts/check-services.sh
```

### Monitor Services
```bash
# Check overall status
./config/startup-scripts/check-services.sh

# Monitor AI Manager logs
tail -f logs/services/ai-manager.log

# Check port allocations
python3 src/port_allocation_cli.py list
```

### Troubleshooting
```bash
# Stop all services and restart
./config/startup-scripts/stop-services.sh
./config/startup-scripts/start-all-services.sh

# Check specific service
curl http://localhost:8002/health  # AI Manager health

# Release stuck ports
python3 src/port_allocation_cli.py cleanup
```

### Frontend Integration
Once services are running, start the frontend components:
```bash
# Personas Manager Dashboard (Port 3003)
cd dashboard/personas-manager && npm run dev

# OOM System Monitor (Port 3001)
cd dashboard/oom-system-monitor && npm run dev
```

## 🔗 Service Integration

### Chat Interface Connectivity
The chat interface in the personas manager connects to:
1. **Personas Service** (Port 4025): Basic persona management
2. **AI Manager** (Port 8002): Advanced AI capabilities with RAG
3. **RAG Engine**: Knowledge-enhanced responses

### API Endpoints
- **AI Manager**: `http://localhost:8002`
  - Health: `/health`
  - Agents: `/agents`
  - Chat: `/agents/{agent_id}/chat`
- **Personas Service**: `http://localhost:4025`
  - Health: `/health`
  - Personas: `/api/personas`

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Check what's using a port
lsof -i :8002

# Release all allocated ports
python3 src/port_allocation_cli.py cleanup
```

#### Service Won't Start
```bash
# Check the log file
tail -f logs/services/<service-name>.log

# Verify dependencies are installed
cd services/<service-path>
pip install -r requirements.txt
```

#### AI Manager Issues
```bash
# Common fixes:
# 1. Ensure virtual environment is activated
source .venv/bin/activate

# 2. Install dependencies
cd services/ai-services/ai-manager
pip install -r requirements.txt

# 3. Check API keys are configured
cat .env
```

### Environment Setup
```bash
# Ensure Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install base dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## 📚 Additional Resources

- **Port Allocation CLI**: `python3 src/port_allocation_cli.py --help`
- **Service Logs**: `logs/services/`
- **PID Files**: `pids/`
- **Main Configuration**: `config/`

## 🎯 Next Steps

1. Run `./config/startup-scripts/start-all-services.sh`
2. Check status with `./config/startup-scripts/check-services.sh`
3. Test the chat interface at `http://localhost:3003`
4. Monitor logs for any issues

For advanced usage and customization, refer to the individual script files which contain detailed comments and configuration options.
