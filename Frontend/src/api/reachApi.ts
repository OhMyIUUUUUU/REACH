import apiClient from './client'
import type { HealthResponse, APIInfoResponse } from './types'

/**
 * REST API client functions for REACH Go backend endpoints.
 */
export const reachApi = {
  /**
   * Health check endpoint: GET /api/health
   */
  async getHealth(): Promise<HealthResponse> {
    const { data } = await apiClient.get<HealthResponse>('/health')
    return data
  },

  /**
   * API info endpoint: GET /api/info
   */
  async getInfo(): Promise<APIInfoResponse> {
    const { data } = await apiClient.get<APIInfoResponse>('/info')
    return data
  },
}
