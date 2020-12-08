import numpy as np
from tkinter import *
from queue import Queue
import threading
import time
from time import sleep
import random
from tkinter import messagebox

#gui thing
root=0
textCol=['#81fd81','#81fd81']
leftP=[12,12]
CID=[[-1]*8 for i in range(8)]
pcol=['white','#8B4513']
poutLine=["#caa472","#caa472"]
swCol=['black','black']
response1=False
posMov=[]
myMove=((-1,-1),(-1,-1))
statusText=[-1,-1]
executing=False
#agent thing
draw=0
utility2={'king':5,'kill':100,'gameEnd':10000}

mat=[[(-1,0)]*8]*8 #cbutton(0,1,-1),king(0,1)
mxDep=4
def wt(t):
    now=time.time()
    future=now+t
    while time.time()<future:
        pass
def pri():
    for i in range(8):
        for j in range(8):
            print(mat[i][j],end="")
        print()
def op(col):
    if col==0:
        return 1
    else:
        return 0
def initilize():
    global mat
    mat=[[(-1,0)]*8]*8
    temp=np.array(mat)
    for i in range(3):
        for j in range(0,8,2):
            if i%2==0:
                k=j+1
                temp[i][k][0]=0
            else:
                temp[i][j][0]=0
    for i in range(5,8):
        for j in range(0,8,2):
            if i%2==0:
                k=j+1
                temp[i][k][0]=1
            else:
                temp[i][j][0]=1
    '''
    for i in range(8):
        for j in range(8):
            print(temp[i][j][1],end=" ")
        print()
    '''
    mat=temp.tolist()

#pos=((x,y),color,king?)


