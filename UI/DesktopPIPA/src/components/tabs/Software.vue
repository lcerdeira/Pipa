<template>
  <div id="software" class="column full-width justify-start" :class="$q.screen.width < 1230 ? 'q-px-lg q-pb-lg' : 'q-px-xl q-pb-xl'">
    <div class="row justify-end q-pt-md q-gutter-x-md">
      <q-btn round color="primary" text-color="black" icon="arrow_back" size="md" @click="currentPage = 0">
        <q-tooltip anchor="center left" self="center right" :offset="[10, 10]">
          Go back
        </q-tooltip>
      </q-btn>
      <q-btn round color="blue" icon="replay" size="md" @click="restart">
        <q-tooltip>
          Reset
        </q-tooltip>
      </q-btn>
    </div>

    <div class="column justify-around full-height">
      <!-- Step 1: Choose Workflow -->
      <div class="items-center">
        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" style="backgroundColor: #FF3116">1</div>
          <div class="text-h6 text-weight-regular">Choose Workflow</div>
        </div>
        <div class="row q-gutter-x-md q-pb-lg">
          <q-card
            class="my-card my-option cursor-pointer q-pa-md"
            :class="[workflow === 'reads' ? 'painted' : '']"
            style="width: 48%"
            @click="workflow = 'reads'"
          >
            <div class="row items-center">
              <q-icon name="biotech" size="2em" :color="workflow === 'reads' ? 'white' : 'primary'" class="q-mr-md"/>
              <div>
                <div class="text-subtitle1 text-weight-bold" :class="workflow === 'reads' ? 'text-white' : ''">Full Pipeline (Raw Reads)</div>
                <div class="text-caption" :class="workflow === 'reads' ? 'text-white' : 'text-grey-7'">FASTQ files &rarr; Trimming &rarr; Assembly &rarr; Annotation</div>
              </div>
            </div>
          </q-card>
          <q-card
            class="my-card my-option cursor-pointer q-pa-md"
            :class="[workflow === 'annotation' ? 'painted' : '']"
            style="width: 48%"
            @click="workflow = 'annotation'"
          >
            <div class="row items-center">
              <q-icon name="find_in_page" size="2em" :color="workflow === 'annotation' ? 'white' : 'primary'" class="q-mr-md"/>
              <div>
                <div class="text-subtitle1 text-weight-bold" :class="workflow === 'annotation' ? 'text-white' : ''">Annotation Only</div>
                <div class="text-caption" :class="workflow === 'annotation' ? 'text-white' : 'text-grey-7'">FASTA assembly &rarr; Choose annotation tools</div>
              </div>
            </div>
          </q-card>
        </div>
      </div>

      <!-- Step 2A: Full Pipeline - Platform & Files -->
      <div v-if="workflow === 'reads'" class="items-center">
        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" style="backgroundColor: #FFBD08">2</div>
          <div class="text-h6 text-weight-regular">Choose Platforms &amp; Files</div>
        </div>
        <div class="row justify-between full-width q-pb-lg" :class="$q.screen.width < 550 ? '' : 'q-gutter-x-md'">
          <q-card
            class="my-card q-mb-lg my-option"
            :class="[program.isChecked ? 'painted' : '']"
            v-for="(program, i) in programs"
            :key="i + program"
            :style="{width: $q.screen.width < 550 ? '100%' : '30%'}"
          >
            <q-card-section class="my-card-section row items-center q-mt-md justify-between" horizontal>
              <div class="row items-center no-wrap">
                <div class="my-border">
                  <q-avatar :style="{margin:'0'}" class="shadow-2">
                    <img :src="'myIcons/logos/' + program.icon">
                  </q-avatar>
                </div>
                <div class="q-pl-md text-subtitle1">
                  <a :href="program.link" target="_blank" class="row no-wrap option-card-title" style="text-decoration: none" :class="[program.isChecked ? 'option-card-title-painted' : 'option-card-title']">
                    {{ program.name }}
                    <div class="column justify-start">
                      <q-icon size="12px" :color="program.isChecked ? 'white' : 'black'" name="eva-external-link-outline"/>
                    </div>
                  </a>
                </div>
              </div>
              <q-checkbox v-model="program.isChecked" :color="program.isChecked ? '' : 'white'"/>
            </q-card-section>
          </q-card>
        </div>
        <div class="row justify-between full-width q-pb-lg" :class="$q.screen.width < 550 ? '' : 'q-gutter-x-md'">
          <q-card
            class="my-file-card q-mb-lg my-option"
            v-for="(program, i) in programs"
            :key="'file'+i"
            :style="{width: $q.screen.width < 550 ? '100%' : '30%'}"
          >
            <div class="column my-file-picker">
              <div>
                <div class="filepicker-top">
                  <div v-if="i == 0">
                    <q-radio
                      v-for="(type, ind) in types_illumina"
                      :key="ind + type"
                      :val="type.val"
                      v-model="type_illumina"
                      :label="type.label"
                      color="secondary"
                      class="my-radio"
                      keep-color
                    />
                  </div>
                  <div v-if="i != 0">
                    <q-radio
                      v-for="(type, ind) in types_illumina.slice(0,1)"
                      :key="ind + type"
                      :val="type_aux"
                      v-model="type_aux"
                      :label="type.label"
                      color="secondary"
                      class="my-radio"
                      keep-color
                    />
                  </div>
                </div>
              </div>
              <q-file
                v-model="program.files"
                label="Choose files"
                filled
                multiple
                clearable
                :disable='!program.isChecked'
                class="q-pb-xs"
                style="height: 55px"
              >
                <template v-slot:prepend>
                  <q-icon name="cloud_upload" class="cloud-icon" @click.stop />
                </template>
              </q-file>
            </div>
          </q-card>
        </div>
      </div>

      <!-- Step 2B: Annotation Only - Upload FASTA & Choose Tools -->
      <div v-if="workflow === 'annotation'" class="items-center">
        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" style="backgroundColor: #FFBD08">2</div>
          <div class="text-h6 text-weight-regular">Upload Assembled Genome (FASTA)</div>
        </div>
        <div class="row q-pb-lg">
          <q-file
            v-model="assemblyFile"
            label="Select FASTA file (.fasta, .fa, .fna)"
            filled
            clearable
            accept=".fasta,.fa,.fna,.fsa"
            class="col-8"
            style="height: 55px"
          >
            <template v-slot:prepend>
              <q-icon name="cloud_upload" class="cloud-icon" @click.stop />
            </template>
          </q-file>
        </div>

        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" style="backgroundColor: #4CAF50">3</div>
          <div class="text-h6 text-weight-regular">Choose Annotation Tools</div>
        </div>
        <div class="row q-gutter-md q-pb-lg">
          <q-card
            v-for="(tool, i) in annotationTools"
            :key="'tool'+i"
            class="my-card q-pa-sm cursor-pointer"
            :class="[tool.enabled ? 'painted' : '']"
            style="min-width: 180px; width: 22%"
            @click="tool.enabled = !tool.enabled"
          >
            <q-card-section class="row items-center no-wrap q-pa-sm">
              <q-checkbox v-model="tool.enabled" :color="tool.enabled ? '' : 'white'" class="q-mr-xs"/>
              <div>
                <div class="text-subtitle2 text-weight-bold" :class="tool.enabled ? 'text-white' : ''">{{ tool.name }}</div>
                <div class="text-caption" :class="tool.enabled ? 'text-white' : 'text-grey-7'">{{ tool.description }}</div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Step 3: Sample Info & Submit -->
      <div class="full-width row full-height">
        <q-form
          ref="myform"
          class="q-gutter-y-md col-6"
        >
          <div class="row full-width q-pb-sm no-wrap items-center">
            <div class="num-square" :style="{backgroundColor: workflow === 'reads' ? '#4CAF50' : '#2196F3'}">{{ workflow === 'reads' ? 3 : 4 }}</div>
            <div class="text-h6 text-weight-regular">Sample Information</div>
          </div>
          <div>
            <div>Sample Name</div>
            <q-input
              filled
              v-model="info.sampleName"
              lazy-rules
              :rules="[ val => val && val.length > 0 || 'Please type something']"
            >
              <template v-if="info.sampleName != null" v-slot:append>
                <q-icon name="close" @click="info.sampleName = null" class="cursor-pointer" />
              </template>
            </q-input>
          </div>
          <div class="row">
            <div class="col-grow column">
              <div>Genus</div>
              <q-select
                filled
                v-model="info.genus"
                :options="filteredGenusOptions"
                use-input
                input-debounce="0"
                @filter="filterGenus"
                new-value-mode="add-unique"
                hint="Select or type a custom genus"
              />
            </div>
            <div class="q-mx-sm"></div>
            <div class="col-grow column">
              <div>Species</div>
              <q-select
                filled
                v-model="info.species"
                :options="filteredSpeciesOptions"
                use-input
                input-debounce="0"
                @filter="filterSpecies"
                new-value-mode="add-unique"
                hint="Select or type a custom species"
              />
            </div>
          </div>
          <div class="row" v-if="workflow === 'reads'">
            <div class="col-grow column">
              <div>Genome Size (for Nanopore assembly)</div>
              <q-input
                filled
                v-model="info.genomeSize"
                hint="e.g., 5m, 4.8m, 2.5m"
              />
            </div>
          </div>
          <div class="q-pb-md">
            <div>Description (Optional)</div>
            <q-input
              filled
              v-model="info.description"
              class="q-ma-none"
            >
              <template v-if="info.description != null" v-slot:append>
                <q-icon name="close" @click="info.description = null" class="cursor-pointer" />
              </template>
            </q-input>
          </div>
          <q-btn
            class="my-button full-width"
            icon-right="send"
            :label="submitting ? 'Submitting...' : 'Submit'"
            :loading="submitting"
            :disable="submitting"
            @click="onSubmit"
          />
        </q-form>
        <div class="col-6 q-pl-xl col-grow column">
          <q-list bordered padding class="rounded-borders col-grow">
            <q-item-label header class="text-weight-bold q-mt-xs row justify-between items-center">
              <div>Previous Jobs Run</div>
              <q-chip class="text-black q-ma-none" style="height: 20px">{{previousJobs.length}}</q-chip>
            </q-item-label>
            <div v-for="(job, i) in previousJobs" :key="'jobs'+i">
              <q-separator/>
              <q-item clickable v-ripple>
                <q-item-section>
                  <q-item-label lines="1">Job {{ job.jobId }}</q-item-label>
                  <q-item-label caption>{{ job.date }} - {{ job.status }}</q-item-label>
                </q-item-section>
              </q-item>
            </div>
          </q-list>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

