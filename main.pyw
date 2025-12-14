# youtube downloader gui by ahmed reda saeed
# Importing Modules
from tkinter import * 
from tkinter import ttk
import yt_dlp

# Creating Main form & configure it
frm = Tk()
frm.title("Youtube Downloader By Ahmed Reda Saeed")
frm.geometry("800x600")
frm.resizable(False, False)
frm.config(bg="black")

# Creating Main Label
Label(frm,text="Youtube Downloader",fg="white",bg="darkblue",font=("Arial",20,"bold")).pack(fill=X)

Label(frm,text="Enter the URL",fg="white",bg="black",font=("Arial",20,"bold")).pack(fill=X)


# Creating Main Entry
url = StringVar()
Entry(frm,font=("Arial",20,"bold"),textvariable=url,bg="black",fg="white").pack(fill=X)

# Dictionary to map display text by format_id
format_map = {}

def get_info():
    global format_map
    format_map = {}  # Reset on new URL
    
    Url = url.get()
    opts = {
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(Url, download=False)
        formts = info.get('formats', [])
        
        display_list = []
        for f in formts:
            if f.get('height'):  # Only video formats
                label = f"{f.get('resolution')} - {f.get('ext')}"
                format_map[label] = f.get('format_id')  # Store mapping
                display_list.append(label)
        
        # Adding available qualities to combobox
        quals_combo['values'] = display_list
        quals_combo.pack(fill=X)

def Download():
    Url = url.get()
    
    if audio_only.get():
        # Audio only download
        opts = {
            'quiet': True,
            'format': 'bestaudio',
            'outtmpl': 'Downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        # Video download
        selected = chosen_qual.get()
        format_id = format_map.get(selected)
        
        if format_id:
            opts = {
                'quiet': True,
                'format': f'{format_id}+bestaudio/best',
                'outtmpl': 'Downloads/%(title)s.%(ext)s',
            }
        else:
            # Fallback to best quality
            opts = {
                'quiet': True,
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'Downloads/%(title)s.%(ext)s',
            }
    
    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([Url])

# Audio Only Checkbox
audio_only = BooleanVar()
Checkbutton(frm, text="Audio Only (MP3)", variable=audio_only, 
            font=("Arial", 14), bg="black", fg="white",
            selectcolor="gray20", activebackground="black",
            activeforeground="white").pack(fill=X)

# Creating Combobox without showing
chosen_qual = StringVar()
quals_combo = ttk.Combobox(frm, font=("Arial", 20, "bold"), textvariable=chosen_qual)

# Creating Getinfo Button
Button(frm, text="Get Info", font=("Arial", 20, "bold"), bg="darkblue", fg="white", command=get_info).pack(fill=X)

# Creating Download Button
Button(frm, text="Download", command=Download, font=("Arial", 20, "bold"), bg="darkblue", fg="white").pack(fill=X)

frm.mainloop()