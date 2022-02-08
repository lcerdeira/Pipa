<template>
  <div class="column full-width">
    <div class="column full-height no-wrap full-width">
      <div class="row q-pb-md justify-between q-pt-xl">
        <div class="row" :class="$q.platform.is.mobile ? 'justify-between full-width' : ''">
          <h4 class="q-ma-none">Results</h4>
          <q-btn v-if="$q.platform.is.mobile" class="my-btn" label="Download" style="width: 120px"/>
          <q-btn-dropdown v-if="!$q.platform.is.mobile" unelevated outline color="white" class="text-black q-ml-md" :label="slide">
            <q-list>
              <q-item clickable v-close-popup v-for="(tab, index) in tabs" :key="index+'tab'" @click="slide = tab.name">
                <q-item-section>
                  <q-item-label>{{tab.label}}</q-item-label>
                </q-item-section>
              </q-item>
            </q-list>
          </q-btn-dropdown>
        </div>
        <q-btn v-if="!$q.platform.is.mobile" class="my-btn" label="Download" style="width: 150px"/>
      </div>
      <q-btn-dropdown v-if="$q.platform.is.mobile" unelevated outline color="white" class="text-black q-mb-md" :label="slide">
        <q-list>
          <q-item clickable v-close-popup v-for="(tab, index) in tabs" :key="index+'tab'" @click="slide = tab.name">
            <q-item-section>
              <q-item-label>{{tab.label}}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
      </q-btn-dropdown>
      <div class="full-width">
        <div class="my-tabs full-width bg-black" style="height: 35px"></div>
        <q-tab-panels
          v-model="slide"
          animated
          class="col-grow my-panel full-width"
          :style="{minHeight: ($q.screen.height - 180) + 'px'}"
        >
          <q-tab-panel
            :name="tabs[0].name"
            class="q-pa-none"
            :style="{height: ($q.screen.height - 180) + 'px'}"
          >
            <div class="column full-height full-width">
              <div class="full-height full-width">
                <q-table
                  :data="data"
                  :columns="columns"
                  row-key="name"
                  :filter="filter"
                  class="full-height"
                  separator="horizontal"
                >
                  <template v-slot:top-left>
                    <q-input
                      dense
                      debounce="300"
                      v-model="filter"
                      placeholder="Search"
                    >
                      <template v-slot:append>
                        <q-icon name="search" />
                      </template>
                    </q-input>
                  </template>
                </q-table>
              </div>
            </div>
          </q-tab-panel>

          <q-tab-panel
            :name="tabs[1].name"
            class="q-pa-none"
            :style="{height: ($q.screen.height - 180) + 'px'}"
          >
            <div class="row full-height">
              <div class="col-grow q-pa-lg column">
                <div class="col-grow">
                  <q-img
                    src="graphs/graph1.jpg"
                    spinner-color="white"
                    class="full-width full-height my-img"
                  />
                </div>
              </div>
              <div class="col-grow q-pa-lg column">
                <div class="row col-grow">
                  <div
                    v-for="(graph, i) in graphs"
                    :key="graph + i"
                    class="my-graph"
                  >
                    <q-img
                      :src="'graphs/' + graph.image"
                      spinner-color="white"
                      contain
                      class="full-height my-img"
                    />
                  </div>
                </div>
              </div>
            </div>
          </q-tab-panel>

          <q-tab-panel
            :name="tabs[2].name"
            class="full-width full-height"
            :style="{height: ($q.screen.height - 180) + 'px'}"
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

const graphs = [
  {
    image: 'graph2.png'
  },
  {
    image: 'graph3.png'
  },
  {
    image: 'graph4.jpg'
  },
  {
    image: 'graph5.png'
  },
  {
    image: 'graph6.png'
  },
  {
    image: 'graph7.jpg'
  }
]

const columns = [
  {
    name: 'desc',
    label: 'Dessert (100g serving)',
    align: 'left',
    field: 'desc',
    sortable: true
  },
  { name: 'calories', label: 'Calories', field: 'calories', sortable: true },
  { name: 'fat', label: 'Fat (g)', field: 'fat', sortable: true },
  { name: 'carbs', label: 'Carbs (g)', field: 'carbs', sortable: true }
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

const data = []

export default {
  data () {
    return {
      tabs,
      graphs,
      filter: '',
      columns,
      data,
      slide: 'table',
      colNames
    }
  },
  methods: {
    getColumns () {
      this.columns = []
      for (let index = 0; index < colNames.length; index++) {
        this.columns.push({
          name: colNames[index],
          label: colNames[index].charAt(0).toUpperCase() + colNames[index].slice(1),
          field: colNames[index],
          sortable: true,
          headerStyle: 'font-weight: bolder;'
        })
      }
    }
  },
  beforeMount () {
    this.getColumns()
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
