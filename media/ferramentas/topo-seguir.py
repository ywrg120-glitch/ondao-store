# O cenário prolongado passa a seguir o movimento e a luz do vídeo do telemóvel (frame a frame)
import cv2, numpy as np, subprocess
VID='/home/claude/ondao-main/media/originais/01-topo-video-telemovel.mp4'
bg=cv2.imread('bg.jpg').astype(np.float32); H,W=bg.shape[:2]
S=1.42; OX,OY=1174,14
cap=cv2.VideoCapture(VID); fr=[]
while True:
    ok,f=cap.read()
    if not ok: break
    fr.append(f)
g=[cv2.cvtColor(f,cv2.COLOR_BGR2GRAY) for f in fr]; vh,vw=g[0].shape
N=len(fr)
# vento na vegetação (como antes)
hsv=cv2.cvtColor(bg.astype(np.uint8),cv2.COLOR_BGR2HSV).astype(np.float32)
veg=((hsv[...,0]>25)&(hsv[...,0]<95)&(hsv[...,1]>40)).astype(np.float32)
yy=np.linspace(0,1,H,dtype=np.float32)[:,None]
veg*=np.clip((yy-0.30)/0.2,0,1); veg=cv2.GaussianBlur(veg,(0,0),9)
rng=np.random.default_rng(3)
def campo(sig):
    f=cv2.GaussianBlur(rng.random((H,W)).astype(np.float32),(0,0),sig); return (f-f.mean())/(f.std()+1e-6)
ph1=campo(60)*1.6; ph2=campo(25)*2.2
amp=veg*(1.0+0.6*np.clip((yy-0.5)*2,0,1))
gx,gy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
# pesos em x: lado esquerdo segue a faixa esquerda do vídeo, lado direito a faixa direita
wx=np.clip((gx-OX)/(S*vw),0,1)
def perfil(flow, x0,x1):
    # média do fluxo por linha na faixa, suavizada, levada para a escala do ecrã
    col=flow[:,x0:x1,:].mean(1)                       # (vh,2)
    col=cv2.GaussianBlur(col.reshape(-1,1,2),(1,0),sigmaX=0,sigmaY=40).reshape(-1,2)
    ys=OY+S*np.arange(vh); yc=np.arange(H)
    dx=np.interp(yc,ys,col[:,0])*S; dy=np.interp(yc,ys,col[:,1])*S
    return dx.astype(np.float32)[:,None], dy.astype(np.float32)[:,None]
def luz(f,x0,x1): return f[60:vh-60,x0:x1].reshape(-1,3).mean(0)
L0=luz(fr[0].astype(np.float32),0,120); R0=luz(fr[0].astype(np.float32),vw-120,vw)
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','bg-segue.mp4'],stdin=subprocess.PIPE)
T=N/24.0
for i in range(N):
    fl=cv2.calcOpticalFlowFarneback(g[0],g[i],None,0.5,4,31,3,5,1.2,0) if i else np.zeros((vh,vw,2),np.float32)
    lx,ly=perfil(fl,0,160); rx,ry=perfil(fl,vw-140,vw)
    dx=lx*(1-wx)+rx*wx; dy=ly*(1-wx)+ry*wx
    t=i/24.0; w=2*np.pi*t/T
    vx=amp*(3.2*np.sin(w*2+ph1)+1.1*np.sin(w*5+ph2)); vy=amp*(0.8*np.sin(w*2+ph1+1.3))
    out=cv2.remap(bg,(gx-dx+vx).astype(np.float32),(gy-dy+vy).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    f=fr[i].astype(np.float32)
    gl=luz(f,0,120)/L0; gr=luz(f,vw-120,vw)/R0
    gain=gl[None,None,:]*(1-wx[...,None])+gr[None,None,:]*wx[...,None]
    out=np.clip(out*gain,0,255).astype(np.uint8)
    p.stdin.write(out.tobytes())
p.stdin.close(); p.wait(); print('ok',N)
