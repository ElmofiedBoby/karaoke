function getList() {
    return fetch('http://localhost:5002/list?state=notfinished')
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
            const itemElement = document.createElement('li');
            itemElement.innerHTML = item;
            listDiv.appendChild(itemElement);
        });
    }).catch(error => {
        console.error('Error updating list:', error);
    });
}

window.onload = updateList;
const interval = setInterval(function() {
    updateList();
}, 5000);