'''
python imgdb raw-tcp sdk

@author: ltmit
'''
import os
import time
import socket
import struct
import types
from cStringIO import StringIO
import pdb
import datetime
import threading
import numpy as np
import shutil

__all__ = ['ImgdbError','COLINFO_FLAG_HAS_DEFVAL','COLINFO_FLAG_NOT_NULL','COLINFO_FLAG_UNIQUE',
          'Api','loadfile_nt','loadfile'  ]

class ImgdbError(Exception):
    '''
        exception class for 'imgdb' sdk
    '''
    def __init__(self,errc,errs):
        self.errc = errc
        self.errs = errs
        
    def __str__(self):
        return repr(self.errc) + ','+ self.errs
    def __repr__(self):
        return 'ImgdbError:'+self.__str__()


COLINFO_FLAG_HAS_DEFVAL=1
COLINFO_FLAG_NOT_NULL=2
COLINFO_FLAG_UNIQUE=4

# (colname,datatype,defval,flag)
        
class Api:
    '''
        'ISE' raw-tcp api
    '''    
    #local static method
    __CMD_CREATE_DB =  1
    __CMD_DELETE_DB =  2
    __CMD_ENUM_ALL_DBS  = 3
    __CMD_SHOW_COL_INFO  =  5
    __CMD_SHOW_LOAD_DBS  =  101
    __CMD_UNLOAD_DB     =   102 
    __CMD_DB_ADD_COL     =  6
    __CMD_DB_RENAME_COL  =  7
    __CMD_DB_DEL_COL  = 8
    __CMD_PUSH_IMAGE_REC  =  10
    __CMD_PUSH_IMAGE_REC_V2  =  60
    __CMD_RETRIEVE_IMAGE_REC_V2  =  63
    __CMD_RETRIEVE_IMAGE_REC  =  11
    __CMD_SELECT_IMAGE_REC = 12
    __CMD_SELECT_IMAGE_REC_V2 = 64
    __CMD_UPDATE_IMAGE_REC =  13
    __CMD_DELETE_IMAGE_REC  =  14
    __CMD_SELECT_REC_COUNT   = 16
    __CMD_SHOW_COL_INFO_V2  = 17
    __CMD_PUSH_IMAGE_REC_CDVS =   18
    __CMD_DELETE_IMAGE_REC_WS =  21
    __CMD_UPDATE_IMAGE_REC_WS  =  22
    __CMD_REPLACE_IMAGE_REC  = 24
    __CMD_UPDATE_IMAGE_REC_WS2  =  26
    #__CMD_RETRIEVE_WITH_CDVS_FEAT  =  30
    #__CMD_SELECT_OFFLINE_INDEX = 31
    __CMD_EXTRACT_FEAT2 = 50
    __CMD_PUSH_IMAGE_FEAT2_V2 = 61
    __CMD_RETRIEVE_IMAGE_FEAT2_V2 = 62
    __CMD_SHOW_LOAD_DBS = 101
    __CMD_UNLOAD_DB = 102
    __CMD_GET_IMGREC_FEAT2 = 70
    __CMD_PUSH_IMAGE_IDX = 75
    __CMD_SELECT_OFFLINE_INDEX = 31
    __CMD_GET_DB_REC_CT  = 65
    __CMD_GET_DONGLE_KEY  = 103
    __CMD_ALLOC_TRUNK = 104
    __CMD_RETRIEVE_IMAGE_REC_WANT_FEATURE = 17
    def __connsock(self):
        s = None
        try:
            s=socket.create_connection(self.server_addr, self.conn_tmo/1000.0)
            s.setsockopt(socket.IPPROTO_TCP,socket.TCP_NODELAY,True)
            s.setblocking(True)
            return s
        except Exception as e:
            if s: s.close()
            raise ImgdbError(-1,str(e))
    
    @staticmethod
    def __pack_cmd(cmdid,content):
        return ''.join((struct.pack('<i', len(content)+4),struct.pack('<i',cmdid),content) )
    
    @staticmethod
    def __recv_all(sock,rcvlen):
        tmpbuf=StringIO(); off = 0
        try:
            while off<rcvlen:
                rbt= sock.recv( min(rcvlen-off,1024*1024) )
                if len(rbt)==0: break
                tmpbuf.write(rbt)
                off+=len(rbt)
            return tmpbuf.getvalue()
        finally:
            tmpbuf.close()
    @staticmethod
    def __sock_recv_cmd(sock):
        d = Api.__recv_all(sock, 4)#sock.recv(4)
        if len(d)<4: 
            raise ImgdbError(-10,'error recv cmd-len. recvbytes='+str(len(d)))
        cmdlen = struct.unpack('<i', d )[0]
        #print 'recv cmd-len=',cmdlen
        if cmdlen<0 or cmdlen > 100000000 :
            raise ImgdbError(-1,"error parse 'cmdlen' ")
        rbt= Api.__recv_all(sock,cmdlen) #sock.recv(cmdlen);
        if len(rbt)<cmdlen:
            raise ImgdbError(-3,'recv cmd partially! read='+str(len(rbt))+'when req='+str(cmdlen))
        return rbt
    
    @staticmethod
    def __sio_write(sio,*args):
        for i in args: sio.write(i)
        
    #type->lambda map
    __tfm = {types.IntType: lambda sio,val: sio.write(struct.pack('<i',val)) ,\
             types.FloatType: lambda sio,val: sio.write(struct.pack('<f',val)),\
             types.StringType: lambda sio,val: Api.__sio_write(sio,struct.pack('<i',len(val)),val),\
             types.LongType: lambda sio,val: sio.write(struct.pack('<q',val)) }
    
    class __SeqReader(object):
        def __init__(self, strv ,off=0):
            self.__str = strv
            self.__off = off
        def __readtype(self,typelen,fmt):
            tmp = self.__str[self.__off : self.__off+ typelen]
            self.__off += typelen
            return struct.unpack(fmt,tmp)[0]
        def readInt(self):
            return self.__readtype(4,'<i')
        def readLong(self):
            return self.__readtype(8,'<q')
        def readFloat(self):
            return self.__readtype(4,'<f')
        def readBuffer(self,buflen):
            tmp = self.__str[self.__off : self.__off + buflen]
            self.__off += buflen
            return tmp
        def readString(self):
            buflen = self.readInt()
            return self.readBuffer(buflen)
