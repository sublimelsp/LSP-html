"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
const path = require("path");
const fs = require("fs");
const vscode_uri_1 = require("vscode-uri");
const languageModes_1 = require("./languageModes");
const strings_1 = require("../utils/strings");
const arrays_1 = require("../utils/arrays");
function getPathCompletionParticipant(document, workspaceFolders, result) {
    return {
        onHtmlAttributeValue: ({ tag, attribute, value: valueBeforeCursor, range }) => {
            const fullValue = stripQuotes(document.getText(range));
            if (shouldDoPathCompletion(tag, attribute, fullValue)) {
                if (workspaceFolders.length === 0) {
                    return;
                }
                const workspaceRoot = resolveWorkspaceRoot(document, workspaceFolders);
                const paths = providePaths(valueBeforeCursor, vscode_uri_1.URI.parse(document.uri).fsPath, workspaceRoot);
                result.push(...paths.map(p => pathToSuggestion(p, valueBeforeCursor, fullValue, range)));
            }
        }
    };
}
exports.getPathCompletionParticipant = getPathCompletionParticipant;
function stripQuotes(fullValue) {
    if (strings_1.startsWith(fullValue, `'`) || strings_1.startsWith(fullValue, `"`)) {
        return fullValue.slice(1, -1);
    }
    else {
        return fullValue;
    }
}
function shouldDoPathCompletion(tag, attr, value) {
    if (strings_1.startsWith(value, 'http') || strings_1.startsWith(value, 'https') || strings_1.startsWith(value, '//')) {
        return false;
    }
    if (PATH_TAG_AND_ATTR[tag]) {
        if (typeof PATH_TAG_AND_ATTR[tag] === 'string') {
            return PATH_TAG_AND_ATTR[tag] === attr;
        }
        else {
            return arrays_1.contains(PATH_TAG_AND_ATTR[tag], attr);
        }
    }
    return false;
}
/**
 * Get a list of path suggestions. Folder suggestions are suffixed with a slash.
 */
function providePaths(valueBeforeCursor, activeDocFsPath, root) {
    const lastIndexOfSlash = valueBeforeCursor.lastIndexOf('/');
    const valueBeforeLastSlash = valueBeforeCursor.slice(0, lastIndexOfSlash + 1);
    const startsWithSlash = strings_1.startsWith(valueBeforeCursor, '/');
    let parentDir;
    if (startsWithSlash) {
        if (!root) {
            return [];
        }
        parentDir = path.resolve(root, '.' + valueBeforeLastSlash);
    }
    else {
        parentDir = path.resolve(activeDocFsPath, '..', valueBeforeLastSlash);
    }
    try {
        const paths = fs.readdirSync(parentDir).map(f => {
            return isDir(path.resolve(parentDir, f))
                ? f + '/'
                : f;
        });
        return paths.filter(p => p[0] !== '.');
    }
    catch (e) {
        return [];
    }
}
function isDir(p) {
    try {
        return fs.statSync(p).isDirectory();
    }
    catch (e) {
        return false;
    }
}
function pathToSuggestion(p, valueBeforeCursor, fullValue, range) {
    const isDir = p[p.length - 1] === '/';
    let replaceRange;
    const lastIndexOfSlash = valueBeforeCursor.lastIndexOf('/');
    if (lastIndexOfSlash === -1) {
        replaceRange = shiftRange(range, 1, -1);
    }
    else {
        // For cases where cursor is in the middle of attribute value, like <script src="./s|rc/test.js">
        // Find the last slash before cursor, and calculate the start of replace range from there
        const valueAfterLastSlash = fullValue.slice(lastIndexOfSlash + 1);
        const startPos = shiftPosition(range.end, -1 - valueAfterLastSlash.length);
        // If whitespace exists, replace until there is no more
        const whitespaceIndex = valueAfterLastSlash.indexOf(' ');
        let endPos;
        if (whitespaceIndex !== -1) {
            endPos = shiftPosition(startPos, whitespaceIndex);
        }
        else {
            endPos = shiftPosition(range.end, -1);
        }
        replaceRange = languageModes_1.Range.create(startPos, endPos);
    }
    if (isDir) {
        return {
            label: p,
            kind: languageModes_1.CompletionItemKind.Folder,
            textEdit: languageModes_1.TextEdit.replace(replaceRange, p),
            command: {
                title: 'Suggest',
                command: 'editor.action.triggerSuggest'
            }
        };
    }
    else {
        return {
            label: p,
            kind: languageModes_1.CompletionItemKind.File,
            textEdit: languageModes_1.TextEdit.replace(replaceRange, p)
        };
    }
}
function resolveWorkspaceRoot(activeDoc, workspaceFolders) {
    for (const folder of workspaceFolders) {
        if (strings_1.startsWith(activeDoc.uri, folder.uri)) {
            return path.resolve(vscode_uri_1.URI.parse(folder.uri).fsPath);
        }
    }
    return undefined;
}
function shiftPosition(pos, offset) {
    return languageModes_1.Position.create(pos.line, pos.character + offset);
}
function shiftRange(range, startOffset, endOffset) {
    const start = shiftPosition(range.start, startOffset);
    const end = shiftPosition(range.end, endOffset);
    return languageModes_1.Range.create(start, end);
}
// Selected from https://stackoverflow.com/a/2725168/1780148
const PATH_TAG_AND_ATTR = {
    // HTML 4
    a: 'href',
    area: 'href',
    body: 'background',
    del: 'cite',
    form: 'action',
    frame: ['src', 'longdesc'],
    img: ['src', 'longdesc'],
    ins: 'cite',
    link: 'href',
    object: 'data',
    q: 'cite',
    script: 'src',
    // HTML 5
    audio: 'src',
    button: 'formaction',
    command: 'icon',
    embed: 'src',
    html: 'manifest',
    input: ['src', 'formaction'],
    source: 'src',
    track: 'src',
    video: ['src', 'poster']
};