class EnviornMent():
    @staticmethod
    def validMove(pos):
        up=pos[1]|pos[2]
        dow=(op(pos[1]))|pos[2]
        ret=[]
        x,y=pos[0]
        if up: 
            if x-1>=0 and  y+1<8:
                    if mat[x-1][y+1][0]<0:
                            ret.append((x-1,y+1))
                    elif op(pos[1])==mat[x-1][y+1][0]:
                            if x-2>=0 and y+2<8:
                                    if mat[x-2][y+2][0]<0:
                                            ret.append((x-2,y+2))
            if x-1>=0 and y-1>=0:
                    if mat[x-1][y-1][0]<0:
                            ret.append((x-1,y-1))
                    elif op(pos[1])==mat[x-1][y-1][0]:
                            if x-2>=0 and y-2>=0:
                                    if mat[x-2][y-2][0]<0:
                                            ret.append((x-2,y-2))
        if dow:
            if x+1<8 and y+1<8:
                if mat[x+1][y+1][0]<0:
                    ret.append((x+1,y+1))
                elif op(pos[1])==mat[x+1][y+1][0]:
                    if x+2<8 and y+2<8:
                        if mat[x+2][y+2][0]<0:
                            ret.append((x+2,y+2))
                            jump2=True
            if x+1<8 and y-1>=0:
                if mat[x+1][y-1][0]<0:
                    ret.append((x+1,y-1))
                elif op(pos[1])==mat[x+1][y-1][0]:
                    if x+2<8 and y-2>=0:
                        if mat[x+2][y-2][0]<0:
                            ret.append((x+2,y-2))
        return ret
    @staticmethod
    def ret1s():
        ret=[]
        for i in range(8):
            for j in range(8):
                if mat[i][j][0]==1:
                    temp=((i,j),1,mat[i][j][1])
                    ret.append(temp)
        return ret
    @staticmethod
    def ret0s():
        ret=[]
        for i in range(8):
            for j in range(8):
                if mat[i][j][0]==0:
                    temp=((i,j),0,mat[i][j][1])
                    ret.append(temp)
        #print(len(ret))
        return ret
    
    @staticmethod
    def numberOFmoves(player,weit):
        if player==0:
            ret=0
            pos0=EnviornMent.ret0s()
            totalMv=0
            pos1=EnviornMent.ret1s()
            if len(pos0)==0:
                return -utility2['gameEnd']
            if len(pos1)==0:
                return utility2['gameEnd']
            templ=[]
            for i in pos0:
                minD=np.inf
                for j in pos1:
                    minD=min(minD,abs(i[0][0]-j[0][0]))
                templ.append(minD)
            templ.sort()
            ret+=(8-templ[len(templ)-1])*0.1
            k0=0
            k1=0
            for i in pos1:
                if i[2]==1:
                    k1+=1
            for i in pos0:
                if i[2]==1:
                    k0+=1
            p0=len(pos0)-k0
            p1=len(pos1)-k1
            ret+=((k1-k0)*(utility2['king']+utility2['kill']))
            ret+=((p1-p0)*utility2['kill'])

            '''
            for i in pos:
                totalMv+=len(EnviornMent.validMove(i))
            return totalMv*weit
            '''
            return ret
        if player==1:
            ret=0
            pos0=EnviornMent.ret0s()
            totalMv=0
            pos1=EnviornMent.ret1s()
            templ=[]
            if len(pos0)==0:
                return utility2['gameEnd']
            if len(pos1)==0:
                return -utility2['gameEnd']
            for i in pos1:
                minD=np.inf
                for j in pos0:
                    minD=min(minD,abs(i[0][0]-j[0][0]))
                templ.append(minD)
            templ.sort()
            ret+= (-(8-templ[len(templ)-1])*0.1)
            k0=0
            k1=0
            for i in pos1:
                if i[2]==1:
                    k1+=1
            for i in pos0:
                if i[2]==1:
                    k0+=1
            p0=len(pos0)-k0
            p1=len(pos1)-k1
            ret+=((k0-k1)*-(utility2['king']+utility2['kill']))
            ret+=((p0-p1)*-(utility2['kill']))
            return ret
    @staticmethod
    def makeChange(mv):
        global mat
        global draw
        x,y=mv[0]
        x1,y1=mv[1]
        player=mv[2]
        if abs(x-x1)==2:
            leftP[op(player)]-=1
        if player==0:
            if abs(x-x1)==2:
                draw=0
                mat[x][y][0]=-1
                midx,midy=(int((x+x1)/2),int((y+y1)/2))
                mat[midx][midy][0]=-1
                mat[x1][y1][0]=0
                if x1==0 or x1==7 or mat[x][y][1]==1:
                    mat[x1][y1][1]=1
                else:
                    mat[x1][y1][1]=0
                mat[x][y][1]=0
                mat[midx][midy][1]=0

            else:
                draw+=1
                mat[x][y][0]=-1
                mat[x1][y1][0]=0
                if x1==0 or x1==7 or mat[x][y][1]==1:
                    mat[x1][y1][1]=1
                else:
                    mat[x1][y1][1]=0
                mat[x][y][1]=0
        else:
            if abs(x-x1)==2:
                draw=0
                mat[x][y][0]=-1
                midx,midy=(int((x+x1)/2),int((y+y1)/2))
                mat[midx][midy][0]=-1
                mat[x1][y1][0]=1
                if x1==0 or x1==7 or mat[x][y][1]==1:
                    mat[x1][y1][1]=1
                else:
                    mat[x1][y1][1]=0
                mat[x][y][1]=0
                mat[midx][midy][1]=0
            else:
                draw+=1
                mat[x][y][0]=-1
                mat[x1][y1][0]=1
                if x1==0 or x1==7 or mat[x][y][1]==1:
                    mat[x1][y1][1]=1
                else:
                    mat[x1][y1][1]=0
                mat[x][y][1]=0
        if draw>100:
            showRes("100 moves without kill ,match draw")
