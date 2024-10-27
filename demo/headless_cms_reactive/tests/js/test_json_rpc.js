
const HOST = 'localhost'
const PORT = 8070
const DB = 'kernel'
const USER = 'admin'
const PASS = 'admin'


async function json_rpc(url, method, params) {

    const req = await fetch(url, {
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            id: 1,
            jsonrpc: "2.0",
            method: method,
            params: params,
        }),
        method: "POST",
        mode: "no-cors",
        credentials: "same-origin",
    });

    const reply = await req.json();
    
    return reply.result;
}


async function call(url, service, method, args) {
    return await json_rpc(url, 'call', {service, method, args});
}


(async function exeQuery() {
    // log in the given database
    const url = `http://${HOST}:${PORT}/jsonrpc`;
    uid = await call(url, "common", "login", [DB, USER, PASS]);

    console.log("USER ID:", uid);

    // query user
    const domain = ["login", "=", "admin"]

    const note_id = await call(url, "object", "execute", [DB, uid, PASS, 'res.users', 'search_read', [domain], {'login': "login", 'name': "name"}]);

    console.log("NOTE IS SUCCESSFUL:", note_id);

    // call a path
    const uid_2 = await call(url, "common", "version", []);

    console.log("PATH CALL SUCCESSFUL:", uid_2);

})();



async function odoo_fetch() {

    // login functionality
    const req_1 = await fetch('http://localhost:8070/jsonrpc', {
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            id: 1,
            jsonrpc: "2.0",
            method: "call",
            params: {
                'service': 'common',
                'method': 'login',
                'args': ['kernel', 'admin', 'admin']
            },
        }),
        method: "POST",
        mode: "no-cors",
        credentials: "same-origin",
    });

    const reply_1 = await req_1.json();
    
    // console.log(req_1);
    console.log(reply_1, reply_1.result);

    const domain_2 = ["id", "=", 2];
    
    // execute functionality
    const req_2 = await fetch('http://localhost:8070/jsonrpc', {
        headers: {
            "Content-type": "application/json",
        },
        body: JSON.stringify({
            id: 1,
            jsonrpc: "2.0",
            method: "call",
            params: {
                'service': 'object',
                'method': 'execute',
                'args': ['kernel', 2, 'admin', 'res.users', 'search_read', [domain_2], {'login': "login", 'name': "name"}]
            },
        }),
        method: "POST",
        mode: "no-cors",
        credentials: "same-origin",
    });

    const reply_2 = await req_2.json();
    
    // console.log(req_2);
    console.log(reply_2);
}

odoo_fetch();
