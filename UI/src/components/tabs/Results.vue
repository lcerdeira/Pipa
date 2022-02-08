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
          <q-btn class="my-btn" label="Download" style="width: 150px"/>
        </div>
      </div>
      <div class="full-width">
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
          <q-tab-panel
            :name="tabs[0].name"
            class="q-pa-none"
            :style="{height: '800px'}"
          >
            <div class="column full-height full-width">
              <div class="full-height full-width">
                <q-table
                  :data="filteredRows"
                  :columns="columns"
                  row-key="name"
                  :filter="filter"
                  :filter-method="filterTable"
                  :loading="loading"
                  class="full-height"
                  separator="horizontal"
                  :rows-per-page-options="[ 50, 100, 150, 200, 250, 300, 350, 400, 0 ]"
                  :pagination="{sortBy: colNames[0]}"
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
                  <template v-slot:header-cell="props">
                    <q-th :props="props">
                      {{ props.col.label }}
                      <q-btn-dropdown class="q-mx-xs" :class="!options[props.col.name][1] ? 'bg-blue text-white' : ''" outline size="sm" dense square @click.stop="">
                        <q-list>
                          <q-item class="q-pa-none">
                            <q-item-section>
                              <div class="row items-center">
                                <q-checkbox
                                  v-model="options[props.col.name][1]"
                                  color="info"
                                  @input="updateCheck({name: props.col.name, bool: options[props.col.name][1]})"
                                />
                                <q-item-label>All</q-item-label>
                              </div>
                            </q-item-section>
                          </q-item>
                          <q-scroll-area style="height: 300px; width: 200px">
                            <q-item
                              v-for="(op, i) in options[props.col.name][0]"
                              class="q-pa-none"
                              :key="i+'op'+i"
                            >
                              <q-item-section>
                                <div class="row items-center">
                                  <q-checkbox
                                    v-model="op.bool"
                                    :disable="!op.active && op.bool"
                                    :color="op.active ?'info' : 'primary'"
                                    @input="updateCheck({name: props.col.name, bool: op.bool, item: i})"
                                  />
                                  <q-item-label>{{op.column}}</q-item-label>
                                </div>
                              </q-item-section>
                            </q-item>
                          </q-scroll-area>
                        </q-list>
                      </q-btn-dropdown>
                    </q-th>
                  </template>
                </q-table>
              </div>
            </div>
          </q-tab-panel>

          <q-tab-panel
            :name="tabs[1].name"
            class="q-pa-none"
            :style="{height: '800px'}"
          >
            <div class="row full-height">
              <div class="col-6" style="height: 50%">
                <highcharts :options="stackChart"></highcharts>
              </div>
              <div class="col-6" style="height: 50%">
                <highcharts :options="scatterChart"></highcharts>
              </div>
            </div>
          </q-tab-panel>

          <q-tab-panel
            :name="tabs[2].name"
            class="full-width full-height"
            :style="{height: '800px'}"
          >
            <div id="jbrowse_linear_view" class=""></div>
            <script type="module">
            import assembly from './jbrowse/assembly.js'
            import tracks from './jbrowse/tracks.js'
            const genomeView = new JBrowseLinearView({
              container: document.getElementById('jbrowse_linear_view'),
              assembly,
              tracks,
              location: '1:100,987,269..100,987,368'
            })
            </script>
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </div>
</template>

<script>
const tabs = [
  {
    name: 'table',
    label: 'Table'
  },
  {
    name: 'graph',
    label: 'Graphics'
  },
  {
    name: 'jbrowser',
    label: 'J-Browser'
  },
  {
    name: 'apollo',
    label: 'Apollo'
  },
  {
    name: 'bandage',
    label: 'Bandage'
  }
]

const colNames = [
  'strain',
  'species',
  'species_match',
  'contig_count',
  'N50',
  'largest_contig',
  'ambiguous_bases',
  'ST',
  'virulence_score',
  'resistance_score',
  'num_resistance_classes',
  'num_resistance_genes',
  'Yersiniabactin',
  'YbST',
  'Colibactin',
  'CbST',
  'Aerobactin',
  'AbST',
  'Salmochelin',
  'SmST',
  'rmpA',
  'rmpA2',
  'wzi',
  'K_locus',
  'K_locus_problems',
  'K_locus_confidence',
  'K_locus_identity',
  'K_locus_missing_genes',
  'O_locus',
  'O_locus_problems',
  'O_locus_confidence',
  'O_locus_identity',
  'O_locus_missing_genes',
  'Chr_ST',
  'gapA',
  'infB',
  'mdh',
  'pgi',
  'phoE',
  'rpoB',
  'tonB',
  'ybtS',
  'ybtX',
  'ybtQ',
  'ybtP',
  'ybtA',
  'irp2',
  'irp1',
  'ybtU',
  'ybtT',
  'ybtE',
  'fyuA',
  'clbA',
  'clbB',
  'clbC',
  'clbD',
  'clbE',
  'clbF',
  'clbG',
  'clbH',
  'clbI',
  'clbL',
  'clbM',
  'clbN',
  'clbO',
  'clbP',
  'clbQ',
  'AGly',
  'Col',
  'Fcyn',
  'Flq',
  'Gly',
  'MLS',
  'Ntmdz',
  'Phe',
  'Rif',
  'Sul',
  'Tet',
  'Tgc',
  'Tmt',
  'Omp',
  'Bla',
  'Bla_Carb',
  'Bla_ESBL',
  'Bla_ESBL_inhR',
  'Bla_broad',
  'Bla_broad_inhR'
]
const columns = []
const data = []

