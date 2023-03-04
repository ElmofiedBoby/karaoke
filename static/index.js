function getList() {
    return fetch('http://localhost:5002/list?state=finished')
      .then(response => response.json())
      .catch(error => {
        console.error('Error fetching list:', error);
      });
  }

function updateList() {
    getList().then(data => {
        const listDiv = document.getElementById('list');
        listDiv.innerHTML = '';

        data.forEach(item => {
            let artist = item.split(' - ')[0];
            console.log(artist)
            let song = item.split(' - ')[1];
            console.log(song)
            const itemElement = document.createElement('li');
            itemElement.innerHTML = '<a href="/player?artist='+artist+'&song='+song+'">'+item+'</a>';
            listDiv.appendChild(itemElement);
        });
    }).catch(error => {
        console.error('Error updating list:', error);
    });
}

window.onload = updateList;