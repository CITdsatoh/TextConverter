import tkinter as tk
import tkinter.filedialog as filedialog
import os
from tkinter import messagebox

class TextConverter:

  def __init__(self):
    self.master=tk.Tk()
    self.master.geometry("1536x1536")
    self.master.title("ファイルのテキスト変換機")
    self.UI=tk.Label(self.master,text="テキスト変換機\n例えば，プログラムを書いていて突然変数名を変更したくなったときありませんか?\nもし，ある変数名を変えた時，その変数に対して,全箇所変数名を手動で修正するのは面倒くさいですよね？\nこのアプリは，ファイル内のあるテキスト全箇所に対して，指定した別のテキストに変えてくれるものです",font=("",20,"bold"))
    self.UI.place(x=32,y=16)
    self.read=tk.Label(self.master,text="読込元ファイル:指定されていません",font=("",16,"bold"))
    self.read.place(x=256,y=160)
    self.write=tk.Label(self.master,text="書き込み先ファイル:指定されていません",font=("",16,"bold"))
    self.write.place(x=256,y=192)
    self.fieldlist=[]
    self.before=tk.Label(self.master,text="変更前のテキスト")
    self.before.place(x=40,y=224)
    self.after=tk.Label(self.master,text="変更後のテキスト")
    self.after.place(x=384,y=224)
    for i in range(16):
      textfield={}
      textfield["from"]=tk.Entry(self.master)
      place_y=(i*32)+256
      textfield["from"].place(x=40,y=place_y,width=216)
      textfield["fromlabel"]=tk.Label(self.master,text="の箇所を")
      textfield["fromlabel"].place(x=256,y=place_y,width=128)
      textfield["to"]=tk.Entry(self.master)
      textfield["to"].place(x=384,y=place_y,width=216)
      textfield["tolabel"]=tk.Label(self.master,text="へ変更")
      textfield["tolabel"].place(x=672,y=place_y)
      textfield["errser_btn"]=tk.Button(self.master,text="消去")
      textfield["errser_btn"].place(x=768,y=place_y,width=128)
      textfield["errser_btn"].bind('<1>',self.errser)
      self.fieldlist.append(textfield)
    
    self.rewritebtn=tk.Button(self.master,text="変更した内容を上書き保存")
    self.rewritebtn.place(x=1024,y=256)
    self.rewritebtn.bind('<1>',self.rewrite)
    self.newwritebtn=tk.Button(self.master,text="変更した内容を別のファイルに保存")
    self.newwritebtn.place(x=1024,y=320)
    self.newwritebtn.bind('<1>',self.newwrite)
    self.redobtn=tk.Button(self.master,text="先ほど選択されたファイルに対して,同じ動作をもう一度行う")
    self.redobtn.place(x=1024,y=384)
    self.redobtn.bind('<1>',self.writing)
    self.resetbtn=tk.Button(self.master,text="すべての入力されたテキスト情報をリセット")
    self.resetbtn.place(x=1024,y=448)
    self.resetbtn.bind('<1>',self.reset)
    self.allresetbtn=tk.Button(self.master,text="すべてのテキスト情報と入出力ファイル情報をリセット")
    self.allresetbtn.place(x=1024,y=512)
    self.allresetbtn.bind('<1>',self.reset)
    self.quitbtn=tk.Button(self.master,text="終了")
    self.quitbtn.place(x=1024,y=576)
    self.quitbtn.bind('<1>',self.quit)
    
    self.readfiles=[]
    self.writefiles=[]
    self.writefilecontent=[]
    
    self.master.mainloop()

  def errser(self,event):
    eventbtn=event.widget
    eventindex=-1
    for i in range(len(self.fieldlist)):
     if self.fieldlist[i]["errser_btn"] == eventbtn:
        eventindex=i
        break
    
    for i in range(eventindex,len(self.fieldlist)-1):
      nextfromstr=self.fieldlist[i+1]["from"].get()
      nexttostr=self.fieldlist[i+1]["to"].get()
      self.fieldlist[i]["from"].delete(0,tk.END)
      self.fieldlist[i]["from"].insert(0,nextfromstr)
      self.fieldlist[i]["to"].delete(0,tk.END)
      self.fieldlist[i]["to"].insert(0,nexttostr)
    
    last=len(self.fieldlist)-1
    self.fieldlist[last]["from"].delete(0,tk.END)
    self.fieldlist[last]["to"].delete(0,tk.END)

  def rewrite(self,event):
    candidate_list,error_flag=self.arrange()
    if len(candidate_list) ==0:
      messagebox.showerror("エラー","変更するテキストが何も入力されていません")
      return
    if error_flag:
      messagebox.showerror("エラー","空文字列を通常の文字列に変更することはできません.その箇所は無視されます")
    self.readfiles=[]
    self.writefiles=[]
    ftype=[("","*.txt;*.csv;*.c;*.java;*.py;*.js;*.cpp;*.html;*.css;*,ini;*.rb;*.vbs")]
    idir=os.path.abspath(os.path.dirname(__file__))
    self.readfiles=filedialog.askopenfilenames(filetypes=ftype,initialdir=idir,title="テキストを変更したいファイルを選択してください(上書き保存されます)")
    while len(self.readfiles) == 0:
     ans=messagebox.askquestion("ファイルの選択","引き続きファイルの選択を続けますか?")
     if ans != "yes":
       return
     self.readfiles=filedialog.askopenfilenames(filetypes=ftype,initialdir=idir,title="テキストを変更したいファイルを選択してください(上書き保存されます)")
  
    dispstrread="読込元ファイル:"
    dispstrwrite="書き込み先ファイル:"
    for fname in self.readfiles:
      dispstrread=dispstrread+","+fname
      dispstrwrite=dispstrwrite+","+fname
    self.read.config(text=dispstrread)
    self.write.config(text=dispstrwrite)
    self.writefiles=self.readfiles[::]
    self.writing(event)

  def newwrite(self,event):
    candidate_list,error_flag=self.arrange()
    if len(candidate_list) ==0:
      messagebox.showerror("エラー","変更するテキストが何も入力されていません")
      return
    if error_flag:
      messagebox.showerror("エラー","空文字列を通常の文字列に変更することはできません.その箇所は無視されます")
    self.readfiles=[]
    self.writefiles=[]
    ftype=[("","*.txt;*.csv;*.c;*.java;*.py;*.js;*.cpp;*.html;*.css;*,ini;*.rb;*.vbs")]
    idir=os.path.abspath(os.path.dirname(__file__))
    self.readfiles=filedialog.askopenfilenames(filetypes=ftype,initialdir=idir,title="テキストを変更したい読み取りファイルを選んでください(変更した結果は別ファイルに保存されます)")
    while len(self.readfiles) == 0:
     ans=messagebox.askquestion("ファイルの選択","引き続きファイルの選択を続けますか?")
     if ans != "yes":
       return
     self.readfiles=filedialog.askopenfilenames(filetypes=ftype,initialdir=idir,title="テキストを変更したい読み取りファイルを選んでください(変更した結果は別ファイルに保存されます)")
    self.choosewritefiles()
    dispstrread="読込元ファイル:"
    dispstrwrite="書き込み先ファイル:"
    for fname in self.readfiles:
      dispstrread=dispstrread+","+fname
    for fname in self.writefiles:
      dispstrwrite=dispstrwrite+","+fname
    self.read.config(text=dispstrread)
    self.write.config(text=dispstrwrite)
    self.writing(event)

  def writing(self,event):
    rwlist,error_flag=self.arrange()
    if len(self.readfiles) == 0 and len(self.writefiles) == 0:
      messagebox.showerror("ファイルが未選択","ファイルの選択が行われていません。まずはファイルを選択してください")
      result=messagebox.askyesnocancel("ファイルを選択","これからファイルの選択を行いますが，上書きモードでよろしいですか?\nyes・・上書きモード,no・・別ファイル書き込み,cancel・・キャンセル")
      if result:
        self.rewrite(event)
        return
      elif result == False:
         self.newwrite(event)
         return
      elif result == None:
          return
     
    if len(rwlist) == 0:
       messagebox.showerror("エラー","変更するテキストが何も入力されていません")
       return
    if error_flag:
       messagebox.showerror("エラー","空文字列を通常の文字列に変更することはできません.その箇所は無視されます")
       
    for i in range(0,len(self.readfiles)):
      with open(self.readfiles[i],encoding="UTF-8") as file:
       try:
        self.writefilecontent=file.readlines()
       except PermissonError:
        messagebox.showerror("エラー","読み込もうとしたファイルが開かれているため，読み込みができませんでした。ファイルを閉じてください")
       finally:
        file.close()
      prechangecontent=self.writefilecontent[::]
      for combi_num in range(0,len(rwlist)):
       replaced_flag = self.hasReplaced(rwlist[combi_num][0],rwlist,combi_num)
       for line in range(len(self.writefilecontent)):
         if not replaced_flag or prechangecontent[line].find(rwlist[combi_num][0]) != -1:
            self.writefilecontent[line]=self.writefilecontent[line].replace(rwlist[combi_num][0],rwlist[combi_num][1])
            
      with open(self.writefiles[i],mode='w',encoding="UTF-8") as file:
        try:
         file.writelines(self.writefilecontent)
        except PermissonError:
         messagebox.showerror("エラー","選択したファイルが開かれているせいで書き込みができませんでした。ファイルを閉じてください")
        finally:
         file.close()
     
    messagebox.showinfo("書き込み完了","書き込みが終了しました")
        
  def choosewritefiles(self):
    messagebox.showinfo("書き込みファイルは1つずつ","書き込みファイルは複数選択ではなく，1つずつ選んでもらいます。よって，全部で"+str(len(self.readfiles))+"回選択処理を繰り返します")
    ftype=[("","*.txt;*.csv;*.c;*.java;*.py;*.js;*.cpp;*.html;*.css;*,ini;*.rb;*.vbs")]
    idir=os.path.abspath(os.path.dirname(__file__))
    for i in range(0,len(self.readfiles)):
      messagebox.showinfo(str(i+1)+"回目",str(i+1)+"回目.ファイル"+self.readfiles[i]+"の結果を保存するファイルを選んでください")
      tmpfname=filedialog.asksaveasfilename(filetypes=ftype,initialdir=idir,title="テキストを変更した結果を保存したファイルを選んでください.\nこれは"+self.readfiles[i]+"の結果を保存します",defaultextension=TextConverter.getExtension(self.readfiles[i]))
      while len(tmpfname) == 0:
        ans=messagebox.askquestion("ファイルの選択","引き続きファイルの選択を続けますか?(ここでやめてしまうと，先ほど選択した読み取り用のファイル情報もなくなります")
        if ans != "yes":
          self.readfiles=[]
          self.writefiles=[]
          return
        tmpfname=filedialog.asksaveasfilename(filetypes=ftype,initialdir=idir,title="テキストを変更した結果を保存したファイルを選んでください\nこれは"+self.readfiles[i]+"の結果を保存します",defaultextension=TextConverter.getExtension(self.readfiles[i]))
      self.writefiles.append(tmpfname) 

  def arrange(self):
     rwlist=[]
     error_flag=False
     for textfield in self.fieldlist:
       rwcombi=[]
       prereplace=textfield["from"].get()
       postreplace=textfield["to"].get()
       if len(prereplace) != 0:
         rwcombi.append(prereplace)
         rwcombi.append(postreplace)
         rwlist.append(rwcombi)
       elif len(postreplace) != 0:
         error_flag=True
       
     return rwlist,error_flag
     
  def hasReplaced(self,current_prereplace,lists,finished):
     
       for i in range(0,finished+1):
          if current_prereplace == lists[i][1]:
            return True 
       return False
       
      
  
  @classmethod
  def getExtension(cls,file):
     start=file.rfind(".")
     if start == -1:
       return ""
     return file[start:len(file)]
       
  def reset(self,event):
     for textfield in self.fieldlist:
       textfield["from"].delete(0,tk.END)
       textfield["to"].delete(0,tk.END)
     
     if event.widget == self.allresetbtn:
       self.readfiles=[]
       self.writefiles=[]
       self.writefilecontent=""
       self.read.config(text="読込元ファイル:指定されていません")
       self.write.config(text="書き込み先ファイル:指定されていません")
       
  def quit(self,event):
     self.master.destroy()           

     
    
      
      
    
