const {test}=require('node:test');const assert=require('node:assert/strict');const c=require('./core');const dictionary=require('./dictionary.json');const lex=new c.Lexicon(dictionary);
test('show follows the agreed mapping',()=>assert.equal(c.encode(['SH','OW1']),'ᛋᚳᚩᚹ'));
test('custom runes preserve voicing contrasts',()=>{assert.notEqual(c.encode(['V','AE1','N']),c.encode(['F','AE1','N']));assert.equal(c.encode(['DH','IH1','S']),'\uE001ᛁᛋ');});
test('all homophone matches are kept',()=>{const matches=lex.lookup(c.encode(['R','AY1','T'])).map(x=>x.word);for(const w of ['right','write','rite'])assert.ok(matches.includes(w));});
test('every CMU phone is supported',()=>{for(const variants of Object.values(dictionary))for(const phones of variants)for(const p of phones)assert.ok(c.MAP[p.replace(/[012]$/,'')],p);});
test('unstressed vowels and syllabic rhotic vowels',()=>{assert.equal(c.encode(['AH0','ER0','ER1']),'ᛟᛟᚱᚢᚱ');assert.equal(c.pronunciation(['AH0','ER0']),'əɚ');});
test('compatibility forms normalize',()=>{assert.equal(c.normalize('ᛁᛡᚫᚫᛥᛢ'),'ᛇᚪᛋᛏᛣᚹ');});
test('token ranges handle PUA, punctuation, and emoji',()=>assert.deepEqual(c.tokens('😀 ᚠ\uE000᛫ᚦ\uE001'),[{text:'ᚠ\uE000',start:3,end:5},{text:'ᚦ\uE001',start:6,end:8}]));
test('correction ranking finds an intended neighboring spelling',()=>{assert.ok(lex.suggest('ᛋᚳᚩᛡ').some(x=>x.runes==='ᛋᚳᚩᚹ'));});
test('sequence hover resolves both cells',()=>{assert.equal(c.runeInfo('ᛋᚳᚩᚹ',1).sound,'/ʃ/');assert.equal(c.runeInfo('ᛋᚳᚩᚹ',3).sound,'/oʊ/');});
test('every generated dictionary character has font coverage',()=>{const glyphs=require('./glyphs.json');for(const key of lex.index.keys())for(const ch of key)assert.ok(glyphs[ch],ch);});

test('notebook dots separate words with exact editor ranges',()=>assert.deepEqual(c.tokens('ᚠᚫᚾ.\uE000ᚫᚾ·ᚦᛁᚾ'),[{text:'ᚠᚫᚾ',start:0,end:3},{text:'\uE000ᚫᚾ',start:4,end:7},{text:'ᚦᛁᚾ',start:8,end:11}]));
