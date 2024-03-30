async function candidateSelectJob(jobId){
  await fetch(`/api/get_job_details/${jobId}`)
  .then(response => response.json())
  .then(data => {
    document.getElementById('selected_job_title').textContent = data.title
    document.getElementById('selected_job_description').textContent = data.description
    document.getElementById('selected_job_closing_date').textContent = data.closing_date
    document.getElementById('selected_job_type').textContent = data.job_type
    document.getElementById('selected_job_company').textContent = data.company
    document.getElementById('selected_job_location').textContent = data.location
    document.getElementById('selected_job_experience_type').textContent = data.experience

    // Qualifications
    const qualificationsContainer = document.getElementById('qualifications')
    while (qualificationsContainer.firstChild){
      qualificationsContainer.removeChild(qualificationsContainer.firstChild)
    }

    if(data.qualifications == null){
      const tableItem = document.createElement('dd');
        tableItem.className = "text-sm leading-6 text-gray-500 rounded-md bg-gray-200 px-2 py-1 text-wrap mb-2 mr-2"
        tableItem.textContent = 'No requirements'
        qualificationsContainer.appendChild(tableItem)
    }
    else{
      data.qualifications.forEach(q => {
        const tableItem = document.createElement('dd');
        tableItem.className = "text-sm leading-6 text-gray-500 rounded-md bg-gray-200 px-2 py-1 text-wrap mb-2 mr-2"
        tableItem.textContent = q;
        qualificationsContainer.appendChild(tableItem)
      });
    }

    // Skills
    const skillsContainer = document.getElementById('skills')
    while (skillsContainer.firstChild){
      skillsContainer.removeChild(skillsContainer.firstChild)
    }

    if(data.skills == null){
      const tableItem = document.createElement('dd');
        tableItem.className = "text-sm leading-6 text-gray-700 rounded-md bg-indigo-200 px-2 py-1 text-nowrap mb-2 mr-2"
        tableItem.textContent = 'No requirements'
        skillsContainer.appendChild(tableItem)
    }
    else{
      data.skills.forEach(s => {
        const tableItem = document.createElement('dd');
        tableItem.className = "text-sm leading-6 text-gray-700 rounded-md bg-indigo-200 px-2 py-1 text-nowrap mb-2 mr-2"
        tableItem.textContent = s;
        skillsContainer.appendChild(tableItem)
      });
    }
  })
}