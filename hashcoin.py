import random as rand
from tkinter import * 
import tkinter as tk
def mysql(s):
    import mysql.connector
    mydb = mysql.connector.connect(host="localhost",user="atit",password="atitpatel",database='hashcoin')
    collection=[]
    mycursor=mydb.cursor()
    mycursor.execute(s)
    for i in mycursor:
        collection.append(i)
    mydb.commit()
    mydb.disconnect()
    return collection

def seq_hash_gen(seq):
    unused=['0x2406e','0x1a599','0x1b7df','0x25dab','0x2786c','0x21ace','0x1d3ba','0x1ad26','0x20bfb','0x1eedf']
    c_key=[ 0x1afd8,0x27852,0x1ffc7,0x1d2f3,0x20a4c,0x20c72,0x18ab7,0x21fd7,0x1c463,0x1a65f,0x1b603,0x18e0f,0x21f9b,
            0x24e8f,0x1ef5f,0x20ba5,0x219e0,0x260ac,0x2358a,0x19cc0,0x1b569,0x21d35,0x1d7be,0x2119b,0x1ba59,0x24899,
            0x27372,0x216a0,0x1d9df,0x1c3f1,0x235fc,0x2732b,0x274e5,0x1a018,0x18bc0,0x1d5f1,0x18e6e,0x1c1f6,0x1b250,
            0x23263,0x1ea80,0x23a19,0x1c29a,0x21a96,0x25883,0x219d2,0x1bcd5,0x1cd79,0x19da8,0x2419b,0x23ad9,0x22eec ]
    l_key=[ 0x1abe8,0x24910,0x25256,0x1a5c6,0x25d9e,0x20e9b,0x1e3c3,0x2038b,0x257e1,0x2074d,0x22cf6,0x1db25,0x1c11d,
            0x1e013,0x1a12b,0x1fec6,0x2504b,0x20b98,0x1f08f,0x23bcc,0x1a1e1,0x187df,0x20084,0x1acbe,0x1c740,0x1c5bc,
            0x1bbea,0x24a41,0x2147f,0x1908c,0x26922,0x21920,0x267bc,0x1d417,0x24642,0x1b182,0x1ff97,0x27435,0x1a645,
            0x247a5,0x1b175,0x21e6a,0x1d2a2,0x247a3,0x18dd2,0x2239d,0x1ebe3,0x2699c,0x1cc6b,0x1e108,0x26dd7,0x21f03 ]
    n_key=[ 0x21886,0x18cd5,0x275eb,0x2424e,0x1bdb0,0x19c7c,0x229f2,0x21b50,0x2100d,0x1a9fe ]
    s_key=[ 0x1955e,0x1c0c9 ]
    freq={}
    lst_key=[]
    seq=str(seq)
    for i in seq:
        if i.isalpha():
            if i in freq:
                freq[i]=freq[i]+1
            else:
                freq[i]=1
            if (ord(i)>=97 and ord(i)<=122):
                if freq[i]%2==1:
                    lst_key.append(l_key[ord(i)-97])
                else:
                    lst_key.append(l_key[ord(i)-97+26])
            elif (ord(i)>=65 and ord(i)<=90):
                if freq[i]%2==1:
                    lst_key.append(c_key[ord(i)-65])
                else:
                    lst_key.append(c_key[ord(i)-65+26])
        elif i.isnumeric():
            lst_key.append(n_key[int(i)])
        elif i == ' ':
            lst_key.append(s_key[0])
        else:
            lst_key.append(s_key[1])
    dct={0:[0x26e43],1:[0x2565a],2:[0x267d1],3:[0x1f029],4:[0x26c15]}
    for i in range(len(lst_key)):
        j=i%5
        dct[j].append(lst_key[i])
    hex_list=[]
    for i in dct:
        sum_of=0
        for j in dct[i]:
            sum_of=sum_of+j
        hex_list.append(sum_of)
    string=""
    for itr in range(len(hex_list)):
        temp=hex(hex_list[itr])
        temp=temp[-5:]
        string=string+temp
    return string

def start():
    start_frame.tkraise()

