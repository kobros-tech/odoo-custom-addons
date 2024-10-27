
async function test_get() {

    try{
        const response = await fetch('http://localhost:8070/json_call', {
            headers: {
                "Content-type": "application/json",
            },
            method: "GET",
            mode: "cors",
            credentials: "include",
        });
        const data = await response.json();
        
        console.log("Successful Get");
        console.log(data);
    }
    catch(err) {
        console.log(err);
    }
    
}



async function test_post() {

    try{
        const response = await fetch('http://localhost:8070/json_call/153', {
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({
                id: 1,
                jsonrpc: "2.0",
                method: "call",
                params: {
                    model: "mail.partner.device",
                    method: "register_devices",
                    args: [],
                    kwargs: {},
                    context: {},
                    path: {'key': 2, 'value': false},
                    index: 154,
                },
            }),
            method: "POST",
            mode: "cors",
            credentials: "include",
        });
        const data = await response.json();
        
        console.log("Successful Post");
        console.log(data);
    }
    catch(err) {
        console.log(err);
    }
    
}

async function test_json_calls_get() {

    try{
        const response = await fetch('http://localhost:8070/json_call_get', {
            headers: {
                "Content-type": "application/json",
            },
            method: "GET",
            mode: "cors",
            credentials: "same-origin",
        });
        const data = await response.json();
        
        console.log("Successful Get");
        console.log(data);
    }
    catch(err) {
        console.log(err);
    }
    
}

async function test_json_calls_post() {

    try{
        const response = await fetch('http://localhost:8070/json_call_post', {
            headers: {
                "Content-type": "application/json",
            },
            body: JSON.stringify({
                id: 1,
                jsonrpc: "2.0",
                method: "call",
                params: {
                    model: "mail.partner.device",
                    method: "register_devices",
                    args: [],
                    kwargs: {},
                    context: {},
                    path: {'key': 2, 'value': false},
                    index: 154,
                },
            }),
            method: "POST",
            mode: "cors",
            credentials: "same-origin",
        });
        const data = await response.json();
        
        console.log("Successful Get");
        console.log(data);
    }
    catch(err) {
        console.log(err);
    }
    
}


test_get();
test_post();
test_json_calls_get();
test_json_calls_post();
