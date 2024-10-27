/** @odoo-module **/

import { registry } from "@web/core/registry";

console.log("recording a service...");

const testCMSService = {
    dependencies: ['title'],
    start(env, { title }) {

        // console.log(env);
        console.log(title);
        console.log(title.getParts());
        title.setParts({ zopenerp: "kobros-tech", action: "Login" });
        
        return true;
    },
};
registry.category("services").add("testCMSService", testCMSService, {force: true});
