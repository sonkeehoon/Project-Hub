# 내장 라이브러리
from pathlib import Path
from constants import *
import os

# 외장 라이브러리
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.messagebox as msgbox
from tkinter.colorchooser import *



def resource_path(relpath: str)-> str:
    
    try:
        abspath = sys._MEIPASS
    except Exception:
        abspath = os.path.abspath(".")
    return os.path.join(abspath, relpath)

def update_Entry(target: tk.Entry, content: str)-> None: # 엔트리 내용 갱신
    
    target.config(state="normal")
    target.delete(0, tk.END)
    target.insert(0, content)
    target.config(state="readonly")
    
def color_pick(txt_color: tk.StringVar)-> None:
    
    txt_color.set(askcolor()[1]) # askcolor() returns (RGB, HEX)
    
    if txt_color.get():
        font_color_Label.config(bg=txt_color.get(), 
                                text="현재 글자색")   

def add_file()-> None:
    
    file = filedialog.askopenfilename(title="이미지 파일을 선택하세요", 
                                      filetypes=[("이미지 파일","*.jpg;*.jpeg;*.png")])
    
    if file: update_Entry(image_ent, file)

def browse_dest_path()-> None:
    
    folder_selected = filedialog.askdirectory(title="저장 경로 선택")
    
    if folder_selected == "": # 사용자가 취소 누를때
        return
    
    if txt_dest_path: update_Entry(txt_dest_path, folder_selected)
    
def make_watermark()-> None:
    
    # 예외 처리
    if not image_ent.get(): # 이미지 선택 안한경우
        msgbox.showwarning("이미지 없음", "이미지를 선택하세요")
        return
    
    if not txt_entry.get(): # 텍스트 입력 안한경우
        msgbox.showwarning("텍스트 없음", "텍스트를 입력하세요")
        return
    
    if not txt_color.get(): # 글자색 선택 안한경우
        msgbox.showwarning("글자색 없음", "글자색을 선택하세요")
        return
    
    if not txt_dest_path.get(): # 저장경로 선택 안한경우
        msgbox.showwarning("저장경로 없음", "저장경로를 선택하세요")
        return
    
    # 워터마크 만들기
    try:
        
        img = Image.open(image_ent.get())
        width, height = img.size

        draw = ImageDraw.Draw(img)
        color = txt_color.get()
        text = txt_entry.get()
        
        """PIL ImageFont 적용"""
        
        pil_font = ImageFont.truetype(FONT_TYPE, FONT_SIZE)
        _, _, width_txt, height_txt = pil_font.getbbox(text)

        x = width - width_txt - MARGIN
        y = height - height_txt - MARGIN

        draw.text((x, y), text, fill = color, font=pil_font)
        
        dest_path = Path(txt_dest_path.get())
        filename, ext = Path(image_ent.get()).name.split('.')
        new_filename = filename + WATERMARK_SUFFIX + ext
        p = dest_path / new_filename
        
        img.save(p)
        msgbox.showinfo("알림", "작업이 완료되었습니다")
        
    except Exception as err:
        msgbox.showerror("error", err)


# 윈도우
win = tk.Tk()
ico = tk.PhotoImage(file=resource_path(ICON))
win.iconphoto(False, ico)
win.title(WINDOW_TITLE)
win.resizable(False, False)
win.configure(bg=BACKGROUND_COLOR)
win.geometry(WINDOW_SIZE)

# 탭 스타일 설정
#     탭 스타일은 구글링으로 찾아냈습니다
#     코드 : https://stackoverflow.com/questions/23038356/change-color-of-tab-header-in-ttk-notebook

