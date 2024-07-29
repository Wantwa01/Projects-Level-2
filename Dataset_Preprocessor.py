import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

root = tk.Tk()
root.title("Data Preprocessor")
root.geometry("800x600")

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            global df
            df = pd.read_csv(file_path)
            display_data(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

def display_data(dataframe):
    text.delete("1.0", tk.END)
    text.insert(tk.END, dataframe.head())

def handle_missing_values():
    missing_value_option = missing_values_var.get()
    if missing_value_option == "Drop Rows":
        df.dropna(inplace=True)
    elif missing_value_option == "Fill with Mean":
        df.fillna(df.mean(), inplace=True)
    display_data(df)

def encode_categorical_variables():
    for column in df.select_dtypes(include=['object']).columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        
    display_data(df)

def scale_features():
    scaler = StandardScaler()
    df[df.columns] = scaler.fit_transform(df[df.columns])
    display_data(df)

def split_data():
    train_size = float(train_size_entry.get())
    train, test = train_test_split(df, train_size=train_size)
    messagebox.showinfo("Success", f"Data split into {len(train)} training samples and {len(test)} testing samples.")

def save_file(dataframe):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    if file_path:
        dataframe.to_csv(file_path, index=False)
        messagebox.showinfo("Save File", "File saved successfully to " + file_path)
    
upload_button = tk.Button(root, text="Upload CSV", command=upload_file)
upload_button.pack()

text = tk.Text(root, wrap='none', height=15)
text.pack()

missing_values_var = tk.StringVar()
missing_values_var.set("Drop Rows")

drop_rows_rb = tk.Radiobutton(root, text="Drop Rows", variable=missing_values_var, value="Drop Rows")
fill_mean_rb = tk.Radiobutton(root, text="Fill with Mean", variable=missing_values_var, value="Fill with Mean")

drop_rows_rb.pack()
fill_mean_rb.pack()

handle_missing_button = tk.Button(root, text="Handle Missing Values", command=handle_missing_values)
handle_missing_button.pack()

encode_button = tk.Button(root, text="Encode Categorical Variables", command=encode_categorical_variables)
encode_button.pack()

scale_button = tk.Button(root, text="Scale Features", command=scale_features)
scale_button.pack()

train_size_label = tk.Label(root, text="Training Set Size (0-1):")
train_size_label.pack()

train_size_entry = tk.Entry(root)
train_size_entry.pack()
train_size_entry.insert(0, "0.8")

split_button = tk.Button(root, text="Split Data", command=split_data)
split_button.pack()

save_button = tk.Button(root, text="Save dataset", command=lambda : save_file(df))
save_button.pack()

root.mainloop()
