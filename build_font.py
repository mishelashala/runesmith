"""Build original continuous pen-path rune outlines; no ligature substitutions."""
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen
from pathlib import Path
import math, json
ROOT=Path(__file__).resolve().parent
# Design coordinates in a 600-unit cell; recentered into a tighter 500-unit monospace cell.
S=((300,80),(300,680))
patterns={
'ᚠ':[S,((300,570),(510,680)),((300,390),(510,500))],
'\ue000':[S,((300,570),(510,680)),((300,390),(510,500)),((300,570),(90,680)),((300,390),(90,500))],
'ᚦ':[S,((300,570),(500,400)),((500,400),(300,230))],
'\ue001':[S,((300,570),(500,400)),((500,400),(300,230)),((190,370),(395,370))],
'ᚢ':[((100,80),(100,680)),((100,680),(500,500)),((500,500),(500,80))],
'ᚣ':[((100,80),(100,680)),((100,680),(500,500)),((500,500),(500,80)),((300,80),(300,260))],
'ᚩ':[((120,80),(120,680)),((120,680),(350,540)),((350,540),(480,680)),((120,380),(350,300)),((350,300),(480,450))],
'ᚪ':[S,((300,570),(510,450)),((300,390),(510,270))],
'ᚫ':[S,((300,590),(510,470)),((300,430),(510,310)),((300,270),(510,150))],
'ᚱ':[S,((300,680),(490,540)),((490,540),(300,400)),((300,400),(510,80))],
'ᚳ':[S,((300,400),(510,570))],
'ᛣ':[S,((300,400),(100,570)),((300,400),(500,570))],
'ᚷ':[((100,80),(500,680)),((100,680),(500,80))],
'ᚸ':[((100,80),(500,680)),((100,680),(500,80)),((100,260),(300,80)),((300,680),(500,500))],
'ᚹ':[S,((300,680),(500,520)),((500,520),(300,360))],
'ᚻ':[((100,80),(100,680)),((500,80),(500,680)),((100,540),(500,250))],
'ᚾ':[S,((100,490),(500,270))], 'ᛁ':[S],
'ᛡ':[S,((90,540),(510,220)),((90,220),(510,540))],
'ᛄ':[((140,560),(320,680)),((320,680),(320,430)),((460,200),(280,80)),((280,80),(280,330))],
'ᛇ':[S,((300,680),(120,570)),((300,80),(480,190))],
'ᛈ':[S,((300,680),(500,520)),((500,520),(420,440)),((300,80),(500,240)),((500,240),(420,320))],
'ᛉ':[S,((300,420),(90,650)),((300,420),(510,650))],
'ᛋ':[((300,680),(200,380)),((200,380),(400,380)),((400,380),(300,80))],
'ᛏ':[S,((300,680),(90,460)),((300,680),(510,460))],
'ᛒ':[S,((300,680),(500,530)),((500,530),(300,380)),((300,380),(500,230)),((500,230),(300,80))],
'ᛖ':[((100,80),(100,680)),((500,80),(500,680)),((100,680),(300,420)),((300,420),(500,680))],
'ᛗ':[((100,80),(100,680)),((500,80),(500,680)),((100,680),(500,380)),((500,680),(100,380))],
'ᛚ':[S,((300,680),(510,510))],
'ᛝ':[((130,680),(470,80)),((470,680),(130,80)),((300,520),(100,380)),((100,380),(300,240)),((300,240),(500,380)),((500,380),(300,520))],
'ᛞ':[((100,80),(100,680)),((500,80),(500,680)),((100,80),(500,680)),((100,680),(500,80))],
'ᛟ':[((300,680),(100,450)),((100,450),(300,260)),((300,260),(500,450)),((500,450),(300,680)),((100,80),(500,450)),((500,80),(100,450))],
'ᛠ':[S,((100,400),(500,400)),((100,400),(100,210)),((500,400),(500,210))],
'ᛢ':[S,((300,680),(100,520)),((100,520),(300,360)),((300,680),(500,520)),((500,520),(300,360))],
'ᛥ':[S,((100,530),(300,680)),((300,680),(500,530)),((100,270),(300,420)),((300,420),(500,270))],
}
def glyph(lines,weight=60):
 """Expand a connected pen path once, with round caps and joins, then emit its unified boundary."""
 from shapely.geometry import LineString
 from shapely.ops import unary_union, linemerge
 from shapely.geometry.polygon import orient
 p=TTGlyphPen(None)
 if not lines:return p.glyph()
 network=unary_union([LineString([(x-50,y) for x,y in (a,b)]) for a,b in lines])
 if network.geom_type=='MultiLineString':network=linemerge(network)
 # Round joins follow the motion of a pen through bends; union removes every seam.
 outline=network.buffer(weight/2,cap_style='round',join_style='round',quad_segs=8)
 polygons=[outline] if outline.geom_type=='Polygon' else list(outline.geoms)
 for polygon in polygons:
  polygon=orient(polygon,sign=-1)
  for ring in [polygon.exterior,*polygon.interiors]:
   pts=list(ring.coords)[:-1];p.moveTo(pts[0])
   for pt in pts[1:]:p.lineTo(pt)
   p.closePath()
 return p.glyph()
chars={' ':[],'.':[],'·':[],'•':[],**patterns,'᛫':[((300,355),(300,405))],'᛬':[((300,245),(300,295)),((300,465),(300,515))]}
def separator():
 p=TTGlyphPen(None);cx,cy,r=250,380,30
 p.moveTo((cx+r,cy))
 for i in range(1,24):
  angle=-2*math.pi*i/24;p.lineTo((cx+r*math.cos(angle),cy+r*math.sin(angle)))
 p.closePath();return p.glyph()
names={c:'uni%04X'%ord(c) for c in chars}; order=['.notdef']+list(names.values())
fb=FontBuilder(800,isTTF=True); fb.setupGlyphOrder(order); fb.setupCharacterMap({ord(c):n for c,n in names.items()})
g={names[c]:separator() if c in '.·•᛫' else glyph(v,44 if c=='᛬' else 60) for c,v in chars.items()}; g['.notdef']=glyph([((100,80),(100,680)),((100,680),(500,680)),((500,680),(500,80)),((500,80),(100,80))])
fb.setupGlyf(g); fb.setupHorizontalMetrics({n:(500,0) for n in order}); fb.setupHorizontalHeader(ascent=740,descent=-120)
fb.setupNameTable({'familyName':'RuneSmith Mono','styleName':'Regular','uniqueFontIdentifier':'RuneSmithMono-0.1.0','fullName':'RuneSmith Mono Regular','psName':'RuneSmithMono-Regular','version':'Version 0.1.0','copyright':'Copyright (c) 2026 Michell Ayala','licenseDescription':ROOT.joinpath('LICENSE').read_text(),'licenseInfoURL':'https://github.com/mishelashala/runesmith/blob/main/LICENSE'})
fb.setupOS2(sTypoAscender=740,sTypoDescender=-120,sTypoLineGap=0,usWinAscent=740,usWinDescent=120,fsSelection=0x40)
fb.setupPost(isFixedPitch=1); fb.setupMaxp(); fb.save(ROOT/'RuneSmithMono-Regular.ttf')
from fontTools.ttLib import TTFont
from fontTools.ttLib.removeOverlaps import removeOverlaps
f=TTFont(ROOT/'RuneSmithMono-Regular.ttf'); removeOverlaps(f); f.save(ROOT/'RuneSmithMono-Regular.ttf')
ROOT.joinpath('glyphs.json').write_text(json.dumps({c:n for c,n in names.items()},ensure_ascii=False))
print('Built',len(chars),'characters')
