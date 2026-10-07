import { useState } from 'react'

interface HealthResponse {
  status: string
  timestamp: string
  uptime: string
}

function App() {
  const [clickCount, setClickCount] = useState<number>(0)
  const [loading, setLoading] = useState<boolean>(false)
  const [healthData, setHealthData] = useState<HealthResponse | null>(null)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  const checkBackendHealth = async () => {
    setLoading(true)
    setErrorMsg(null)
    setHealthData(null)

    try {
      const response = await fetch('/api/health')
      if (!response.ok) {
        throw new Error(`HTTP Error: ${response.status} ${response.statusText}`)
      }
      const data: HealthResponse = await response.json()
      setHealthData(data)
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMsg(err.message)
      } else {
        setErrorMsg('Failed to reach backend server. Ensure Go server is running on :8080.')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between p-6 md:p-12 selection:bg-sky-500 selection:text-white">
      <div className="max-w-6xl w-full mx-auto space-y-12">
        {/* Header */}
        <header className="text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-500/30 text-sky-400 text-xs font-semibold uppercase tracking-wider">
            <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-[0_0_8px_#34d399] animate-pulse"></span>
            Fullstack Workspace Ready
          </div>
          <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
            REACH Platform
          </h1>
          <p className="text-slate-400 max-w-xl mx-auto text-base md:text-lg">
            Modern React 19 & TypeScript frontend styled with Tailwind CSS v4, paired with a Go REST backend.
          </p>
        </header>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Frontend Card */}
          <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800 hover:border-sky-500/40 rounded-2xl p-6 md:p-8 transition-all duration-300 shadow-xl space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 font-bold text-xl">
                  ⚛
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">Frontend</h2>
                  <p className="text-xs text-slate-500">React 19 + TypeScript + Vite</p>
                </div>
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-full font-medium bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
                Active
              </span>
            </div>

            <p className="text-sm text-slate-400 leading-relaxed">
              Ultra-fast build performance with Vite, strict TypeScript validation, and native Tailwind CSS v4 styling.
            </p>

            <div className="flex flex-wrap gap-2">
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">React 19</span>
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">TypeScript</span>
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-sky-950/60 text-sky-300 border border-sky-500/30">Tailwind CSS v4</span>
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">Vite 8</span>
            </div>

            <div className="pt-2">
              <button
                type="button"
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-600 hover:from-sky-400 hover:to-indigo-500 text-white font-semibold text-sm shadow-lg shadow-sky-500/20 hover:shadow-sky-500/30 transition-all duration-200 cursor-pointer"
                onClick={() => setClickCount((prev) => prev + 1)}
                id="counter-button"
              >
                Interactive State: {clickCount}
              </button>
            </div>
          </div>

          {/* Backend Card */}
          <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800 hover:border-sky-500/40 rounded-2xl p-6 md:p-8 transition-all duration-300 shadow-xl space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-11 h-11 rounded-xl bg-cyan-500/10 border border-cyan-500/30 flex items-center justify-center text-cyan-400 font-bold text-lg font-mono">
                  Go
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white">Backend</h2>
                  <p className="text-xs text-slate-500">Go 1.27 + net/http</p>
                </div>
              </div>
              <span className="text-xs px-2.5 py-0.5 rounded-full font-medium bg-slate-800 text-slate-400 border border-slate-700/50">
                Port 8080
              </span>
            </div>

            <p className="text-sm text-slate-400 leading-relaxed">
              Lightweight HTTP server with JSON routing, CORS headers, and graceful shutdown handling.
            </p>

            <div className="flex flex-wrap gap-2">
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">Go 1.27</span>
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">reach/backend</span>
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">CORS Ready</span>
              <span className="text-xs font-medium px-2.5 py-1 rounded-md bg-slate-800/80 text-slate-300 border border-slate-700/50">Graceful Exit</span>
            </div>

            <div className="pt-2">
              <button
                type="button"
                className="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm border border-slate-700 transition-all duration-200 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                onClick={checkBackendHealth}
                disabled={loading}
                id="ping-backend-button"
              >
                {loading ? 'Pinging /api/health...' : 'Test Backend Connection'}
              </button>
            </div>

            {healthData && (
              <div className="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-300 text-xs font-mono space-y-1">
                <div><strong>✓ Connected:</strong> Status: {healthData.status}</div>
                <div><strong>Uptime:</strong> {healthData.uptime}</div>
                <div><strong>Time:</strong> {healthData.timestamp}</div>
              </div>
            )}

            {errorMsg && (
              <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-300 text-xs font-mono space-y-1">
                <div><strong>⚠ Offline or Unreachable:</strong></div>
                <div>{errorMsg}</div>
                <div className="text-slate-400 mt-1">
                  Run <code className="text-cyan-300">go run main.go</code> in <code className="text-cyan-300">/Backend</code> to start.
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Directory Architecture */}
        <section className="space-y-4 pt-4">
          <h2 className="text-xl font-bold text-white">Workspace Directory Architecture</h2>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
            <div className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 transition-colors">
              <div className="font-mono text-xs font-bold text-sky-400">Frontend/</div>
              <div className="text-xs text-slate-500 mt-1">React 19 + TS + Tailwind</div>
            </div>
            <div className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 transition-colors">
              <div className="font-mono text-xs font-bold text-cyan-400">Backend/</div>
              <div className="text-xs text-slate-500 mt-1">Go REST service</div>
            </div>
            <div className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 transition-colors">
              <div className="font-mono text-xs font-bold text-amber-400">DB/</div>
              <div className="text-xs text-slate-500 mt-1">Schemas & migrations</div>
            </div>
            <div className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 transition-colors">
              <div className="font-mono text-xs font-bold text-violet-400">Nlp-service/</div>
              <div className="text-xs text-slate-500 mt-1">AI / NLP service</div>
            </div>
            <div className="bg-slate-900/40 border border-slate-800 hover:border-slate-700 rounded-xl p-3.5 transition-colors">
              <div className="font-mono text-xs font-bold text-emerald-400">Docs/</div>
              <div className="text-xs text-slate-500 mt-1">System design specs</div>
            </div>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="mt-16 text-center text-xs text-slate-600 border-t border-slate-800/80 pt-6">
        REACH Workspace • React 19, TypeScript, Tailwind CSS v4 & Go
      </footer>
    </div>
  )
}

export default App