def new_user():
    def submit(var_user_id,var_fname,var_lname,var_pass):
        user_id=var_user_id.get()
        hash_user_id=seq_hash_gen(user_id)

        password = var_pass.get()
        hash_password=seq_hash_gen(password)

        fname= var_fname.get()
        lname= var_lname.get()

        pin_no=str(rand.randint(100000,999999))
        pin_hash=seq_hash_gen(pin_no)

        private_key=seq_hash_gen(lname[::-1]+user_id)

        mysql("insert into user values('" +hash_user_id+ "','" +fname+ "','" +lname+ "','" +pin_hash+ "','" +private_key+"','"+hash_password+ "');")
        wallet_id=new_wallet(hash_user_id)
        #wallet_id='w0000'
        
        t_user_id ="User ID:--"+str(user_id)
        t_pass ="Password:--"+str(password)
        t_fname="First Name:--"+str(fname)
        t_lname="Last Name:--"+str(lname)
        t_pin="PIN:--"+str(pin_no)
        t_wallet_id ="Wallet ID:--"+str(wallet_id)
        
        info_new_user_frame=Frame(root,bg='black',width=420,height=220)
        info_new_user_frame.pack_propagate(0)
        info_new_user_frame.grid(row=0,column=0,sticky='nsew')
        # have to give a fresh wallet id and a pin_no with prompt of their usage
        info_new_user_user_id_label = Label(info_new_user_frame,text=t_user_id,fg='#1affff',bg='#000000')
        info_new_user_user_id_label.place(x=50,y=15,anchor='nw')
        info_new_user_pass_label = Label(info_new_user_frame,text=t_pass,fg='#1affff',bg='#000000')
        info_new_user_pass_label.place(x=50,y=45,anchor='nw')
        info_new_user_fname_label = Label(info_new_user_frame,text=t_fname,fg='#1affff',bg='#000000')
        info_new_user_fname_label.place(x=50,y=75,anchor='nw')
        info_new_user_lname_label = Label(info_new_user_frame,text=t_lname,fg='#1affff',bg='#000000')
        info_new_user_lname_label.place(x=50,y=105,anchor='nw')
        info_new_user_pin_label = Label(info_new_user_frame,text=t_pin,fg='#1affff',bg='#000000')
        info_new_user_pin_label.place(x=50,y=135,anchor='nw')
        info_new_user_wallet_label = Label(info_new_user_frame,text=t_wallet_id,fg='#1affff',bg='#000000')
        info_new_user_wallet_label.place(x=50,y=165,anchor='nw')

        info_new_user_pin_use_label = Label(info_new_user_frame,text="User PIN No to\nauthenticate transaction",fg='#1affff',bg='#000000')
        info_new_user_pin_use_label.place(x=300,y=60,anchor='n')
        info_new_user_wallet_id_label = Label(info_new_user_frame,text="Wallet ID is for\nsending/recieving Coins",fg='#1affff',bg='#000000')
        info_new_user_wallet_id_label.place(x=300,y=120,anchor='n')

        info_new_user_log_btn= Button(info_new_user_frame,relief=FLAT,text='login',fg='#000000',bg='#1affff',command=login)
        info_new_user_log_btn.place(x=200,y=190,anchor='n')
        
        info_new_user_frame.tkraise()
    
    new_user_frame=Frame(root,bg='black',width=420,height=220)
    new_user_frame.pack_propagate(0)
    new_user_frame.grid(row=0,column=0,sticky='nsew')
    
    new_user_user_id_label = Label(new_user_frame,text='User ID:',fg='#1affff',bg='#000000')
    new_user_user_id_label.place(x=120,y=30)
    new_user_pass_label=Label(new_user_frame,text='Password:',fg='#1affff',bg='#000000')
    new_user_pass_label.place(x=106,y=60)
    new_user_fname_label = Label(new_user_frame,text='First Name:',fg='#1affff',bg='#000000')
    new_user_fname_label.place(x=100,y=90)
    new_user_lname_label = Label(new_user_frame,text='Last Name:',fg='#1affff',bg='#000000')
    new_user_lname_label.place(x=100,y=120)
    
    var_user_id = StringVar()
    var_fname = StringVar()
    var_lname = StringVar()
    var_pass = StringVar()
    
    new_user_user_id_entry = Entry(new_user_frame,relief=FLAT,textvariable=var_user_id)
    new_user_user_id_entry.place(x=170,y=30)
    new_user_pass_entry = Entry(new_user_frame,relief=FLAT,textvariable=var_pass)
    new_user_pass_entry.place(x=170,y=60)
    new_user_fname_entry = Entry(new_user_frame,relief=FLAT,textvariable=var_fname)
    new_user_fname_entry.place(x=170,y=90)
    new_user_lname_entry = Entry(new_user_frame,relief=FLAT,textvariable=var_lname)
    new_user_lname_entry.place(x=170,y=120)

    new_user_enter_btn = Button(new_user_frame,relief=FLAT,text='Create User',fg='#000000',bg='#1affff',command=lambda:submit(var_user_id,var_fname,var_lname,var_pass))
    new_user_enter_btn.place(x=210,y=170,anchor='n',width=120,height=25)

    new_user_frame.tkraise()

