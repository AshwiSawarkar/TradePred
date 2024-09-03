import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def process_file(file_path):
    start_time = time.time()

    df = pd.read_csv(file_path, skiprows=1)
    selected_columns = ['CHNG IN OI', 'LTP', 'CHNG IN OI.1', 'LTP.1']
    df = df[selected_columns]

    # Processing CALL data
    df['CHNG IN OI'] = df['CHNG IN OI'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    df['CHNG IN OI'] = pd.to_numeric(df['CHNG IN OI'], errors='coerce')
    df['LTP'] = df['LTP'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    df['LTP'] = pd.to_numeric(df['LTP'], errors='coerce') 
    df['CHNG IN OI'] = df['CHNG IN OI'].fillna(0)
    df['LTP'] = df['LTP'].fillna(0)
    df['CALL TOTAL'] = df['CHNG IN OI'] * df['LTP']
    Call_sum = sum(df['CALL TOTAL'])

    # Processing PUT data
    df['CHNG IN OI.1'] = df['CHNG IN OI.1'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    df['CHNG IN OI.1'] = pd.to_numeric(df['CHNG IN OI.1'], errors='coerce')
    df['LTP.1'] = df['LTP.1'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
    df['LTP.1'] = pd.to_numeric(df['LTP.1'], errors='coerce') 
    df['CHNG IN OI.1'] = df['CHNG IN OI.1'].fillna(0)
    df['LTP.1'] = df['LTP.1'].fillna(0)
    df['PUT TOTAL'] = df['CHNG IN OI.1'] * df['LTP.1']
    put_sum = sum(df['PUT TOTAL'])

    # Calculate the difference
    difference = Call_sum - put_sum

    # Decision making
    if put_sum < 0 or Call_sum < 0:
        decision = 'NT'
    elif put_sum < Call_sum:
        decision = 'Buy PUT'
    elif put_sum > Call_sum:
        decision = 'Buy CALL'

    end_time = time.time()
    execution_time = end_time - start_time

    return Call_sum, put_sum, difference, decision, execution_time

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        Call_sum, put_sum, difference, decision, execution_time = process_file(file_path)
        show_large_messagebox("Results", f"CALL SUM: {Call_sum}\nPUT SUM: {put_sum}\nDifference (CALL - PUT): {difference}\nDecision: {decision}\nExecution Time: {execution_time:.2f} seconds")
    else:
        messagebox.showwarning("File Error", "You must select a valid CSV file.")

def show_large_messagebox(title, message):
    large_popup = tk.Toplevel(root)
    large_popup.title(title)
    large_popup.geometry("600x400")  # Adjust the size as needed
    tk.Label(large_popup, text=message, wraplength=550, justify="left", padx=20, pady=20).pack(expand=True)
    tk.Button(large_popup, text="OK", command=large_popup.destroy).pack(pady=20)

    # Close the popup after pressing OK
    large_popup.protocol("WM_DELETE_WINDOW", large_popup.destroy)

# Set up the GUI
root = tk.Tk()
root.title("Automated Decision Program")
root.geometry("400x200")  # Set the main window size

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

select_button = tk.Button(frame, text="Select File and Process", command=browse_file)
select_button.pack()

root.mainloop()
