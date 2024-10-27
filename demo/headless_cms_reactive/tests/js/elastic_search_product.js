const username = 'elastic';  // Replace with your username
const password = 'your_elastic_password';  // Replace with your password
const url = "http://localhost:9200/elastic_external_fs_2_product_variant_en_us-1/_search";

async function searchProduct(productName) {
  const headers = {
    "Authorization": "Basic " + btoa(`${username}:${password}`),
    "Content-Type": "application/json"
  };

  const body = JSON.stringify({
    query: {
      match: {
        name: productName  // Replace with the field you want to search
      }
    }
  });

  try {
    const response = await fetch(url, {
      method: "POST",  // POST method since we are sending a query body
      headers: headers,
      body: body
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();
    console.log(data);  // Handle the data, e.g., display search results
    console.log(data.hits.hits);
  } catch (error) {
    console.error("Fetch error:", error);
  }
}

// Call the function and search for a product
searchProduct("Meuble TV");
