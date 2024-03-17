async function setJobStatus(recruiter_id, job_id) {
  await fetch(`/api/change_job_status/${job_id}`)
  window.location.href = `/recruiter/${recruiter_id}/dashboard/`
}