################################################################        
    def __init__(self,addr=None,tmo=None):
        '''
        Constructor
        '''
        self.server_addr = addr or ('127.0.0.1',2001)
        self.conn_tmo = tmo or 3000
    
    @staticmethod
    def __check_ret_err(chrd):
        retc = chrd.readInt()
        if retc !=0 :
            errs = chrd.readString()
            raise ImgdbError(retc,errs)
        
    def __rt_cmd_comm(self,cmdid,*sargs):
        sock = self.__connsock(); sio=StringIO()
        try:
            for a in sargs:
                self.__tfm[type(a)](sio, a)
            bufcmd = self.__pack_cmd(cmdid,sio.getvalue())
            sock.sendall(bufcmd)
            #sock.recv
            bufcmd = self.__sock_recv_cmd(sock)
            #print len(bufcmd)
            chrd = self.__SeqReader(bufcmd)
            self.__check_ret_err(chrd)
            return chrd
        finally:
            sock.close(); sio.close()
    '''________________________________________'''
    def rt_get_all_db(self):
        chrd = self.__rt_cmd_comm(self.__CMD_ENUM_ALL_DBS)
        retc = chrd.readInt()
        return tuple( chrd.readString() for _i in xrange(retc) )
    
    def rt_get_dongle_key(self):
        chrd = self.__rt_cmd_comm(self.__CMD_GET_DONGLE_KEY)
        return chrd.readString()
    
    def rt_alloc_trunk(self,dbname,count):
        assert isinstance(dbname, str) and isinstance(count, int)
        self.__rt_cmd_comm(self.__CMD_ALLOC_TRUNK,dbname,count)

    def rt_create_db(self,dbname):
        assert isinstance(dbname, str)
        self.__rt_cmd_comm(self.__CMD_CREATE_DB,dbname)

    def rt_delete_db(self,dbname):
        assert isinstance(dbname, str)
        self.__rt_cmd_comm(self.__CMD_DELETE_DB,dbname)
        
    def rt_show_load_db(self):
        chrd = self.__rt_cmd_comm(self.__CMD_SHOW_LOAD_DBS)
        retc = chrd.readInt()
        return [ chrd.readString() for _i in xrange(retc) ]   
    
    def rt_unload_db(self,dbname):
        assert isinstance(dbname, str)
        self.__rt_cmd_comm(self.__CMD_UNLOAD_DB,dbname)
        
    def rt_get_col_info2(self,dbname):
        assert isinstance(dbname, str)
        chrd = self.__rt_cmd_comm(self.__CMD_SHOW_COL_INFO_V2,dbname)
        retc = chrd.readInt()
        return tuple((chrd.readString(),chrd.readString(),chrd.readString(),chrd.readInt()) for _i in xrange(retc)  )
    
    def rt_push_img_rec_feat(self,dbname,featType,featureData):
        assert isinstance(dbname, str) and isinstance(featType, int) and \
            isinstance(featureData, str)
        chrd= self.__rt_cmd_comm(self.__CMD_PUSH_IMAGE_REC,dbname,featType,featureData)
        return chrd.readLong()
    
    def rt_push_img_rec_idx(self,dbname,featType,featureData,idx):
        assert isinstance(dbname, str) and isinstance(featType, int) and \
            isinstance(featureData, str) and isinstance(idx, int)
        chrd= self.__rt_cmd_comm(self.__CMD_PUSH_IMAGE_IDX,dbname,featType,featureData,idx)
        return chrd.readLong()
    
    def rt_push_img_rec_v2(self,dbname,featType,featureData,paramlist):
        assert isinstance(dbname, str) and isinstance(featType, int) and \
            isinstance(featureData, str) and isinstance(paramlist, str) 
        chrd=self.__rt_cmd_comm(self.__CMD_PUSH_IMAGE_REC,dbname,featType,featureData,paramlist)
        return chrd.readLong()
    
    def rt_push_img_rec_v3(self,dbname,featType,featureData,idx,wantedparam,paramlist):
        assert isinstance(dbname, str) and isinstance(featType, int) and \
            isinstance(featureData, str) and isinstance(idx, long) and \
            isinstance(wantedparam, str) and isinstance(paramlist, str) 
        chrd=self.__rt_cmd_comm(self.__CMD_PUSH_IMAGE_IDX,dbname,featType,featureData,idx,wantedparam,paramlist)
        return chrd.readLong()
    
    def rt_push_img_rec(self,dbname,imgdata,wantedparam,paramlist):
        assert isinstance(dbname, str) and isinstance(imgdata, str) and \
            isinstance(wantedparam, str) and isinstance(paramlist, str)
        chrd= self.__rt_cmd_comm(self.__CMD_PUSH_IMAGE_REC,dbname,imgdata,'.jpg',wantedparam,paramlist)
        return chrd.readLong()
            
    def rt_cnn_img_extract(self,imgdata):
        chrd=self.__rt_cmd_comm(802,imgdata)
        return chrd.readString()
    
    def rt_cnn_img_extract2(self,imgdata):
        chrd=self.__rt_cmd_comm(802,4,imgdata)
        return chrd.readString()
       
    @staticmethod
    def __get_img_recs(chrd):
        def _chkint(val,msg):
            if val<0 or val>1000000000: raise ImgdbError(-2,msg+str(val))
        retc = chrd.readInt();  _chkint(retc, 'error get ImgRecord.count ')
        print retc
        def _readparam():
            pct =chrd.readInt(); _chkint(pct, 'error get ImgRecord.param_ct ')
            return tuple(chrd.readString() for _i in xrange(pct))
        return tuple( (chrd.readLong(),chrd.readFloat(),_readparam()) for _j in xrange(retc) )
    
    @staticmethod
    def __get_img_recs_5(chrd):
        def _chkint(val,msg):
            if val<0 or val>1000000000: raise ImgdbError(-2,msg+str(val))
        retc = chrd.readInt();  _chkint(retc, 'error get ImgRecord.count ')
        print retc
        def _readparam():
            pct =chrd.readInt(); _chkint(pct, 'error get ImgRecord.param_ct ')
            return tuple(chrd.readString() for _i in xrange(pct))
        return tuple( (chrd.readLong(),chrd.readFloat(),chrd.readString(),_readparam()) for _j in xrange(retc) )
    
    @staticmethod
    def __get_img_recs_2(chrd):
        def _chkint(val,msg):
            if val<0 or val>1000000000: raise ImgdbError(-2,msg+str(val))
        retc = chrd.readInt();  _chkint(retc, 'error get ImgRecord.count ')
        def _readparam():
            pct =chrd.readInt(); _chkint(pct, 'error get ImgRecord.param_ct ')
            return tuple(chrd.readString() for _i in xrange(pct))
        return tuple( (chrd.readLong(),chrd.readFloat(),_readparam()) for _j in xrange(retc) )
    
    def rt_retrieve_img_rec_em(self,dbname,imgdata,wantpara,wherestmt,rt_param):
        assert isinstance(dbname, str) and isinstance(imgdata, str) and \
            isinstance(wantpara, str) and isinstance(wherestmt, str) and \
            isinstance(rt_param,str) 
        chrd = self.__rt_cmd_comm(self.__CMD_RETRIEVE_IMAGE_REC_V2,dbname,imgdata,'.jpg',wantpara,wherestmt,\
                rt_param)
        return self.__get_img_recs(chrd)
    
    def rt_retrieve_img_rec_feat(self,dbname,featType,featureData,wherestmt,sel2=80,sim_min=0.0000001):
        assert isinstance(dbname, str) and isinstance(featType, int) and \
            isinstance(featureData, str) and isinstance(sel2, int) 
        chrd = self.__rt_cmd_comm(self.__CMD_RETRIEVE_IMAGE_REC_WANT_FEATURE,dbname,featType,featureData,wherestmt,sel2,float(sim_min))
        return self.__get_img_recs_5(chrd)
    
    def rt_retrieve_img_rec(self,dbname,featType,featureData,wherestmt,sel2=80,sim_min=0.0001):
        assert isinstance(dbname, str) and isinstance(featType, int) and \
            isinstance(featureData, str) and isinstance(sel2, int)  and isinstance(wherestmt, str) 
        chrd = self.__rt_cmd_comm(self.__CMD_RETRIEVE_IMAGE_REC,dbname,featType,featureData,wherestmt,sel2,float(sim_min))
        return self.__get_img_recs(chrd)
    
    def rt_select_img_rec(self,dbname,wherestmt,sortpara,reverse,maxrec=1000):
        assert isinstance(dbname, str) and isinstance(wherestmt, str)
        chrd = self.__rt_cmd_comm(self.__CMD_SELECT_IMAGE_REC,dbname,wherestmt,int(maxrec),sortpara,reverse)
        return self.__get_img_recs_2(chrd)
     
    def rt_select_img_rec_v2(self,dbname,wantpara,wherestmt,maxrec=1000):
        assert isinstance(dbname, str) and\
            isinstance(wantpara, str) and isinstance(wherestmt, str)
        chrd = self.__rt_cmd_comm(self.__CMD_SELECT_IMAGE_REC_V2,dbname,wantpara,wherestmt,int(maxrec))
        return self.__get_img_recs(chrd)
    
    def rt_get_img_feat(self,dbname,index):
        assert isinstance(dbname, str) and isinstance(index, long)
        chrd =  self.__rt_cmd_comm(self.__CMD_GET_IMGREC_FEAT2,dbname,long(index))
        return self.__get_img_recs(chrd)
    
    def rt_delete_img_rec(self,dbname,index):
        assert isinstance(dbname, str) and isinstance(index, long)
        self.__rt_cmd_comm(self.__CMD_DELETE_IMAGE_REC,dbname,long(index))
    
    def rt_delete_rec_ws(self,dbname,wherestmt):
        assert isinstance(dbname, str) and isinstance(wherestmt, str)
        self.__rt_cmd_comm(self.__CMD_DELETE_IMAGE_REC_WS,dbname,wherestmt)
        
    def rt_select_rec_ct(self,dbname,wherestmt):
        assert isinstance(dbname, str) and isinstance(wherestmt, str)
        chrd = self.__rt_cmd_comm(self.__CMD_SELECT_REC_COUNT,dbname,wherestmt)
        return chrd.readLong()
    
    def rt_update_img_rec(self,dbname,index,setstmt):
        assert isinstance(dbname, str) and isinstance(setstmt, str) and\
            isinstance(index, long)
        self.__rt_cmd_comm(self.__CMD_UPDATE_IMAGE_REC,dbname,long(index),setstmt)

    def rt_update_img_rec_ws(self,dbname,wherestmt,setstmt):
        assert isinstance(dbname, str) and isinstance(setstmt, str) and\
            isinstance(wherestmt, str)
        self.__rt_cmd_comm(self.__CMD_UPDATE_IMAGE_REC_WS,dbname,wherestmt,setstmt)

    def rt_update_img_rec_ws2(self,dbname,wherestmt,setstmt):
        assert isinstance(dbname, str) and isinstance(setstmt, str) and\
            isinstance(wherestmt, str)
        self.__rt_cmd_comm(self.__CMD_UPDATE_IMAGE_REC_WS2,dbname,wherestmt,setstmt)
        
    def rt_mult_facefeat_extract(self,image):
        assert isinstance(image, str)
        return json.loads(self.__rt_cmd_comm(1316,image).readString())
    
    ##########################################
    def rt_get_all_load_db(self):
        chrd = self.__rt_cmd_comm(self.__CMD_SHOW_LOAD_DBS)
        retc = chrd.readInt()
        return tuple( chrd.readString() for _i in xrange(retc) )
    
    def rt_force_unload_db(self,dbname):
        assert isinstance(dbname, str) 
        self.__rt_cmd_comm(self.__CMD_UNLOAD_DB,dbname)
        
    
    def rt_get_rec_count(self,dbname):
        assert isinstance(dbname, str)
        return self.__rt_cmd_comm(self.__CMD_GET_DB_REC_CT,dbname).readLong()
        
