import cv2, numpy as np, subprocess
bg=cv2.imread('bg.jpg'); H,W=bg.shape[:2]
hsv=cv2.cvtColor(bg,cv2.COLOR_BGR2HSV).astype(np.float32)
h,s,v=hsv[...,0],hsv[...,1],hsv[...,2]
veg=((h>25)&(h<95)&(s>40)).astype(np.float32)          # tons verdes/oliva = vegetação
yy=np.linspace(0,1,H)[:,None]
veg*=np.clip((yy-0.30)/0.2,0,1)                         # arribas lá em cima ficam quietas
veg=cv2.GaussianBlur(veg,(0,0),9)
rng=np.random.default_rng(3)
def campo(sig): 
    f=cv2.GaussianBlur(rng.random((H,W)).astype(np.float32),(0,0),sig); f=(f-f.mean())/(f.std()+1e-6); return f
ph1=campo(60)*1.6; ph2=campo(25)*2.2
T=8.0417; N=193
gx,gy=np.meshgrid(np.arange(W,dtype=np.float32),np.arange(H,dtype=np.float32))
amp=veg*(1.0+0.6*np.clip((yy-0.5)*2,0,1))               # mais perto = mexe mais
p=subprocess.Popen(['ffmpeg','-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r','24','-i','-','-c:v','libx264','-preset','medium','-crf','16','-pix_fmt','yuv420p','bg-vento.mp4'],stdin=subprocess.PIPE)
for i in range(N):
    t=i/24.0; w=2*np.pi*t/T
    dx=amp*(3.2*np.sin(w*2+ph1)+1.1*np.sin(w*5+ph2))     # balanço lento + tremido de rajada
    dy=amp*(0.8*np.sin(w*2+ph1+1.3))
    fr=cv2.remap(bg,(gx+dx).astype(np.float32),(gy+dy).astype(np.float32),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
    p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
cv2.imwrite('veg.png',(veg*255).astype(np.uint8))
