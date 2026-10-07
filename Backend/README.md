# REACH Backend

Go backend service for the REACH project.

## Requirements
- Go 1.22+ (tested with Go 1.27)

## Getting Started

### Run Development Server
```bash
go run main.go
```
The server will start on port `8080` (or the port defined in the `PORT` environment variable):
```
http://localhost:8080
```

### Build Binary
```bash
go build -o server .
./server
```

## Endpoints
- `GET /` - Root status and API documentation entry point
- `GET /api/health` - Health check status and uptime
- `GET /api/info` - Service metadata and environment info
