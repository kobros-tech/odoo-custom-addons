

// all indices
// http://localhost:9200/_cat/indices?v

const username = 'elastic';  // Replace with your username
const password = 'your_elastic_password';  // Replace with your password
const url = "http://localhost:9200/elastic_external_fs_2_product_variant_en_us-1/_search?pretty";


async function fetchProducts() {
  const headers = {
    "Authorization": "Basic " + btoa(`${username}:${password}`),
    "Content-Type": "application/json"
  };

  try {
    const response = await fetch(url, { method: "GET", headers });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);  // Handle or return the data as needed
    console.log(data.hits.hits);
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

fetchProducts();  // Call the function