def login():
    def submit(var_user_id,var_pass):
        user_id=var_user_id.get()
        password=var_pass.get()
        if user_id=="" or password=="":
            login_error_label= Label(login_frame,text="Please enter a\nUser ID and Password",bg='#000000',fg='#ff0000')
            login_error_label.place(x=210,y=160,anchor='n')

        hash_password=seq_hash_gen(password)
        hash_user_id=seq_hash_gen(user_id)
        l=[hash_user_id,hash_password]
        chk=mysql("select password from user where user_id='"+hash_user_id+"';")
        if chk[0][0]==hash_password:
            user(hash_user_id)
        else:
            error_label=Label(login_frame,text='Wrong Password or user ID\nTry Again',bg='#000000',fg='#ff0000').place(x=210,y=165,anchor='n')
    
    login_frame=Frame(root,bg='black',width=420,height=220)#done
    login_frame.pack_propagate(0)
    login_frame.grid(row=0,column=0,sticky='nsew')

    login_user_id_label=Label(login_frame,text='User ID:',fg='#1affff',bg='#000000').place(x=120,y=50)
    login_pass_label=Label(login_frame,text='Password:',fg='#1affff',bg='#000000').place(x=105,y=100)
        
    var_user_id = StringVar()
    var_pass = StringVar()

    login_user_id_entry=Entry(login_frame,relief=FLAT,textvariable=var_user_id).place(x=170,y=50)
    login_pass_entry=Entry(login_frame,relief=FLAT,textvariable=var_pass,show='*').place(x=170,y=100)

    login_submit_btn= Button(login_frame,relief=FLAT,text='LOGIN',fg='#000000',bg='#1affff',command=lambda:submit(var_user_id,var_pass)).place(x=190,y=130)

    login_frame.tkraise()

def user(user_id):
    user_frame=Frame(root,bg='black',width=420,height=220)
    user_frame.pack_propagate(0)
    user_frame.grid(row=0,column=0,sticky='nsew')

    user_top_label = Label(user_frame,text='Select From Options:',fg='#1affff',bg='#000000')
    user_top_label.place(x=210,y=20,anchor='n')

    user_send_coin_btn = Button(user_frame,relief=FLAT,text='Send Coins',fg='#000000',bg='#1affff',command=lambda:send_coins(user_id))
    user_send_coin_btn.place(x=140,y=60,anchor='n',width=120)
    user_chk_balance_btn = Button(user_frame,relief=FLAT,text='Check Balance',fg='#000000',bg='#1affff',command=lambda:check_balance(user_id))
    user_chk_balance_btn.place(x=280,y=60,anchor='n',width=120)
    user_mine_btn = Button(user_frame,relief=FLAT,text='Mine Coins',fg='#000000',bg='#1affff',command=lambda:mining(user_id))
    user_mine_btn.place(x=140,y=100,anchor='n',width=120)
    user_req_wallet_btn = Button(user_frame,relief=FLAT,text='Request New Wallet',fg='#000000',bg='#1affff',command=lambda:req_new_wallet(user_id))
    user_req_wallet_btn.place(x=280,y=100,anchor='n',width=120)
    user_statment_btn= Button(user_frame,relief=FLAT,text='Get Statement of Recent 5',fg='#000000',bg='#1affff',command=lambda:statement(user_id))
    user_statment_btn.place(x=210,y=140,anchor='n')
    user_logout_btn = Button(user_frame,relief=FLAT,text='Logout',fg="#ff0000",bg="#000000",command=start)
    user_logout_btn.place(x=210,y=180,anchor='n',width=80,height=40)

    user_frame.tkraise()

