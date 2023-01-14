from tkinter import *
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3



class PharmacyManagmentSystem:
    def __init__(self,root):
        self.root=root
        self.root.title("Pharmacy Managment System")
        self.root.geometry("1280x720+0+0")
        root.iconbitmap(r"doc.ico")
 
        img1=Image.open(r"new.png")
        img1=img1.resize((45,45))
        
        photoimg1=ImageTk.PhotoImage(img1)
        txt = "PHARMACY MANAGEMENT SYSTEM"
        self.count=0
        self.text = ""        
        heading = Label(self.root,text=txt,
                             font=("times new roman", 30, "bold"), bg='grey1', fg="green", bd=9, relief=RIDGE)
        heading.pack(side=TOP, fill=X)

        
        def slider():
            
            
                if self.count>=len(txt):
                    self.count=-1
                    self.text=""
                    heading.config(text=self.text)
                else:
                    self.text=self.text+txt[self.count]
                    heading.config(text=self.text)
                self.count+=1
                b1=Button(self.root,image=photoimg1,borderwidth=0)
                b1.place(x=75,y=9)
                heading.after(250,slider)
                
        slider()
        ################### DATA FRAME ################
        DataFrame=Frame(self.root,bd=15,relief=RIDGE,padx=20,bg="white")
        DataFrame.place(x=0,y=285,width=1280,height=350)

        DataFrameLeft=LabelFrame(DataFrame,relief=RIDGE,padx=20,text="Medicine Information",
                                 fg="darkgreen",font=("arial",12,"bold"))
        DataFrameLeft.place(x=465,y=5,width=750,height=305)

        DataFrameRight=LabelFrame(DataFrame,relief=RIDGE,padx=20,text="Medicine Add Department",
                                 fg="darkgreen",font=("ariel",12,"bold"))
        DataFrameRight.place(x=0,y=5,width=450,height=305)
