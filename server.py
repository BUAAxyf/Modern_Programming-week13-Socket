import socket,os,time
from threading import Thread

class Manager():
    '''
    服务器，管理成员进入和离开聊天室，接收成员消息并广播
    '''
    def __init__(self,socket,ip,port,username='default'):
        self.socket=socket
        self.ip=ip
        self.port=port
        self.id=ip+':'+str(port)
        self.username=username
        log_path=os.path.join(os.getcwd(),'server_log.txt')
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
        print(text)
        print('--------------------------------------------')

    def AddClient(m):
        '''
        连接client
        '''
        m.Log('ip {} is trying to connect'.format(m.id))
        m.username=m.Receive()
        Manager.broadcast('{}({})has been connected'.format(m.username,m.id))
        clinets_data[m.username]=m.id

    def Receive(self,max=64):
        '''
        接收信息
        '''
        text=self.socket.recv(max).decode('utf8')
        self.Log(text+'\n'+'Server receives from <'+self.username+'>')
        return text
        
    def Send(self,text):
        '''
        发送信息
        '''
        self.socket.send(text.encode('utf8'))
        self.Log(text+'\n'+'#Server sends to <'+self.username+'>')

    def broadcast(text):
        '''
        广播消息
        '''
        for client in clients.values():
            client.Send(text)
        #不用Log，Send会Log
        #self.Log(text)

    def chat(m):
        '''
        实现聊天功能
        '''
        Manager.AddClient(m)
        while True:
            text=m.Receive()
            if text.split(':')[3]==' quit':#退出
                break
            elif text.split('>>>',1)[1].split(':',1)[1][1]=='@':#定向转发
                m.Send(text)
                target_name=text.split('>>>',1)[1].split(':',1)[1].split()[0][1:]
                if target_name not in clinets_data:
                    sender=text.split('>>>',1)[1].split(':',1)[0]
                    clients[clinets_data[sender]].Send("Can't find {} in clients".format(target_name))
                else:
                    clients[clinets_data[target_name]].Send(text)
            else:
                Manager.broadcast(text)
        m.Log(m.username+'({}) has disconnceted'.format(m.id))
        clients.pop(m.id)
        m.socket.close()

if __name__=='__main__':
    IP='127.0.0.1'
    PORT=7060#端口号
    clients={}#在线client{id:Manager}
    clinets_data={}#client数据{username:id}

    ServerSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.bind((IP,PORT))
    #开始监听
    ServerSocket.listen(64)
    print('server is listening...')
    print('server is listening to {}'.format(ServerSocket.getsockname()))
    while True:
        DataSocket,addr=ServerSocket.accept()
        m=Manager(DataSocket,addr[0],addr[1])
        clients[m.id]=m
        t=Thread(target=Manager.chat,args=(m,))
        t.start()
    print('server has been closed')
