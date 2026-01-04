import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import struct, threading, queue, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Schema definition

SCHEMA = {
    "Scenario Info 1": {
        "offset": 0x5A, "size": 631, "count": 1,
        "fields": [
            ("Number", "int", 1), ("Year", "int", 2), ("Month", "int", 1), 
            ("Unk", "int", 1), ("Name", "str", 26), ("Description", "str", 600)
        ]
    },
    "Scenario Info 2": {
        "offset": 0x673B, "size": 7, "count": 1,
        "fields": [
            ("In Game Year", "int", 2), ("In Game Month", "int", 1), ("Unk", "int", 1),
            ("Emperor", "int", 2), ("Game Mode (set to 1 for Rise Of Heroes)", "int", 1)
        ]
    },
    "Forces": {
        "offset": 0x3A4, "size": 607, "count": 42,
        "fields": [
            ("Difficulty", "int", 1), ("Description", "str", 606)
        ]
    },  
    "Officer": {
        "offset": 0x6D63, "size": 152, "count": 850,
        "fields": [
            ("Family Name", "str", 12), ("Given Name", "str", 12), ("padding", "pad", 29),
            ("Portrait", "int", 2), ("Sex", "int", 1), ("Available Date", "int", 2),
            ("Birth Date", "int", 2), ("Death Date", "int", 2), ("Death", "int", 1),
            ("Clan", "int", 2), ("Father", "int", 2), ("Mother", "int", 2),
            ("Generation", "int", 1), ("Spouse", "int", 2), ("Sworn Brother", "int", 2),
            ("Compatibility", "int", 1), ("Liked Officer 1", "int", 2), ("Liked Officer 2", "int", 2), ("Liked Officer 3", "int", 2),
            ("Liked Officer 4", "int", 2), ("Liked Officer 5", "int", 2), ("Disliked Officer 1", "int", 2), ("Disliked Officer 2", "int", 2),
            ("Disliked Officer 3", "int", 2), ("Disliked Officer 4", "int", 2), ("Disliked Officer 5", "int", 2), ("Allegiance", "int", 1),
            ("Service", "int", 2), ("Location", "int", 2), ("Status", "int", 1), ("Rank", "int", 1), ("Dependence", "int", 2),
            ("Loyalty", "int", 1), ("Deeds", "int", 2), ("Spear Affinity", "int", 1), ("Pike Affinity", "int", 1), ("Bow Affinity", "int", 1),
            ("Cavalry Affinity", "int", 1), ("Siege Affinity", "int", 1), ("Navy Affinity", "int", 1), ("LDR", "int", 1), ("WAR", "int", 1), ("INT", "int", 1),
            ("POL", "int", 1), ("CHR", "int", 1), ("LDR Growth", "int", 1), ("WAR Growth", "int", 1), ("INT Growth", "int", 1),
            ("POL Growth", "int", 1), ("CHR Growth", "int", 1), ("Birth Place", "int", 1), ("Skill", "int", 1), ("Debate Style", "int", 1), ("Virtue", "int", 1),
            ("Desire", "int", 1), ("Rank Selection", "int", 1), ("Character", "int", 1), ("Voice", "int", 1), ("Tone", "int", 1), ("Court Importance", "int", 1),
            ("Strategic Tendency", "int", 1), ("Local Affiliation", "int", 1), ("Model Stance", "int", 1), ("Model Head Gear", "int", 1), ("Model Face", "int", 1),
            ("Model Body", "int", 1), ("Model Cape", "int", 1), ("Model Arms", "int", 1), ("Model Boots", "int", 1), ("Model Arrows", "int", 1), ("Model Unk", "int", 1),
            ("Model Bow", "int", 1), ("Model Weapon", "int", 1), ("Model Horse", "int", 1), ("Portrait Age", "int", 1), ("Guide Cards", "int", 1), ("padding", "pad", 3),
        ]
    },
    "Item": {
        "offset": 0x26613, "size": 34, "count": 100,
        "fields": [
            ("Item Name", "str", 27), ("Item Type", "int", 1), ("Item Loyalty", "int", 1),
            ("Item Picture", "int", 1), ("Owner", "int", 2), ("Item City", "int", 1), ("Item Owner", "int", 1)
        ]
    },
    "Force Info": {
        "offset": 0x2735B, "size": 68, "count": 43,
        "fields": [
            ("Force Ruler", "int", 2), ("Strategist", "int", 2), ("Relationship 1", "int", 1),
            ("Relationship 2", "int", 1), ("Relationship 3", "int", 1), ("Relationship 4", "int", 1),
            ("Relationship 5", "int", 1), ("Relationship 6", "int", 1), ("Relationship 7", "int", 1),
            ("Relationship 8", "int", 1), ("Relationship 9", "int", 1), ("Relationship 10", "int", 1),
            ("Relationship 11", "int", 1), ("Relationship 12", "int", 1), ("Relationship 13", "int", 1),
            ("Relationship 14", "int", 1), ("Relationship 15", "int", 1), ("Relationship 16", "int", 1),
            ("Relationship 17", "int", 1), ("Relationship 18", "int", 1), ("Relationship 19", "int", 1),
            ("Relationship 20", "int", 1), ("Relationship 21", "int", 1), ("Relationship 22", "int", 1),
            ("Relationship 23", "int", 1), ("Relationship 24", "int", 1), ("Relationship 25", "int", 1),
            ("Relationship 26", "int", 1), ("Relationship 27", "int", 1), ("Relationship 28", "int", 1),
            ("Relationship 29", "int", 1), ("Relationship 30", "int", 1), ("Relationship 31", "int", 1),
            ("Relationship 32", "int", 1), ("Relationship 33", "int", 1), ("Relationship 34", "int", 1),
            ("Relationship 35", "int", 1), ("Relationship 36", "int", 1), ("Relationship 37", "int", 1),
            ("Relationship 38", "int", 1), ("Relationship 39", "int", 1), ("Relationship 40", "int", 1),
            ("Relationship 41", "int", 1), ("Relationship 42", "int", 1), ("Relationship Qiang", "int", 1),
            ("Relationship Shanyue", "int", 1), ("Relationship Whuhuan", "int", 1), ("Relationship Nanman", "int", 1),
            ("Relationship Bandits", "int", 1), ("Title", "int", 1), ("Country", "int", 1),
            ("Color", "int", 1), ("Goal", "int", 2), ("Alliance", "int", 7), ("Research", "int", 4), ("Unk", "int", 1)
        ]
    },
    "District": {
        "offset": 0x27FD7, "size": 8, "count": 42,
        "fields": [
            ("District Force", "int", 1), ("Number", "int", 1), ("District Ruler", "int", 2), ("Target", "int", 2), ("Specific Target", "int", 2)
        ]
    },
    "City Some Info": {
        "offset": 0x02D2, "size": 1, "count": 42,
        "fields": [
            ("City Color", "int", 1)
        ]
    },
    "City Most Info": {
        "offset": 0x2814F, "size": 81, "count": 42,
        "fields": [
            ("District", "int", 1), ("Max Troops", "int", 4), ("Troops", "int", 4),
            ("Gold", "int", 4), ("Food", "int", 4), ("padding_a", "pad", 4),
            ("Spears", "int", 4), ("Pikes", "int", 4), ("Bows", "int", 4),
            ("Horses", "int", 4), ("Rams", "int", 4), ("Towers", "int", 4),
            ("padding_b", "pad", 12), ("Ships", "int", 4), ("padding_c", "pad", 4),
            ("Unk", "int", 1), ("Trade", "int", 1), ("Revenue", "int", 2),
            ("Harvest", "int", 2), ("Max HP", "int", 2), ("Will", "int", 1),
            ("Order", "int", 1), ("Specialty", "int", 6)
        ]
    },
    "Gate Port": {
        "offset": 0x28E99, "size": 64, "count": 45,
        "fields": [
            ("District", "int", 1), ("Troops", "int", 4), ("Gold", "int", 4),
            ("Food", "int", 4), ("padding_d", "pad", 4), ("Spears", "int", 4),
            ("Pikes", "int", 4), ("Bows", "int", 4), ("Horses", "int", 4), ("Rams", "int", 4),
            ("Towers", "int", 4), ("padding_e", "pad", 12), ("Ships", "int", 4), ("padding_f", "pad", 4),
            ("Will", "int", 1), ("Unk", "int", 2)
        ]
    },
    "Country": {
        "offset": 0x299D9, "size": 103, "count": 84,
        "fields": [
            ("Name", "str", 17), ("Description", "str", 80), ("Unk_a", "int", 1),
            ("Unk_b", "int", 1), ("padding_g", "pad", 3)
        ]
    }
}

