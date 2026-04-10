export function isRunning (state) {
  return state.pipelineStatus === 'running' || state.pipelineStatus === 'uploading'
}

export function isCompleted (state) {
  return state.pipelineStatus === 'completed' || state.pipelineStatus === 'completed_with_errors'
}

export function hasErrors (state) {
  return state.errors && state.errors.length > 0
}

export function downloadUrl (state) {
  if (!state.jobId) return null
  return `${state.apiBaseUrl}/results/${state.jobId}/files`
}
