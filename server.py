from bluetooth import *
from time import sleep
import math
import threading
import sys
#import user
#import converter
from user import User
from user import UserDao
from converter import GetUsersConverter


#TODO: count connections and prevent by maxConnections new creation on sockets.
# remove socket from list when connection is canceled from client. -> use map with key which contains uuid from client (client_info)

class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.__maxConnections = 5
        #self.__current_connections = 0
        self.__connectionList = []
        self.__uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.__close_connection = False
        self.__server_socket = None
            
    def run(self):        
         self.__connect_request()

    def __connect_request(self):
        self.__init_bluetooth()
        self.__server_socket.settimeout(10)
        try:
            while self.__close_connection == False:
                print("listen")
                client_socket, client_info = self.__server_socket.accept()
                print("Accepted connection from", client_info)
                self.__start_new_connectionthread(client_socket)
        except:
            print("exit while")    
             
    def __init_bluetooth(self):
        self.__server_socket = BluetoothSocket(RFCOMM)
        self.__server_socket.bind(("",PORT_ANY))
        self.__server_socket.listen(self.__maxConnections)
        advertise_service(self.__server_socket, "SmartMirror", 
                          service_id = self.__uuid,
                          service_classes = [self.__uuid, SERIAL_PORT_CLASS],
                          profiles = [SERIAL_PORT_PROFILE])        
            
    def __start_new_connectionthread(self, client_socket):
         conn = self.Connection(client_socket)
         conn.start()
         self.__connectionList.append(conn)
         
    class Connection(threading.Thread):
        OK = "OK"
        FAILURE = "FAILURE"
        def __init__(self, socket):
            threading.Thread.__init__(self)
            self.__socket = socket
            self.__socket.settimeout(50000)
            self.close_connection = False
            self.__request_options = {"GETUSERS" : self.__getusers,
                                      "DELETEUSER" : self.__deleteuser,
                                      "ADDPICTURE" : self.__addpicture,
                                      "GETWIDGETS" : self.__getwidgets,
                                      "UPDATEWIDGETS" : self.__updatewidgets,
                                      "NEWUSER" : self.__newuser,
                                      "CANCELCONNECTION" : self.__cancelconnection}
            self.__kind_of_request = "NONE"
            self.__specific_progress = "NONE"
            self.__decoded_data = ""
        def run(self):
            try:
                while self.close_connection == False:
                    data = self.__socket.recv(1024)
                    self.__decoded_data = data.decode('utf-8')
                    if self.__kind_of_request == "NONE":
                        self.__kind_of_request = self.__decoded_data
                    self.__request_options[self.__kind_of_request]()
            except IOError:
                pass  
            finally:
                self.__socket.close()          
        
        def __getusers(self):
            dao = UserDao()
            converter = GetUsersConverter()
            self.__socket.send(converter.get_json(dao.get_users()))
            self.__reset_request()
        
        def __deleteuser(self):
            self.__reset_request()
        
        def __addpicture(self):
            self.__reset_request()
        
        def __getwidgets(self):
            self.__reset_request()
        
        def __updatewidgets(self):
            self.__reset_request()
        
        def __newuser(self):
            if self.__kind_of_request == "NONE":
                self.__socket.send(OK)
                self.__kind_of_request = "SENDOK"
            if self.__kind_of_request == "SENDOK":
                converter = GetUsersConverter()
                user = converter.get_user(self.__decoded_data)  
                dao = UserDao()
                if dao.new_user(user) == True:
                    self.__socket.send(OK)
                else:        
                    self.__socket.send(FAILURE)
                self.__reset_request()
                    
        def __cancelconnection(self):
            self.__reset_request()
        
        def __send_header(self, toSend):
            header = str(len(toSend)) + 'H'
            self.__socket.send(header)
            
        def __reset_request(self):
            self.__kind_of_request = "NONE"    
            self.__specific_progress = "NONE"
            
            
            
            
#######################################
###              Tests              ###
#######################################

def test_start_stop_server():
    server = Server()
    server.start()
 #   if 'e' == input("Exit  "):
 #       server.close_connection()
 #       print("deactivated")    

def test_get_users():
    pass

test_start_stop_server()