const programs = [
  {
    name: 'Illumina',
    description: 'Short-read sequencing platform for high-throughput genomic analysis.',
    isChecked: false,
    files: null,
    icon: 'illumina.jpg',
    link: 'https://www.illumina.com/'
  },
  {
    name: 'Nanopore',
    description: 'Long-read sequencing technology for real-time, portable genomic analysis.',
    isChecked: false,
    files: null,
    icon: 'nanopore.jpg',
    link: 'https://nanoporetech.com/'
  },
  {
    name: 'Pacbio',
    description: 'Long-read sequencing platform with high accuracy for comprehensive genome assembly.',
    isChecked: false,
    files: null,
    icon: 'pacbio.png',
    link: 'https://www.pacb.com/'
  }
]

const defaultAnnotationTools = [
  { name: 'Prokka', key: 'prokka', enabled: true, description: 'Gene annotation' },
  { name: 'MLST', key: 'mlst', enabled: true, description: 'Sequence typing' },
  { name: 'Barrnap', key: 'barrnap', enabled: true, description: 'Ribosomal RNA' },
  { name: 'Abricate', key: 'abricate', enabled: true, description: 'Resistance genes' },
  { name: 'AMRFinderPlus', key: 'amrfinderplus', enabled: false, description: 'AMR detection (NCBI)' },
  { name: 'PlasmidFinder', key: 'plasmidfinder', enabled: false, description: 'Plasmid replicons' },
  { name: 'MOB-suite', key: 'mobsuite', enabled: false, description: 'Plasmid typing' },
  { name: 'Phigaro', key: 'phigaro', enabled: false, description: 'Phage detection' },
  { name: 'CRISPRCasFinder', key: 'crisprcasfinder', enabled: false, description: 'CRISPR arrays' },
  { name: 'tRNAscan-SE', key: 'trnascan', enabled: false, description: 'tRNA prediction' },
  { name: 'Kleborate', key: 'kleborate', enabled: false, description: 'Klebsiella typing' },
  { name: 'KOFAM', key: 'kofam', enabled: false, description: 'KEGG annotation' }
]