def check_balance(user_id):
    wallet_lst=mysql("select wallet_id,balance from wallet where user_id='"+user_id+"';")
    str_message="Wallet Id         Balance\n"
    
    for i in wallet_lst:
        str_message=str_message+i[0]+"-------------"+str(i[1])+"\n"
     
    chk_balance_frame=Frame(root,bg='black',width=420,height=220)
    chk_balance_frame.pack_propagate(0)
    chk_balance_frame.grid(row=0,column=0,sticky='nsew')

    chk_balance_info_label=Label(chk_balance_frame,text='Balance:',fg='#1affff',bg='#000000')
    chk_balance_info_label.place(x=210,y=10,anchor='n')
    chk_balance_message_label = Label(chk_balance_frame,text=str_message,fg='#1affff',bg='#000000')
    chk_balance_message_label.place(x=210,y=50,anchor='n')

    chk_balance_back_btn = Button(chk_balance_frame,relief=FLAT,text='Back',bg='#1affff',fg='#000000',command=lambda:user(user_id))
    chk_balance_back_btn.place(x=210,y=160,anchor='n')

    chk_balance_frame.tkraise()

def send_coins(user_id):
    def send(var_sender,var_reciever,var_ammount,var_pin,user_id):
        sender=var_sender.get()
        reciever=var_reciever.get()
        ammount=var_ammount.get()
        pin_no=var_pin.get()
        pin_no=seq_hash_gen(pin_no)
        
        chk_amount=mysql("select balance from wallet where wallet_id='"+sender+"';")
        if len(chk_amount)==1:
            chk_amount=chk_amount[0][0]
        else:
            chk_amount=0
        chk_pin=mysql("select pin_no from user where user_id='"+user_id+"';")[0][0]
        chk_sender=mysql("select * from wallet where user_id='"+user_id+"' and wallet_id ='"+sender+"';")
        chk_reciever=mysql("select * from wallet where wallet_id = '"+reciever+"';")
        send_coins_error_label=Label(send_coins_frame,text='Error occured\nInfo given or pin or ammount is insufficient',bg='#000000',fg='#ff0000')
        if len(chk_sender)==0 or len(chk_reciever)==0 or chk_amount<int(ammount) or pin_no!=chk_pin:
            
            send_coins_error_label.place(x=210,y=180,anchor='n')
            send_coins_back_btn=Button(send_coins_frame,relief=FLAT,text='Back',fg='#000000',bg='#1affff',command=lambda:user(user_id))
            send_coins_back_btn.place(x=250,y=150,anchor='n')
            send_coins_send_btn.place(x=190,y=150,anchor='n')

        elif pin_no == chk_pin:

            block=Block(sender,reciever,int(ammount))
            print_block_to_ledger(block)
            sender_balance=mysql("select balance from wallet where wallet_id='"+sender+"';")[0][0]
            reciever_balance=mysql("select balance from wallet where wallet_id='"+reciever+"';")[0][0]
            sender_balance=sender_balance-int(ammount)
            reciever_balance=reciever_balance+int(ammount)
            mysql("update wallet set balance="+str(sender_balance)+" where wallet_id ='"+sender+"';")
            mysql("update wallet set balance="+str(reciever_balance)+" where wallet_id ='"+reciever+"';")
            tar=mysql("select max(transaction_id) from ledger")[0][0]
            t_success_label="coins sent!!!!\ntransaction ID--"+tar

            send_coins_success_label=Label(send_coins_frame,text=t_success_label,bg='#000000',fg='#1affff')
            send_coins_success_label.place(x=210,y=180,anchor='n')
            send_coins_back_btn=Button(send_coins_frame,relief=FLAT,text='Back',fg='#000000',bg='#1affff',command=lambda:user(user_id))
            send_coins_back_btn.place(x=250,y=150,anchor='n')
            send_coins_send_btn.place(x=190,y=150,anchor='n')

    send_coins_frame=Frame(root,bg='black',width=420,height=220)
    send_coins_frame.pack_propagate(0)
    send_coins_frame.grid(row=0,column=0,sticky='nsew')

    send_coins_sender_label = Label(send_coins_frame,text='Your Wallet ID:',fg='#1affff',bg='#000000')
    send_coins_sender_label.place(x=165,y=20,anchor='ne')
    send_coins_reciever_label = Label(send_coins_frame,text='Reciever Wallet Id:',fg='#1affff',bg='#000000')
    send_coins_reciever_label.place(x=165,y=50,anchor='ne')
    send_coins_amount_label = Label(send_coins_frame,text='Ammount:',fg='#1affff',bg='#000000')
    send_coins_amount_label.place(x=165,y=80,anchor='ne')
    send_coins_pin_label = Label(send_coins_frame,text='PIN:',fg='#1affff',bg='#000000')
    send_coins_pin_label.place(x=165,y=110,anchor='ne')

    var_sender = StringVar()
    var_reciever = StringVar()
    var_ammount = StringVar()
    var_pin = StringVar()

    send_coins_sender_entry = Entry(send_coins_frame,relief=FLAT,textvariable=var_sender)
    send_coins_sender_entry.place(x=175,y=20)
    send_coins_reciever_entry = Entry(send_coins_frame,relief=FLAT,textvariable=var_reciever)
    send_coins_reciever_entry.place(x=175,y=50)
    send_coins_ammount_entry = Entry(send_coins_frame,relief=FLAT,textvariable=var_ammount)
    send_coins_ammount_entry.place(x=175,y=80)
    send_coins_pin_entry = Entry(send_coins_frame,relief=FLAT,show='#',textvariable=var_pin)
    send_coins_pin_entry.place(x=175,y=110)

    send_coins_send_btn = Button(send_coins_frame,relief=FLAT,text='Send',fg='#000000',bg='#1affff',command=lambda:send(var_sender,var_reciever,var_ammount,var_pin,user_id))
    send_coins_send_btn.place(x=210,y=150,anchor='n')
    send_coins_frame.tkraise()

