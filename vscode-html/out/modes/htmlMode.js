"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
const languageModelCache_1 = require("../languageModelCache");
const pathCompletion_1 = require("./pathCompletion");
function getHTMLMode(htmlLanguageService, workspace) {
    let htmlDocuments = languageModelCache_1.getLanguageModelCache(10, 60, document => htmlLanguageService.parseHTMLDocument(document));
    return {
        getId() {
            return 'html';
        },
        getSelectionRange(document, position) {
            return htmlLanguageService.getSelectionRanges(document, [position])[0];
        },
        doComplete(document, position, settings = workspace.settings) {
            let options = settings && settings.html && settings.html.suggest;
            let doAutoComplete = settings && settings.html && settings.html.autoClosingTags;
            if (doAutoComplete) {
                options.hideAutoCompleteProposals = true;
            }
            let pathCompletionProposals = [];
            let participants = [pathCompletion_1.getPathCompletionParticipant(document, workspace.folders, pathCompletionProposals)];
            htmlLanguageService.setCompletionParticipants(participants);
            const htmlDocument = htmlDocuments.get(document);
            let completionList = htmlLanguageService.doComplete(document, position, htmlDocument, options);
            completionList.items.push(...pathCompletionProposals);
            return completionList;
        },
        doHover(document, position) {
            return htmlLanguageService.doHover(document, position, htmlDocuments.get(document));
        },
        findDocumentHighlight(document, position) {
            return htmlLanguageService.findDocumentHighlights(document, position, htmlDocuments.get(document));
        },
        findDocumentLinks(document, documentContext) {
            return htmlLanguageService.findDocumentLinks(document, documentContext);
        },
        findDocumentSymbols(document) {
            return htmlLanguageService.findDocumentSymbols(document, htmlDocuments.get(document));
        },
        format(document, range, formatParams, settings = workspace.settings) {
            let formatSettings = settings && settings.html && settings.html.format;
            if (formatSettings) {
                formatSettings = merge(formatSettings, {});
            }
            else {
                formatSettings = {};
            }
            if (formatSettings.contentUnformatted) {
                formatSettings.contentUnformatted = formatSettings.contentUnformatted + ',script';
            }
            else {
                formatSettings.contentUnformatted = 'script';
            }
            formatSettings = merge(formatParams, formatSettings);
            return htmlLanguageService.format(document, range, formatSettings);
        },
        getFoldingRanges(document) {
            return htmlLanguageService.getFoldingRanges(document);
        },
        doAutoClose(document, position) {
            let offset = document.offsetAt(position);
            let text = document.getText();
            if (offset > 0 && text.charAt(offset - 1).match(/[>\/]/g)) {
                return htmlLanguageService.doTagComplete(document, position, htmlDocuments.get(document));
            }
            return null;
        },
        doRename(document, position, newName) {
            const htmlDocument = htmlDocuments.get(document);
            return htmlLanguageService.doRename(document, position, newName, htmlDocument);
        },
        onDocumentRemoved(document) {
            htmlDocuments.onDocumentRemoved(document);
        },
        findMatchingTagPosition(document, position) {
            const htmlDocument = htmlDocuments.get(document);
            return htmlLanguageService.findMatchingTagPosition(document, position, htmlDocument);
        },
        dispose() {
            htmlDocuments.dispose();
        }
    };
}
exports.getHTMLMode = getHTMLMode;
function merge(src, dst) {
    for (const key in src) {
        if (src.hasOwnProperty(key)) {
            dst[key] = src[key];
        }
    }
    return dst;
}