#---------------------------------------FUNCTIONS---------------------------------
        def clear():
            inref.set("Select")
            incompanyname.delete(0,END);intypeofmed.set("Select");inmedname.set("Select");inlotno.delete(0,END);
            inissuedate.delete(0,END);inexpdate.delete(0,END);inuses.delete(0,END);insideeffs.delete(0,END);
            inprec.delete(0,END);indosage.delete(0,END);inprice.delete(0,END);inqt.delete(0,END);
    
        def reset():
            inrefno2.delete(0,END);inmedname2.delete(0,END)

        def fetch_datamed():           
            medtable.tag_configure("oddrow",background="white")
            medtable.tag_configure("evenrow",background="lightblue")
            medtable.delete(*medtable.get_children())
            conn=sqlite3.connect('database.db')
            cursor=conn.cursor()
            records=cursor.execute("SELECT * from med ")
            dvar=0
            for record in records:
                if dvar%2==0:
                    medtable.insert(parent='',index='end',iid=record[0],text="",values=record,tags="evenrow")                    
                else:
                    medtable.insert(parent='',index='end',iid=record[0],text="",values=record,tags="oddrow")
                dvar+=1
            conn.commit()
            conn.close()

        def fetch_datapharma():
            pharmacy_table.tag_configure("oddrow",background="white")
            pharmacy_table.tag_configure("evenrow",background="lightblue")
            pharmacy_table.delete(*pharmacy_table.get_children())
            conn=sqlite3.connect('database.db')
            cursor=conn.cursor()
            records=cursor.execute("SELECT * from pharma ")
            num=0
            for record in records:
                if num %2 == 0 : 
                    pharmacy_table.insert(parent='',index='end',iid=record[0],text="",values=record,tags="evenrow")
                else:
                    pharmacy_table.insert(parent='',index='end',iid=record[0],text="",values=record,tags="oddrow")
                num+=1

            conn.commit()
            conn.close()
            
            
        def add():
            if intypeofmed.get()=="Select" or inref.get()=="Select" or inmedname.get()=="Select" :
                messagebox.showerror("Message","Please select valid option from Dropdown Menu")
            else:
                try:
                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()
                    record=(inref.get(),str(incompanyname.get()),str(intypeofmed.get()),
                        str(inmedname.get()),str(inlotno.get()),str(inissuedate.get()),str(inexpdate.get()),str(inuses.get()),str(insideeffs.get()),str(inprec.get()),
                                                    str(indosage.get()),str(inprice.get()),str(inqt.get()))
                    cursor.execute("INSERT INTO pharma VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)", record)
                    conn.commit()
                    conn.close()
                    fetch_datapharma()
                    messagebox.showinfo("Status", "Medincine Record Inserted")
                    clear()
                except sqlite3.IntegrityError:
                    messagebox.showinfo("Status","Please enter Unique Reference No.")
                except Exception as e:
                    messagebox.showinfo("Status",e)
                

        def add1():
            if inmedname2.get()=="":
                messagebox.showinfo("Status","Please Enter complete Information")
            else:
                try:
                    conn = sqlite3.connect('database.db')
                    cursor = conn.cursor()
                    s=(inmedname2.get())
                    cursor.execute("INSERT INTO med VALUES(?,?)",(inrefno2.get(),''.join(s.split())))
                    conn.commit()
                    conn.close()
                    fetch_datamed()
                    messagebox.showinfo("Status", "Medincine Record Inserted")
                    reset()
                    delcombo()
                    combo()
                except :
                    messagebox.showinfo("Status","Please Enter valid Information")
                    
        def delete():
            if inref.get()=="Select" :
                messagebox.showerror("Message","Please select valid Reference No!!!")
            else:
                try:
                    conn=sqlite3.connect('database.db')
                    cursor=conn.cursor()
                    cursor.execute("DELETE from pharma WHERE ref=" +inref.get())
                    conn.commit()
                    conn.close()
                    fetch_datapharma()
                    messagebox.showinfo("Success","Record Deleted")
                    clear();
                except Exception as e:
                    messagebox.showerror("Error",e)


        def delete1():
            conn=sqlite3.connect('database.db')
            try:
                cursor=conn.cursor()
                cursor.execute("DELETE from med WHERE ref=" +inrefno2.get())
                conn.commit()
                conn.close()
                fetch_datamed()
                messagebox.showinfo("Success","Record Deleted")
                reset()
                delcombo()
                combo()
            except Exception as e:
                reset()
                messagebox.showerror("Error",e)


        def update():
            if intypeofmed.get()=="Select" or inref.get()=="Select" or inmedname.get()=="Select" :
                messagebox.showerror("Message","Please select valid option from Dropdown Menu")
            else:
                try:
                    conn=sqlite3.connect('database.db')
                    cur = conn.cursor()
                    ref=inref.get()
                    cur.execute("""update pharma set companyname=?,type=?,
                                    name=?,lotno=?,
                                    issuedate=?,expdate=?,
                                    uses=?,sideeffects=?,
                                    warning=?,dosage=?,
                                    price=?,quantity=?
                                    WHERE ref=?""",(str(incompanyname.get()),str(intypeofmed.get()),
                        str(inmedname.get()),str(inlotno.get()),str(inissuedate.get()),str(inexpdate.get()),
                                                     str(inuses.get()),str(insideeffs.get()),str(inprec.get()),
                                                    str(indosage.get()),str(inprice.get()),str(inqt.get()),ref))
                    conn.commit()
                    conn.close()
                    fetch_datapharma()
                    clear()
                    messagebox.showinfo("Success","Medicine Record Updated")
                except Exception as e:
                    messagebox.showerror("Error",e)


        def update1():
            if inrefno2.get()=="" or inmedname2.get()=="" :
                messagebox.showerror("Message","Please Enter valid Details")
            else:
                try:
                    conn=sqlite3.connect('database.db')
                    cur = conn.cursor()
                    ref=inrefno2.get()
                    medname=inmedname2.get()                    
                    cur.execute(f'update med set medname="{medname}" WHERE ref={ref}')
                    conn.commit()
                    conn.close()
                    fetch_datamed()
                    reset()
                    delcombo()
                    combo()
                    messagebox.showinfo("Success","Medicine Record Updated")
                except :
                    messagebox.showerror("Error","Please Enter valid Information")

    
        def search():
            try:
                conn=sqlite3.connect('database.db')
                cursor=conn.cursor()
                if search_combo.get()=="Ref No":
                    cursor.execute(f"SELECT * from pharma where ref={insearch.get()}")
                    info=cursor.fetchall()
                    if info==[]:
                        messagebox.showinfo("Error","No record found")
                        return
                elif search_combo.get()=="MedName":
                    cursor.execute(f'SELECT * from pharma where name="{insearch.get()}"')
                    info=cursor.fetchall()
                    if info==[]:
                        messagebox.showinfo("Error","No record found")
                        return
                elif search_combo.get()=="Lot":
                    cursor.execute(f'SELECT * from pharma where lotno="{insearch.get()}"')
                    info=cursor.fetchall()
                    if info==[]:
                        messagebox.showinfo("Error","No record found")
                        return
                pharmacy_table.delete(*pharmacy_table.get_children())
                for record in info:
                        pharmacy_table.insert(parent='',index='end',iid=record[0],text="",values=record,tags="evenrow")
                insearch.delete(0,END)
                conn.commit()
                conn.close()
            except sqlite3.OperationalError:
                messagebox.showerror("Error","Please enter valid information")
            except Exception as e:
                messagebox.showinfo("Error",e)


        def medgetcursor(event=""):
            try:
                cursor_row=medtable.focus()
                content=medtable.item(cursor_row)
                row=content["values"]
                reset()
                inrefno2.insert(0,row[0])
                inmedname2.insert(0,row[1])
            except:
                pass
            

        def pharmagetcursor(event=""):
            try:
                cursor_row=pharmacy_table.focus()
                content=pharmacy_table.item(cursor_row)
                row=content["values"]
                clear()
                inref.set(row[0])
                incompanyname.insert(0,row[1]);intypeofmed.set(row[2]);inmedname.set(row[3]);inlotno.insert(0,row[4]);
                inissuedate.insert(0,row[5]);inexpdate.insert(0,row[6]);inuses.insert(0,row[7]);insideeffs.insert(0,row[8]);
                inprec.insert(0,row[9]);indosage.insert(0,row[10]);inprice.insert(0,row[11]);inqt.insert(0,row[12]);
            except:
                pass

        def clearall():
            try:
                showrefno1.destroy();showmedname1.destroy();showcompanyname1.destroy();showtypeofmed1.destroy();showlotno1.destroy();
                showissuedate1.destroy();showexpdate1.destroy();showdosage1.destroy();
                showprice1.destroy();showqt1.destroy();showuses1.destroy();showsideeffs1.destroy();showprec1.destroy()
                inshow.delete(0,END)
            except NameError:
                pass


        
        def view():
            
            view=Toplevel(root)
            view.geometry("1280x720+0+0")
            global ViewFrame
            ViewSearch=LabelFrame(view,relief=RIDGE,padx=20,bd=10,text="View Data BY Reference no..",
                                 fg="darkgreen",background="purple1",font=("arial",15,"bold"))
            ViewSearch.place(x=0,y=5,width=1280,height=120)
            ViewFrame=LabelFrame(view,bd=15,relief=RIDGE,padx=20,bg="mediumpurple4")
            ViewFrame.place(x=0,y=130,width=1280,height=500)
            showrefno=Label(ViewFrame,font=("ariel",12,"bold"),text='Reference No      :',bg="mediumpurple4",padx=4,pady=4,fg="black")
            showrefno.place(x=10,y=5)
            showmedname=Label(ViewFrame,text="Medicine Name   :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showmedname.place(x=10,y=50)

            showcompanyname=Label(ViewFrame,text="Company Name  :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showcompanyname.place(x=600,y=5)

            showtypeofmed=Label(ViewFrame,text="Medicine Type     :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showtypeofmed.place(x=600,y=50)
           
            showlotno=Label(ViewFrame,text="Lot No                   :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showlotno.place(x=10,y=95)
           
            showissuedate=Label(ViewFrame,text="Issue Date            :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showissuedate.place(x=600,y=95)

            showexpdate=Label(ViewFrame,text="Expiry Date          :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showexpdate.place(x=600,y=140)
           
            showdosage=Label(ViewFrame,text="Dosage                 :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showdosage.place(x=10,y=140)
           
            showprice=Label(ViewFrame,text="Price                      :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showprice.place(x=600,y=185)
       
            showqt=Label(ViewFrame,text="Quantity               :",font=("arial",12,"bold"),padx=2,bg="mediumpurple4",pady=4)
            showqt.place(x=10,y=185)
           
            showuses=Label(ViewFrame,text="Uses                      :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showuses.place(x=10,y=230)
           
            showsideeffs=Label(ViewFrame,text="Side Effects         :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=1)
            showsideeffs.place(x=10,y=275)
           
            showprec=Label(ViewFrame,text="Prec & Warning   :",font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
            showprec.place(x=10,y=320)

            
            lbl=Label(view,text="Enter Reference No. :",font=("calibri",14,"bold"),bg="purple1",padx=2,pady=4)
            lbl.place(x=10,y=35)
            
            btnview=Button(view,text="VIEW",font=("arial",10,"bold"),bg="lime",fg="white",width=14,command=show)
            btnview.place(x=400,y=40)
            btnclearall=Button(view,text="CLEARALL",font=("arial",10,"bold"),bg="red",fg="white",width=14,command=clearall)
            btnclearall.place(x=540,y=40)
            global inshow
            inshow=Entry(view,font=("arial",12,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
            inshow.place(x=190,y=40)
            
        def show():
            
            try:
                global showrefno1
                global showmedname1
                global showcompanyname1
                global showtypeofmed1
                global showlotno1
                global showissuedate1
                global showexpdate1
                global showdosage1
                global showuses1
                global showprice1
                global showqt1
                global showsideeffs1
                global showprec1
                conn=sqlite3.connect('database.db')
                cursor=conn.cursor()
                cursor.execute(f"SELECT * from pharma WHERE ref={inshow.get()}")
                details=cursor.fetchall()
                
                showrefno1=Label(ViewFrame,font=("ariel",12,"bold"),text=details[0][0],bg="mediumpurple4",padx=4,pady=4,fg="black")
                showrefno1.place(x=165,y=5)            
                showmedname1=Label(ViewFrame,text=details[0][3],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showmedname1.place(x=165,y=50)            
                showcompanyname1=Label(ViewFrame,text=details[0][1],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showcompanyname1.place(x=760,y=5)            
                showtypeofmed1=Label(ViewFrame,text=details[0][2],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showtypeofmed1.place(x=760,y=50)            
                showlotno1=Label(ViewFrame,text=details[0][4],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showlotno1.place(x=165,y=95)                        
                showissuedate1=Label(ViewFrame,text=details[0][5],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showissuedate1.place(x=760,y=95)            
                showexpdate1=Label(ViewFrame,text=details[0][6],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showexpdate1.place(x=760,y=140)                        
                showdosage1=Label(ViewFrame,text=details[0][10],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showdosage1 .place(x=165,y=140)                        
                showprice1=Label(ViewFrame,text=details[0][11],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showprice1.place(x=760,y=185)                    
                showqt1=Label(ViewFrame,text=details[0][12],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showqt1.place(x=165,y=185)                        
                showuses1=Label(ViewFrame,text=details[0][7],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showuses1.place(x=165,y=230)                        
                showsideeffs1=Label(ViewFrame,text=details[0][8],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=1)
                showsideeffs1.place(x=165,y=275)            
                showprec1=Label(ViewFrame,text=details[0][9],font=("arial",12,"bold"),bg="mediumpurple4",padx=2,pady=4)
                showprec1.place(x=165,y=320)
                conn.commit()
                conn.close()
            except IndexError:
                messagebox.showerror("Error","enter valid reference no!!")
            except sqlite3.OperationalError:
                messagebox.showerror("Error","Reference NO must be Integer ")

        
            
                
        

           
        #################Button Frame ######################
        
        ButtonFrame=Frame(self.root,bd=5,relief=SUNKEN,padx=20,bg="grey")
        ButtonFrame.place(x=0,y=235,width=1280,height=45)

        #------------------------ Button  -------------------------

        addbtn=Button(DataFrameLeft,text="ADD",font=("ariel",12,"bold"),bg="green2",fg="white",width=14,command=add)
        addbtn.place(x=375,y=168)
        updatebtn=Button(DataFrameLeft,text="UPDATE",font=("ariel",12,"bold"),bg="green2",fg="white",width=14,command=update)
        updatebtn.place(x=560,y=168)
        delbtn=Button(DataFrameLeft,text="DELETE",font=("ariel",12,"bold"),bg="green2",fg="white",width=14,command=delete)
        delbtn.place(x=375,y=209)
        resetbtn=Button(DataFrameLeft,text="CLEAR",font=("ariel",12,"bold"),bg="green2",fg="white",width=14,command=clear)
        resetbtn.place(x=560,y=209)
        exitbtn=Button(DataFrameLeft,text="EXIT",font=("ariel",12,"bold"),bg="green2",fg="white",width=14,command=root.destroy)   
        exitbtn.place(x=460,y=249)

        #------------------------Search by -------------------------------------

        lblsearch=Label(ButtonFrame,font=("ariel",12,"bold"),text='Search By',padx=10,pady=4,bg="red",fg="white")
        lblsearch.place(x=250,y=0)
    
        search_combo=ttk.Combobox(ButtonFrame,width=9,font=("arial",12,"bold"),state="readonly")
        search_combo["values"]=("Ref No","MedName","Lot")
        search_combo.current(0)
        search_combo.place(x=355,y=3)
        insearch=Entry(ButtonFrame,relief=RIDGE,width=12,font=("arial",12,"bold"))
        insearch.place(x=460,y=4)
            
        searchbtn=Button(ButtonFrame,text="SEARCH",font=("ariel",12,"bold"),bg="darkgreen",fg="white",width=10,command=search)
        searchbtn.place(x=575,y=0)
        showallbtn=Button(ButtonFrame,text="SHOW ALL",font=("ariel",12,"bold"),bg="darkgreen",fg="white",width=10,command=fetch_datapharma)
        showallbtn.place(x=687,y=0)
        viewbtn=Button(ButtonFrame,text="View",font=("ariel",12,"bold"),bg="darkgreen",fg="white",width=10,command=view)
        viewbtn.place(x=800,y=0)
        
        #-----------------------Label and entry In Left Frame------------------------------------

        
        def delcombo():
            inref.destroy()
            inmedname.destroy()
        def combo():
            conn=sqlite3.connect('database.db')
            cursor=conn.cursor()
            global inref
            global inmedname
            cursor.execute("SELECT ref from med")
            data=cursor.fetchall()
            inref=ttk.Combobox(DataFrameLeft,width=20,font=("arial",12,"bold"),state="readonly")
            inref["values"]=data
            inref.set("Select")        
            inref.grid(row=0,column=1)

            cursor.execute("SELECT medname from med")
            data=cursor.fetchall()
            inmedname=ttk.Combobox(DataFrameLeft,width=20,font=("arial",12,"bold"),state="readonly")
            inmedname["values"]=data
            inmedname.set("Select")        
            inmedname.grid(row=3,column=1)
            conn.commit()
            conn.close()    
        combo()
        
        lblref=Label(DataFrameLeft,text="Ref No :",font=("arial",12,"bold"),padx=2,pady=4)
        lblref.grid(row=0,column=0,sticky=W)

        lblmedname=Label(DataFrameLeft,text="Medicine Name :",font=("arial",12,"bold"),padx=2,pady=4)
        lblmedname.grid(row=3,column=0,sticky=W)

        lblcompanyname=Label(DataFrameLeft,text="Company Name :",font=("arial",12,"bold"),padx=2,pady=4)
        lblcompanyname.grid(row=1,column=0,sticky=W)
        incompanyname=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        incompanyname.grid(row=1,column=1)


        lbltypeofmed=Label(DataFrameLeft,text="Medicine Type :",font=("arial",12,"bold"),padx=2,pady=4)
        lbltypeofmed.grid(row=2,column=0,sticky=W)
        intypeofmed=ttk.Combobox(DataFrameLeft,width=20,font=("arial",12,"bold"),state="readonly")
        intypeofmed["values"]=("Select", "Tablet", "Capsule", "Injection", "Ayurvedic", "Drops", "Inhales")
        intypeofmed.current(0)        
        intypeofmed.grid(row=2,column=1)

        
        lbllotno=Label(DataFrameLeft,text="Lot No :",font=("arial",12,"bold"),padx=2,pady=4)
        lbllotno.grid(row=4,column=0,sticky=W)
        inlotno=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inlotno.grid(row=4,column=1)


        lblissuedate=Label(DataFrameLeft,text="Issue Date :",font=("arial",12,"bold"),padx=2,pady=4)
        lblissuedate.grid(row=5,column=0,sticky=W)
        inissuedate=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inissuedate.grid(row=5,column=1)


        lblexpdate=Label(DataFrameLeft,text="Expiry Date :",font=("arial",12,"bold"),padx=2,pady=4)
        lblexpdate.grid(row=6,column=0,sticky=W)
        inexpdate=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inexpdate.grid(row=6,column=1)


        lbluses=Label(DataFrameLeft,text="Uses :",font=("arial",12,"bold"),padx=2,pady=4)
        lbluses.grid(row=7,column=0,sticky=W)
        inuses=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inuses.grid(row=7,column=1)


        lblsideeffs=Label(DataFrameLeft,text="Side Effects :",font=("arial",12,"bold"),padx=2,pady=1)
        lblsideeffs.grid(row=8,column=0,sticky=W)
        insideeffs=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        insideeffs.grid(row=8,column=1)


        lblprec=Label(DataFrameLeft,text="Prec&Warning:",font=("arial",12,"bold"),padx=20,pady=4)
        lblprec.grid(row=0,column=2,sticky=W)
        inprec=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inprec.grid(row=0,column=3)


        lbldosage=Label(DataFrameLeft,text="Dosage :",font=("arial",12,"bold"),padx=20,pady=4)
        lbldosage.grid(row=1,column=2,sticky=W)
        indosage=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        indosage.grid(row=1,column=3)


        lblprice=Label(DataFrameLeft,text="Price :",font=("arial",12,"bold"),padx=20,pady=4)
        lblprice.grid(row=2,column=2,sticky=W)
        inprice=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inprice.grid(row=2,column=3)


        lblqt=Label(DataFrameLeft,text="Quantity :",font=("arial",12,"bold"),padx=20,pady=4)
        lblqt.grid(row=3,column=2,sticky=W)
        inqt=Entry(DataFrameLeft,font=("arial",13,"bold"),bg="white",bd=2,relief=RIDGE,width=22)
        inqt.grid(row=3,column=3)

        #-----------------------------Images---------------------------------
        lblslogan=Label(DataFrameLeft,font=("arial",12,"bold"),text='Stay Home Stay Safe',padx=2,pady=5,width=35,bg="white",fg="cyan")
        lblslogan.place(x=365,y=127)


        #------------------------------dataframeRight-------------------------------


        img7=Image.open(r"pharma.png")
        img7=img7.resize((140,140))
        self.photoimg7=ImageTk.PhotoImage(img7)
        b7=Label(DataFrameRight,image=self.photoimg7,borderwidth=0)
        b7.place(x=285,y=0)
        
        

        #Labels and entries
        lblrefno2=Label(DataFrameRight,font=("arial",10,"bold"),text='Reference No',padx=2,pady=4,fg="black")
        lblrefno2.place(x=0,y=90)
        inrefno2=Entry(DataFrameRight,font=("arial",10,"bold"),bg="white",bd=2,relief=RIDGE,width=15)
        inrefno2.place(x=130,y=90)

        lblmedname2=Label(DataFrameRight,font=("arial",10,"bold"),text='Medicine Name ',padx=2,pady=4,fg="black")
        lblmedname2.place(x=0,y=120)
        inmedname2=Entry(DataFrameRight,font=("arial",10,"bold"),bg="white",bd=2,relief=RIDGE,width=15)
        inmedname2.place(x=130,y=120)

        #--------------------------------TREE Frame -------------------------------

        Tree_Frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="white")
        Tree_Frame.place(x=0,y=150,width=290,height=120)

        sc_x=ttk.Scrollbar(Tree_Frame,orient=HORIZONTAL)
        sc_x.pack(side=BOTTOM,fill=X)
        sc_y=ttk.Scrollbar(Tree_Frame,orient=VERTICAL)
        sc_y.pack(side=RIGHT,fill=Y)
        

        medtable=ttk.Treeview(Tree_Frame,xscrollcommand=sc_x.set,yscrollcommand=sc_y.set)
        sc_y.config(command=medtable.yview)
        sc_x.config(command=medtable.xview)
        

        medtable['columns']=("ref","medname")
        medtable.column("#0",width=0,stretch=NO)
        medtable.column("ref",anchor=CENTER,width=50)
        medtable.column("medname",anchor=W,width=50)
        
        medtable.heading("#0",text="",anchor=CENTER)      
        medtable.heading("ref",text="Ref No.",anchor=CENTER)
        medtable.heading("medname",text="Medicine name ",anchor=W)

        medtable.tag_configure("oddrow",background="white")
        medtable.tag_configure("evenrow",background="lightblue")


        medtable.bind("<ButtonRelease-1>",medgetcursor)
        
        fetch_datamed()
        medtable.pack(fill=BOTH,expand=1)
       

        #---------------------------------new Side Frame---------------------------

        Down_Frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="magenta")
        Down_Frame.place(x=295,y=150,width=128,height=120)

        btnadd=Button(Down_Frame,text="ADD",font=("arial",10,"bold"),bg="lime",fg="white",width=14,command=add1)
        btnadd.grid(row=0,column=0)
        btnupdate=Button(Down_Frame,text="UPDATE",font=("arial",10,"bold"),bg="red",fg="white",width=14,command=update1)
        btnupdate.grid(row=1,column=0)
        btndelete=Button(Down_Frame,text="DELETE",font=("arial",10,"bold"),bg="purple",fg="white",width=14,command=delete1)
        btndelete.grid(row=2,column=0)
        btnclear=Button(Down_Frame,text="CLEAR",font=("arial",10,"bold"),bg="orange",fg="white",width=14,command=reset)
        btnclear.grid(row=3,column=0)
        
        
        #-----------------------------------------------Main Table And ScrollBar--------------------------------------
        
        MainFrame=Frame(root,bd=10,relief=RIDGE)
        MainFrame.place(x=0,y=70,width=1280,height=160)
        
        scroll_x=ttk.Scrollbar(MainFrame,orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y=ttk.Scrollbar(MainFrame,orient=VERTICAL)
        scroll_y.pack(side=RIGHT,fill=Y)

        pharmacy_table=ttk.Treeview(MainFrame,column=("ref","companyname","type","name","lotno","issuedate","expdate",
                                                            "uses","sideeffects","warning","dosage","price","quantity"),
                                                              xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        

        scroll_x.config(command=pharmacy_table.xview)
        scroll_y.config(command=pharmacy_table.yview)


        pharmacy_table["show"]="headings"
        pharmacy_table.heading("ref",text="Reference No.")
        pharmacy_table.heading("companyname",text="Company Name")
        pharmacy_table.heading("type",text="Medicine Type")
        pharmacy_table.heading("name",text="Medicine Name")
        pharmacy_table.heading("lotno",text="Lot No")
        pharmacy_table.heading("issuedate",text="Issue Date")
        pharmacy_table.heading("expdate",text="Expiry Date")
        pharmacy_table.heading("uses",text="Uses")
        pharmacy_table.heading("sideeffects",text="Side Effects")
        pharmacy_table.heading("warning",text="Warnings")
        pharmacy_table.heading("dosage",text="Dosage")
        pharmacy_table.heading("price",text="Price")
        pharmacy_table.heading("quantity",text="Quantity")
        pharmacy_table.pack(fill=BOTH,expand=1)


        pharmacy_table.column("ref",width=100)
        pharmacy_table.column("companyname",width=100)
        pharmacy_table.column("type",width=100)
        pharmacy_table.column("name",width=100)
        pharmacy_table.column("lotno",width=100)
        pharmacy_table.column("issuedate",width=100)
        pharmacy_table.column("expdate",width=100)
        pharmacy_table.column("uses",width=100)
        pharmacy_table.column("sideeffects",width=100)
        pharmacy_table.column("warning",width=100)
        pharmacy_table.column("dosage",width=100)
        pharmacy_table.column("price",width=100)
        pharmacy_table.column("quantity",width=100)

        pharmacy_table.bind("<ButtonRelease-1>",pharmagetcursor)

        
            


if __name__=="__main__": 
    root=Tk()
    obj=PharmacyManagmentSystem(root)
    root.mainloop()

   




        
        
