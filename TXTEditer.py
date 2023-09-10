import tkinter as tk
from tkinter import Menu, messagebox, filedialog, Toplevel, Canvas, Scrollbar, Button, Label, Entry, Frame, StringVar, END
import re
from zhconv import convert
import os

# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))

class TXTEditor:
    def __init__(self, root):
    
        self.root = root
        self.root.title("Dylan's TXT Editor")
        self.root.geometry("800x600")
        self.left_status_text = StringVar()
        self.right_status_text = StringVar()

        # 获取ICO图标的绝对路径
        icon_path = os.path.join(script_directory, "ico/TXTEditer.ico")

        # 加载ICO图标
        root.iconbitmap(default=icon_path)

        # 创建Text组件
        self.text_widget = tk.Text(root, wrap=tk.WORD, undo=True, autoseparators=True)
        self.text_widget.pack(fill=tk.BOTH, expand=tk.YES)
        
        self.menu_bar = Menu(root)
        self.root.config(menu=self.menu_bar)

    # 以下是菜单栏

        # 创建文档菜单、格式单
        self.document_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="文档", menu=self.document_menu)
        self.format_menu = Menu(self.menu_bar, tearoff=0)

        # 添加文档菜单项
        self.document_menu.add_command(label="打开文档", command=self.open_document)
        self.document_menu.add_command(label="保存文档", command=self.save_document)
        self.document_menu.add_command(label="另存文档", command=self.save_document_as)

        # 创建编辑菜单
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="编辑", menu=self.edit_menu)

        # 添加编辑菜单项
        self.edit_menu.add_command(label="剪切 （Ctrl+X）", command=self.cut)
        self.edit_menu.add_command(label="复制 （Ctrl+C）", command=self.copy)
        self.edit_menu.add_command(label="粘贴 （Ctrl+V）", command=self.paste)
        self.edit_menu.add_separator()        
        self.edit_menu.add_command(label="撤销 （Ctrl+Z）", command=self.undo)
        self.edit_menu.add_command(label="重做 （Ctrl+Y）", command=self.redo)

        # 创建功能菜单
        self.format_menu = Menu(self.menu_bar, tearoff=0)
        self.symbol_menu = Menu(self.menu_bar, tearoff=0)
        self.encoding_menu = Menu(self.menu_bar, tearoff=0)
        self.replace_menu = Menu(self.menu_bar, tearoff=0)

        # 添加功能菜单到菜单栏
        self.menu_bar.add_cascade(label="排版", menu=self.format_menu)
        self.menu_bar.add_cascade(label="符号", menu=self.symbol_menu)
        self.menu_bar.add_cascade(label="编码", menu=self.encoding_menu)
        self.menu_bar.add_cascade(label="替换", menu=self.replace_menu)

        # 排版菜单
        self.format_menu.add_command(label="段首缩进", command=self.indent_paragraph)
        self.format_menu.add_command(label="去掉空格", command=self.remove_spaces)
        self.format_menu.add_command(label="增加段落空行", command=self.add_paragraph_spacing)
        self.format_menu.add_command(label="去掉段落空行", command=self.delete_paragraph_spacing)
        self.format_menu.add_separator() #这种是分隔线（下同）
        self.format_menu.add_command(label="半角符号转全角", command=self.half_to_full_width)
        self.format_menu.add_command(label="全角符号转半角", command=self.full_to_half_width)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="中文简体转繁体", command=self.simplify_to_traditional)
        self.format_menu.add_command(label="中文繁体转简体", command=self.traditional_to_simplify)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="英文小写转大写", command=self.lower_to_upper)
        self.format_menu.add_command(label="英文大写转小写", command=self.upper_to_lower)
        self.format_menu.add_command(label="英文句首字母转大写", command=self.capitalize_sentences)
        self.format_menu.add_command(label="英文词首字母转大写", command=self.capitalize_words)

        # 符号菜单
        self.symbol_menu.add_command(label="常用符号", command=self.insert_symbol) 
        self.symbol_menu.add_command(label="特殊符号", command=self.insert_special_symbol)             
        self.symbol_menu.add_command(label="数学符号", command=self.insert_math_symbol)
        self.symbol_menu.add_command(label="序列符号", command=self.insert_sequence_symbol) 
        self.symbol_menu.add_command(label="希腊字母", command=self.insert_greek_alphabet)
        self.symbol_menu.add_command(label="日文假名", command=self.insert_japanese_kana)
        self.symbol_menu.add_command(label="制表符号", command=self.insert_table_symbol) 

        # 编码菜单
        self.encoding_menu.add_command(label="转换为Big5码", command=self.convert_to_big5)
        self.encoding_menu.add_command(label="转换为UTF-8", command=self.convert_to_utf8)

        # 替换菜单
        self.replace_menu.add_command(label="替换", command=self.replace_text)

        # 创建关于菜单项
        self.menu_bar.add_command(label="关于", command=self.show_about_info)

    # 以下是状态栏

        # 创建状态栏
        self.status_bar = tk.Label(root, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 设置左侧的文本
        self.left_status_text.set("行: 1  列: 1     字符数: 0     编码: UTF-8")
        self.status_bar.config(textvariable=self.left_status_text)

        # 创建一个标签来显示右侧的文本，使用空格填充以保持布局
        right_status_label = tk.Label(self.status_bar, text="软件作者: Dylan Lim", anchor=tk.E)
        right_status_label.pack(side=tk.RIGHT)

        # 设置右侧的文本
        self.right_status_text.set("软件作者: Dylan Lim")
        right_status_label.config(textvariable=self.right_status_text)

        # 添加滚动条
        scroll_y = tk.Scrollbar(self.text_widget)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.config(yscrollcommand=scroll_y.set)
        scroll_y.config(command=self.text_widget.yview)

        # 绑定事件处理程序
        self.text_widget.bind("<KeyRelease>", self.update_status_bar)

    def update_status_bar(self, event):
        # 获取当前光标位置
        cursor_position = self.text_widget.index(tk.INSERT)

        # 获取文本总字符数
        text_content = self.text_widget.get(1.0, tk.END)
        char_count = len(text_content)

        # 获取文本编码方式
        encoding = self.text_widget.tk.call("encoding", "system")

        # 更新状态栏文本
        status_text = f"行: {cursor_position.split('.')[0]} 列: {cursor_position.split('.')[1]} 字符数: {char_count} 编码: {encoding}   软件作者: Dylan Lim"
        self.status_bar.config(text=status_text)

    # 以下是系统功能

    # 打开文档功能
    def open_document(self):
        # 打开文档
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.text_widget.delete("1.0", "end")
                self.text_widget.insert("1.0", content)
    
    # 保存文档功能
    def save_document(self):
        # 保存文档
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            content = self.text_widget.get("1.0", "end")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

    # 另存文档功能
    def save_document_as(self):
        # 另存文档
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            content = self.text_widget.get("1.0", "end")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

    # 剪切文本
    def cut(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)

    # 复制文本
    def copy(self):
        selected_text = self.text_widget.get(tk.SEL_FIRST, tk.SEL_LAST)
        self.root.clipboard_clear()
        self.root.clipboard_append(selected_text)

    # 粘贴文本
    def paste(self):
        clipboard_text = self.root.clipboard_get()
        self.text_widget.insert(tk.INSERT, clipboard_text)

    # 撤销功能
    def undo(self):
        # 撤销操作
        try:
            self.text_widget.edit_undo()
        except Exception as e:
            messagebox.showerror("错误", "无法撤销：" + str(e))

    # 重做功能
    def redo(self):
        # 重做操作
        try:
            self.text_widget.edit_redo()
        except Exception as e:
            messagebox.showerror("错误", "无法重做：" + str(e))

    # 段首缩进
    def indent_paragraph(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，缩进整个文档
            text = self.text_widget.get("1.0", "end")
            paragraphs = text.split('\n')
            indented_paragraphs = ["　　" + paragraph if paragraph else paragraph for paragraph in paragraphs]
            indented_text = "\n".join(indented_paragraphs)

            # 替换整个文档内容
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", indented_text)
            return

        # 获取所选文本的起始和结束位置
        sel_start = self.text_widget.index(tk.SEL_FIRST)
        sel_end = self.text_widget.index(tk.SEL_LAST)

        if sel_start and sel_end:
            # 有文本被选中，只缩进选中部分
            start_line, start_col = map(int, sel_start.split("."))
            end_line, end_col = map(int, sel_end.split("."))
            
            selected_text = self.text_widget.get(sel_start, sel_end)
            indented_text = "　　" + selected_text.replace("\n", "\n　　")

            # 替换所选文本
            self.text_widget.delete(sel_start, sel_end)
            self.text_widget.insert(sel_start, indented_text)

    # 删除空格
    def remove_spaces(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            
            # 使用正则表达式将多个回车替换为一个回车
            text = re.sub(r'(\n\r|\n|\r)+', '\n', text)
            
            # 删除全角、半角空格
            text = re.sub(r'[ 　]+', '', text)
            
            # 删除文本开头的回车
            text = text.lstrip('\n')
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 使用正则表达式将多个回车替换为一个回车
                selected_text = re.sub(r'(\n\r|\n|\r)+', '\n', selected_text)
                
                # 删除全角、半角空格
                selected_text = re.sub(r'[ 　]+', '', selected_text)
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, selected_text)

    # 增加空行
    def add_paragraph_spacing(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            
            # 使用正则表达式在段落之间插入一个空行
            text = re.sub(r'(?<=\S)\n(?=\S)', '\n\n', text)
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 使用正则表达式在段落之间插入一个空行
                selected_text = re.sub(r'(?<=\S)\n(?=\S)', '\n\n', selected_text)
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, selected_text)

    # 删除段落间空行
    def delete_paragraph_spacing(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            
            # 使用正则表达式删除段落之间的空行
            text = re.sub(r'(\S)\n{2,}(\S)', r'\1\n\2', text)
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 使用正则表达式删除段落之间的空行
                selected_text = re.sub(r'(\S)\n{2,}(\S)', r'\1\n\2', selected_text)
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, selected_text)

    # 半角字符转全角功能
    def half_to_full_width(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            full_width_text = ''.join([chr(0xFF00 + ord(char) - 32) if 32 <= ord(char) <= 126 else char for char in text])
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", full_width_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的半角符号转为全角符号
                full_width_text = ''.join([chr(0xFF00 + ord(char) - 32) if 32 <= ord(char) <= 126 else char for char in selected_text])
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, full_width_text)

    # 全角字符转半角字符功能
    def full_to_half_width(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            half_width_text = ''.join([chr(0x0020 + ord(char) - 0xFF00) if 0xFF00 <= ord(char) <= 0xFF5E else char for char in text])
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", half_width_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的全角符号转为半角符号
                half_width_text = ''.join([chr(0x0020 + ord(char) - 0xFF00) if 0xFF00 <= ord(char) <= 0xFF5E else char for char in selected_text])
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, half_width_text)

    # 中文简转繁功能
    def simplify_to_traditional(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            converted_text = convert(text, 'zh-hant')  # 中文简转繁
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", converted_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的中文简转繁
                converted_text = convert(selected_text, 'zh-hant')
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, converted_text)

    # 中文繁转简功能
    def traditional_to_simplify(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            converted_text = convert(text, 'zh-hans')  # 中文繁转简
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", converted_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的中文繁转简
                converted_text = convert(selected_text, 'zh-hans')
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, converted_text)

    # 添加英文小写转大写功能
    def lower_to_upper(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            converted_text = text.upper()  # 英文字符转为大写
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", converted_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的英文字符转为大写
                converted_text = selected_text.upper()
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, converted_text)

    # 添加英文大写转小写功能
    def upper_to_lower(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            converted_text = text.lower()  # 英文字符转为小写
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", converted_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的英文字符转为小写
                converted_text = selected_text.lower()
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, converted_text)

    # 添加英文句首字母转大写功能
    def capitalize_sentences(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            sentences = text.split('.')  # 假设句子以句号分隔
            converted_sentences = [sentence.strip().capitalize() for sentence in sentences]
            converted_text = '. '.join(converted_sentences)
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", converted_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的句子首字母转为大写
                sentences = selected_text.split('.')  # 假设句子以句号分隔
                converted_sentences = [sentence.strip().capitalize() for sentence in sentences]
                converted_text = '. '.join(converted_sentences)
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, converted_text)
    
    # 添加英文单词首字母转大写功能
    def capitalize_words(self):
        # 检查是否有文本被选中
        if not self.text_widget.tag_ranges(tk.SEL):
            # 如果没有文本被选中，操作整个文档
            text = self.text_widget.get("1.0", "end")
            converted_text = text.title()
            
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", converted_text)
        else:
            # 获取所选文本的起始和结束位置
            sel_start = self.text_widget.index(tk.SEL_FIRST)
            sel_end = self.text_widget.index(tk.SEL_LAST)
            
            if sel_start and sel_end:
                # 有文本被选中，只执行所选文本部分
                selected_text = self.text_widget.get(sel_start, sel_end)
                
                # 将选定的单词首字母转为大写
                converted_text = selected_text.title()
                
                # 替换所选文本
                self.text_widget.delete(sel_start, sel_end)
                self.text_widget.insert(sel_start, converted_text)

    # 插入常用符号
    def insert_symbol(self):
        # 创建一个顶级窗口用于选择符号
        symbol_window = Toplevel(self.root)
        symbol_window.geometry("360x240")  # 设置窗口大小为 320x240
        symbol_window.title("插入常用符号")  # 设置窗口标题为"插入常用符号"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(symbol_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建常用符号表
        symbols = [
            "，", "。", "？", "！", "：", "；", "、", "…", "……", "“", "”",
            "‘", "’", "「", "」", "（", "）", "［", "］", "｛", "｝", "＜", "＞",
            "《", "》", "【", "】", "〖", "〗", "/", "\\", "～", "＠", "＃", "＆",
            "—", "|", "＋", "－", "×", "÷", "＝", "←", "↙", "↓", "↘", "→", "↗", "↑", "↖"
            "㏂", "㏘", "♂", "♀", "※", "№"
        ]

        row, col = 0, 0
        buttons = []
        for symbol in symbols:
            symbol_button = tk.Button(canvas, text=symbol, command=lambda s=symbol: self.insert_symbol_text(s))
            symbol_button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(symbol_button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row + 1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    def insert_symbol_text(self, symbol):
        if symbol:
            self.text_widget.insert(tk.INSERT, symbol)

    # 插入特殊符号
    def insert_special_symbol(self):
        # 创建一个顶级窗口用于选择特殊符号
        special_symbol_window = Toplevel(self.root)
        special_symbol_window.geometry("360x280")  # 设置窗口大小为 360x240
        special_symbol_window.title("插入特殊符号")  # 设置窗口标题为"插入特殊符号"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(special_symbol_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建特殊符号表
        special_symbols = [
            "℃", "®", "™", "©", "§", "¥", "＄", "€", "℗", "℡", "㏇", "•", "▪", "‥", "…", "∷", 
            "△", "▽", "◁", "▷", "○", "◇", "□", "☆", "♤", "♡", "♢", "♧", 
            "▲", "▼", "◀", "▶", "●", "◆", "■", "★", "♠", "♥", "♦", "♣", 
            "㊤", "㊧", "㊦", "㊨", "㊥", "㊣", 
            "♔", "♕", "♗", "♘", "♖", "♙", "♚", "♛", "♝", "♞", "♜", "♟", 
        ]

        row, col = 0, 0
        buttons = []
        for special_symbol in special_symbols:
            special_symbol_button = tk.Button(canvas, text=special_symbol, command=lambda s=special_symbol: self.insert_symbol_text(s))
            special_symbol_button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(special_symbol_button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row + 1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    # 插入数学符号
    def insert_math_symbol(self):
        # 创建一个顶级窗口用于选择数学符号
        math_symbol_window = Toplevel(self.root)
        math_symbol_window.geometry("360x240")  # 设置窗口大小为 360x240
        math_symbol_window.title("插入数学符号")  # 设置窗口标题为"插入数学符号"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(math_symbol_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建数学符号表
        math_symbols = [
            "+", "-", "×", "÷", "=", "≠", "<", ">", "≤", "≥",
            "∞", "∑", "∏", "∫", "√", "∛", "∜", "∝", "∂", "∆",
            "∈", "∉", "∋", "∌", "∩", "∪", "∫", "∮", "∴", "∵",
            "°", "′", "″", "∠", "≈", "≡", "≢", "≤", "≥", "≪",
            "≫", "⊕", "⊖", "⊗", "⊘", "⊙", "⊚", "⊛", "⊜", "⊝"
        ]

        row, col = 0, 0
        buttons = []
        for math_symbol in math_symbols:
            math_symbol_button = tk.Button(canvas, text=math_symbol, command=lambda s=math_symbol: self.insert_symbol_text(s))
            math_symbol_button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(math_symbol_button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row + 1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    # 插入序列符号
    def insert_sequence_symbol(self):
        # 创建一个顶级窗口用于选择序列符号
        sequence_symbol_window = Toplevel(self.root)
        sequence_symbol_window.geometry("360x420")  # 设置窗口大小为 360x240
        sequence_symbol_window.title("插入序列符号")  # 设置窗口标题为"插入序列符号"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(sequence_symbol_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建序列符号表
        sequence_symbols = [
            "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩",
            "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳",
            "⑴", "⑵", "⑶", "⑷", "⑸", "⑹", "⑺", "⑻", "⑼", "⑽",
            "⑾", "⑿", "⒀", "⒁", "⒂", "⒃", "⒄", "⒅", "⒆", "⒇",
            "⒈", "⒉", "⒊", "⒋", "⒌", "⒍", "⒎", "⒏", "⒐", "⒑",
            "⒒", "⒓", "⒔", "⒕", "⒖", "⒗", "⒘", "⒙", "⒚", "⒛",
            "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "❿",
            "㈠", "㈡", "㈢", "㈣", "㈤", "㈥", "㈦", "㈧", "㈨", "㈩",
            "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ",
            "ⅰ", "ⅱ", "ⅲ", "ⅳ", "ⅴ", "ⅵ", "ⅶ", "ⅷ", "ⅸ", "ⅹ",
        ]

        row, col = 0, 0
        buttons = []
        for sequence_symbol in sequence_symbols:
            sequence_symbol_button = tk.Button(canvas, text=sequence_symbol, command=lambda s=sequence_symbol: self.insert_symbol_text(s))
            sequence_symbol_button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(sequence_symbol_button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row + 1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    # 插入希腊字母
    def insert_greek_alphabet(self):
        # 创建一个顶级窗口用于选择希腊字母
        greek_alphabet_window = Toplevel(self.root)
        greek_alphabet_window.geometry("320x240")  # 设置窗口大小为 320x240
        greek_alphabet_window.title("插入希腊字母")  # 设置窗口标题为"插入希腊字母"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(greek_alphabet_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建希腊字母符号表
        greek_alphabet = [
            "Α", "α", "Β", "β", "Γ", "γ", "Δ", "δ", "Ε", "ε", "Ζ", "ζ", "Η", "η", "Θ", "θ", "Ι", "ι", "Κ", "κ", "Λ", "λ",
            "Μ", "μ", "Ν", "ν", "Ξ", "ξ", "Ο", "ο", "Π", "π", "Ρ", "ρ", "Σ", "σ", "ς", "Τ", "τ", "Υ", "υ", "Φ", "φ", "Χ", 
            "χ", "Ψ", "ψ", "Ω", "ω"
        ]

        row, col = 0, 0
        buttons = []
        for letter in greek_alphabet:
            button = Button(canvas, text=letter, command=lambda l=letter: self.insert_symbol_text(l))
            button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row+1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    # 插入日文假名
    def insert_japanese_kana(self):
        # 创建一个顶级窗口用于选择日文假名
        japanese_kana_window = Toplevel(self.root)
        japanese_kana_window.geometry("360x380")  # 设置窗口大小为 360x240
        japanese_kana_window.title("插入日文假名")  # 设置窗口标题为"插入日文假名"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(japanese_kana_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建日文假名符号表
        japanese_kana = [
            "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ",
            "さ", "し", "す", "せ", "そ", "た", "ち", "つ", "て", "と",
            "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
            "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り",
            "る", "れ", "ろ", "わ", "を", "ん", 
            "ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ",
            "サ", "シ", "ス", "セ", "ソ", "タ", "チ", "ツ", "テ", "ト",
            "ナ", "ニ", "ヌ", "ネ", "ノ", "ハ", "ヒ", "フ", "ヘ", "ホ",
            "マ", "ミ", "ム", "メ", "モ", "ヤ", "ユ", "ヨ", "ラ", "リ",
            "ル", "レ", "ロ", "ワ", "ヲ", "ン"
        ]

        row, col = 0, 0
        buttons = []
        for kana in japanese_kana:
            kana_button = tk.Button(canvas, text=kana, command=lambda s=kana: self.insert_symbol_text(s))
            kana_button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(kana_button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row + 1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    # 插入制表符号
    def insert_table_symbol(self):
        # 创建一个顶级窗口用于选择日文假名
        table_symbol_window = Toplevel(self.root)
        table_symbol_window.geometry("360x380")  # 设置窗口大小为 360x240
        table_symbol_window.title("插入制表符号")  # 设置窗口标题为"插入制表符号"

        # 创建一个带有滚动条的 Canvas
        canvas = Canvas(table_symbol_window)
        canvas.pack(fill=tk.BOTH, expand=True)

        # 创建日文假名符号表
        table_symbols = [
            "┌", "┬", "┐", "├", "┼", "┤", "└", "┴", "┘", 
            "┏", "┳", "┓", "┣", "╋", "┫", "┗", "┻", "┛", 
            "╔", "╦", "╗", "╠", "╬", "╣", "╚", "╩", "╝", 
            "╱", "╲", "╳", "┄", "┆", "┅", "┇", "┈", "┊", "┉", "┋",              
        ]

        row, col = 0, 0
        buttons = []
        for table_symbol in table_symbols:
            table_symbol_button = tk.Button(canvas, text=table_symbol, command=lambda s=table_symbol: self.insert_symbol_text(s))
            table_symbol_button.grid(row=row, column=col, padx=5, pady=5)
            buttons.append(table_symbol_button)
            col += 1
            if col >= 10:  # 每行最多显示 10 个按钮
                col = 0
                row += 1

        # 添加垂直滚动条
        scroll_y = Scrollbar(canvas, orient=tk.VERTICAL)
        scroll_y.grid(row=0, column=10, rowspan=row + 1, sticky=tk.NS)
        canvas.config(yscrollcommand=scroll_y.set)

        # 配置 Canvas 部件以支持滚动
        canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scroll_y.set)

    def convert_to_big5(self):
        # 转换为Big5编码
        text = self.text_widget.get("1.0", "end")
        try:
            text = text.encode("big5").decode("big5")
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("错误", "无法转换为Big5编码：" + str(e))

    def convert_to_utf8(self):
        # 转换为UTF-8编码
        text = self.text_widget.get("1.0", "end")
        try:
            text = text.encode("utf-8").decode("utf-8")
            self.text_widget.delete("1.0", "end")
            self.text_widget.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("错误", "无法转换为UTF-8编码：" + str(e))

# 查找和替换功能
    def replace_text(self):
        # 创建一个新的Toplevel窗口
        replace_window = Toplevel(self.root)
        replace_window.geometry("220x120")  # 设置窗口大小为 220x120
        replace_window.title("查找和替换")  # 设置窗口标题为"查找和替换"

        # 添加标签和输入框
        find_label = Label(replace_window, text="查找内容:", anchor=tk.W, justify=tk.LEFT, width=28)
        find_label.pack()
        find_entry = Entry(replace_window, width=30)  # 增加输入框宽度为 30
        find_entry.pack()

        replace_label = Label(replace_window, text="替换内容:", anchor=tk.W, justify=tk.LEFT, width=28)
        replace_label.pack()
        replace_entry = Entry(replace_window, width=30)  # 增加输入框宽度为 30
        replace_entry.pack()

        # 创建查找和替换按钮的Frame
        buttons_frame = Frame(replace_window)
        buttons_frame.pack(pady=10)  # 调整上下间距以使按钮居中

        # 创建查找按钮并放入Frame中
        find_button = Button(buttons_frame, text="查找", command=lambda: self.find_and_replace(find_entry.get(), replace_entry.get()))
        find_button.pack(side=tk.LEFT)

        # 创建替换按钮并放入Frame中
        replace_button = Button(buttons_frame, text="替换", command=lambda: self.replace(find_entry.get(), replace_entry.get()))
        replace_button.pack(side=tk.LEFT)

    def find_and_replace(self, find_text, replace_text):
        # 查找并高亮匹配的文本
        text = self.text_widget.get("1.0", "end")
        text = text.replace(find_text, f"<{find_text}>")  # 使用尖括号高亮文本
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)

    def replace(self, find_text, replace_text):
        # 替换文本
        text = self.text_widget.get("1.0", "end")
        text = text.replace(find_text, replace_text)
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("1.0", text)


    # 关于窗口
    def show_about_info(self):
        messagebox.showinfo("关于", "软件版本：Dylan's TXT Editor V1.0.0\n软件作者：Dylan Lim\n联系邮箱：801396@qq.com")

if __name__ == "__main__":
    root = tk.Tk()
    app = TXTEditor(root)
    root.mainloop()