const stackChart = {
  chart: {
    type: 'column'
  },
  xAxis: {
    categories: ['One', 'Two', 'Three', 'Four', 'Five']
  },
  plotOptions: {
    column: {
      stacking: 'normal'
    }
  },
  series: [
    {
      data: [29.9, 71.5, 106.4, 129.2, 144.0],
      stack: 0
    },
    {
      data: [30, 176.0, 135.6, 148.5, 216.4],
      stack: 0
    },
    {
      data: [106.4, 129.2, 144.0, 29.9, 71.5],
      stack: 1
    },
    {
      data: [148.5, 216.4, 30, 176.0, 135.6],
      stack: 1
    }
  ]
}

const scatterChart = {
  chart: {
    type: 'scatter',
    zoomType: 'xy'
  },
  title: {
    text: 'Height Versus Weight of 507 Individuals by Gender'
  },
  subtitle: {
    text: 'Source: Heinz  2003'
  },
  xAxis: {
    title: {
      enabled: true,
      text: 'Height (cm)'
    },
    startOnTick: true,
    endOnTick: true,
    showLastLabel: true
  },
  yAxis: {
    title: {
      text: 'Weight (kg)'
    }
  },
  legend: {
    layout: 'vertical',
    align: 'left',
    verticalAlign: 'top',
    x: 100,
    y: 70,
    floating: true,
    borderWidth: 1
  },
  plotOptions: {
    scatter: {
      marker: {
        radius: 5,
        states: {
          hover: {
            enabled: true,
            lineColor: 'rgb(100,100,100)'
          }
        }
      },
      states: {
        hover: {
          marker: {
            enabled: false
          }
        }
      },
      tooltip: {
        headerFormat: '<b>{series.name}</b><br>',
        pointFormat: '{point.x} cm, {point.y} kg'
      }
    }
  },
  series: [{
    name: 'Female',
    color: 'rgba(223, 83, 83, .5)',
    data: [[161.2, 51.6], [167.5, 59.0], [159.5, 49.2], [157.0, 63.0], [155.8, 53.6],
      [170.0, 59.0], [159.1, 47.6], [166.0, 69.8], [176.2, 66.8], [160.2, 75.2],
      [172.5, 55.2], [170.9, 54.2], [172.9, 62.5], [153.4, 42.0], [160.0, 50.0],
      [147.2, 49.8], [168.2, 49.2], [175.0, 73.2], [157.0, 47.8], [167.6, 68.8],
      [159.5, 50.6], [175.0, 82.5], [166.8, 57.2], [176.5, 87.8], [170.2, 72.8],
      [174.0, 54.5], [173.0, 59.8], [179.9, 67.3], [170.5, 67.8], [160.0, 47.0],
      [154.4, 46.2], [162.0, 55.0], [176.5, 83.0], [160.0, 54.4], [152.0, 45.8],
      [162.1, 53.6], [170.0, 73.2], [160.2, 52.1], [161.3, 67.9], [166.4, 56.6],
      [168.9, 62.3], [163.8, 58.5], [167.6, 54.5], [160.0, 50.2], [161.3, 60.3],
      [167.6, 58.3], [165.1, 56.2], [160.0, 50.2], [170.0, 72.9], [157.5, 59.8],
      [167.6, 61.0], [160.7, 69.1], [163.2, 55.9], [152.4, 46.5], [157.5, 54.3],
      [168.3, 54.8], [180.3, 60.7], [165.5, 60.0], [165.0, 62.0], [164.5, 60.3],
      [156.0, 52.7], [160.0, 74.3], [163.0, 62.0], [165.7, 73.1], [161.0, 80.0],
      [162.0, 54.7], [166.0, 53.2], [174.0, 75.7], [172.7, 61.1], [167.6, 55.7],
      [151.1, 48.7], [164.5, 52.3], [163.5, 50.0], [152.0, 59.3], [169.0, 62.5],
      [164.0, 55.7], [161.2, 54.8], [155.0, 45.9], [170.0, 70.6], [176.2, 67.2],
      [170.0, 69.4], [162.5, 58.2], [170.3, 64.8], [164.1, 71.6], [169.5, 52.8],
      [163.2, 59.8], [154.5, 49.0], [159.8, 50.0], [173.2, 69.2], [170.0, 55.9],
      [161.4, 63.4], [169.0, 58.2], [166.2, 58.6], [159.4, 45.7], [162.5, 52.2],
      [159.0, 48.6], [162.8, 57.8], [159.0, 55.6], [179.8, 66.8], [162.9, 59.4],
      [161.0, 53.6], [151.1, 73.2], [168.2, 53.4], [168.9, 69.0], [173.2, 58.4],
      [171.8, 56.2], [178.0, 70.6], [164.3, 59.8], [163.0, 72.0], [168.5, 65.2],
      [166.8, 56.6], [172.7, 105.2], [163.5, 51.8], [169.4, 63.4], [167.8, 59.0],
      [159.5, 47.6], [167.6, 63.0], [161.2, 55.2], [160.0, 45.0], [163.2, 54.0],
      [162.2, 50.2], [161.3, 60.2], [149.5, 44.8], [157.5, 58.8], [163.2, 56.4],
      [172.7, 62.0], [155.0, 49.2], [156.5, 67.2], [164.0, 53.8], [160.9, 54.4],
      [162.8, 58.0], [167.0, 59.8], [160.0, 54.8], [160.0, 43.2], [168.9, 60.5],
      [158.2, 46.4], [156.0, 64.4], [160.0, 48.8], [167.1, 62.2], [158.0, 55.5],
      [167.6, 57.8], [156.0, 54.6], [162.1, 59.2], [173.4, 52.7], [159.8, 53.2],
      [170.5, 64.5], [159.2, 51.8], [157.5, 56.0], [161.3, 63.6], [162.6, 63.2],
      [160.0, 59.5], [168.9, 56.8], [165.1, 64.1], [162.6, 50.0], [165.1, 72.3],
      [166.4, 55.0], [160.0, 55.9], [152.4, 60.4], [170.2, 69.1], [162.6, 84.5],
      [170.2, 55.9], [158.8, 55.5], [172.7, 69.5], [167.6, 76.4], [162.6, 61.4],
      [167.6, 65.9], [156.2, 58.6], [175.2, 66.8], [172.1, 56.6], [162.6, 58.6],
      [160.0, 55.9], [165.1, 59.1], [182.9, 81.8], [166.4, 70.7], [165.1, 56.8],
      [177.8, 60.0], [165.1, 58.2], [175.3, 72.7], [154.9, 54.1], [158.8, 49.1],
      [172.7, 75.9], [168.9, 55.0], [161.3, 57.3], [167.6, 55.0], [165.1, 65.5],
      [175.3, 65.5], [157.5, 48.6], [163.8, 58.6], [167.6, 63.6], [165.1, 55.2],
      [165.1, 62.7], [168.9, 56.6], [162.6, 53.9], [164.5, 63.2], [176.5, 73.6],
      [168.9, 62.0], [175.3, 63.6], [159.4, 53.2], [160.0, 53.4], [170.2, 55.0],
      [162.6, 70.5], [167.6, 54.5], [162.6, 54.5], [160.7, 55.9], [160.0, 59.0],
      [157.5, 63.6], [162.6, 54.5], [152.4, 47.3], [170.2, 67.7], [165.1, 80.9],
      [172.7, 70.5], [165.1, 60.9], [170.2, 63.6], [170.2, 54.5], [170.2, 59.1],
      [161.3, 70.5], [167.6, 52.7], [167.6, 62.7], [165.1, 86.3], [162.6, 66.4],
      [152.4, 67.3], [168.9, 63.0], [170.2, 73.6], [175.2, 62.3], [175.2, 57.7],
      [160.0, 55.4], [165.1, 104.1], [174.0, 55.5], [170.2, 77.3], [160.0, 80.5],
      [167.6, 64.5], [167.6, 72.3], [167.6, 61.4], [154.9, 58.2], [162.6, 81.8],
      [175.3, 63.6], [171.4, 53.4], [157.5, 54.5], [165.1, 53.6], [160.0, 60.0],
      [174.0, 73.6], [162.6, 61.4], [174.0, 55.5], [162.6, 63.6], [161.3, 60.9],
      [156.2, 60.0], [149.9, 46.8], [169.5, 57.3], [160.0, 64.1], [175.3, 63.6],
      [169.5, 67.3], [160.0, 75.5], [172.7, 68.2], [162.6, 61.4], [157.5, 76.8],
      [176.5, 71.8], [164.4, 55.5], [160.7, 48.6], [174.0, 66.4], [163.8, 67.3]]

  }]
}

