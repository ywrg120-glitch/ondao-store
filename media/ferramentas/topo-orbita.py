# O cenário prolongado acompanha o movimento de câmara do Seedance (paralaxe), em duas camadas: arribas e chão
import cv2, numpy as np, subprocess
from scipy.ndimage import gaussian_filter1d
VID='/home/claude/ondao-main/media/originais/01-topo-video-telemovel.mp4'
cap=cv2.VideoCapture(VID); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(f)
g=[cv2.cvtColor(f,cv2.COLOR_BGR2GRAY) for f in fr]; h,w=g[0].shape; N=len(g)
pessoa=np.full((h,w),255,np.uint8)
cv2.ellipse(pessoa,(w//2,int(h*0.42)),(int(w*0.31),int(h*0.31)),0,0,360,0,-1)
cv2.rectangle(pessoa,(int(w*0.12),int(h*0.55)),(int(w*0.92),h),0,-1)
def banda(y0,y1):
    m=pessoa.copy(); m[:int(h*y0)]=0; m[int(h*y1):]=0
    p0=cv2.goodFeaturesToTrack(g[0],600,0.004,7,mask=m)
    P=[]
    prev=p0; A_acc=[]
    for i in range(N):
        p1,st,_=cv2.calcOpticalFlowPyrLK(g[0],g[i],p0,None,winSize=(41,41),maxLevel=5)
        ok=st.ravel()==1
        A,_=cv2.estimateAffinePartial2D(p0[ok],p1[ok],method=cv2.RANSAC,ransacReprojThreshold=2.0)
        s=np.hypot(A[0,0],A[1,0]); r=np.arctan2(A[1,0],A[0,0])
        P.append([s,r,A[0,2],A[1,2]])
    P=np.array(P); P=gaussian_filter1d(P,2.0,axis=0,mode='nearest'); P[0]=[1,0,0,0]
    return P
cima=banda(0.0,0.50); baixo=banda(0.50,1.0)
print('cima tx range',cima[:,2].min().round(1),cima[:,2].max().round(1),' baixo',baixo[:,2].min().round(1),baixo[:,2].max().round(1))
def M(p):
    s,r,tx,ty=p; return np.array([[s*np.cos(r),-s*np.sin(r),tx],[s*np.sin(r),s*np.cos(r),ty]],np.float32)
S=1.42; OX,OY=1174.0,14.0
C=np.array([[S,0,OX],[0,S,OY],[0,0,1]],np.float32); Ci=np.linalg.inv(C)
def canvas(A):
    A3=np.vstack([A,[0,0,1]]); return (C@A3@Ci)[:2]
bg=cv2.imread('bg.jpg'); H,W=bg.shape[:2]
# peso vertical da camada de baixo (transição suave entre 40% e 70% da altura da imagem do vídeo, em coordenadas do ecrã)
yv=(np.arange(H)-OY)/S/h
wb=np.clip((yv-0.42)/0.25,0,1).astype(np.float32)[:,None,None]
# vento leve na vegetação (como antes, mais suave)
hsv=cv2.cvtColor(bg,cv2.COLOR_BGR2HSV).astype(np.float32)
veg=((hsv[...,0]>25)&(hsv[...,0]<95)&(hsv[...,1]>40)).astype(np.float32)
yy=np.linspace(0,1,H,dtype=np.float32)[:,None]; veg*=np.clip((yy-0.30)/0.2,0,1); veg=cv2.GaussianBlur(veg,(0,0),9)
rng=np.random.default_rng(3)
def campo(sig):
    f=cv2.GaussianBlur(rng.random((H,W)).astype(np.float32),(0,0),sig); return (f-f.mean())/(f.std()+1e-6)
ph1=campo(60)*1.6; ph2=campo(25)*2.2
gx,gy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
L0=fr[0][60:h-60,0:120].reshape(-1,3).astype(np.float32).mean(0)
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','bg-orbita.mp4'],stdin=subprocess.PIPE)
T=N/24
for i in range(N):
    t=i/24; wv=2*np.pi*t/T
    vx=veg*(1.6*np.sin(wv*2+ph1)+0.6*np.sin(wv*5+ph2))
    b=cv2.remap(bg,gx+vx,gy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    top=cv2.warpAffine(b,canvas(M(cima[i])),(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    bot=cv2.warpAffine(b,canvas(M(baixo[i])),(W,H),flags=cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    out=top*(1-wb)+bot*wb
    gain=fr[i][60:h-60,0:120].reshape(-1,3).astype(np.float32).mean(0)/L0
    out=np.clip(out*gain[None,None,:],0,255).astype(np.uint8)
    p.stdin.write(out.tobytes())
p.stdin.close(); p.wait(); print('ok')
