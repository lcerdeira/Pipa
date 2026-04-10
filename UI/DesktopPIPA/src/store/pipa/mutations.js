export const changePage = (state, page) => {
  state.currentPage = page
}

export const setJobId = (state, jobId) => {
  state.jobId = jobId
}

export const setPipelineStatus = (state, status) => {
  state.pipelineStatus = status
}

export const setPipelineStage = (state, stage) => {
  state.pipelineStage = stage
}

export const setPipelineMessage = (state, message) => {
  state.pipelineMessage = message
}

export const setPipelineProgress = (state, progress) => {
  state.pipelineProgress = progress
}

export const setResults = (state, results) => {
  state.results = results
}

export const setResultFiles = (state, files) => {
  state.resultFiles = files
}

export const setErrors = (state, errors) => {
  state.errors = errors
}

export const addPreviousJob = (state, job) => {
  state.previousJobs.unshift(job)
}

export const resetPipeline = (state) => {
  state.jobId = null
  state.pipelineStatus = null
  state.pipelineStage = null
  state.pipelineMessage = ''
  state.pipelineProgress = 0
  state.results = null
  state.resultFiles = []
  state.errors = []
}
