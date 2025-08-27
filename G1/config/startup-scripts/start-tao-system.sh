#!/bin/bash
# Tao AI System Startup Script with Dedicated Port Management
# This script starts the Tao AI System using ports defined in PORTS.env

set -e  # Exit on any error

# Load port configuration
source ./load_ports.sh

echo ""
echo "🚀 Starting Tao AI System with Dedicated Ports"
echo "=============================================="

# Function to check if port is available
check_port() {
    local port=$1
    local service=$2
    
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "❌ Port $port is already in use (required for $service)"
        echo "   Please stop the service using port $port or update PORTS.env"
        return 1
    else
        echo "✅ Port $port is available for $service"
        return 0
    fi
}

# Check all required ports
echo "📋 Checking Port Availability..."
check_port $TAO_API_PORT "Tao API Server" || exit 1
check_port $TAO_FRONTEND_PORT "Frontend Application" || exit 1
check_port $AI_MANAGER_PORT "AI Manager Service" || exit 1
check_port $TAO_REDIS_PORT "Redis Message Bus" || exit 1
check_port $TAO_WEBSOCKET_PORT "WebSocket Server" || exit 1

echo ""
echo "🔧 Starting Services..."

# Start Redis if not running (optional - may be external)
if ! pgrep redis-server > /dev/null 2>&1; then
    echo "🔴 Redis not detected. Please start Redis on port $TAO_REDIS_PORT"
    echo "   Example: redis-server --port $TAO_REDIS_PORT"
else
    echo "✅ Redis is running"
fi

# Start Tao API Server
echo "🌐 Starting Tao API Server on port $TAO_API_PORT..."
export TAO_API_PORT=$TAO_API_PORT
export TAO_REDIS_PORT=$TAO_REDIS_PORT
export AI_MANAGER_PORT=$AI_MANAGER_PORT

# Check if Python virtual environment is activated
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Using virtual environment: $VIRTUAL_ENV"
    PYTHON_CMD="python"
else
    # Use the project's virtual environment
    if [[ -f ".venv/bin/python" ]]; then
        echo "✅ Using project virtual environment: .venv"
        PYTHON_CMD=".venv/bin/python"
    else
        echo "⚠️ No virtual environment detected, using system Python"
        PYTHON_CMD="python"
    fi
fi

# Start the API server in background
echo "🚀 Launching Tao API Server..."
$PYTHON_CMD -m src.tao.api.main &
API_PID=$!

# Wait a moment for server to start
sleep 2

# Check if API server started successfully
if ps -p $API_PID > /dev/null 2>&1; then
    echo "✅ Tao API Server started successfully (PID: $API_PID)"
    echo "   Access at: http://localhost:$TAO_API_PORT"
    echo "   API Docs: http://localhost:$TAO_API_PORT/docs"
else
    echo "❌ Failed to start Tao API Server"
    exit 1
fi

echo ""
echo "📊 Service Status:"
echo "  API Server:    http://localhost:$TAO_API_PORT ✅"
echo "  Frontend:      http://localhost:$TAO_FRONTEND_PORT (not started)"
echo "  AI Manager:    http://localhost:$AI_MANAGER_PORT (external service)"
echo "  Redis:         localhost:$TAO_REDIS_PORT (check manually)"
echo ""
echo "🎯 Next Steps:"
echo "1. Start your AI Manager service on port $AI_MANAGER_PORT"
echo "2. Start the frontend application on port $TAO_FRONTEND_PORT"
echo "3. Test the API: curl http://localhost:$TAO_API_PORT/health"
echo ""
echo "To stop services:"
echo "  kill $API_PID  # Stop API Server"
echo "  ./stop.sh      # Stop all services (if script exists)"

# Keep script running and show logs
echo ""
echo "📝 API Server Logs (Press Ctrl+C to stop):"
echo "==========================================="
wait $API_PID
