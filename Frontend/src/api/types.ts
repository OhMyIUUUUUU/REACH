export interface HealthResponse {
  status: string
  timestamp: string
  uptime: string
}

export interface APIInfoResponse {
  name: string
  version: string
  environment: string
  status: string
}

export interface ApiError {
  message: string
  status?: number
  code?: string
}
