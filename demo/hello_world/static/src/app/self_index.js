/** @odoo-module */
import { Component, whenReady, App, onWillStart, onMounted, useState } from "@odoo/owl";
import { makeEnv, startServices } from "@web/env";
import { templates } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";
import { MainComponentsContainer } from "@web/core/main_components_container";
import { parseHash, parseSearchQuery, routeToUrl } from "@web/core/browser/router_service";


// http://localhost:8070/home#name=Mohamed


export class selfIndex extends Component {
    static template = "hello_world.selfIndex";
    static props = [];
    static components = {
        MainComponentsContainer,
    }
    
    setup() {

        this.state = useState({
            name: '',
        });

        onWillStart(async ()=> {
            console.log("this...");
            console.log(this);
        })

        onMounted(async ()=> {
            console.log("this...");
            console.log(document.querySelector('h2'));
            console.log(document.querySelector('h2').dataset.name);
            console.log(odoo.csrf_token);
            console.log(window.location.hash);

            let args = parseHash(window.location.hash);
            
            if (args.name) {
                this.state.name = args.name;
            }

            console.log(args);
            console.log(this.state.args);
            console.log(typeof(this.state));
            console.log(this.state.name);
            console.log(typeof(this.state));
        })
    }

    fooName() {
        console.log("Foo clicked!");
        this.state.name = "Foo";
    }

    async json_calls_get() {

        try{
            const response = await fetch('/json_call_get', {
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

    async json_calls_post() {
        try{
            const response = await fetch('/json_call_post', {
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

    async json_calls_login() {
        // login functionality
        const req_1 = await fetch('/jsonrpc', {
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
            mode: "cors",
            credentials: "include",
        });

        const reply_1 = await req_1.json();
        
        // console.log(req_1);
        console.log(reply_1, reply_1.result);
    }
}

export async function createPublicRoot() {
    await whenReady();
    const env = makeEnv();
    await startServices(env);
    const app = new App(selfIndex, {
        templates,
        env: env,
        dev: env.debug,
        translateFn: _t,
        translatableAttributes: ["data-tooltip"],
    });
    return app.mount(document.body);
}

createPublicRoot();
export default { selfIndex, createPublicRoot };
