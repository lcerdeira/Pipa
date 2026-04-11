<template>
  <div id="about">
    <!-- Hero Section -->
    <div class="hero gradient-hero q-pa-xl">
      <div class="row items-center justify-between" style="min-height: 400px">
        <div class="col-12 col-md-6">
          <div class="hero-badge q-mb-md">
            <q-icon name="biotech" size="16px" class="q-mr-xs"/>
            Open-Source Bioinformatics
          </div>
          <h1 class="hero-title q-ma-none">
            Microbial<br/>
            <span class="hero-highlight">Genomic Analysis</span>
          </h1>
          <p class="hero-subtitle q-mt-md">
            From raw reads to annotated genomes in minutes.
            Supports Illumina, Nanopore, and PacBio with 12+ analysis tools.
          </p>
          <div class="row q-gutter-md q-mt-lg">
            <q-btn
              class="glow-btn"
              label="Get Started"
              icon-right="arrow_forward"
              size="lg"
              no-caps
              padding="12px 32px"
              @click="currentPage = 1"
            />
            <q-btn
              flat
              label="Documentation"
              icon="menu_book"
              size="lg"
              no-caps
              padding="12px 24px"
              class="text-white"
              style="border: 1px solid rgba(255,255,255,0.2); border-radius: 12px"
              @click="openExternal('https://pipa-tool.readthedocs.io/en/latest/')"
            />
          </div>
        </div>
        <div class="col-12 col-md-5 q-mt-lg-md">
          <!-- Pipeline Flow Diagram -->
          <div class="pipeline-diagram">
            <div class="pipeline-node" v-for="(step, i) in pipelineSteps" :key="'step'+i"
              :style="{ animationDelay: (i * 0.2) + 's' }"
            >
              <div class="pipeline-icon-wrap">
                <q-icon :name="step.icon" size="28px" color="white"/>
              </div>
              <div class="pipeline-label">{{ step.label }}</div>
              <div class="pipeline-tools">{{ step.tools }}</div>
              <div v-if="i < pipelineSteps.length - 1" class="pipeline-arrow">
                <q-icon name="south" size="20px" style="color: rgba(82,183,136,0.6)"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Features Section -->
    <div class="features-section q-pa-xl">
      <div class="text-center q-mb-xl">
        <div class="section-label">WHY PIPA</div>
        <h2 class="section-title">Built for Researchers</h2>
      </div>
      <div class="row q-gutter-lg justify-center">
        <div class="col-12 col-sm-5 col-md-3" v-for="(feature, i) in features" :key="'feat'+i">
          <div class="feature-card text-center" :style="{ animationDelay: (i * 0.1) + 's' }">
            <div class="feature-icon-wrap q-mb-md">
              <q-icon :name="feature.icon" size="32px" :style="{ color: feature.color }"/>
            </div>
            <div class="text-h6 text-weight-bold q-mb-sm">{{ feature.title }}</div>
            <div class="text-body2 text-grey-7">{{ feature.description }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Workflows Section -->
    <div class="workflows-section q-pa-xl" style="background: #f0f4f8">
      <div class="text-center q-mb-xl">
        <div class="section-label">TWO WORKFLOWS</div>
        <h2 class="section-title">Choose Your Path</h2>
      </div>
      <div class="row q-gutter-lg justify-center">
        <div class="col-12 col-md-5">
          <q-card class="workflow-card" flat>
            <q-card-section class="q-pa-lg">
              <div class="row items-center q-mb-md">
                <div class="workflow-icon gradient-hero">
                  <q-icon name="biotech" size="28px" color="white"/>
                </div>
                <div class="q-ml-md">
                  <div class="text-h6 text-weight-bold">Full Pipeline</div>
                  <div class="text-caption text-grey-7">Raw reads to annotation</div>
                </div>
              </div>
              <q-separator class="q-my-md"/>
              <div class="text-body2 q-mb-md">Upload FASTQ files and PIPA handles everything:</div>
              <div class="workflow-steps">
                <div class="workflow-step" v-for="(s, i) in ['Quality Trimming', 'Genome Assembly', 'Gene Annotation', 'Report Generation']" :key="i">
                  <q-icon name="check_circle" color="positive" size="18px" class="q-mr-sm"/>
                  <span>{{ s }}</span>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
        <div class="col-12 col-md-5">
          <q-card class="workflow-card" flat>
            <q-card-section class="q-pa-lg">
              <div class="row items-center q-mb-md">
                <div class="workflow-icon gradient-accent">
                  <q-icon name="find_in_page" size="28px" color="white"/>
                </div>
                <div class="q-ml-md">
                  <div class="text-h6 text-weight-bold">Annotation Only</div>
                  <div class="text-caption text-grey-7">Assembled genome to results</div>
                </div>
              </div>
              <q-separator class="q-my-md"/>
              <div class="text-body2 q-mb-md">Upload a FASTA assembly and pick your tools:</div>
              <div class="workflow-steps">
                <div class="workflow-step" v-for="(s, i) in ['Prokka, MLST, Barrnap, Abricate', 'AMRFinderPlus, PlasmidFinder', 'CRISPRCasFinder, tRNAscan-SE', '12+ tools available']" :key="i">
                  <q-icon name="check_circle" color="info" size="18px" class="q-mr-sm"/>
                  <span>{{ s }}</span>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </div>

    <!-- Stats Section -->
    <div class="stats-section q-pa-xl gradient-hero">
      <div class="row justify-center q-gutter-xl">
        <div class="stat-item text-center" v-for="(stat, i) in stats" :key="'stat'+i">
          <div class="stat-number">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="cta-section q-pa-xl text-center">
      <h2 class="section-title q-mb-md">Ready to Analyze?</h2>
      <p class="text-body1 text-grey-7 q-mb-lg" style="max-width: 500px; margin: 0 auto">
        Upload your sequencing data and get annotated results in minutes.
      </p>
      <q-btn
        class="glow-btn"
        label="Start Analysis"
        icon-right="arrow_forward"
        size="xl"
        no-caps
        padding="16px 48px"
        @click="currentPage = 1"
      />
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      pipelineSteps: [
        { icon: 'content_cut', label: 'Trimming', tools: 'Trim Galore, Porechop' },
        { icon: 'hub', label: 'Assembly', tools: 'SPAdes, Flye, Canu' },
        { icon: 'search', label: 'Annotation', tools: 'Prokka, MLST, Abricate' },
        { icon: 'assessment', label: 'Report', tools: 'KEGG-decoder' }
      ],
      features: [
        { icon: 'speed', title: 'Fast', description: 'Parallel processing with optimized tools for rapid results', color: '#00B4D8' },
        { icon: 'tune', title: 'Flexible', description: 'Choose exactly which tools to run. Support for any bacterial genome', color: '#52B788' },
        { icon: 'lock_open', title: 'Open Source', description: 'Free forever. GPL-3.0 licensed. Community-driven development', color: '#F4A261' },
        { icon: 'devices', title: 'Cross-Platform', description: 'Desktop apps for Windows, macOS, Linux. Web SPA. Docker. API', color: '#E63946' }
      ],
      stats: [
        { value: '12+', label: 'Analysis Tools' },
        { value: '3', label: 'Sequencing Platforms' },
        { value: '4', label: 'OS Supported' },
        { value: 'GPL-3', label: 'Open License' }
      ]
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
  methods: {
    openExternal (url) {
      if (window.__TAURI__) {
        window.__TAURI__.shell.open(url)
      } else {
        window.open(url, '_blank')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
// Hero
.hero {
  color: white;
  min-height: 500px;
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(82, 183, 136, 0.15);
  border: 1px solid rgba(82, 183, 136, 0.3);
  color: #52B788;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.hero-title {
  font-size: 52px;
  font-weight: 700;
  line-height: 1.1;
  letter-spacing: -1px;
}

.hero-highlight {
  background: linear-gradient(135deg, #00B4D8, #52B788);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 18px;
  color: rgba(224, 225, 221, 0.8);
  line-height: 1.6;
  max-width: 480px;
}

// Pipeline diagram
.pipeline-diagram {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.pipeline-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeInUp 0.6s ease forwards;
  opacity: 0;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.pipeline-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(0, 180, 216, 0.3), rgba(82, 183, 136, 0.3));
  border: 1px solid rgba(82, 183, 136, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.pipeline-label {
  font-weight: 700;
  font-size: 14px;
  color: white;
  margin-top: 6px;
}

.pipeline-tools {
  font-size: 11px;
  color: rgba(224, 225, 221, 0.6);
}

.pipeline-arrow {
  margin: 2px 0;
}

// Features
.features-section {
  background: white;
}

.section-label {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #52B788;
  margin-bottom: 8px;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #0D1B2A;
  margin: 0;
}

.feature-icon-wrap {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: #f0f4f8;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

// Workflows
.workflow-card {
  border-radius: 16px;
  border: 1px solid #e8e8e8;
  transition: all 0.3s ease;
  height: 100%;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(13, 27, 42, 0.1);
  }
}

.workflow-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.workflow-steps {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.workflow-step {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #415A77;
}

// Stats
.stats-section {
  color: white;
}

.stat-item {
  min-width: 120px;
}

.stat-number {
  font-size: 42px;
  font-weight: 700;
  background: linear-gradient(135deg, #00B4D8, #52B788);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 14px;
  color: rgba(224, 225, 221, 0.7);
  margin-top: 4px;
}

// CTA
.cta-section {
  background: white;
  padding-bottom: 60px;
}
</style>
