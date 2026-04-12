<template>
  <q-layout view="lHh Lpr lFf">
    <!-- Backend loading overlay -->
    <q-dialog v-model="showLoading" persistent seamless position="standard">
      <q-card class="text-center q-pa-xl" style="min-width: 400px; border-radius: 16px">
        <div class="q-mb-lg">
          <q-img src="~assets/PipaLogo.jpeg" width="100px" style="border-radius: 12px"/>
        </div>
        <div class="text-h5 text-weight-bold q-mb-md">PIPA</div>

        <div v-if="backendStatus === 'checking-docker'">
          <q-spinner-gears size="40px" color="primary" class="q-mb-md"/>
          <div class="text-body1">Checking Docker...</div>
        </div>

        <div v-else-if="backendStatus === 'pulling'">
          <q-spinner-dots size="40px" color="info" class="q-mb-md"/>
          <div class="text-body1 q-mb-sm">Downloading analysis tools</div>
          <div class="text-caption text-grey-7 q-mb-md">First launch only (~3 GB)</div>
          <div class="text-caption text-grey-6" style="max-width:350px; word-break:break-all">{{ pullMessage }}</div>
        </div>

        <div v-else-if="backendStatus === 'starting-docker' || backendStatus === 'starting-local'">
          <q-spinner-gears size="40px" color="positive" class="q-mb-md"/>
          <div class="text-body1">Starting backend...</div>
        </div>

        <div v-else-if="backendStatus === 'waiting'">
          <q-spinner-hourglass size="40px" color="warning" class="q-mb-md"/>
          <div class="text-body1">Waiting for backend to respond...</div>
        </div>

        <div v-else-if="backendStatus === 'failed'">
          <q-icon name="error_outline" size="40px" color="negative" class="q-mb-md"/>
          <div class="text-body1 text-negative q-mb-sm">Backend not available</div>
          <div class="text-caption text-grey-7 q-mb-md">
            Install <a href="https://www.docker.com/products/docker-desktop/" target="_blank">Docker Desktop</a>
            and restart PIPA.
          </div>
          <q-btn flat label="Continue without backend" color="grey" no-caps @click="showLoading = false"/>
        </div>

        <div v-else-if="backendStatus === 'pull-failed'">
          <q-icon name="cloud_off" size="40px" color="negative" class="q-mb-md"/>
          <div class="text-body1 text-negative q-mb-sm">Failed to download tools</div>
          <div class="text-caption text-grey-7 q-mb-md">Check your internet connection and try again.</div>
          <q-btn flat label="Continue anyway" color="grey" no-caps @click="showLoading = false"/>
        </div>
      </q-card>
    </q-dialog>

    <q-drawer
      v-model="drawer"
      show-if-above
      :width="300"
      :breakpoint="1100"
      content-class="gradient-dark my-drawer"
    >
      <q-scroll-area class="fit">
        <div class="column">
          <div class="column items-center q-py-lg">
            <q-img
              src="~assets/PipaLogo.jpeg"
              :height="'180px'"
              :width="'180px'"
              spinner-color="white"
              style="border-radius: 20px"
            />
            <div class="text-h6 text-white text-weight-bold q-mt-md">PIPA</div>
            <div class="text-caption" style="color: rgba(224,225,221,0.6)">Microbial Genomic Analysis</div>
          </div>
          <q-separator dark style="background: rgba(255,255,255,0.08)"/>
          <q-list dark class="q-mt-sm">
            <q-item
              v-for="(menuItem, index) in menuList"
              :key="menuItem+index"
              clickable
              v-ripple
              dark
              class="menu-item q-mx-sm"
              style="border-radius: 10px; margin-bottom: 4px"
              @click="openExternal(menuItem.link)"
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" color="grey-5" size="22px"/>
              </q-item-section>
              <q-item-section style="color: rgba(224,225,221,0.9); font-size: 15px">
                {{ menuItem.label }}
              </q-item-section>
              <q-item-section side>
                <q-icon name="open_in_new" size="14px" style="color: rgba(224,225,221,0.3)"/>
              </q-item-section>
            </q-item>
          </q-list>
          <q-space/>
          <!-- Backend mode indicator -->
          <div class="q-pa-sm q-mx-sm q-mb-xs" style="border-radius: 8px; background: rgba(255,255,255,0.04)">
            <div class="row items-center justify-center">
              <q-icon :name="backendIcon" :color="backendColor" size="14px" class="q-mr-xs"/>
              <span style="color: rgba(224,225,221,0.4); font-size: 11px">{{ backendLabel }}</span>
            </div>
          </div>
          <div class="q-pa-md text-center" style="color: rgba(224,225,221,0.3); font-size: 11px">
            v2.0.0
          </div>
        </div>
      </q-scroll-area>
    </q-drawer>
    <q-footer v-if="currentPage === 0" class="gradient-dark text-center" style="height: 44px; display: flex; align-items: center; justify-content: center">
      <div style="color: rgba(224,225,221,0.6); font-size: 13px">
        Copyright 2026 | DOI: <a href="https://doi.org/10.5281/zenodo.19521044" target="_blank" style="color: #52B788; text-decoration: none">10.5281/zenodo.19521044</a>
      </div>
    </q-footer>
    <q-page-container>
      <router-view/>
    </q-page-container>
  </q-layout>
