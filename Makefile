.PHONY: build up down logs restart test clean

# Build all services
build:
	docker-compose build

# Start services in detached mode
up:
	docker-compose up -d

# Stop all services
down:
	docker-compose down

# View logs for all services (follow mode)
logs:
	docker-compose logs -f

# Restart all services
restart:
	docker-compose restart

# Run backend tests
test:
	docker-compose build bmp-sensor
	docker-compose run --rm bmp-sensor pytest /app/backend/tests

# Clean up docker system (prune)
clean:
	docker system prune -f
