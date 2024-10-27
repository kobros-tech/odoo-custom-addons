# -*- coding: utf-8 -*-
# Part of kobros-tech. See LICENSE file for full copyright and licensing details.

{
    "name": "Hello World",
    "description": "Hello World Web App using Odoo",
    "author": "Mohamed Alkobrosli",
    "website": "https://www.kobros-tech.com",
    "license": "AGPL-3",
    "depends": [
        "web",
        'web_editor',
        "website",
    ],
    "data": [
        "data/hello.xml",
        "data/home.xml",
    ],
    "assets": {
        'web.assets_frontend': [
            'headless_cms_reactive/static/src/patch/main_component_patch.js',
        ],
    },
}