const genusItems = [
  'Acinetobacter', 'Bacillus', 'Burkholderia', 'Campylobacter', 'Clostridioides',
  'Clostridium', 'Corynebacterium', 'Enterobacter', 'Enterococcus', 'Escherichia',
  'Haemophilus', 'Helicobacter', 'Klebsiella', 'Legionella', 'Listeria',
  'Mycobacterium', 'Neisseria', 'Pseudomonas', 'Salmonella', 'Serratia',
  'Shigella', 'Staphylococcus', 'Streptococcus', 'Vibrio', 'Yersinia'
]

const speciesItems = [
  'aeruginosa', 'anthracis', 'aureus', 'baumannii', 'cereus', 'coli',
  'difficile', 'enterica', 'faecalis', 'faecium', 'influenzae',
  'monocytogenes', 'pneumoniae', 'pyogenes', 'tuberculosis', 'typhimurium'
]

import { scroll, openURL } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll

export default {
  data () {
    return {
      workflow: 'annotation',
      programs,
      assemblyFile: null,
      annotationTools: defaultAnnotationTools.map(t => ({ ...t })),
      files: null,
      info: {
        sampleName: 'My_Sample1',
        genus: genusItems[9], // Escherichia
        species: speciesItems[5], // coli
        genomeSize: '5m',
        description: null
      },
      types_illumina: [
        { val: 0, label: 'Single-end' },
        { val: 1, label: 'Paired-end' }
      ],
      type_illumina: 0,
      type_aux: 0,
      genusItems,
      speciesItems,
      filteredGenusOptions: genusItems,
      filteredSpeciesOptions: speciesItems,
      submitting: false
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
    previousJobs () {
      return this.$store.state.pipa.previousJobs
    }
  },
  methods: {
    openURL,
    filterGenus (val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.filteredGenusOptions = genusItems.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    },
    filterSpecies (val, update) {
      update(() => {
        const needle = val.toLowerCase()
        this.filteredSpeciesOptions = speciesItems.filter(v => v.toLowerCase().indexOf(needle) > -1)
      })
    },
    restart () {
      this.workflow = 'annotation'
      this.assemblyFile = null
      this.annotationTools = defaultAnnotationTools.map(t => ({ ...t }))
      this.info = {
        sampleName: 'My_Sample1',
        genus: genusItems[9],
        species: speciesItems[5],
        genomeSize: '5m',
        description: null
      }
      this.type_illumina = 0
      for (let i = 0; i < this.programs.length; i++) {
        this.programs[i].files = null
        this.programs[i].isChecked = false
      }
      this.$store.commit('pipa/resetPipeline')
    },
    async onSubmit () {
      const success = await this.$refs.myform.validate()
      if (!success) return

      if (this.workflow === 'reads') {
        const hasFiles = this.programs[0].files || this.programs[1].files || this.programs[2].files
        if (!hasFiles) {
          this.$q.notify({ color: 'red-5', textColor: 'white', icon: 'warning', message: 'Please choose at least one platform and upload files' })
          return
        }
      } else {
        if (!this.assemblyFile) {
          this.$q.notify({ color: 'red-5', textColor: 'white', icon: 'warning', message: 'Please select a FASTA file' })
          return
        }
        const enabledTools = this.annotationTools.filter(t => t.enabled)
        if (enabledTools.length === 0) {
          this.$q.notify({ color: 'red-5', textColor: 'white', icon: 'warning', message: 'Please select at least one annotation tool' })
          return
        }
      }

      this.submitting = true
      try {
        // Step 1: Upload files
        if (this.workflow === 'reads') {
          await this.$store.dispatch('pipa/uploadFiles', {
            files: {
              illumina: this.programs[0].files,
              nanopore: this.programs[1].files,
              pacbio: this.programs[2].files
            },
            illuminaType: this.type_illumina
          })
        } else {
          await this.$store.dispatch('pipa/uploadFiles', {
            files: { illumina: [this.assemblyFile] },
            illuminaType: 0
          })
        }

        // Step 2: Start pipeline
        const enabledToolKeys = this.annotationTools.filter(t => t.enabled).map(t => t.key)
        await this.$store.dispatch('pipa/startPipeline', {
          genus: this.info.genus,
          species: this.info.species,
          sampleName: this.info.sampleName,
          genomeSize: this.info.genomeSize,
          inputType: this.workflow === 'annotation' ? 'assembly' : 'reads',
          tools: enabledToolKeys
        })

        this.$q.notify({ color: 'green-5', textColor: 'white', icon: 'check', message: 'Pipeline started successfully!' })
        this.currentPage = 2
      } catch (error) {
        console.error('Submission failed:', error)
        this.$q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Failed to start pipeline: ' + (error.response ? error.response.data.error : error.message)
        })
      } finally {
        this.submitting = false
      }
    },
    handleScroll () {
      const ele = document.getElementById('software')
      const target = getScrollTarget(ele)
      const offset = ele.offsetTop - ele.scrollHeight
      const duration = 0
      setScrollPosition(target, offset, duration)
    }
  },
  mounted () {
    this.handleScroll()
  }
}
</script>

