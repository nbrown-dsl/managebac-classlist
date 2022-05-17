import tkinter as tk
from functions.doc_output import mailmergeDoc
from functions.data import *


def genTranscript():
    """gen transcript doc
    """
    id = ent_temperature.get()
    studentObject = studentData(id)["student"]
    studentStart = studentObject["created_at"]
    years = studentTranscript(id, studentStart)
    mailmergeDoc(years,studentObject)

    lbl_result["text"] = "doc generated"

window = tk.Tk()
window.title("Transcript generator")
window.resizable(width=False, height=False)

frm_entry = tk.Frame(master=window)
ent_temperature = tk.Entry(master=frm_entry, width=40)
lbl_temp = tk.Label(master=frm_entry, text="student ID")

ent_temperature.grid(row=0, column=0, sticky="e")
lbl_temp.grid(row=0, column=1, sticky="w")

btn_convert = tk.Button(
    master=window,
    text="\N{RIGHTWARDS BLACK ARROW}",
    command=genTranscript
)
lbl_result = tk.Label(master=window, text="doc")

frm_entry.grid(row=0, column=0, padx=10)
btn_convert.grid(row=0, column=1, pady=10)
lbl_result.grid(row=0, column=2, padx=10)

window.mainloop()