class agent():
    @staticmethod
    def efMove(turn,alpha,beta,dep):
        global mat
        movePiece=((-1,-1),(-1,-1))
        if dep>mxDep:
            return (EnviornMent.numberOFmoves(turn,0),movePiece)
        if turn:
            if whoWins()==0:
                return (-utility2['gameEnd'],movePiece)
            elif whoWins()==1:
                return (utility2['gameEnd'],movePiece)
            pos1=EnviornMent.ret1s()
            finRet=-np.inf
            if len(pos1)==0:
                return (-utility2['gameEnd'],movePiece)
            for pos in pos1:
                x,y=pos[0]
                mv=EnviornMent.validMove(pos)
                ret=-np.inf
                moveTemp=((-1,-1),(-1,-1))
                for i in mv:
                    
                    x1,y1=i
                    #print(pos[0],i)
                    if abs(x-x1)==2:
                        king=mat[x][y][1]
                        if x1==0 or x1==7:
                            king=1
                        midx,midy=(int((x1+x)/2),int((y1+y)/2))
                
                        mat[x][y][0]=-1
                        mat[midx][midy][0]=-1
                        mat[x1][y1][0]=1
                        preKing=[mat[x][y][1],mat[midx][midy][1],mat[x1][y1][1]]
                        mat[x][y][1]=0
                        mat[midx][midy][1]=0
                        mat[x1][y1][1]=king
                        temp,something=agent.efMove(0,alpha,beta,dep+1)

                        #temp+=utility2['kill']
                        if temp>ret:
                            ret=temp
                            moveTemp=((x,y),(x1,y1))
                        mat[x][y][0]=1
                        mat[midx][midy][0]=0
                        mat[x1][y1][0]=-1

                        mat[x][y][1]=preKing[0]
                        mat[midx][midy][1]=preKing[1]
                        mat[x1][y1][1]=preKing[2]
                        


                    else:
                        king=pos[2]
                        
                        if x1==0 or x1==7:
                            king=1



                        mat[x][y][0]=-1
                        mat[x1][y1][0]=1
                        preKing=[mat[x][y][1],mat[x1][y1][1]]
                        mat[x1][y1][1]=king
                        temp,something=agent.efMove(0,alpha,beta,1+dep)
                        '''
                        if king==1 and preKing[0]==0:
                            temp+=2
                        '''
                        if temp>ret:
                            ret=temp
                            moveTemp=((x,y),(x1,y1))
                        mat[x][y][0]=1
                        mat[x1][y1][0]=-1

                        mat[x][y][1]=preKing[0]
                        mat[x1][y1][1]=preKing[1]
                     

               
                if finRet<ret:
                    finRet=ret
                    movePiece=moveTemp
                    alpha=finRet
                #print(alpha,beta)
                if finRet>beta:
                    return (finRet,movePiece)
            
            return (finRet,movePiece)
        else:
            if whoWins()==0:
                return (utility2['gameEnd'],movePiece)
            elif whoWins()==1:
                return (-utility2['gameEnd'],movePiece)
            pos0=EnviornMent.ret0s()
            if len(pos0)==0:
                return (utility2['gameEnd'],movePiece)
            finRet=np.inf
            for pos in pos0:
                x,y=pos[0]
                mv=EnviornMent.validMove(pos)
                ret=np.inf
                moveTemp=((-1,-1),(-1,-1))
                for i in mv:
                 
                    x1,y1=i
                    if abs(x-x1)==2:
                        king=pos[2]
                        if x1==0 or x1==7:
                            king=1


                        midx,midy=(int((x1+x)/2),int((y1+y)/2))
            
                        mat[x][y][0]=-1
                        mat[midx][midy][0]=-1
                        mat[x1][y1][0]=0

                        preKing=[mat[x][y][1],mat[midx][midy][1],mat[x1][y1][1]]

                        mat[x1][y1][1]=king
                        temp,something=agent.efMove(1,alpha,beta,1+dep)
                        '''
                        temp-=utility2['kill']
                        if king==1 and preKing[0]==0:
                            temp-=utility2['king']
                        '''

                        if temp<ret:
                            ret=temp
                            moveTemp=((x,y),(x1,y1))
                            
                        mat[x][y][0]=0
                        mat[midx][midy][0]=1
                        mat[x1][y1][0]=-1

                        mat[x][y][1]=preKing[0]
                        mat[midx][midy][1]=preKing[1]
                        mat[x1][y1][1]=preKing[2]
                        
                         


                    else:
                        king=pos[2]
                        
                        if x1==0 or x1==7:
                            king=1
                        
                        mat[x][y][0]=-1
                        mat[x1][y1][0]=0
                        preKing=[mat[x][y][1],mat[x1][y1][1]]
                        mat[x1][y1][1]=king
                        temp,something=agent.efMove(1,alpha,beta,1+dep)
                        '''
                        if king==1 and preKing[0]==0:
                            temp-=utility2['king']
                        '''
                        if temp<ret:
                            ret=temp
                            moveTemp=((x,y),(x1,y1))
                            
                        mat[x][y][0]=0
                        mat[x1][y1][0]=-1
                        mat[x][y][1]=preKing[0]
                        mat[x1][y1][1]=preKing[1]
                        
                            
                        


                
                if finRet>ret:
                    finRet=ret
                    movePiece=moveTemp
                    
                    beta=finRet
                if finRet<alpha:
                    return (finRet,movePiece)
            return (finRet,movePiece)



def computerMove():
    something=agent.efMove(0,-np.inf,np.inf,0)
    x,y=something[1][0]
    x1,y1=something[1][1]
    temp=((x,y),(x1,y1),0,mat[x][y][1])
    EnviornMent.makeChange(temp)
    temp=((x,y),(x1,y1),0,mat[x1][y1][1])
    l=getChanges(temp)
    root.after(3000)
    updateG1(l)
    if whoWins()==0:
        showRes("loose")
    elif whoWins()==1:
        showRes("win")
    statusText[0].updateText(str(12-leftP[1]))

