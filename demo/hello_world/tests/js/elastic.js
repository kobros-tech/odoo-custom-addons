const username = 'elastic';  // Your Elasticsearch username
const password = 'your_elastic_password';  // Your Elasticsearch password
const url = 'http://localhost:9200/_cat/indices?v';  // The API endpoint

async function getIndices() {
  const headers = {
    "Authorization": "Basic " + btoa(`${username}:${password}`),  // Basic Auth header
    "Content-Type": "application/json"
  };

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.text();  // Elasticsearch _cat API returns plain text
    console.log(data);  // Display the list of indices
  } catch (error) {
    console.error('Fetch error:', error);
  }
}

getIndices();
