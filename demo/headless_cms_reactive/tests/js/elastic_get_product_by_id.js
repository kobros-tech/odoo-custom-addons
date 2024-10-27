

async function get_indices() {
    const username = 'elastic';
    const password = 'your_elastic_password';
    const url = `http://localhost:9200/elastic_external_fs_2_product_variant_en_us-1/_doc/61?pretty`;

    
    const headers = {
        "Authorization": "Basic " + btoa(`${username}:${password}`),  // Basic Auth header
        "Content-Type": "application/json"
    };

    try{
        const response = await fetch(url, {
            method: 'GET',
            headers: headers
          });
        const data = await response.json();
        
        console.log("Successful Get");
        console.log(data);
        console.log(typeof(data));
    }
    catch(err) {
        console.log(err);
    }
    
}


get_indices();