#print(CID)
class canButton():
    def __init__(self, x, y, sz,can):
        self.rectID=can.create_rectangle(x,y,x+2*sz,y+(sz)/2,fill=pcol[1])
        x,y=(((x+x+2*sz)/2), ((y+y+(sz)/2)/2))
        self.tid=can.create_text(x,y,text='New Game',fill=textCol[0],font="Times 26 italic bold")
        can.tag_bind(self.tid,'<ButtonPress-1>',self.clicked1)
        can.tag_bind(self.rectID,'<ButtonPress-1>',self.clicked1)
    def clicked1(self,event):
        letsStartAgain()


class textCan():
    def __init__(self, x, y, sz,can):
        self.can=can
        #self.rectID=can.create_rectangle(x,y,x+sz,y+sz,fill='black')
        x,y=(((x+x+sz)/2),((y+y+sz)/2))
        r=0.85*(sz/2);
        self.cid=can.create_oval(x-r,y-r,x+r,y+r,width=10,fill="white",outline="#caa472",tags="playbutton")
        self.tid=can.create_text(x,y,text='0',fill=textCol[0],font="Times 40 italic bold")
    def fillCircle(self,col):
        self.can.itemconfigure(self.cid,fill=col,outline="#caa472")
    def updateText(self,msg):
        self.can.itemconfigure(self.tid,text=msg)


class circle():
  def __init__(self, x, y, r,can):
    self.can=can
    self.coord=(int(y/85),int(x/85))
    self.id=can.create_oval(x-r,y-r,x+r,y+r,width=10,fill="white",outline="#caa472",tags="playbutton")
    self.tid=can.create_text(x,y,text='k',fill='black',font="Times 40 italic bold")
    can.tag_bind(self.id,'<ButtonPress-1>',self.clicked1)
    #can.tag_bind(self.id,'<Button-3>',self.clicked2)
    can.tag_bind(self.tid,'<ButtonPress-1>',self.clicked1)
    #can.tag_bind(self.tid,'<Button-3>',self.clicked2)
    
  def clicked1(self,event):
    global executing
    global response1
    global posMov
    global myMove
    global mat
    if executing:
        #print("executing")
        return
    x1,y1=self.coord
    posTemp=(x1,y1)
    if response1 and posMov.count(posTemp)!=0:
        #print("stop 1")
        executing=True
        self.clicked2(posTemp)
    elif response1 and mat[x1][y1][0]!=1:
        #print("stop 2")
        for i in posMov:
            x,y=i
            CID[x][y].dehighLight()
    elif response1 and mat[x1][y1][0]==1:
        #print("stop 3")
        for i in posMov:
            x,y=i
            CID[x][y].dehighLight()
        response1=True
        x,y=self.coord
        pos=((x,y),mat[x][y][0],mat[x][y][1])
        posMov=EnviornMent.validMove(pos)
        myMove=((x,y),myMove[1])
        for i in posMov:
            x,y=i
            CID[x][y].highLight()
    elif mat[x1][y1][0]==1:
       #print("stop 4")
        response1=True
        x,y=self.coord
        pos=((x,y),mat[x][y][0],mat[x][y][1])
        posMov=EnviornMent.validMove(pos)
        myMove=((x,y),myMove[1])
        for i in posMov:
            x,y=i
            CID[x][y].highLight()

  def clicked2(self,mvCoord):
    global response1
    global posMov
    global myMove
    global executing
    if response1:
        x1,y1=mvCoord
        pos=(x1,y1)
        response1=False
        if True:
            x,y=myMove[0]
            temp=((x,y),(x1,y1),1,mat[x][y][1])
            EnviornMent.makeChange(temp)
            temp=((x,y),(x1,y1),1,mat[x1][y1][1])
            
            for i in  posMov:
                xt,yt=i
                CID[xt][yt].dehighLight()
            l=getChanges(temp)
            updateG1(l)

            if whoWins()==0:
                showRes("loose")
            elif whoWins()==1:
                showRes("win")
            statusText[1].updateText(str(12-leftP[0]))
            computerMove()
        posMov=[]
        executing=False

 

 






  def dehighLight(self):
    self.can.itemconfigure(self.id, outline='black')
  def highLight(self):
    self.can.itemconfigure(self.id, outline=textCol[0])

  def fillColor(self,col):
    self.can.itemconfigure(self.id,fill=col,outline="#caa472")
    self.can.itemconfigure(self.tid,fill=col)
  def setDark(self):
    self.can.itemconfigure(self.id, fill="black",outline="#caa472")
  def setLight(self):
    self.can.itemconfigure(self.id, fill="white",outline="#caa472")
  def setCLear(self,col):
    self.can.itemconfigure(self.id, fill=col)
  def makeBlank(self):
    self.can.itemconfigure(self.id, fill='black',outline='black')
    self.can.itemconfigure(self.tid, fill='black')
  def fillText(self,col):
    self.can.itemconfigure(self.tid, fill=col)


