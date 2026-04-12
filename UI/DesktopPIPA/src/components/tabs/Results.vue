<template>
  <div id="results" class="column full-width" :class="$q.screen.width < 1230 ? 'q-pa-lg' : 'q-pa-xl'">
    <div class="column full-height no-wrap full-width">
      <div class="row q-pb-md justify-between">
        <div class="row" :class="$q.platform.is.mobile ? 'justify-between full-width' : ''">
          <h4 class="q-ma-none">Results</h4>
        </div>
        <div class="row">
          <q-btn round color="primary q-mr-md" text-color="black" icon="arrow_back" size="md" @click="currentPage = 1">
            <q-tooltip anchor="center left" self="center right" :offset="[10, 10]">
              Go back
            </q-tooltip>
          </q-btn>
          <q-btn
            class="my-btn"
            label="Download All"
            style="width: 150px"
            :disable="!isCompleted"
            @click="downloadResults"
          />
        </div>
      </div>

      <!-- Progress section -->
      <div v-if="isRunning" class="q-pb-lg">
        <div class="row items-center q-pb-sm">
          <q-spinner-gears color="primary" size="2em" class="q-mr-sm"/>
          <span class="text-h6">Pipeline Running</span>
        </div>
        <q-linear-progress
          :value="pipelineProgress / 100"
          size="25px"
          color="primary"
          track-color="grey-3"
          class="q-mb-sm"
        >
          <div class="absolute-full flex flex-center">
            <q-badge color="white" text-color="primary" :label="pipelineProgress + '%'" />
          </div>
        </q-linear-progress>
        <div class="text-caption text-grey-7">
          <strong>Stage:</strong> {{ pipelineStage || 'Initializing' }}
          <span v-if="pipelineMessage"> &mdash; {{ pipelineMessage }}</span>
        </div>
      </div>

      <!-- Error alerts -->
      <div v-if="hasErrors" class="q-pb-md">
        <q-banner v-for="(err, i) in errors" :key="'err'+i" class="bg-red-1 text-red q-mb-sm" rounded>
          <template v-slot:avatar>
            <q-icon name="warning" color="red"/>
          </template>
          {{ typeof err === 'string' ? err : err.error }}
        </q-banner>
      </div>

      <div class="full-width" v-if="isCompleted || hasTableData">
        <q-tabs
          v-model="slide"
          stretch
          indicator-color="transparent"
          class="my-tabs text-white full-width bg-black"
          align="justify"
          style="height: 45px"
        >
          <q-tab style="text-transform: none" v-for="(tab, i) in tabs" :key="i+'tab'" :name="tab.name" :label="tab.label" />
        </q-tabs>
        <q-tab-panels
          v-model="slide"
          animated
          class="col-grow my-panel full-width"
          :style="{minHeight: '800px'}"
        >
          <!-- Data Table -->
          <q-tab-panel
            :name="tabs[0].name"
            class="q-pa-none"
            :style="{height: '800px'}"
          >
            <div class="column full-height full-width">
              <div class="full-height full-width">
                <q-table
                  :data="tableRows"
                  :columns="tableColumns"
                  row-key="__index"
                  :filter="filter"
                  :loading="loading"
                  class="full-height"
                  separator="horizontal"
                  :rows-per-page-options="[ 50, 100, 150, 200, 0 ]"
                >
                  <template v-slot:top-left>
                    <q-input
                      dense
                      debounce="300"
                      v-model="filter"
                      placeholder="Search"
                    >
                      <template v-slot:append>
                        <q-btn v-if="filter != ''" flat round icon="close" @click="filter = ''"/>
                        <q-icon name="search" />
                      </template>
                    </q-input>
                  </template>
                </q-table>
              </div>
            </div>
          </q-tab-panel>

          <!-- Pipeline Summary -->
          <q-tab-panel
            :name="tabs[1].name"
            class="q-pa-md"
            :style="{height: '800px'}"
          >
            <div v-if="results && results.stages" class="column q-gutter-y-md">
              <q-card v-for="(stage, name) in results.stages" :key="name" flat bordered>
                <q-card-section>
                  <div class="row items-center justify-between">
                    <div class="text-h6 text-capitalize">{{ name }}</div>
                    <q-badge
                      :color="stage.status === 'completed' ? 'green' : 'red'"
                      :label="stage.status"
                    />
                  </div>
                  <div class="text-caption text-grey-7 q-mt-xs">
                    Duration: {{ stage.elapsed_seconds }}s
                  </div>
                  <div v-if="stage.error" class="text-red q-mt-sm">
                    {{ stage.error }}
                  </div>
                </q-card-section>
              </q-card>
            </div>
            <div v-else class="text-grey-5 text-center q-mt-xl">
              No pipeline results yet.
            </div>
          </q-tab-panel>

          <!-- Files Browser -->
          <q-tab-panel
            :name="tabs[2].name"
            class="q-pa-md"
            :style="{height: '800px'}"
          >
            <q-list bordered separator v-if="resultFiles.length > 0">
              <q-item v-for="(file, i) in resultFiles" :key="'file'+i" clickable @click="downloadFile(file)">
                <q-item-section avatar>
                  <q-icon name="insert_drive_file" color="primary"/>
                </q-item-section>
                <q-item-section>
                  <q-item-label>{{ file }}</q-item-label>
                </q-item-section>
                <q-item-section side>
                  <q-icon name="download"/>
                </q-item-section>
              </q-item>
            </q-list>
            <div v-else class="text-grey-5 text-center q-mt-xl">
              No result files available yet.
            </div>
          </q-tab-panel>
        </q-tab-panels>
      </div>

      <!-- Empty state -->
      <div v-if="!isRunning && !isCompleted && !hasTableData" class="text-center q-mt-xl">
        <q-icon name="hourglass_empty" size="4em" color="grey-4"/>
        <div class="text-h6 text-grey-5 q-mt-md">Waiting for pipeline to complete</div>
      </div>
    </div>
  </div>
