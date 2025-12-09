# 简化版的IP子网切分工具

import tkinter as tk
from tkinter import ttk, messagebox
from ip_subnet_calculator import split_subnet

class SimpleIPSplitterApp:    
    def __init__(self, root):
        self.root = root
        self.root.title("IP子网切分工具")
        self.root.geometry("500x400")
        
        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建输入区域
        ttk.Label(main_frame, text="父网段 (如: 10.0.0.0/8)").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.parent_entry = ttk.Entry(main_frame, width=30)
        self.parent_entry.grid(row=0, column=1, padx=10, pady=5)
        self.parent_entry.insert(0, "10.0.0.0/8")
        
        ttk.Label(main_frame, text="切分网段 (如: 10.21.60.0/23)").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.split_entry = ttk.Entry(main_frame, width=30)
        self.split_entry.grid(row=1, column=1, padx=10, pady=5)
        self.split_entry.insert(0, "10.21.60.0/23")
        
        # 执行按钮
        self.execute_btn = ttk.Button(main_frame, text="执行切分", command=self.execute_split)
        self.execute_btn.grid(row=2, column=0, columnspan=2, pady=15)
        
        # 结果区域
        self.result_text = tk.Text(main_frame, height=15, width=60, font=('微软雅黑', 9))
        self.result_text.grid(row=3, column=0, columnspan=2, pady=5)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(main_frame, command=self.result_text.yview)
        scrollbar.grid(row=3, column=2, sticky=tk.NS, pady=5)
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        # 初始消息
        self.result_text.insert(tk.END, "欢迎使用IP子网切分工具！\n请输入父网段和切分网段，然后点击'执行切分'按钮。\n")
    
    def execute_split(self):
        """执行切分操作"""
        parent = self.parent_entry.get().strip()
        split = self.split_entry.get().strip()
        
        # 清空结果区域
        self.result_text.delete(1.0, tk.END)
        
        # 验证输入
        if not parent or not split:
            messagebox.showerror("错误", "父网段和切分网段都不能为空！")
            return
        
        try:
            # 尝试切分
            result = split_subnet(parent, split)
            
            if 'error' in result:
                self.result_text.insert(tk.END, f"❌ 错误: {result['error']}\n")
                return
            
            # 显示结果
            self.result_text.insert(tk.END, f"✅ 切分成功！\n\n")
            self.result_text.insert(tk.END, f"父网段: {result['parent']}\n")
            self.result_text.insert(tk.END, f"切分网段: {result['split']}\n\n")
            
            # 显示切分网段信息
            self.result_text.insert(tk.END, "切分网段信息:\n")
            for key, value in result['split_info'].items():
                self.result_text.insert(tk.END, f"  {key}: {value}\n")
            
            # 显示剩余网段
            self.result_text.insert(tk.END, f"\n剩余网段列表 ({len(result['remaining_subnets'])}个):\n")
            for i, subnet in enumerate(result['remaining_subnets'], 1):
                self.result_text.insert(tk.END, f"  {i}. {subnet}\n")
                
        except Exception as e:
            self.result_text.insert(tk.END, f"❌ 执行失败: {str(e)}\n")
            import traceback
            self.result_text.insert(tk.END, f"\n详细错误信息:\n{traceback.format_exc()}\n")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SimpleIPSplitterApp(root)
        root.mainloop()
    except Exception as e:
        print(f"应用程序启动失败: {e}")
        import traceback
        traceback.print_exc()
