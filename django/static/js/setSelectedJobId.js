async function setSelectedJobId(jobId) {
  await fetch(`/api/get_job_details/${jobId}`)
  .then(response => response.json())
  .then(data => {
    const currentHref = document.getElementById('selected_job_link').href
    const splitUrl = currentHref.split('/')
    const baseUrl = splitUrl[0] + '//' + splitUrl[2] + '/' + splitUrl[3] + '/' + splitUrl[4] + '/'
    document.getElementById('selected_job_link').href = baseUrl + data.id

    document.getElementById('selected_job_company').textContent = data.company
    document.getElementById('selected_job_title').textContent = data.title
    document.getElementById('selected_job_location').textContent = data.location

    job_status = document.getElementById('selected_job_status')
    job_status.textContent = data.status
    if (data.status === "Open"){
      job_status.className = "rounded-md px-2 py-1 text-xs font-medium bg-green-50 text-green-600 ring-1 ring-inset ring-green-600/20"
    }else{
      job_status.className = "rounded-md px-2 py-1 text-xs font-medium bg-red-50 text-red-600"
    }
    
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

    // Applications
    const applicationsContainer = document.getElementById('applications')
    
    while (applicationsContainer.firstChild){
      applicationsContainer.removeChild(applicationsContainer.firstChild)
    }
    if(data.applications == null){
    }
    else{
      data.applications.forEach(a => {
      const row = document.createElement('tr')
      row.classList.add('even:bg-gray-50', 'cursor-pointer')
      row.onclick = () => navigateApplication(a.id)

      const candidateCell = document.createElement('td')
      candidateCell.classList.add('whitespace-nowrap', 'py-5', 'pl-4', 'pr-3', 'text-sm', 'sm:pl-0')
      const candidateDiv = document.createElement('div')
      candidateDiv.classList.add('flex', 'items-center')
      const textWrapDiv = document.createElement('div')
      textWrapDiv.classList.add('text-wrap')
      const nameDiv = document.createElement('div')
      nameDiv.classList.add('font-medium', 'text-gray-900')
      nameDiv.id = `application_candidate_${a.id}`
      nameDiv.textContent = `${a.candidate_name}`
      const jobTitleDiv = document.createElement('div')
      jobTitleDiv.classList.add('mt-1', 'text-gray-500')
      jobTitleDiv.textContent = a.latest_job_title

      textWrapDiv.appendChild(nameDiv)
      textWrapDiv.appendChild(jobTitleDiv)
      candidateDiv.appendChild(textWrapDiv)
      candidateCell.appendChild(candidateDiv)
      row.appendChild(candidateCell)
      
      const scoreCell = document.createElement('td')
      scoreCell.classList.add('whitespace-nowrap', 'px-3', 'py-5', 'text-sm', 'text-gray-500')
      scoreCell.textContent = `${a.matching_score}%`
      row.appendChild(scoreCell)
      
      const statusCell = document.createElement('td')
      statusCell.classList.add('whitespace-nowrap', 'px-3', 'py-5', 'text-sm', 'text-gray-500')
      const statusSpan = document.createElement('span')
      let statusClasses = ''
      if (a.status === 'Applied') {
          statusClasses = 'inline-flex items-center rounded-md bg-red-50 px-2 py-1 text-xs font-medium text-red-700 ring-1 ring-inset ring-red-600/20'
      } else if (a.status === 'Screening') {
          statusClasses = 'inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-inset ring-blue-600/20'
      } else if (a.status === 'Interview') {
          statusClasses = 'inline-flex items-center rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 ring-1 ring-inset ring-green-600/20'
      }
      statusSpan.classList.add(...statusClasses.split(' '))
      statusSpan.textContent = a.status
      statusCell.appendChild(statusSpan)
      row.appendChild(statusCell)

      applicationsContainer.appendChild(row)
      })
    }
  })
}