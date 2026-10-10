from pathlib import Path
import cmudict,json,shutil
root=Path(__file__).resolve().parent
entries={w:ps for w,ps in cmudict.dict().items() if all(c.isalpha() or c in "'-" for c in w)}
(root/'dictionary.json').write_text(json.dumps(entries,separators=(',',':')))
shutil.copyfile(Path(cmudict.__file__).parent/'data/LICENSE',root/'CMUDICT-LICENSE.txt')
print('Bundled',len(entries),'words')
