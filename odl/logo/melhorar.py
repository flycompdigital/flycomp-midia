import cv2,numpy as np
i=cv2.imread('odl-logo-original-baixa.jpg');H,W=i.shape[:2];S=4
hsv=cv2.cvtColor(i,cv2.COLOR_BGR2HSV)
core=hsv[...,2]>150
oc=np.median(i[core&(hsv[...,0]<40)],axis=0);cc=np.median(i[core&(hsv[...,0]>70)],axis=0);print(oc,cc)
v=cv2.resize(hsv[...,2].astype(np.float32),(W*S,H*S),interpolation=cv2.INTER_CUBIC)
v=cv2.GaussianBlur(v,(0,0),S*0.5)
m=np.clip((v-185)/22,0,1)  # soft threshold = antialiased edge
hue=cv2.resize(hsv[...,0].astype(np.float32),(W*S,H*S),interpolation=cv2.INTER_NEAREST)
hue=cv2.medianBlur(hue.astype(np.uint8),5)
# split by side: cyan only right half of head region; icons all orange -> use hue
isc=(hue>60)&(hue<120)
col=np.where(isc[...,None],cc,oc).astype(np.float32)
lines=m[...,None]*col
glow=cv2.GaussianBlur(lines,(0,0),S*9)*0.9+cv2.GaussianBlur(lines,(0,0),S*3)*0.45
out=np.clip(np.maximum(lines,0)+glow*(1-m[...,None]),0,255).astype(np.uint8)
cv2.imwrite('./odl-logo-alta.png',out)
# transparent version (lines only, no glow)
rgba=np.dstack([col.astype(np.uint8),(m*255).astype(np.uint8)])
cv2.imwrite('./odl-logo-transparente.png',rgba)
cv2.imwrite('./cmp.jpg',np.hstack([cv2.resize(i[350:750,250:650],(800,800),interpolation=cv2.INTER_CUBIC),cv2.resize(out[350*S:750*S,250*S:650*S],(800,800),interpolation=cv2.INTER_AREA)]))
print(out.shape)