'''
    global helper function
'''    
              
import requests
import json
import urllib2

img_url='http://192.168.4.236:9083/wmzt_image?uid='
def down_img(url,img_name):
    try:
        f = urllib2.urlopen(url) 
        data = f.read() 
        with open(img_name, "wb") as code: 
            code.write(data)
            return ''
        print 'download file error'
    except urllib2.URLError, e:
        print 'requrl error--->',str(e)
        return ''

if __name__=="__main__":
    import random
    print '------> start <------'
    download_dir='d:/test'
    dbname='bl_face_5a797adee88545db985d5e3336b8e4fe'
    api=Api( ('192.168.4.213',2017),3500 )
    index=0
    for kk in range(0,120):
        param='&,%d&|%d&,' % (1000*kk+1,1000*kk+1000)
        print '------> downcount[%d], [%d] %s <------' % (index, kk, param)
        rsp=api.rt_select_img_rec(dbname, param, -1, 1, 1100)
        #print rsp
    
        for i in range(0,len(rsp)):
            print rsp[i][2][1]
            print rsp[i][2][3]
            print rsp[i][2][4]
            aid=rsp[i][2][1]
            face_url_s=img_url+rsp[i][2][3]
            face_url_f=img_url+rsp[i][2][4]
            face_name_s='%s/%s_%d_s.jpg' % (download_dir,aid,index)
            face_name_f='%s/%s_%d_f.jpg' % (download_dir,aid,index)
            down_img(face_url_s,face_name_s)
            down_img(face_url_f,face_name_f)
            index += 1
            print '--------------'
