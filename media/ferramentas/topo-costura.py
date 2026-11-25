# Versão 3: o cenário segue exatamente o movimento medido na borda do vídeo (fluxo denso DIS), linha a linha, suavizado
import cv2, numpy as np, subprocess, sys
from scipy.ndimage import gaussian_filter1d, gaussian_filter
VID='/home/claude/ondao-main/media/originais/01-topo-video-telemovel.mp4'
cap=cv2.VideoCapture(VID); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(f)
g=[cv2.cvtColor(f,cv2.COLOR_BGR2GRAY) for f in fr]; h,w=g[0].shape; N=len(g)
dis=cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
L=np.zeros((N,h,2),np.float32); R=np.zeros((N,h,2),np.float32)
for i in range(1,N):
    fl=dis.calc(g[0],g[i],None)
    L[i]=np.median(fl[:,4:110,:],axis=1); R[i]=np.median(fl[:,w-110:w-4,:],axis=1)
# suavizar em y (sem rasgos) e no tempo (sem tremer)
for A in (L,R):
    A[:]=gaussian_filter1d(A,25,axis=1,mode='nearest'); A[:]=gaussian_filter1d(A,1.5,axis=0,mode='nearest'); A[0]=0
np.save('L.npy',L); np.save('R.npy',R)
print('esq dx min/max',L[...,0].min().round(1),L[...,0].max().round(1),' dir',R[...,0].min().round(1),R[...,0].max().round(1))
S=1.42; OX,OY=1174.0,14.0
bg=cv2.imread('bg.jpg'); H,W=bg.shape[:2]
gx,gy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
ys=OY+S*np.arange(h); yc=np.arange(H)
wx=np.clip((gx-OX)/(S*w),0,1)
hsv=cv2.cvtColor(bg,cv2.COLOR_BGR2HSV).astype(np.float32)
veg=((hsv[...,0]>25)&(hsv[...,0]<95)&(hsv[...,1]>40)).astype(np.float32)
yy=np.linspace(0,1,H,dtype=np.float32)[:,None]; veg*=np.clip((yy-0.30)/0.2,0,1); veg=cv2.GaussianBlur(veg,(0,0),9)
rng=np.random.default_rng(3)
def campo(sig):
    f=cv2.GaussianBlur(rng.random((H,W)).astype(np.float32),(0,0),sig); return (f-f.mean())/(f.std()+1e-6)
ph1=campo(60)*1.6; ph2=campo(25)*2.2
L0=fr[0][60:h-60,0:120].reshape(-1,3).astype(np.float32).mean(0); R0=fr[0][60:h-60,w-120:w].reshape(-1,3).astype(np.float32).mean(0)
saida=sys.argv[1] if len(sys.argv)>1 else 'bg-costura.mp4'
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p',saida],stdin=subprocess.PIPE)
T=N/24
for i in range(N):
    lx=np.interp(yc,ys,L[i,:,0])*S; ly=np.interp(yc,ys,L[i,:,1])*S
    rx=np.interp(yc,ys,R[i,:,0])*S; ry=np.interp(yc,ys,R[i,:,1])*S
    dx=(lx[:,None]*(1-wx)+rx[:,None]*wx).astype(np.float32); dy=(ly[:,None]*(1-wx)+ry[:,None]*wx).astype(np.float32)
    t=i/24; wv=2*np.pi*t/T
    vx=veg*(1.2*np.sin(wv*2+ph1)+0.4*np.sin(wv*5+ph2))
    out=cv2.remap(bg,gx-dx+vx,gy-dy,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT).astype(np.float32)
    f=fr[i].astype(np.float32)
    gl=f[60:h-60,0:120].reshape(-1,3).mean(0)/L0; gr=f[60:h-60,w-120:w].reshape(-1,3).mean(0)/R0
    gain=gl[None,None,:]*(1-wx[...,None])+gr[None,None,:]*wx[...,None]
    p.stdin.write(np.clip(out*gain,0,255).astype(np.uint8).tobytes())
p.stdin.close(); p.wait(); print('ok')
