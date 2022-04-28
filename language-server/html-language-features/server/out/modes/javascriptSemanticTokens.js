"use strict";
/*---------------------------------------------------------------------------------------------
 *  Copyright (c) Microsoft Corporation. All rights reserved.
 *  Licensed under the MIT License. See License.txt in the project root for license information.
 *--------------------------------------------------------------------------------------------*/
Object.defineProperty(exports, "__esModule", { value: true });
exports.getSemanticTokens = exports.getSemanticTokenLegend = void 0;
function getSemanticTokenLegend() {
    if (tokenTypes.length !== 12 /* _ */) {
        console.warn('TokenType has added new entries.');
    }
    if (tokenModifiers.length !== 6 /* _ */) {
        console.warn('TokenModifier has added new entries.');
    }
    return { types: tokenTypes, modifiers: tokenModifiers };
}
exports.getSemanticTokenLegend = getSemanticTokenLegend;
function* getSemanticTokens(jsLanguageService, document, fileName) {
    const { spans } = jsLanguageService.getEncodedSemanticClassifications(fileName, { start: 0, length: document.getText().length }, '2020');
    for (let i = 0; i < spans.length;) {
        const offset = spans[i++];
        const length = spans[i++];
        const tsClassification = spans[i++];
        const tokenType = getTokenTypeFromClassification(tsClassification);
        if (tokenType === undefined) {
            continue;
        }
        const tokenModifiers = getTokenModifierFromClassification(tsClassification);
        const startPos = document.positionAt(offset);
        yield {
            start: startPos,
            length: length,
            typeIdx: tokenType,
            modifierSet: tokenModifiers
        };
    }
}
exports.getSemanticTokens = getSemanticTokens;
function getTokenTypeFromClassification(tsClassification) {
    if (tsClassification > 255 /* modifierMask */) {
        return (tsClassification >> 8 /* typeOffset */) - 1;
    }
    return undefined;
}
function getTokenModifierFromClassification(tsClassification) {
    return tsClassification & 255 /* modifierMask */;
}
const tokenTypes = [];
tokenTypes[0 /* class */] = 'class';
tokenTypes[1 /* enum */] = 'enum';
tokenTypes[2 /* interface */] = 'interface';
tokenTypes[3 /* namespace */] = 'namespace';
tokenTypes[4 /* typeParameter */] = 'typeParameter';
tokenTypes[5 /* type */] = 'type';
tokenTypes[6 /* parameter */] = 'parameter';
tokenTypes[7 /* variable */] = 'variable';
tokenTypes[8 /* enumMember */] = 'enumMember';
tokenTypes[9 /* property */] = 'property';
tokenTypes[10 /* function */] = 'function';
tokenTypes[11 /* method */] = 'method';
const tokenModifiers = [];
tokenModifiers[2 /* async */] = 'async';
tokenModifiers[0 /* declaration */] = 'declaration';
tokenModifiers[3 /* readonly */] = 'readonly';
tokenModifiers[1 /* static */] = 'static';
tokenModifiers[5 /* local */] = 'local';
tokenModifiers[4 /* defaultLibrary */] = 'defaultLibrary';
