#!/bin/bash

# Meeting Prep Docker Deployment Script
# This script helps you build and run the dockerized Meeting Prep application

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}======================================${NC}"
    echo -e "${BLUE}  Meeting Prep Docker Deployment${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

check_requirements() {
    echo "Checking requirements..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    print_success "Docker is installed"
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    print_success "Docker Compose is installed"
    
    # Check if .env file exists
    if [ ! -f .env ]; then
        print_warning ".env file not found. Creating from example..."
        cp .env.example .env
        print_warning "Please edit .env file with your actual API keys before running the application"
        return 1
    fi
    print_success ".env file exists"
    return 0
}

build_image() {
    echo ""
    echo "Building Docker image..."
    docker build -t meeting-prep-app .
    print_success "Docker image built successfully"
}

run_development() {
    echo ""
    echo "Starting development environment..."
    docker-compose up --build -d
    print_success "Application is running at http://localhost:8501"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
}

run_production() {
    echo ""
    echo "Starting production environment with Nginx..."
    docker-compose --profile production up --build -d
    print_success "Application is running at http://localhost (port 80)"
    print_success "Streamlit direct access: http://localhost:8501"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose --profile production down"
}

show_logs() {
    echo ""
    echo "Showing application logs..."
    docker-compose logs -f meeting-prep-app
}

stop_services() {
    echo ""
    echo "Stopping all services..."
    docker-compose down
    docker-compose --profile production down 2>/dev/null || true
    print_success "All services stopped"
}

show_help() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build the Docker image"
    echo "  dev         Run in development mode (port 8501)"
    echo "  prod        Run in production mode with Nginx (port 80)"
    echo "  logs        Show application logs"
    echo "  stop        Stop all services"
    echo "  clean       Stop services and remove containers/images"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev      # Start development server"
    echo "  $0 prod     # Start production server with Nginx"
    echo "  $0 logs     # View logs"
    echo "  $0 stop     # Stop all services"
}

clean_up() {
    echo ""
    echo "Cleaning up containers and images..."
    docker-compose down
    docker-compose --profile production down 2>/dev/null || true
    docker rmi meeting-prep-app 2>/dev/null || true
    docker system prune -f
    print_success "Cleanup completed"
}

# Main script
print_header

case "${1:-help}" in
    "build")
        if check_requirements; then
            build_image
        fi
        ;;
    "dev")
        if check_requirements; then
            run_development
        else
            print_error "Please configure your .env file with API keys first"
            exit 1
        fi
        ;;
    "prod")
        if check_requirements; then
            run_production
        else
            print_error "Please configure your .env file with API keys first"
            exit 1
        fi
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        stop_services
        ;;
    "clean")
        clean_up
        ;;
    "help"|*)
        show_help
        ;;
esac