def new_wallet(user_id):
    result = mysql("select max(wallet_id) from wallet;")
    if result[0][0]==None:
        wallet_id="w1000"
    else:
        num=result[0][0][1:]
        num=int(num)
        num=num+1
        wallet_id="w"+str(num)
    mysql("insert into wallet values('"+wallet_id+"','"+user_id+"',0);")
    return wallet_id

def req_new_wallet(user_id):
    new_wallet_frame=Frame(root,bg='black',width=420,height=220)
    new_wallet_frame.pack_propagate(0)
    new_wallet_frame.grid(row=0,column=0,sticky='nsew')
    
    wallet_id = new_wallet(user_id)
    string = "You're new wallet ID is:\n"+wallet_id
    
    new_wallet_label = Label(new_wallet_frame,text=string,fg='#1affff',bg='#000000')
    new_wallet_label.place(x=210,y=100,anchor='n')
    
    new_wallet_back_btn = Button(new_wallet_frame,relief=FLAT,text='Back',fg='#000000',bg='#1affff',command= lambda:user(user_id))
    new_wallet_back_btn.place(x=210,y=170,anchor='n')

def statement(user_id):
    def show(var_wallet_id,user_id):
        wallet_id = var_wallet_id.get()
        lst=mysql("select sender,reciever,amount from ledger where sender='"+wallet_id+"' or reciever='"+wallet_id+"';")
        message="Sender Reciever Amount\n"
        for i in lst[-5:]:
            message=message+i[0]+"   "+i[1]+"     "+str(i[2])+"\n"
        statement_info_label = Label(statement_frame, text=message,bg='#000000',fg='#1affff')
        statement_info_label.place(x=210,y=70,anchor='n')

    statement_frame = Frame(root,bg='#000000',width=420,height=220)
    statement_frame.pack_propagate(0)
    statement_frame.grid(row=0,column=0,sticky='nsew')

    statement_title_label = Label(statement_frame, text='STATEMENT',bg='#000000',fg='#1affff')
    statement_title_label.place(x=210,y=20,anchor='n')

    statement_wallet_label=Label(statement_frame,text='Wallet ID',bg='#000000',fg='#1affff')
    statement_wallet_label.place(x=120,y=50,anchor='n')
    
    var_wallet_id = StringVar()
    statemant_wallet_entry=Entry(statement_frame,relief=FLAT,textvariable=var_wallet_id)
    statemant_wallet_entry.place(x=210,y=50,anchor='n')
    
    statement_go_btn= Button(statement_frame,relief=FLAT,text='GO',fg='#000000',bg='#1affff',command=lambda:show(var_wallet_id,user_id))
    statement_go_btn.place(x=300,y=50,anchor='n')
    statment_back_btn = Button(statement_frame,relief=FLAT,text='back',bg='#1affff',fg='#000000',command=lambda:user(user_id))
    statment_back_btn.place(x=210,y=180,anchor='n')

