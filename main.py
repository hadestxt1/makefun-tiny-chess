import json,os,urllib.request as W
E=os.getenv("MAKEFUN_ENV_URL")
VL=[0,100,320,330,500,900,20000]
KN=[(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]
K8=[(a,b)for a in(-1,0,1)for b in(-1,0,1)if a or b]
nd=0;Ab=Exception
def post(p,b):
 r=W.urlopen(E+p,data=json.dumps(b).encode())
 return json.load(r)
def parse(fen):
 f=fen.split();b=[0]*64;i=0
 for c in f[0].replace("/",""):
  if c.isdigit():i+=int(c)
  else:
   p="pnbrqk".index(c.lower())+1;b[i]=p if c.isupper()else-p;i+=1
 cs=sum({"K":1,"Q":2,"k":4,"q":8}.get(k,0)for k in f[2])
 ep=-1
 if f[3]!="-":ep=(8-int(f[3][1]))*8+ord(f[3][0])-97
 return b,1 if f[1]=="w"else-1,cs,ep
def atk(b,sq,by):
 fi,ri=sq%8,sq//8
 for ds,pc in((KN,2),(K8,6),(((-1,by),(1,by)),1)):
  for df,dr in ds:
   f2,r2=fi+df,ri+dr
   if 0<=f2<8 and 0<=r2<8 and b[r2*8+f2]==pc*by:return 1
 for df,dr in K8:
  f2,r2=fi+df,ri+dr
  while 0<=f2<8 and 0<=r2<8:
   p=b[r2*8+f2]
   if p:
    if p/by in(5,3 if df and dr else 4):return 1
    break
   f2+=df;r2+=dr
 return 0
def gen(b,s,cs,ep,cap=0):
 ms=[]
 for i,p in enumerate(b):
  if not p or(p>0)!=(s>0):continue
  t=abs(p);fi,ri=i%8,i//8
  if t==1:
   d=-s
   for df in(-1,0,1):
    to=i+d*8+df
    if not(0<=fi+df<8 and 0<=to<64):continue
    pm=to//8 in(0,7)
    if df:
     if not(b[to]and(b[to]>0)!=(s>0))and to!=ep:continue
    elif cap and not pm or b[to]:continue
    for pr in((5,2)if pm else(0,)):ms.append((i,to,pr))
    if not df and not pm and ri==(6 if s>0 else 1)and not b[i+d*16]:ms.append((i,i+d*16,0))
  else:
   ds=KN if t==2 else K8;sl=2<t<6
   for df,dr in ds:
    if t==3 and not(df and dr):continue
    if t==4 and df and dr:continue
    f2,r2=fi,ri
    while 1:
     f2+=df;r2+=dr
     if not(0<=f2<8 and 0<=r2<8):break
     to=r2*8+f2
     if b[to]:
      if(b[to]>0)!=(s>0):ms.append((i,to,0))
      break
     if not cap:ms.append((i,to,0))
     if not sl:break
   if t==6 and not cap and i==(60 if s>0 else 4):
    bt=1 if s>0 else 4
    if cs&bt and not b[i+1]and not b[i+2]and b[i+3]==4*s:ms.append((i,i+2,0))
    if cs&bt*2 and not b[i-1]and not b[i-2]and not b[i-3]and b[i-4]==4*s:ms.append((i,i-2,0))
 return ms
def mk(b,m,cs,ep):
 frm,to,pr=m;p=b[frm];b=b[:]
 if abs(p)==1 and to==ep and not b[to]and frm%8!=to%8:b[to+(8 if p>0 else-8)]=0
 b[to]=pr*(p//abs(p))if pr else p;b[frm]=0
 if abs(p)==6 and abs(to-frm)==2:
  d=1 if to>frm else-1;o=frm+(3 if d>0 else 4)*d;b[frm+d]=b[o];b[o]=0
 nc=cs
 for sq in(frm,to):nc&=~{0:8,7:4,56:2,63:1}.get(sq,0)
 if abs(p)==6:nc&=12 if p>0 else 3
 ne=(frm+to)//2 if abs(p)==1 and abs(to-frm)==16 else-1
 return b,nc,ne
def leg(b,s,cs,ep,cap=0):
 return[(y[0],m,y[1],y[2])for m in gen(b,s,cs,ep,cap)if not atk((y:=mk(b,m,cs,ep))[0],y[0].index(6*s),-s)]
def evl(b):
 eg=5 not in b and-5 not in b;s=0
 for i,p in enumerate(b):
  if not p:continue
  t=abs(p);fi,ri=i%8,i//8
  if p<0:ri=7-ri
  cf=int(3.5-abs(3.5-fi));ci=cf+int(3.5-abs(3.5-ri))
  bo=[0,6*(6-ri),ci*6,ci*4,0,0,ci*8 if eg else-ci*5][t]
  s+=(VL[t]+bo)*(p//t)
 return s
def okey(b,m):
 frm,to,pr=m;v=0
 if b[to]:v=10*VL[abs(b[to])]-VL[abs(b[frm])]
 if pr:v+=900+VL[pr]
 return-v
def sr(b,s,cs,ep,d,a,be):
 global nd;nd+=1
 if nd>24000:raise Ab
 if d<=0:
  st=evl(b)*s
  if st>=be:return be
  if st>a:a=st
 ms=leg(b,s,cs,ep,1 if d<=0 else 0)
 if not ms:
  return a if d<=0 else(-100000 if atk(b,b.index(6*s),-s)else 0)
 ms.sort(key=lambda x:okey(b,x[1]));bst=a if d<=0 else-10**9
 for nb,m,nc,ne in ms:
  sc=-sr(nb,-s,nc,ne,d-1,-be,-a)
  if sc>bst:bst=sc
  if sc>a:a=sc
  if a>=be:break
 return bst
def uci(m):
 frm,to,pr=m
 return chr(97+frm%8)+str(8-frm//8)+chr(97+to%8)+str(8-to//8)+("nbrq"[pr-2]if pr else"")
def choose(fen):
 global nd
 b,s,cs,ep=parse(fen);ms=leg(b,s,cs,ep)
 nd=0;best=ms[0][1];a=-10**9
 try:
  for nb,m,nc,ne in sorted(ms,key=lambda x:okey(b,x[1])):
   sc=-sr(nb,-s,nc,ne,4,-10**9,-a)
   if sc>a:a,best=sc,m
 except Ab:pass
 return uci(best)
while 1:
 g=post("/game",{})
 if g.get("status")=="done":break
 while g.get("status")=="your_move":
  mv=choose(g["fen"]);lm=g["legal_moves"]
  g=post("/move",{"game":g["game"],"move":mv if mv in lm else lm[0]})
