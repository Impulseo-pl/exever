from PIL import Image, ImageOps
import os
K='kat/'; O='of/'; OUT='../img2/'
def load(p):
    i=Image.open(p)
    if i.mode=='CMYK': i=i.convert('RGB')
    return ImageOps.exif_transpose(i).convert('RGB')
def save(im,name,sizes=(720,1400,2000),q=80):
    w=im.width
    res=[]
    for s in sizes:
        if s>=w: s=w
        t=im.resize((s,round(im.height*s/w)),Image.LANCZOS) if s<w else im
        fn=f'{name}-{s}.webp'; t.save(OUT+fn,'WEBP',quality=q,method=6); res.append((fn,t.size))
        if s==w: break
    print(name,im.size,[r[0] for r in res])
jobs={
 'dom-narozny':(K+'k9-1.jpg',(430,0,1879,1840)),
 'dom-plac':(K+'k2.jpg',(0,120,1480,1960)),
 'dom-dlugi':(K+'k5-1.jpg',(320,20,1879,940)),
 'elewacja':(K+'k3-1.jpg',(330,0,1879,1900)),
 'szkielet-hala':(K+'k7-1.jpg',(370,0,1879,1971)),
 'welna':(K+'k4.jpg',(0,0,1500,1971)),
 'osb':(K+'k5-1.jpg',(480,1060,1879,1960)),
 'wnetrze':(K+'k8.jpg',(0,0,1390,1971)),
 'hala-kurierska':(O+'1751374470094-crop-img-20230119-155049.jpg',None),
 'hala-przenosniki':(O+'1751374523746-crop-img-20230119-154802.jpg',None),
 'rozdzielnia':(O+'1751374495257-crop-img-20220604-125201.jpg',None),
 'budynek-wielorodzinny':(O+'1751374545072-crop-img-20230718-102816.jpg',None),
 'resort':(O+'1751374663598-crop-img-20210518-161256.jpg',None),
 'kotly':(O+'1752756188090-crop-1000032533.jpg',None),
 'kotlownia':(O+'1752756190691-crop-1000032534.jpg',None),
}
for n,(p,box) in jobs.items():
    im=load(p)
    if box: im=im.crop(box)
    save(im,n)
# przekroj sciany
im=load(K+'k6.jpg'); 
g=im.convert('L').point(lambda v:255 if v<245 else 0); bb=g.getbbox(); print('k6 bbox',bb)
pad=40; im=im.crop((max(0,bb[0]-pad),max(0,bb[1]-pad),min(im.width,bb[2]+pad),min(im.height,bb[3]+pad)))
save(im,'przekroj',(900,1400))
