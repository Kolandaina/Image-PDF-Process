import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from PIL import Image
import PyPDF2
from pathlib import Path
import threading

class ImagePDFProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("图片PDF处理工具")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Create main frame
        self.create_widgets()
        
    def create_widgets(self):
        # Create notebook widget (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Image merge tab
        self.image_frame = ttk.Frame(notebook)
        notebook.add(self.image_frame, text="图片合并为PDF")
        self.create_image_merge_widgets()
        
        # PDF merge tab
        self.pdf_frame = ttk.Frame(notebook)
        notebook.add(self.pdf_frame, text="PDF合并")
        self.create_pdf_merge_widgets()
        
    def create_image_merge_widgets(self):
        # Folder selection area
        folder_frame = ttk.LabelFrame(self.image_frame, text="选择图片文件夹", padding=10)
        folder_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.folder_path_var = tk.StringVar()
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=60)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        folder_btn = ttk.Button(folder_frame, text="选择文件夹", command=self.select_folder)
        folder_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Image type selection area
        type_frame = ttk.LabelFrame(self.image_frame, text="选择图片类型", padding=10)
        type_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.image_types = {
            'PNG': tk.BooleanVar(value=True),
            'JPG': tk.BooleanVar(value=True),
            'JPEG': tk.BooleanVar(value=True),
            'WEBP': tk.BooleanVar(),
            'BMP': tk.BooleanVar(),
            'TIFF': tk.BooleanVar()
        }
        
        for i, (ext, var) in enumerate(self.image_types.items()):
            cb = ttk.Checkbutton(type_frame, text=ext, variable=var)
            cb.grid(row=i//3, column=i%3, sticky=tk.W, padx=10, pady=2)
        
        # Image list area
        list_frame = ttk.LabelFrame(self.image_frame, text="图片文件列表", padding=10)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create listbox and scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True)
        
        self.image_listbox = tk.Listbox(list_container, selectmode=tk.EXTENDED)
        scrollbar_img = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.image_listbox.yview)
        self.image_listbox.configure(yscrollcommand=scrollbar_img.set)
        
        self.image_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_img.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button area
        btn_frame = ttk.Frame(self.image_frame)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        refresh_btn = ttk.Button(btn_frame, text="刷新列表", command=self.refresh_image_list)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        merge_btn = ttk.Button(btn_frame, text="合并为PDF", command=self.merge_images_to_pdf)
        merge_btn.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress_img = ttk.Progressbar(self.image_frame, mode='indeterminate')
        self.progress_img.pack(fill=tk.X, padx=10, pady=5)
        
    def create_pdf_merge_widgets(self):
        # PDF file selection area
        pdf_select_frame = ttk.LabelFrame(self.pdf_frame, text="选择PDF文件", padding=10)
        pdf_select_frame.pack(fill=tk.X, padx=10, pady=5)
        
        select_btn = ttk.Button(pdf_select_frame, text="选择PDF文件", command=self.select_pdf_files)
        select_btn.pack(side=tk.LEFT)
        
        clear_btn = ttk.Button(pdf_select_frame, text="清空列表", command=self.clear_pdf_list)
        clear_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # PDF file list area
        pdf_list_frame = ttk.LabelFrame(self.pdf_frame, text="PDF文件列表（按顺序合并）", padding=10)
        pdf_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Create listbox and scrollbar
        pdf_container = ttk.Frame(pdf_list_frame)
        pdf_container.pack(fill=tk.BOTH, expand=True)
        
        self.pdf_listbox = tk.Listbox(pdf_container, selectmode=tk.EXTENDED)
        scrollbar_pdf = ttk.Scrollbar(pdf_container, orient=tk.VERTICAL, command=self.pdf_listbox.yview)
        self.pdf_listbox.configure(yscrollcommand=scrollbar_pdf.set)
        
        self.pdf_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_pdf.pack(side=tk.RIGHT, fill=tk.Y)
        
        # List operation buttons
        list_btn_frame = ttk.Frame(self.pdf_frame)
        list_btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        up_btn = ttk.Button(list_btn_frame, text="上移", command=self.move_pdf_up)
        up_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        down_btn = ttk.Button(list_btn_frame, text="下移", command=self.move_pdf_down)
        down_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        remove_btn = ttk.Button(list_btn_frame, text="移除选中", command=self.remove_selected_pdf)
        remove_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        merge_pdf_btn = ttk.Button(list_btn_frame, text="合并PDF", command=self.merge_pdfs)
        merge_pdf_btn.pack(side=tk.RIGHT)
        
        # Progress bar
        self.progress_pdf = ttk.Progressbar(self.pdf_frame, mode='indeterminate')
        self.progress_pdf.pack(fill=tk.X, padx=10, pady=5)
        
    def select_folder(self):
        folder = filedialog.askdirectory(title="选择包含图片的文件夹")
        if folder:
            self.folder_path_var.set(folder)
            self.refresh_image_list()
    
    def refresh_image_list(self):
        folder_path = self.folder_path_var.get()
        if not folder_path or not os.path.exists(folder_path):
            messagebox.showwarning("警告", "请先选择有效的文件夹")
            return
        
        # Get selected file types
        selected_types = []
        for ext, var in self.image_types.items():
            if var.get():
                selected_types.extend([f'.{ext.lower()}', f'.{ext.upper()}'])
        
        if not selected_types:
            messagebox.showwarning("警告", "请至少选择一种图片类型")
            return
        
        # Clear list
        self.image_listbox.delete(0, tk.END)
        
        # Get image files
        image_files = []
        try:
            for file in os.listdir(folder_path):
                if any(file.endswith(ext) for ext in selected_types):
                    image_files.append(file)
            
            # Sort in dictionary order
            image_files.sort()
            
            # Add to listbox
            for file in image_files:
                self.image_listbox.insert(tk.END, file)
                
            messagebox.showinfo("信息", f"找到 {len(image_files)} 个图片文件")
            
        except Exception as e:
            messagebox.showerror("错误", f"读取文件夹失败：{str(e)}")
    
    def merge_images_to_pdf(self):
        folder_path = self.folder_path_var.get()
        if not folder_path:
            messagebox.showwarning("警告", "请先选择文件夹")
            return
        
        if self.image_listbox.size() == 0:
            messagebox.showwarning("警告", "没有找到图片文件")
            return
        
        # 选择保存位置
        output_file = filedialog.asksaveasfilename(
            title="保存PDF文件",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")]
        )
        
        if not output_file:
            return
        
        # 在新线程中执行合并操作
        thread = threading.Thread(target=self._merge_images_thread, args=(folder_path, output_file))
        thread.daemon = True
        thread.start()
    
    def _merge_images_thread(self, folder_path, output_file):
        try:
            self.progress_img.start()
            
            # Get all image file paths
            image_files = []
            for i in range(self.image_listbox.size()):
                filename = self.image_listbox.get(i)
                image_files.append(os.path.join(folder_path, filename))
            
            # Convert images and save as PDF
            images = []
            for img_path in image_files:
                try:
                    img = Image.open(img_path)
                    # Convert to RGB mode (required for PDF)
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    images.append(img)
                except Exception as e:
                    print(f"处理图片 {img_path} 时出错：{str(e)}")
            
            if images:
                # Save as PDF
                images[0].save(output_file, save_all=True, append_images=images[1:])
                
                self.root.after(0, lambda: messagebox.showinfo("成功", f"图片已成功合并为PDF：\n{output_file}"))
            else:
                self.root.after(0, lambda: messagebox.showerror("错误", "没有有效的图片文件"))
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"合并图片失败：{str(e)}"))
        finally:
            self.progress_img.stop()
    
    def select_pdf_files(self):
        files = filedialog.askopenfilenames(
            title="选择PDF文件",
            filetypes=[("PDF文件", "*.pdf")]
        )
        
        for file in files:
            # 避免重复添加
            if file not in [self.pdf_listbox.get(i) for i in range(self.pdf_listbox.size())]:
                self.pdf_listbox.insert(tk.END, file)
    
    def clear_pdf_list(self):
        self.pdf_listbox.delete(0, tk.END)
    
    def move_pdf_up(self):
        selection = self.pdf_listbox.curselection()
        if not selection or selection[0] == 0:
            return
        
        index = selection[0]
        item = self.pdf_listbox.get(index)
        self.pdf_listbox.delete(index)
        self.pdf_listbox.insert(index - 1, item)
        self.pdf_listbox.selection_set(index - 1)
    
    def move_pdf_down(self):
        selection = self.pdf_listbox.curselection()
        if not selection or selection[0] == self.pdf_listbox.size() - 1:
            return
        
        index = selection[0]
        item = self.pdf_listbox.get(index)
        self.pdf_listbox.delete(index)
        self.pdf_listbox.insert(index + 1, item)
        self.pdf_listbox.selection_set(index + 1)
    
    def remove_selected_pdf(self):
        selection = self.pdf_listbox.curselection()
        if selection:
            # 从后往前删除，避免索引变化
            for index in reversed(selection):
                self.pdf_listbox.delete(index)
    
    def merge_pdfs(self):
        if self.pdf_listbox.size() < 2:
            messagebox.showwarning("警告", "请至少选择两个PDF文件")
            return
        
        # 选择保存位置
        output_file = filedialog.asksaveasfilename(
            title="保存合并后的PDF文件",
            defaultextension=".pdf",
            filetypes=[("PDF文件", "*.pdf")]
        )
        
        if not output_file:
            return
        
        # 在新线程中执行合并操作
        pdf_files = [self.pdf_listbox.get(i) for i in range(self.pdf_listbox.size())]
        thread = threading.Thread(target=self._merge_pdfs_thread, args=(pdf_files, output_file))
        thread.daemon = True
        thread.start()
    
    def _merge_pdfs_thread(self, pdf_files, output_file):
        try:
            self.progress_pdf.start()
            
            merger = PyPDF2.PdfMerger()
            
            for pdf_file in pdf_files:
                try:
                    merger.append(pdf_file)
                except Exception as e:
                    print(f"处理PDF文件 {pdf_file} 时出错：{str(e)}")
            
            # Save merged PDF
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            merger.close()
            
            self.root.after(0, lambda: messagebox.showinfo("成功", f"PDF文件已成功合并：\n{output_file}"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("错误", f"合并PDF失败：{str(e)}"))
        finally:
            self.progress_pdf.stop()

def main():
    root = tk.Tk()
    app = ImagePDFProcessor(root)
    root.mainloop()

if __name__ == "__main__":
    main()