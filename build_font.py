"""Build original geometric rune outlines; no ligature substitutions."""
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
'ᚣ':[((100,80),(100,680)),((100,680),(500,500)),((500,500),(500,80)),((100,80),(500,80)),((300,230),(300,510))],
'ᚩ':[S,((300,570),(510,680)),((300,390),(510,500)),((300,570),(510,450)),((300,390),(510,270))],
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
'ᛝ':[((300,680),(100,500)),((100,500),(500,260)),((500,260),(300,80)),((300,80),(100,260)),((100,260),(500,500)),((500,500),(300,680))],
'ᛞ':[((100,80),(100,680)),((500,80),(500,680)),((100,80),(500,680)),((100,680),(500,80))],
'ᛟ':[((300,650),(100,430)),((100,430),(300,210)),((300,210),(500,430)),((500,430),(300,650)),((100,80),(220,300)),((500,80),(380,300))],
'ᛠ':[S,((100,400),(500,400)),((100,400),(100,210)),((500,400),(500,210))],
'ᛢ':[S,((300,680),(100,520)),((100,520),(300,360)),((300,680),(500,520)),((500,520),(300,360))],
'ᛥ':[S,((100,530),(300,680)),((300,680),(500,530)),((100,270),(300,420)),((300,420),(500,270))],
}
def glyph(lines,weight=60):
 p=TTGlyphPen(None)
 for a,b in lines:
  dx,dy=b[0]-a[0],b[1]-a[1]; length=math.hypot(dx,dy); nx,ny=-dy/length*weight/2,dx/length*weight/2
  pts=[(a[0]-50+nx,a[1]+ny),(b[0]-50+nx,b[1]+ny),(b[0]-50-nx,b[1]-ny),(a[0]-50-nx,a[1]-ny)]
  # Clockwise contours for TrueType; overlapping strokes share the same direction.
  p.moveTo(pts[0]); [p.lineTo(t) for t in pts[1:]]; p.closePath()
 # Fill shared endpoints with true miter joins rather than exposed butt caps.
 vertices={}
 for a,b in lines:
  vertices.setdefault(a,[]).append(b);vertices.setdefault(b,[]).append(a)
 for v,ends in vertices.items():
  if len(ends)!=2:continue
  # A junction on a through-stem needs no extra corner beyond the union.
  if any(v!=a and v!=b and abs((v[0]-a[0])*(b[1]-a[1])-(v[1]-a[1])*(b[0]-a[0]))<1e-6 and min(a[0],b[0])<=v[0]<=max(a[0],b[0]) and min(a[1],b[1])<=v[1]<=max(a[1],b[1]) for a,b in lines):continue
  rays=[]
  for e in ends:
   dx,dy=e[0]-v[0],e[1]-v[1];length=math.hypot(dx,dy);rays.append((dx/length,dy/length))
  u,w=rays;cross=u[0]*w[1]-u[1]*w[0]
  if abs(cross)<1e-6:continue
  for side in [-1,1]:
   a=(v[0]-side*u[1]*weight/2,v[1]+side*u[0]*weight/2)
   b=(v[0]+side*w[1]*weight/2,v[1]-side*w[0]*weight/2)
   delta=(b[0]-a[0],b[1]-a[1]);t=(delta[0]*w[1]-delta[1]*w[0])/cross
   m=(a[0]+t*u[0],a[1]+t*u[1])
   if math.hypot(m[0]-v[0],m[1]-v[1])>weight:m=v
   pts=[v,a,m,b]
   area=sum(pts[i][0]*pts[(i+1)%4][1]-pts[(i+1)%4][0]*pts[i][1] for i in range(4))
   if area>0:pts.reverse()
   p.moveTo((pts[0][0]-50,pts[0][1]))
   for x,y in pts[1:]:p.lineTo((x-50,y))
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