'''
def circle(x,y,r,w):
  return w.create_oval(x-r,y-r,x+r,y+r,width=10,fill="white",outline="#caa472")
'''
def drawRect(master,sqsz):
    global CID
    w = Canvas(master, width=12*sqsz, height=8*sqsz,bg="red")
    r=0.85*(sqsz/2)
    for i in range(8):
        for j in range(8):
            if i%2==0 and j%2==1:
                w.create_rectangle(sqsz*i, sqsz*j,sqsz*(i+1),sqsz*(j+1),fill="black")
            if i%2==1 and j%2==0:
                w.create_rectangle(sqsz*i, sqsz*j,sqsz*(i+1),sqsz*(j+1),fill="black")

      
      
    for i in range(8):
        for j in range(8):
            y=(sqsz*i+sqsz*(i+1))/2
            x=(sqsz*j+sqsz*(j+1))/2
            if mat[i][j][0]>=0:
                CID[i][j]=circle(x,y,r,w)
                CID[i][j].fillColor(pcol[mat[i][j][0]])
            else:
                if (i%2==0 and j%2==1) or (i%2==1 and j%2==0):
                    CID[i][j]=circle(x,y,r,w)
                    CID[i][j].makeBlank()
    statusText[0]=textCan(10*sqsz,sqsz,sqsz,w)
    statusText[0].fillCircle(pcol[1])
    statusText[1]=textCan(10*sqsz,6*sqsz,sqsz,w)
    temp=canButton(9.5*sqsz,3.5*sqsz,sqsz,w)
    w.create_line(8*sqsz+1,0,8*sqsz+1,8*sqsz,fill='white',width=2)
    w.pack()
def updateG1(ev):
    for l in ev:
        i,j=l[0]
        if l[1]==0:
            CID[i][j].fillColor(pcol[0])
            if l[2]==1:
                CID[i][j].fillText(textCol[0])
            else:
                CID[i][j].fillText(pcol[0])
        elif l[1]==1:
            CID[i][j].fillColor(pcol[1])
            if l[2]==1:
                CID[i][j].fillText(textCol[0])
            else:
                CID[i][j].fillText(pcol[1])
        else:
            CID[i][j].makeBlank()
        
   
        
def gui():
  global root
  master = Tk()
  root=master
  drawRect(master,85)
  mainloop()
  #updateG(master)



def getChanges(mv):
    x,y=mv[0]
    x1,y1=mv[1]
    player=mv[2]
    l=[]
    king=mv[3]
    if player==0:
        if abs(x-x1)==2:
            l.append(((x,y),-1,king))
            midx,midy=(int((x+x1)/2),int((y+y1)/2))
            l.append(((midx,midy),-1,king))
            l.append(((x1,y1),0,king))
        else:
            l.append(((x,y),-1,king))
            l.append(((x1,y1),0,king))
    else:
        if abs(x-x1)==2:
            l.append(((x,y),-1,king))
            midx,midy=(int((x+x1)/2),int((y+y1)/2))
            l.append(((midx,midy),-1,king))
            l.append(((x1,y1),1,king))
           
        else:
            l.append(((x,y),-1,king))
            l.append(((x1,y1),1,king))
    return l
def whoWins():
    numMv1=0
    numMv0=0
    pos=EnviornMent.ret0s()
    for i in pos:
        if len(EnviornMent.validMove(i))>0:
            numMv0=100
            break
    pos=EnviornMent.ret1s()
    for i in pos:
        if len(EnviornMent.validMove(i))>0:
            numMv1=100
            break
    if numMv1>0 and numMv0>0:
        return -1
    elif numMv0>0:
        return 0
    else:
        return 1

        

def showRes(msg):
    finalMessage="you"+" "+msg
    if msg=="loose":
        messagebox.showinfo("oops",finalMessage)
    elif msg=='win':
        messagebox.showinfo("hurray",finalMessage)
    else:
        messagebox.showinfo("hurray",msg)


    letsStartAgain()
def letsStartAgain():
    global draw
    global leftP
    global executing
    root.destroy()
    executing=False
    leftP=[12,12]
    draw=0
    initilize()
    gui()
if __name__ == '__main__':
    initilize()
    gui()

    
    