# Theme Logic

def apply_lilac_theme(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    bg = "#EFE6FF"          
    panel = "#F6F1FF"       
    tab_bg = "#E6D8FF"      
    tab_sel = "#D2B9FF"     
    entry_bg = "#FBF9FF"    
    tree_bg = "#FFFFFF"
    fg = "#2A2136"          
    subtle = "#6A5A7A"      

    try:
        root.configure(bg=bg)
    except Exception:
        pass

    style.configure(".", background=bg, foreground=fg)
    style.configure("TFrame", background=panel)
    style.configure("TLabel", background=panel, foreground=fg)
    style.configure("TLabelframe", background=panel, foreground=fg)
    style.configure("TLabelframe.Label", background=panel, foreground=fg)
    style.configure("TButton", background=tab_bg, foreground=fg, padding=6)
    style.map("TButton", background=[("active", tab_sel), ("pressed", tab_sel)], foreground=[("disabled", "#999999")])
    style.configure("TEntry", fieldbackground=entry_bg, background=panel, foreground=fg)
    style.configure("Vertical.TScrollbar", background=panel, troughcolor=bg)
    style.configure("Horizontal.TScrollbar", background=panel, troughcolor=bg)

    return {"bg": bg, "panel": panel, "entry_bg": entry_bg, "fg": fg, "subtle": subtle}

# Backend Lohic

class DataHandler:
    def __init__(self):
        self.raw_data = bytearray()
        self.parsed_data = {} 

    def load_file(self, filepath):
        with open(filepath, 'rb') as f:
            self.raw_data = bytearray(f.read())
        self.parse_all()

    def parse_all(self):
        self.parsed_data = {}
        for section_name, props in SCHEMA.items():
            offset = props['offset']
            count = props['count']
            struct_size = props['size']
            
            section_records = []
            for i in range(count):
                current_pos = offset + (i * struct_size)
                # Slice the buffer for this specific record
                record_bytes = self.raw_data[current_pos : current_pos + struct_size]
                
                record_dict = self.unpack_record(record_bytes, props['fields'])
                section_records.append(record_dict)
                
            self.parsed_data[section_name] = section_records

    def unpack_record(self, buffer, fields):
        data = {}
        ptr = 0
        
        for name, dtype, length in fields:
            if dtype == "pad":
                ptr += length
                continue
            
            chunk = buffer[ptr : ptr + length]
            
            if dtype == "int":
                # Use from_bytes to handle standard (1,2,4) and non-standard (6,7) lengths
                val = int.from_bytes(chunk, byteorder='little')
                data[name] = val
                
            elif dtype == "str":
                try:
                    # decoding with replace, prevents crashes on garbage data
                    val = chunk.decode('shift_jis', errors='replace').rstrip('\x00') 
                except:
                    val = ""
                data[name] = val
            
            ptr += length
            
        return data

    def save_mod(self, filepath):
        # Clone original file to preserve header/structure
        with open(filepath, 'wb') as f:
            f.write(self.raw_data)

        # Patch modified records
        with open(filepath, 'r+b') as f:
            for section_name, records in self.parsed_data.items():
                props = SCHEMA[section_name]
                base_offset = props['offset']
                struct_size = props['size']
                
                for i, record_dict in enumerate(records):
                    current_pos = base_offset + (i * struct_size)
                    
                    original_bytes = self.raw_data[current_pos : current_pos + struct_size]
                    new_bytes = self.pack_record(record_dict, props['fields'], original_bytes)
                    
                    if len(new_bytes) != struct_size:
                        print(f"Warning: Size mismatch for {section_name} {i}. Skipping write.")
                        continue

                    f.seek(current_pos)
                    f.write(new_bytes)

    def pack_record(self, data_dict, fields, original_bytes):
        buffer = bytearray(original_bytes) 
        ptr = 0
        
        for name, dtype, length in fields:
            if dtype == "pad":
                ptr += length
                continue
                
            val = data_dict.get(name)
            
            if dtype == "int":
                packed = b''
                try:
                    val = int(val)
                    # Use to_bytes to support arbitrary lengths (like 7 or 6)
                    # This replaces the limited struct.pack calls
                    packed = val.to_bytes(length, byteorder='little')
                except OverflowError:
                    # If value is too big for the field (e.g. > 255 for int 1)
                    # or negative (if unsigned), fallback to zeros or original
                    # For safety, we write 0 bytes if input is invalid
                    packed = b'\x00' * length
                except Exception:
                    packed = b'\x00' * length
                
                buffer[ptr : ptr + length] = packed
                
            elif dtype == "str":
                try:
                    # Encode to Shift-JIS, replace converts unsupported chars to ?
                    encoded = str(val).encode('shift_jis', errors='replace')
                    
                    if len(encoded) > length:
                        # Ensure null terminator exists if we fill the field
                        encoded = encoded[:length-1] + b'\x00'
                    else:
                        encoded = encoded + b'\x00' * (length - len(encoded))
                    buffer[ptr : ptr + length] = encoded
                except:
                    pass
            
            ptr += length
        return buffer

# GUI

class ScenarioEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vers Editor, ROTK XI Scenario Editor")
        self.root.geometry("900x650") 
        self.palette = apply_lilac_theme(root)
        self.handler = DataHandler()
        self.msg_queue = queue.Queue()
        self.setup_ui()
        self.root.after(100, self._check_queue)

    def setup_ui(self):
        toolbar = ttk.Frame(self.root, padding=5)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        ttk.Button(toolbar, text="Load Scenario", command=self.on_load).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Create Mod (.S11)", command=self.on_save).pack(side=tk.LEFT, padx=5)
        
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.palette["panel"], sashwidth=4)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_left = ttk.Frame(paned)
        self.section_list = tk.Listbox(frame_left, width=15, bg=self.palette["entry_bg"], fg=self.palette["fg"], bd=0, highlightthickness=1)
        self.section_list.bind('<<ListboxSelect>>', self.on_section_select)
        self.section_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        paned.add(frame_left)
        
        frame_mid = ttk.Frame(paned)
        sb_mid = ttk.Scrollbar(frame_mid, orient="vertical")
        self.record_list = tk.Listbox(frame_mid, width=20, bg=self.palette["entry_bg"], fg=self.palette["fg"], bd=0, highlightthickness=1, yscrollcommand=sb_mid.set)
        sb_mid.config(command=self.record_list.yview)
        self.record_list.bind('<<ListboxSelect>>', self.on_record_select)
        self.record_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_mid.pack(side=tk.RIGHT, fill=tk.Y)
        paned.add(frame_mid)
        
        self.editor_frame = ttk.Frame(paned)
        paned.add(self.editor_frame)
        self.canvas = tk.Canvas(self.editor_frame, bg=self.palette["panel"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.editor_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        self.entry_widgets = {} 
        self.current_section = None
        self.current_index = None

    def _check_queue(self):
        try:
            msg = self.msg_queue.get_nowait()
            if msg["type"] == "LOAD_DONE":
                self.populate_sections()
                messagebox.showinfo("Success", "File Loaded Successfully")
            elif msg["type"] == "SAVE_DONE":
                messagebox.showinfo("Success", "Mod Saved Successfully")
            elif msg["type"] == "ERROR":
                messagebox.showerror("Error", msg["text"])
        except queue.Empty:
            pass
        self.root.after(100, self._check_queue)

    def on_load(self):
        self.current_section = None
        self.current_index = None
        self.section_list.delete(0, tk.END)
        self.record_list.delete(0, tk.END)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        path = filedialog.askopenfilename()
        if not path: return
        threading.Thread(target=self.thread_load, args=(path,), daemon=True).start()

    def thread_load(self, path):
        try:
            self.handler.load_file(path)
            self.msg_queue.put({"type": "LOAD_DONE"})
        except Exception as e:
            self.msg_queue.put({"type": "ERROR", "text": str(e)})

    def on_save(self):
        # We also validate the currently open form before saving to file
        self.validate_and_save_entry()
        path = filedialog.asksaveasfilename(defaultextension=".S11", filetypes=[("Scenario Mod", "*.S11")])
        if not path: return
        threading.Thread(target=self.thread_save, args=(path,), daemon=True).start()

    def thread_save(self, path):
        try:
            self.handler.save_mod(path)
            self.msg_queue.put({"type": "SAVE_DONE"})
        except Exception as e:
            self.msg_queue.put({"type": "ERROR", "text": str(e)})

    def populate_sections(self):
        self.section_list.delete(0, tk.END)
        for section in SCHEMA.keys():
            self.section_list.insert(tk.END, section)

    def on_section_select(self, event):
        selection = self.section_list.curselection()
        if not selection: return
        
        # Save previous work
        self.validate_and_save_entry()
        
        # Clear the editor form
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.entry_widgets = {}
        self.current_index = None
        
        # Switch Section
        section_name = self.section_list.get(selection[0])
        self.current_section = section_name
        
        # Populate List
        self.record_list.delete(0, tk.END)
        count = len(self.handler.parsed_data[section_name])
        
        for i in range(count):
            record = self.handler.parsed_data[section_name][i]
            label = f"{section_name} {i}"
            
            # Naming Logic
            if section_name == "Officer":
                if 'Family Name' in record:
                     label += f" , {record['Family Name']} {record.get('Given Name', '')}"
            
            elif section_name == "Scenario Info 1":
                if 'Name' in record:
                    label += f" , {record['Name']}"

            elif section_name == "Item":
                if 'Item Name' in record:
                    label += f" , {record['Item Name']}"
            
            elif section_name == "Country":
                if 'Name' in record:
                    label += f" , {record['Name']}"

            self.record_list.insert(tk.END, label)

    def on_record_select(self, event):
        selection = self.record_list.curselection()
        if not selection: return
        self.validate_and_save_entry()
        index = selection[0]
        self.current_index = index
        self.build_form(self.current_section, index)

    def build_form(self, section, index):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.entry_widgets = {}

        data = self.handler.parsed_data[section][index]
        schema_fields = SCHEMA[section]['fields']
        
        row = 0
        for field in schema_fields:
            name, dtype, length = field
            if dtype == "pad": continue
            
            lbl = ttk.Label(self.scrollable_frame, text=name)
            lbl.grid(row=row, column=0, sticky="ne", padx=5, pady=5)
            
            val = data.get(name, "")
            
            if "description" in name.lower():
                # Text widget with word wrap
                txt_frame = ttk.Frame(self.scrollable_frame)
                txt_frame.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                
                txt = tk.Text(txt_frame, width=65, height=5, wrap="word", bg=self.palette["entry_bg"], fg=self.palette["fg"], relief="flat")
                txt.insert("1.0", str(val))
                txt.pack(side="left")
                
                tsb = ttk.Scrollbar(txt_frame, orient="vertical", command=txt.yview)
                txt.config(yscrollcommand=tsb.set)
                tsb.pack(side="right", fill="y")
                
                self.entry_widgets[name] = txt
            else:
                entry = ttk.Entry(self.scrollable_frame, width=50)
                entry.insert(0, str(val))
                entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)
                self.entry_widgets[name] = entry
                
            row += 1

    def validate_and_save_entry(self):
        """
        Validates input length/size before saving to memory,
        Warns user if truncation occurred
        """
        if self.current_section is None or self.current_index is None: return
        if self.current_section not in self.handler.parsed_data: return
        
        records = self.handler.parsed_data[self.current_section]
        if self.current_index >= len(records): return
        
        record = records[self.current_index]
        schema_fields = SCHEMA[self.current_section]['fields']
        
        # Create a map of field_name -> (dtype, length) for easy lookup
        field_props = {f[0]: (f[1], f[2]) for f in schema_fields}
        
        warnings = []

        for name, widget in self.entry_widgets.items():
            if name not in field_props: continue
            
            dtype, max_len = field_props[name]
            
            try:
                # Get raw input
                if isinstance(widget, tk.Text):
                    raw_val = widget.get("1.0", "end-1c")
                else:
                    raw_val = widget.get()

                # Validation Logic
                if dtype == "str":
                    try:
                        encoded = str(raw_val).encode('shift_jis')
                    except UnicodeEncodeError:
                        warnings.append(f"{name}: Invalid characters removed.")
                        encoded = str(raw_val).encode('shift_jis', 'ignore')

                    allowed_text_len = max_len - 1
                    
                    if len(encoded) > allowed_text_len:
                        warnings.append(f"{name}: Truncated to {allowed_text_len} bytes.")
                        truncated_bytes = encoded[:allowed_text_len]
                        final_val = truncated_bytes.decode('shift_jis')
                        
                        if isinstance(widget, tk.Text):
                            widget.delete("1.0", tk.END)
                            widget.insert("1.0", final_val)
                        else:
                            widget.delete(0, tk.END)
                            widget.insert(0, final_val)
                    else:
                        final_val = raw_val
                        
                    record[name] = final_val

                elif dtype == "int":
                    try:
                        int_val = int(raw_val)
                    except ValueError:
                        int_val = 0 
                    
                    # Dynamic Max Value Calculation
                    # 1 << (8 * max_len) is equivalent to 2^(8 * length)
                    # This works for length 1, 2, 4, 6, 7, etc
                    max_val = (1 << (8 * max_len)) - 1
                    
                    if int_val > max_val:
                        warnings.append(f"{name}: Value exceeds max for {max_len} bytes, clamped.")
                        int_val = max_val
                        widget.delete(0, tk.END)
                        widget.insert(0, str(int_val))
                    
                    record[name] = int_val

            except Exception as e:
                print(f"Error validating {name}: {e}")

        if warnings:
            messagebox.showwarning("Input Truncated", "\n".join(warnings))

if __name__ == "__main__":
    root = tk.Tk()
    app = ScenarioEditorApp(root)
    root.mainloop()