class Block(): 
    
    # The data to be kept in a Block
    data = None # sender(Private Key)   +  reciever(Private_key)  [as a string]
    sender = None
    reciever = None
    ammount = None
    previous_hash = None
    seq=None
    block_hash = None # The hash of the block

    def __init__(self,sender,reciever,ammount):
        self.reciever=reciever
        self.sender=sender
        self.ammount=ammount
        self.get_data()
        self.get_prev_hash()
        self.hash_self()

    def __str__(self):
        return("Data:-"+str(self.data)+
        "\nReciever:-"+str(self.reciever)+
        "\nSender:-"+str(self.sender)+
        "\nAmmount:-"+str(self.ammount)+
        "\nBlock hash:-"+str(self.block_hash)+
        "\nPrevious hash:-"+str(self.previous_hash))
    
    def get(self,var):
        if var == "data":
            return self.data
        elif var == "sender":
            return self.sender
        elif var == "reciever":
            return self.reciever
        elif var == "ammount":
            return self.ammount
        elif var == "hash":
            return self.block_hash
        elif var == "prev_hash":
            return self.previous_hash
    
    def get_data(self):
        sender_user_id=mysql("select user_id from wallet where wallet_id='"+self.sender+"';")[0][0]
        reciver_user_id=mysql("select user_id from wallet where wallet_id='"+self.reciever+"';")[0][0]
        result=mysql("select private_key from user where user_id in('"+sender_user_id+"','"+reciver_user_id+"')")
        data=""
        if result:
            for i in result:
                data=data+i[0]
            self.data=data
        else:
            self.data=data+"0"*50
    
    def get_prev_hash(self):
        result=mysql("select hash from ledger where transaction_id=(select max(transaction_id) from ledger)")
        if result:
            self.previous_hash=result[0][0]
        else:
            self.previous_hash=seq_hash_gen("")
    
    def hash_self(self):
        #   data + sender + reciever + amount + prev_hash [as a string]
        seq = str(self.data) + str(self.sender) + str(self.reciever) + str(self.ammount) + str(self.previous_hash)
        self.seq=seq
        self.block_hash = seq_hash_gen(seq)#   pass seq to seq_hash_gen to get hash of the block

