"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
const vscode_html_languageservice_1 = require("vscode-html-languageservice");
const fs = require("fs");
function getDataProviders(dataPaths) {
    if (!dataPaths) {
        return [];
    }
    const providers = [];
    dataPaths.forEach((path, i) => {
        try {
            if (fs.existsSync(path)) {
                const htmlData = JSON.parse(fs.readFileSync(path, 'utf-8'));
                providers.push(vscode_html_languageservice_1.newHTMLDataProvider(`customProvider${i}`, htmlData));
            }
        }
        catch (err) {
            console.log(`Failed to load tag from ${path}`);
        }
    });
    return providers;
}
exports.getDataProviders = getDataProviders;
