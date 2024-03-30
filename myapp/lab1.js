const searchButton = document.getElementById('search-button');
const searchQuery = document.getElementById('search');
const resultsContainer = document.getElementById('results');
searchQuery.addEventListener('keyup', (event) => {
  if (event.key === 'Enter') {
    const searchTerm = event.target.value;
  const query = searchQuery.value.trim();
  if (!query) {
    alert('Please enter a search query.');
    return;
  }

  const url = `https://www.googleapis.com/books/v1/volumes?q=${query}&key=AIzaSyAY7mQOn538uaX1ql_rp8fQ7qPyA9-an9I`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      resultsContainer.innerHTML = '';
      data.items.forEach((item) => {
        const book = document.createElement('div');
        book.classList.add('book');

        const img = document.createElement('img');
        img.src = item.volumeInfo.imageLinks.thumbnail;
        book.appendChild(img);

        const title = document.createElement('p');
        title.classList.add('title');
        title.textContent = item.volumeInfo.title;
        book.appendChild(title);

        const author = document.createElement('p');
        author.classList.add('author');
        author.textContent = item.volumeInfo.authors[0];
        book.appendChild(author);

        resultsContainer.appendChild(book);
      });
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while searching.');
    });
  }
});
searchButton.addEventListener('click', () => {
  const query = searchQuery.value.trim();
  if (!query) {
    alert('Please enter a search query.');
    return;
  }

  const url = `https://www.googleapis.com/books/v1/volumes?q=${query}&key=AIzaSyAY7mQOn538uaX1ql_rp8fQ7qPyA9-an9I`;

  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      resultsContainer.innerHTML = '';
      data.items.forEach((item) => {
        const book = document.createElement('div');
        book.classList.add('book');

        const img = document.createElement('img');
        img.src = item.volumeInfo.imageLinks.thumbnail;
        book.appendChild(img);

        const title = document.createElement('p');
        title.classList.add('title');
        title.textContent = item.volumeInfo.title;
        book.appendChild(title);

        const author = document.createElement('p');
        author.classList.add('author');
        author.textContent = item.volumeInfo.authors[0];
        book.appendChild(author);

        resultsContainer.appendChild(book);
      });
    })
    .catch((error) => {
      console.error('Error:', error);
      alert('An error occurred while searching.');
    });
});