def mining(user_id):
    def mine(var_wallet_id,user_id):
        wallet_id=var_wallet_id.get()
        mining_label1 = Label(mining_frame,text='Mining...........',bg='#000000',fg='#1affff')
        mining_label1.place(x=210,y=70,anchor='n')
        ledger1=mysql("select * from ledger")
        ledger=[]
        for i in ledger1:
            ledger.append(list(i))
        #checking the blocks in the ledger
        i=1
        while i < len(ledger):
            if ledger[i][5] == ledger[i-1][4]:
                i=i+1
            else:
                tup=ledger[i]
                if i <len(ledger)-1:
                    ledger[i+1][5]=ledger[i-1][4]
                mysql("delete from ledger where transaction_id='"+tup[0]+"';")
                mysql("update ledger set prev_hash='"+ledger[i-1][4]+"' where transaction_id='"+ledger[i+1][0]+"';")
                ledger.remove(tup)
        # getting the hash sum
        hash_lst=[]
        for i in ledger:
            hash_lst.append(int(i[4],16))
        hash_sum=0
        for i in hash_lst:
            hash_sum=hash_sum+i
        hash_sum=hex(hash_sum)[2:]
        mysql("delete from sum_hash")
        mysql("insert into sum_hash values('"+hash_sum+"');")
        balance=mysql("select balance from wallet where wallet_id='"+wallet_id+"';")[0][0]
        mysql("update wallet set balance="+str(balance+1)+" where wallet_id='"+wallet_id+"';")
        mining_label2 = Label(mining_frame,text="Mining Done!!!!",bg='#000000',fg='#1affff')
        mining_label2.place(x=210,y=100,anchor='n')
        mining_label3 = Label(mining_frame,text="Coin added to wallet :)",bg='#000000',fg='#1affff')
        mining_label3.place(x=210,y=130,anchor='n')

    mining_frame=Frame(root,bg='black',width=420,height=220)
    mining_frame.pack_propagate(0)
    mining_frame.grid(row=0,column=0,sticky='nsew')

    mining_label = Label(mining_frame, text='Coin Mining',bg='#000000',fg='#1affff')
    mining_label.place(x=210,y=20,anchor='n')

    mining_wallet_label=Label(mining_frame,text='Wallet ID',bg='#000000',fg='#1affff')
    mining_wallet_label.place(x=120,y=50,anchor='n')
    
    var_wallet_id = StringVar()
    mining_wallet_entry=Entry(mining_frame,relief=FLAT,textvariable=var_wallet_id,)
    mining_wallet_entry.place(x=210,y=50,anchor='n')
    
    mining_go_btn= Button(mining_frame,relief=FLAT,text='GO',fg='#000000',bg='#1affff',command=lambda:mine(var_wallet_id,user_id))
    mining_go_btn.place(x=300,y=50,anchor='n')
    mining_back_btn = Button(mining_frame,relief=FLAT,text='back',bg='#1affff',fg='#000000',command=lambda:user(user_id))
    mining_back_btn.place(x=210,y=180,anchor='n')

def print_block_to_ledger(block):
    result=mysql("select max(transaction_id) from ledger")
    if result[0][0] == None:
        tar = 'tar1000'
    else:
        num=result[0][0][3:]
        num=int(num)
        num=num+1
        tar='tar'+str(num)
    sender=block.sender
    reciever=block.reciever
    ammount=block.ammount
    block_hash=block.block_hash
    prv_hash=block.previous_hash
    mysql("insert into ledger values('"+tar+"','"+sender+"','"+reciever+"',"+str(ammount)+",'"+block_hash+"','"+prv_hash+"');")

#--------------Gui----code Executes from here----------------------------#
root = tk.Tk()
root.geometry('420x220')
root.title('Hashcoin')
root.iconbitmap("hashcoin_icon.ico")
start_frame=Frame(root,width=420,height=220)
start_frame.pack_propagate(0)
start_frame.grid(row=0,column=0,sticky='nsew')

start_background_image=PhotoImage(file="./start_background.gif")
start_background_lable=tk.Label(start_frame,image=start_background_image,height=220,width=420)
start_background_lable.place(x=420,y=220,anchor='se',height=220,width=420)

start_login_btn= Button(start_frame,relief=FLAT,text='LOGIN',bg='#000000',fg='#1affff',command=login).place(x=310,y=50,height=50,width=140,anchor='n')
start_new_user_btn= Button(start_frame,relief=FLAT,text='NEW USER',bg='#000000',fg='#1affff',command=new_user).place(x=310,y=120,height=50,width=140,anchor='n')
start_frame.tkraise()

root.mainloop()