</template>

<script>

const menuList = [
  {
    icon: 'img:myIcons/github2.png',
    label: 'GitHub',
    link: 'https://github.com/lcerdeira/Pipa'
  },
  {
    icon: 'menu_book',
    label: 'Documentation',
    link: 'https://pipa-tool.readthedocs.io/en/latest/'
  },
  {
    icon: 'download',
    label: 'Download Desktop',
    link: 'https://github.com/lcerdeira/Pipa/releases'
  }
]

export default {
  name: 'MainLayout',
  data () {
    return {
      menuList,
      drawer: false,
      backendStatus: 'checking-docker',
      backendMode: 'none',
      pullMessage: '',
      showLoading: false
    }
  },
  computed: {
    currentPage: {
      get () {
        return this.$store.state.pipa.currentPage
      }
    },
    backendIcon () {
      if (this.backendMode === 'docker') return 'cloud_done'
      if (this.backendMode === 'local') return 'computer'
      return 'cloud_off'
    },
    backendColor () {
      if (this.backendMode === 'docker') return 'positive'
      if (this.backendMode === 'local') return 'info'
      return 'grey-6'
    },
    backendLabel () {
      if (this.backendMode === 'docker') return 'Docker backend'
      if (this.backendMode === 'local') return 'Local backend'
      return 'No backend'
    }
  },
  methods: {
    openExternal (url) {
      if (window.__TAURI__) {
        window.__TAURI__.shell.open(url)
      } else {
        window.open(url, '_blank')
      }
    },
    setupTauriListeners () {
      if (!window.__TAURI__) return

      const { listen } = window.__TAURI__.event

      listen('backend-status', (event) => {
        console.log('[PIPA] Backend status:', event.payload)
        this.backendStatus = event.payload

        if (event.payload === 'ready') {
          this.showLoading = false
          // Get the backend mode
          window.__TAURI__.invoke('get_backend_mode').then(mode => {
            this.backendMode = mode
          })
        } else if (event.payload === 'failed' || event.payload === 'pull-failed') {
          // Keep dialog open to show error
        }
      })

      listen('pull-progress', (event) => {
        this.pullMessage = event.payload
      })
    }
  },
  mounted () {
    if (window.__TAURI__) {
      this.showLoading = true
      this.setupTauriListeners()
    } else {
      // Web SPA mode - no Docker needed, direct connection
      this.backendMode = 'local'
      this.backendStatus = 'ready'
    }
  }
}
</script>

<style lang="scss">
  .my-drawer {
    border-right: 1px solid rgba(255, 255, 255, 0.06);
  }
  .menu-item:hover {
    background: rgba(255, 255, 255, 0.06) !important;
  }
</style>