</template>

<script>
const tabs = [
  { name: 'table', label: 'Table' },
  { name: 'summary', label: 'Pipeline Summary' },
  { name: 'files', label: 'Files' }
]

import { scroll } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll

export default {
  data () {
    return {
      tabs,
      filter: '',
      slide: 'table',
      loading: false,
      pollInterval: null,
      tableColumns: [],
      tableRows: []
    }
  },
  computed: {
    currentPage: {
      get () {
        return this.$store.state.pipa.currentPage
      },
      set (val) {
        this.$store.commit('pipa/changePage', val)
      }
    },
    isRunning () {
      return this.$store.getters['pipa/isRunning']
    },
    isCompleted () {
      return this.$store.getters['pipa/isCompleted']
    },
    hasErrors () {
      return this.$store.getters['pipa/hasErrors']
    },
    pipelineProgress () {
      return this.$store.state.pipa.pipelineProgress
    },
    pipelineStage () {
      return this.$store.state.pipa.pipelineStage
    },
    pipelineMessage () {
      return this.$store.state.pipa.pipelineMessage
    },
    results () {
      return this.$store.state.pipa.results
    },
    resultFiles () {
      return this.$store.state.pipa.resultFiles
    },
    errors () {
      return this.$store.state.pipa.errors
    },
    hasTableData () {
      return this.tableRows.length > 0
    }
  },
  watch: {
    results (val) {
      if (val) {
        this.buildTable(val)
      }
    }
  },
  methods: {
    buildTable (results) {
      // Build dynamic table from pipeline results
      if (!results || !results.stages) return

      const rows = []
      const columnSet = new Set()

      // Parse prediction results (MLST, Abricate outputs)
      const stages = results.stages
      for (const stageName in stages) {
        const stage = stages[stageName]
        if (stage.result && typeof stage.result === 'object' && !Array.isArray(stage.result)) {
          for (const key in stage.result) {
            columnSet.add('tool')
            columnSet.add('result')
            rows.push({
              tool: key,
              result: typeof stage.result[key] === 'string' ? stage.result[key] : JSON.stringify(stage.result[key]),
              __index: rows.length
            })
          }
        }
      }

      // Also add stage summary rows
      columnSet.add('stage')
      columnSet.add('status')
      columnSet.add('duration_s')
      for (const stageName in stages) {
        rows.push({
          stage: stageName,
          status: stages[stageName].status,
          duration_s: stages[stageName].elapsed_seconds,
          __index: rows.length
        })
      }

      this.tableColumns = Array.from(columnSet).map(col => ({
        name: col,
        label: col.charAt(0).toUpperCase() + col.slice(1).replace(/_/g, ' '),
        field: col,
        sortable: true,
        align: 'left',
        headerStyle: 'font-weight: bolder;'
      }))
      this.tableRows = rows
    },
    async downloadResults () {
      const jobId = this.$store.state.pipa.jobId
      const apiBase = this.$store.state.pipa.apiBaseUrl
      if (!jobId) return

      for (const file of this.resultFiles) {
        const link = document.createElement('a')
        link.href = `${apiBase}/results/${jobId}/files/${file}`
        link.download = file.split('/').pop()
        link.click()
      }
    },
    downloadFile (file) {
      const jobId = this.$store.state.pipa.jobId
      const apiBase = this.$store.state.pipa.apiBaseUrl
      if (!jobId) return

      const link = document.createElement('a')
      link.href = `${apiBase}/results/${jobId}/files/${file}`
      link.download = file.split('/').pop()
      link.click()
    },
    async initResults () {
      console.log('[Results] initResults, jobId:', this.$store.state.pipa.jobId, 'status:', this.$store.state.pipa.pipelineStatus)
      // Always poll once to get the latest status
      const data = await this.$store.dispatch('pipa/pollStatus')
      console.log('[Results] pollStatus returned:', data)
      if (data && (data.status === 'completed' || data.status === 'completed_with_errors')) {
        console.log('[Results] Pipeline completed, fetching results')
        await this.$store.dispatch('pipa/fetchResults')
        console.log('[Results] Results fetched, status:', this.$store.state.pipa.pipelineStatus)
      } else if (data && data.status === 'running') {
        console.log('[Results] Pipeline running, starting polling')
        this.startPolling()
      } else {
        console.log('[Results] No data or unknown status, trying poll in 1s')
        setTimeout(() => this.initResults(), 1000)
      }
    },
    startPolling () {
      if (this.pollInterval) return
      this.pollInterval = setInterval(async () => {
        try {
          const data = await this.$store.dispatch('pipa/pollStatus')
          if (data && (data.status === 'completed' || data.status === 'completed_with_errors' || data.status === 'failed')) {
            this.stopPolling()
            if (data.status !== 'failed') {
              await this.$store.dispatch('pipa/fetchResults')
            }
          }
        } catch (err) {
          console.error('Poll error:', err)
        }
      }, 3000)
    },
    stopPolling () {
      if (this.pollInterval) {
        clearInterval(this.pollInterval)
        this.pollInterval = null
      }
    },
    handleScroll () {
      const ele = document.getElementById('results')
      const target = getScrollTarget(ele)
      const offset = ele.offsetTop - ele.scrollHeight
      const duration = 0
      setScrollPosition(target, offset, duration)
    }
  },
  mounted () {
    this.handleScroll()
    this.initResults()
  },
  beforeDestroy () {
    this.stopPolling()
  },
  activated () {
    this.initResults()
  }
}
</script>

<style lang="scss" scoped>
.my-btn {
  background-color: $terciary;
  color: white;
}
.my-tabs {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
.tab-active {
  background-color: black;
  color: black;
}
.my-panel {
  border-bottom-left-radius: 10px;
  border-bottom-right-radius: 10px;
  border: 1px solid black;
}
</style>
