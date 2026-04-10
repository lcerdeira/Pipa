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
      <div
        v-for="(option, index) in options"
        :key="index + option"
        class="items-center"
      >
        <div class="row full-width q-pb-lg no-wrap items-center">
          <div class="num-square" :style="{backgroundColor: option.color}">{{ index + 1 }}</div>
          <div class="text-h6 text-weight-regular">{{ option.title }}</div>
        </div>
        <div
          v-if="index == 0"
          class="row justify-between full-width"
          style="padding-bottom: 55px"
          :class="$q.screen.width < 550 ? '' : 'q-gutter-x-md'"
        >
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
        <q-form
          v-if="index == 1"
          class="row justify-between full-width"
          style="padding-bottom: 55px"
          :class="$q.screen.width < 550 ? '' : 'q-gutter-x-md'"
        >
          <q-card
            class="my-file-card q-mb-lg my-option"
            v-for="(program, i) in programs"
            :key="i + program"
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
                q-file
                v-model="program.files"
                label="Choose files"
                filled
                multiple
                clearable
                text-center
                :disable='!program.isChecked'
                lazy-rules
                class="q-pb-xs"
                style="height: 55px"
                :rules="[ val => val != null || 'Please enter file']"
              >
                <template v-slot:prepend>
                  <q-icon name="cloud_upload" class="cloud-icon" @click.stop />
                </template>
                <template v-slot:append>
                  <q-icon
                    name="search"
                    @click.stop="model = null"
                    class="cursor-pointer"
                  />
                </template>
              </q-file>
            </div>
          </q-card>
        </q-form>
      </div>
      <div class="full-width row full-height">
        <q-form
          ref="myform"
          class="q-gutter-y-md col-6"
        >
          <div>
            <div>Metadata File (Optional)</div>
            <div class="row items-center">
              <q-file
                filled
                clearable
                v-model="info.metadata"
                class="q-ma-none col-grow"
                label="Metadata file: browser file"
              >
                <template v-slot:prepend>
                  <q-icon name="cloud_upload" class="cloud-icon" @click.stop />
                </template>
                <template v-slot:append>
                  <q-icon
                    name="search"
                    @click.stop="model = null"
                    class="cursor-pointer"
                  />
                </template>
              </q-file>
              <div class="q-pl-md">
                <q-btn round color="blue" icon="download" size="md" @click="openURL('')">
                  <q-tooltip>
                    Download template format
                  </q-tooltip>
                </q-btn>
              </div>
            </div>
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
          <div class="row">
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
              lazy-rules
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

const options = [
  {
    title: 'Choose Sequence Platforms',
    color: '#FF3116'
  },
  {
    title: 'Choose Files',
    color: '#FFBD08'
  }
]

import { scroll, openURL } from 'quasar'
const { getScrollTarget, setScrollPosition } = scroll

export default {
  data () {
    return {
      options,
      programs,
      files: null,
      info: {
        metadata: null,
        sampleName: 'My_Sample1',
        genus: genusItems[12], // Klebsiella
        species: speciesItems[11], // pneumoniae
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
    checkBox (index) {
      this.programs[index].isChecked = !this.programs[index].isChecked
    },
    getResults () {
      var files = [null, null, null]
      for (let index = 0; index < this.programs.length; index++) {
        if (this.programs[index].files !== null) {
          files[index] = this.programs[index].files
        }
      }
      return files
    },
    restart () {
      this.info = {
        metadata: null,
        sampleName: 'My_Sample1',
        genus: genusItems[12],
        species: speciesItems[11],
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
      const fileData = {
        illumina: this.programs[0].files,
        nanopore: this.programs[1].files,
        pacbio: this.programs[2].files
      }
      const hasFiles = fileData.illumina || fileData.nanopore || fileData.pacbio

      const success = await this.$refs.myform.validate()
      if (!success) return

      if (!hasFiles) {
        this.$q.notify({
          color: 'red-5',
          textColor: 'white',
          icon: 'warning',
          message: 'Please choose at least one sequence platform'
        })
        return
      }

      this.submitting = true
      try {
        // Step 1: Upload files
        await this.$store.dispatch('pipa/uploadFiles', {
          files: fileData,
          illuminaType: this.type_illumina
        })

        // Step 2: Start pipeline
        await this.$store.dispatch('pipa/startPipeline', {
          genus: this.info.genus,
          species: this.info.species,
          sampleName: this.info.sampleName,
          genomeSize: this.info.genomeSize
        })

        this.$q.notify({
          color: 'green-5',
          textColor: 'white',
          icon: 'check',
          message: 'Pipeline started successfully!'
        })

        // Navigate to Results page
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
    height: 25px;
    width: 25px;
    margin-right: 10px;
    color: $font;
    font-size: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .option-card-title{
    color: $primary;
    font-weight: 600;
    color: black;
  }
  .option-card-subtitle{
    color: $primary;
    font-weight: 500;
    color: black;
  }
  .option-card-subtitle-painted, .option-card-title-painted{
    color: white;
  }
  .my-card{
    background-color: #F2F2F2;
  }
  .my-option{
    min-width: 225px;
  }
  .my-button{
    height: 50px;
    background-color: $terciary;
    color: white;
    width: 30%;
  }
  .make-hidden{
    visibility: hidden;
  }
  .make-visible{
    visibility: visible;
  }
  .painted{
    border-color: $accent;
    background-color: $accent;
  }
  .my-card-section{
    padding: 0 16px 16px 16px;
  }
  .btn-program{
    text-transform: none;
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
    color: #616161;
  }
  .filepicker-top{
    background-color: #616161;
  }
  .my-border{
    border-radius: 50%;
    color: rgba(0, 0, 0, 0.2);
  }
  .my-file-card, .filepicker-top{
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
  }
  .btn-sp{
    font-size: 14px;
    color: rgba(0, 0, 0, 0.5);
  }
</style>