<style lang="scss">
  .num-square{
    height: 30px;
    width: 30px;
    margin-right: 12px;
    color: white;
    font-size: 16px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 8px;
    font-weight: 700;
  }
  .option-card-title{
    font-weight: 600;
    color: #0D1B2A;
  }
  .option-card-subtitle-painted, .option-card-title-painted{
    color: white;
  }
  .my-card{
    background-color: #f8f9fa;
    border-radius: 14px;
    border: 1px solid #e8e8e8;
    transition: all 0.3s ease;
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(13, 27, 42, 0.08);
    }
  }
  .my-option{
    min-width: 180px;
  }
  .my-button{
    height: 50px;
    background: linear-gradient(135deg, #00B4D8, #52B788) !important;
    color: white;
    border-radius: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    box-shadow: 0 4px 15px rgba(0, 180, 216, 0.3);
    transition: all 0.3s ease;
    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(0, 180, 216, 0.4);
    }
  }
  .painted{
    border-color: #52B788;
    background: linear-gradient(135deg, #1B4332, #2D6A4F);
    box-shadow: 0 4px 15px rgba(82, 183, 136, 0.3);
  }
  .my-card-section{
    padding: 0 16px 16px 16px;
  }
  .q-file{
    background-color: white;
  }
  .q-radio{
    color: white;
  }
  .my-radio{
    width: 50%;
    justify-content: center;
  }
  .cloud-icon{
    color: #415A77;
  }
  .filepicker-top{
    background: linear-gradient(135deg, #0D1B2A, #1B4332);
    border-radius: 14px 14px 0 0;
  }
  .my-border{
    border-radius: 50%;
    color: rgba(0, 0, 0, 0.2);
  }
  .my-file-card, .filepicker-top{
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }
</style>