style = ttk.Style()
style.theme_create("my_theme", parent="alt", settings={
        "TNotebook": {
            "configure": {"tabmargins": [2, 5, 2, 0] }},
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": FOREGROUND_COLOR},
            "map":       {"background": [("selected", BACKGROUND_COLOR)],
                          "foreground": [("selected", FOREGROUND_COLOR)],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )
style.theme_use("my_theme")
style.configure("TNotebook", background=BACKGROUND_COLOR, borderwidth=1)

# '생성' 탭 설정
notebook = ttk.Notebook(win)

tab1 = tk.Frame(notebook, bg=BACKGROUND_COLOR)
notebook.add(tab1, text="생성")

# 변수
txt_color = tk.StringVar()

# 워터마크 삽입할 이미지 선택
add_frame = tk.LabelFrame(tab1, text = "이미지 파일을 선택하세요", 
                          bg= BACKGROUND_COLOR, 
                          fg=FOREGROUND_COLOR, 
                          font=LABELFRAME_FONT)
add_frame.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

image_ent = tk.Entry(add_frame, fg=FOREGROUND_COLOR, 
                     insertbackground=FOREGROUND_COLOR, 
                     readonlybackground=ENTRY_BACKGROUND_COLOR, 
                     state="readonly")
image_ent.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5, ipady = 4) # 높이 변경

image_add_btn = tk.Button(add_frame, text = "이미지 찾기",
                          width = 10, command = add_file,
                          bg=SEARCH_BUTTON_COLOR['bg'], fg=FOREGROUND_COLOR, 
                          activebackground=SEARCH_BUTTON_COLOR['activebackground'], 
                          activeforeground=SEARCH_BUTTON_COLOR['activeforeground'], 
                          relief="ridge")
image_add_btn.pack(side = "right", padx = 5, pady = 5)

# 텍스트
frame_txt=tk.LabelFrame(tab1, text="텍스트", 
                        bg=BACKGROUND_COLOR, 
                        fg=FOREGROUND_COLOR, 
                        font=LABELFRAME_FONT)
frame_txt.pack(fill="both",padx=5,pady=5,ipady=5)

txt=tk.Label(frame_txt,text="넣고싶은 글자 :", 
             bg=BACKGROUND_COLOR, 
             fg=FOREGROUND_COLOR)
txt.grid(row=0, column=0, padx=5, pady=5, sticky="w")

txt_entry=tk.Entry(frame_txt, 
                   fg=FOREGROUND_COLOR, 
                   bg=ENTRY_BACKGROUND_COLOR, 
                   insertbackground=FOREGROUND_COLOR)
txt_entry.grid(row=0, column=1, padx=5,pady=5,ipady=4, sticky="we")

# 색상 선택
font_color=tk.Label(frame_txt, 
                    text="      글자 색상 :", 
                    bg=BACKGROUND_COLOR, 
                    fg=FOREGROUND_COLOR)
font_color.grid(row=1, column=0, padx=5, pady=5, sticky="w")

font_color_Label=tk.Label(frame_txt, text="색상을 선택하세요 ->", 
                          bg=ENTRY_BACKGROUND_COLOR, 
                          fg=FOREGROUND_COLOR, 
                          relief="solid")
font_color_Label.grid(row=1, column=1, padx=5, pady=5, ipady=4, sticky="we")

font_color_btn=tk.Button(frame_txt, text="색상 선택하기", 
                         bg="#FFA500", fg="black", 
                         activebackground="#FF8C00", 
                         activeforeground="black", 
                         command=lambda: color_pick(txt_color))
font_color_btn.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky="we")

# 저장 경로 설정
path_frame2 = tk.LabelFrame(tab1, text = "결과물을 저장할 위치를 선택하세요", 
                            bg=BACKGROUND_COLOR, 
                            fg=FOREGROUND_COLOR, 
                            font=LABELFRAME_FONT)
path_frame2.pack(fill = "x", padx = 5, pady = 5, ipady = 5)

txt_dest_path = tk.Entry(path_frame2, 
                         bg=ENTRY_BACKGROUND_COLOR, 
                         fg=FOREGROUND_COLOR, 
                         insertbackground=FOREGROUND_COLOR, 
                         readonlybackground=ENTRY_BACKGROUND_COLOR, state="readonly")
txt_dest_path.pack(side = "left", fill = "x", expand = True, padx = 5, pady = 5, ipady = 4) # 높이 변경

btn_dest_path= tk.Button(path_frame2, text = "경로 찾기",
                         width = 10, command = browse_dest_path,
                         bg=SEARCH_BUTTON_COLOR['bg'], fg=FOREGROUND_COLOR, 
                         activebackground=SEARCH_BUTTON_COLOR['activebackground'],
                         activeforeground=SEARCH_BUTTON_COLOR['activeforeground'],
                         relief="ridge")
btn_dest_path.pack(side = "right", padx = 5, pady = 5)

# 만들기 버튼
frame_run=tk.Frame(tab1, bg=BACKGROUND_COLOR)
frame_run.pack(fill="x",padx=5,pady=5)

btn_close=tk.Button(frame_run, text="닫기", 
                    width=12, command=win.quit, 
                    bg="#4CAF50", fg=FOREGROUND_COLOR, 
                    activebackground="#388E3C", 
                    activeforeground="black", 
                    relief="ridge")
btn_close.pack(side="right", padx=5, pady=5)

btn_start=tk.Button(frame_run, text="만들기", 
                    width=12, command=make_watermark, 
                    bg="#D32F2F", fg=FOREGROUND_COLOR, 
                    activebackground="#B71C1C", 
                    activeforeground="black", 
                    relief="ridge")
btn_start.pack(side="right",padx=5,pady=5)

# '개발 환경' 탭 설정
tab2 = tk.Frame(notebook, bg=BACKGROUND_COLOR)
notebook.add(tab2, text='개발 환경')

label2 = tk.Label(tab2, 
                  text=f"Python 버전\t{PYTHON_VERSION}\n라이브러리\t{LIBRARY}\n운영체제\t\t{OS}\n편집기\t\t{IDE}{EMPTY_SPACE*15}\n업데이트 내역\t{UPDATE_HISTORY}", 
                  justify="left", 
                  background=BACKGROUND_COLOR, 
                  foreground=FOREGROUND_COLOR, 
                  font=INFO_FONT)
label2.pack(pady=20)

# '개발자 정보' 탭 설정
tab3 = tk.Frame(notebook, bg=BACKGROUND_COLOR)
notebook.add(tab3, text="개발자 정보")

label3 = tk.Label(tab3,
                  text=f"개발자\t{DEVELOPER_NAME}\n이메일\t{EMAIL_ADDRESS}\n깃허브\t{GITHUB_URL}{EMPTY_SPACE*10}\n제작일\t{CREATION_DATE}",
                  justify="left", 
                  background=BACKGROUND_COLOR, 
                  foreground=FOREGROUND_COLOR, 
                  font=INFO_FONT)
label3.pack(pady=20)


notebook.pack(expand=True, fill="both")

win.mainloop()