import { scroll } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll
import { Chart } from 'highcharts-vue'

export default {
  components: {
    highcharts: Chart
  },
  data () {
    return {
      tabs,
      filter: '',
      columns,
      data,
      slide: 'graph',
      colNames,
      options: {},
      loading: false,
      filteredRows: [],
      allVisibleValues: {},
      stackChart,
      scatterChart
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
    }
  },
  watch: {
    filter (val) {
      if (val === '') {
        for (const key in this.options) {
          for (const value in this.options[key][0]) {
            this.options[key][0][value].active = true
          }
        }
      }
    }
  },
  methods: {
    filterTable (rows) {
      this.allVisibleValues = {}
      if (this.filter === '') {
        this.filterOption()
        this.$forceUpdate()
        return rows
      } else {
        this.removedRows = []
        const filteredRows = []
        const aux = this.filter.toLowerCase()
        for (let i = 0; i < rows.length; i++) {
          for (const key in rows[i]) {
            if ((rows[i][key].toString().toLowerCase()).includes(aux)) {
              filteredRows.push(rows[i])
              for (const name in rows[i]) {
                if (!(name in this.allVisibleValues)) {
                  this.allVisibleValues[name] = [rows[i][name]]
                } else if (!this.allVisibleValues[name].includes(rows[i][name])) {
                  this.allVisibleValues[name].push(rows[i][name])
                }
              }
              break
            }
          }
        }
        this.filterOption()
        this.$forceUpdate()
        return filteredRows
      }
    },
    updateCheck ({ name, bool, item = null }) {
      if (item === null) {
        this.options[name][1] = bool
        for (const i in this.options[name][0]) {
          if (this.options[name][0][i].active) {
            this.options[name][0][i].bool = bool
          }
        }
      } else {
        this.options[name][0][item].bool = bool
        if (!bool) {
          this.options[name][1] = false
        }
      }
      if (bool && this.allEqual(this.options[name][0])) {
        this.options[name][1] = true
      }
      this.filteredRows = this.filterCol()
      // this.filterOption()
      this.$forceUpdate()
    },
    getColumns () {
      this.columns = []
      for (let index = 0; index < colNames.length; index++) {
        this.columns.push({
          name: colNames[index],
          label: colNames[index].charAt(0).toUpperCase() + colNames[index].slice(1),
          field: colNames[index],
          sortable: true,
          align: 'left',
          headerStyle: 'font-weight: bolder;'
        })
      }
    },
    allEqual (arr) {
      for (let i = 0; i < arr.length; i++) {
        if (!arr[i].bool) {
          return false
        }
      }
      return true
    },
    filterCol () {
      const filterCol = []
      const rows = this.data
      for (const i in rows) {
        let aux = true
        for (const key in rows[i]) {
          if (!(this.options[key][0][this.options[key][0].findIndex(x => x.column === rows[i][key])]).bool) {
            aux = false
            break
          }
        }
        if (aux) {
          filterCol.push(rows[i])
        }
      }
      return filterCol
    },
    filterOption () {
      for (const key in this.options) {
        for (const value in this.options[key][0]) {
          if (Object.keys(this.allVisibleValues).length !== 0) {
            if (this.allVisibleValues[key].includes(this.options[key][0][value].column)) {
              this.options[key][0][value].active = true
            } else {
              this.options[key][0][value].active = false
            }
          } else {
            this.options[key][0][value].active = true
          }
        }
      }
    },
    getData () {
      for (let i = 0; i < 10; i++) {
        const aux = {}
        for (const c in this.colNames) {
          const random = Math.floor(Math.random() * 50)
          aux[this.colNames[c]] = random
        }
        this.data.push(aux)
      }
      this.filteredRows = this.data
    },
    handleScroll () {
      const ele = document.getElementById('results') // You need to get your element here
      const target = getScrollTarget(ele)
      const offset = ele.offsetTop - ele.scrollHeight
      const duration = 0
      setScrollPosition(target, offset, duration)
    },
    getOptions () {
      this.options = {}
      this.data.forEach(element => {
        for (const key in element) {
          if (!(key in this.options)) {
            this.options[key] = [[{ column: element[key], bool: true, active: true }], true]
          } else if (!(this.options[key][0].filter(e => e.column === element[key]).length > 0)) {
            this.options[key][0].push({ column: element[key], bool: true, active: true })
          }
          this.options[key][0].sort((a, b) => (a.column > b.column ? 1 : -1))
        }
      })
    }
  },
  beforeMount () {
    this.getColumns()
    this.getData()
    this.getOptions()
  },
  mounted () {
    this.handleScroll()
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
.my-graph {
  width: 47%;
  height: 31%;
}
.my-img {
  border: 1px solid black;
}
</style>
