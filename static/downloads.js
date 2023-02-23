function getList() {
    return fetch('http://localhost:5002/queue')
      .then(response => response.json())
      .catch(error => {
        console.error('Error fetching list:', error);
      });
  }

function updateList() {
    getList().then(data => {
        const listDiv = document.getElementById('downloadslist');
        listDiv.innerHTML = '';

        data.forEach(item => {
            console.log(item);
        });
    }).catch(error => {
        console.error('Error updating list:', error);
    });
}

window.onload = updateList;