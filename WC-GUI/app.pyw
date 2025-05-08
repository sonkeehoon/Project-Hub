'''  

An app that crawls Naver search results and generates a word cloud.

'''

__version__ = "0.0.1"


import os, sys
import tkinter as tk
from tkinter import filedialog, messagebox as msgbox
import tkinter.ttk as ttk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.request
import urllib.parse
from konlpy.tag import Okt
from collections import Counter

# Constants
BLOG = "blog"
CAFE = "cafe"
NEWS = "news"

# Calculate the start year and end year (start, today)
today = datetime.today().strftime("%Y.%m.%d")
start = today.split('.')
today = today.split('.')
year = 3 # Search for results from the past three years
start[0] = str(int(start[0]) - year)
start = ''.join(start)
today = ''.join(today)


# function
def update_progress_bar(state):
    p_var.set(state)
    progress_bar.update()
    
def naver_view_scrap(words):
    
    """This function crawls Naver blogs and cafes."""
    
    input_txt= ""
    
    # blog
    blog_url= f'''https://search.naver.com/search.naver?ssc=tab.{BLOG}.all&sm=tab_jum&query={words}&nso=p%3Afrom{start}to{today}'''
    blog_html= urllib.request.urlopen(blog_url)
    blog_soup= BeautifulSoup(blog_html, 'html.parser')
    blog_titles= blog_soup.find_all("a", "title_link")
    blog_contents= blog_soup.find_all("a", "dsc_link")
    
    for blog_title, blog_content in zip(blog_titles, blog_contents):
        input_txt+= blog_title.get_text()
        input_txt+= blog_content.get_text()
        
    # cafe
    cafe_url= f'''https://search.naver.com/search.naver?ssc=tab.{CAFE}.all&sm=tab_jum&query={words}&nso=p%3Afrom{start}to{today}'''
    cafe_html= urllib.request.urlopen(cafe_url)
    cafe_soup= BeautifulSoup(cafe_html, 'html.parser')
    cafe_titles= cafe_soup.find_all("a", "title_link")
    cafe_contents= cafe_soup.find_all("a", "dsc_link")
    
    for cafe_title, cafe_content in zip(cafe_titles, cafe_contents):
        input_txt+= cafe_title.get_text()
        input_txt+= cafe_content.get_text()
    
    return input_txt

def naver_news_scrap(words):
    
    input_txt= ""

    news_url= f'''https://search.naver.com/search.naver?ssc=tab.{NEWS}.all&where={NEWS}&sm=tab_jum&query={words}&nso=p%3Afrom{start}to{today}'''
    news_html= urllib.request.urlopen(news_url)
    news_soup= BeautifulSoup(news_html, 'html.parser')
    news_titles= news_soup.find_all("a", "news_tit")
    news_contents= news_soup.find_all("a", "api_txt_lines dsc_txt_wrap")

    for news_title, news_content in zip(news_titles, news_contents):
        input_txt+= news_title.get_text()
        input_txt+= news_content.get_text()

    return input_txt

def resource_path(relative_path):
    try:
        base_path= sys._MEIPASS
    except Exception:
        base_path= os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def browse_dest_path():
    folder_selected= filedialog.askdirectory()
    if folder_selected== "": # When the user clicks cancel
        print("Cancel folder selection")
        return
    txt_dest_path.delete(0, tk.END)
    txt_dest_path.insert(0, folder_selected)

def exit_window_x(): 
    # A function to fix the bug where the application doesn't close when the 'X' button is pressed
    print("The program will exit")
    win.quit() 

def makeWC(words):
    
    # Set working directory to WC-GUI
    script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    os.chdir(script_dir)
    
    cand_mask= np.array(Image.open(resource_path('./circle.png'))) # A canvas to create a circular wordcloud
    
    input_txt= ""
    now_state= 0
    parsed_word= urllib.parse.quote_plus(words)
    
    input_txt+= naver_news_scrap(parsed_word)
    now_state+= 25
    update_progress_bar(now_state)

    input_txt+= naver_view_scrap(parsed_word)
    now_state+= 25
    update_progress_bar(now_state)
    
    
    nlpy= Okt()
    nouns= nlpy.nouns(input_txt)
    count= Counter(nouns)
    tag_count= []
    tags= []

    for n, c in count.most_common(50):
        
        dics = {'tag': n, 'count': c}
        
        if len(dics['tag'])>= 2 and len(tags)<= 49:
            
            tag_count.append(dics)
            tags.append(dics['tag'])
            
    freq_file_name= words+ "_frequency.txt"
    freq_dest_path= os.path.join(txt_dest_path.get(), freq_file_name)
    f= open(freq_dest_path,"w", encoding="utf-8")

    for tag in tag_count:
        
        s= f"{tag['tag']:-<10}"
        f.write(str(s)+' '+str(tag['count'])+'\n')
    
    now_state+= 25
    update_progress_bar(now_state)
            
    wordcloud= WordCloud(
        font_path= 'malgun.ttf',
        background_color= 'white',
        mask= cand_mask
    ).generate(input_txt)
    
    plt.figure(figsize= (8, 8))
    plt.imshow(wordcloud, interpolation= 'bilinear')
    plt.axis('off')
    file_name= words+ ".png"
    dest_path= os.path.join(txt_dest_path.get(), file_name)
    plt.savefig(dest_path)
    now_state+= 25
    update_progress_bar(now_state)

def btnClick():
    
    if len(text.get())== 0:
        msgbox.showwarning("Warning", "Please enter a search term")
        return
    
    elif len(txt_dest_path.get())== 0:
        msgbox.showwarning("Warning", "Please select a save path")
        return
        
    try:
        words= text.get()
        makeWC(words)
        msgbox.showinfo("Completed", "The word cloud generation and frequency analysis are complete.\nPlease check the save path.")
        
    except Exception as err:
        msgbox.showerror("error", err)
    

# Window
win= tk.Tk()
win.title("WordCloud")
win.geometry('300x300')

# title
label= tk.Label(win, text= "Creating a word cloud")
label.pack(pady= 5)

# Search term input frame
frame= tk.LabelFrame(win, text= "Enter search term")
frame.pack(fill= "x", padx= 5, pady= 5)

text= tk.Entry(frame)
text.pack(side= "left", fill= "x", expand= True, padx= 5, pady= 5, ipady= 4)

btn= tk.Button(frame, text= "Create", width= 5, command= btnClick)
btn.pack(side= "left", padx= 5, pady= 5)

# Specify save path
path_frame= tk.LabelFrame(win, text= "Save path")
path_frame.pack(fill= "x", padx= 5, pady= 5, ipady= 5)

txt_dest_path= tk.Entry(path_frame)
txt_dest_path.pack(side= "left", fill= "x", expand= True, padx= 5, pady= 5, ipady= 4) # Change height

btn_dest_path= tk.Button(path_frame, text= "Browse", width= 10, command= browse_dest_path)
btn_dest_path.pack(side= "right", padx= 5, pady= 5)

# Progress
frame_progress= tk.LabelFrame(win, text= "Progress")
frame_progress.pack(fill= "x", padx= 5, pady= 5, ipady= 5)

p_var= tk.DoubleVar()
progress_bar= ttk.Progressbar(frame_progress, maximum= 100, variable= p_var)
progress_bar.pack(fill= "x", padx= 5, pady= 5)

win.protocol('WM_DELETE_WINDOW', exit_window_x)
win.mainloop()
