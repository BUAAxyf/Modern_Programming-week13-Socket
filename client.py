import socket,os,time
from threading import Thread

class Chatter():
    '''
    用户, 向管理员发送加入和退出请求，发送和接收消息
    '''
    def __init__(self,socket):
        self.socket=socket
        #默认以时间命名log
        log_path=os.path.join(os.getcwd(),'client_logs',str(time.strftime("%Y%m%d%H%M%S"))+'.txt')
        self.username=log_path.split('.')[-2].split('/')[-1]#用户名默认为初始化时间
        print('log_path: '+self.username)
        dir_path=os.path.dirname(log_path)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        if not os.path.exists(log_path):
            f=open(log_path,'w',encoding='utf8')
            f.close()
        self.log_path=log_path

    def Log(self,text):
        '''
        写日志
        '''
        with open(self.log_path,'a',encoding='utf8') as log:
            log.write(str(time.strftime("%Y/%m/%d %H:%M:%S"))+'\n')
            log.write(text+'\n')
            log.write('--------------------------------------------\n')

    def EnterName(self):
        '''
        输入username
        '''
        QUIT=False#上线
        self.username=input('Enter the username : ')
        while ':' in self.username or ' ' in self.username:
            print("Colons and spaces are not allowed")
            self.username=input('Enter the username again: ')
        self.socket.send((self.username).encode('utf8'))
        self.Log('username: {}'.format(self.username))

    def Send(c):
        '''
        发送信息
        '''
        while True:
            text=str(time.strftime("%Y/%m/%d %H:%M:%S"))+'>>>'+c.username+': '+input('')
            c.socket.send(text.encode('utf8'))
            c.Log('{}: '.format(c.username)+text)
            if text=='quit':
                QUIT=True
                break

    def Receive(c,max=64):
        '''
        接收信息
        '''
        while not QUIT:
            text=c.socket.recv(max).decode('utf8')
            c.Log(text)
            print(text)

if __name__=='__main__':
    IP='127.0.0.1'
    SERVER_PORT=7060

    ClientSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ClientSocket.connect((IP,SERVER_PORT))
    c=Chatter(ClientSocket)
    c.EnterName()
    QUIT=False#用以记录用户是否离线
    tr=Thread(target=Chatter.Receive,args=(c,))
    ts=Thread(target=Chatter.Send,args=(c,))
    tr.start()
    ts.start()
    tr.join()
    ts.join()
    print('you have disconnected')
    ClientSocket.close()
    