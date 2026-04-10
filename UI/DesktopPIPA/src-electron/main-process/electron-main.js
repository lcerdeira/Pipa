import { app, BrowserWindow, nativeTheme } from 'electron'
import { spawn } from 'child_process'
import path from 'path'

try {
  if (process.platform === 'win32' && nativeTheme.shouldUseDarkColors === true) {
    require('fs').unlinkSync(require('path').join(app.getPath('userData'), 'DevTools Extensions'))
  }
} catch (_) { }

if (process.env.PROD) {
  global.__statics = __dirname
}

let mainWindow
let flaskProcess = null
const FLASK_PORT = 5000

function startFlaskBackend () {
  const backendDir = process.env.PROD
    ? path.join(process.resourcesPath, 'back-end')
    : path.resolve(__dirname, '..', '..', '..', '..', '..', 'back-end')

  const env = {
    ...process.env,
    FLASK_APP: 'app.py',
    FLASK_ENV: process.env.PROD ? 'production' : 'development',
    PIPA_DATA_DIR: path.join(app.getPath('userData'), 'pipa-data')
  }

  // Try python3 first, then python
  const pythonCmd = process.platform === 'win32' ? 'python' : 'python3'

  flaskProcess = spawn(pythonCmd, ['-m', 'flask', 'run', '--port', String(FLASK_PORT)], {
    cwd: backendDir,
    env: env,
    stdio: ['ignore', 'pipe', 'pipe']
  })

  flaskProcess.stdout.on('data', (data) => {
    console.log(`[Flask] ${data}`)
  })

  flaskProcess.stderr.on('data', (data) => {
    console.log(`[Flask] ${data}`)
  })

  flaskProcess.on('error', (err) => {
    console.error('Failed to start Flask backend:', err)
  })

  flaskProcess.on('exit', (code) => {
    console.log(`Flask backend exited with code ${code}`)
    flaskProcess = null
  })
}

function stopFlaskBackend () {
  if (flaskProcess) {
    flaskProcess.kill()
    flaskProcess = null
  }
}

function createWindow () {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    useContentSize: true,
    minWidth: 1110,
    minHeight: 600,
    title: 'PIPA - Pipeline for Microbial Genomic Analysis',
    webPreferences: {
      nodeIntegration: process.env.QUASAR_NODE_INTEGRATION,
      nodeIntegrationInWorker: process.env.QUASAR_NODE_INTEGRATION
    }
  })

  mainWindow.loadURL(process.env.APP_URL)

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', () => {
  startFlaskBackend()
  // Give Flask a moment to start, then create the window
  setTimeout(createWindow, 1500)
})

app.on('window-all-closed', () => {
  stopFlaskBackend()
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('will-quit', () => {
  stopFlaskBackend()
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
