import random
import tkinter as tk
from tkinter import ttk, messagebox
import os
import winreg

class RoadCompetitionDrawSystem:
    def __init__(self, master):
        self.master = master
        self.master.title("道路工程抽签系统")
        self.master.geometry("1100x670")
        self.master.state('zoomed')
        self.master.iconbitmap('icon.ico')
        
        # 初始化数据
        self.group = "高中"  # 默认选高中
        self.results = {}
        self.project_positions = {
            1: (120, 80), 2: (300, 80), 3: (480, 80),
            4: (120, 260), 5: (300, 260), 6: (480, 260),
            7: (120, 440), 8: (300, 440), 9: (480, 440)
        }
        
        # 创建界面
        self.create_widgets()
        self.draw_base_map()

    def create_widgets(self):
        # 主容器
        main_frame = tk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 左侧面板
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 控制面板
        control_frame = tk.Frame(left_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(control_frame, text="组别选择:", font=("微软雅黑", 12)).pack(side=tk.LEFT)
        self.group_var = tk.StringVar(value="高中")  # 默认选高中
        group_combo = ttk.Combobox(control_frame, 
                                 textvariable=self.group_var,
                                 values=("小学", "初中", "高中"),
                                 state="readonly",
                                 font=("微软雅黑", 12))
        group_combo.current(2)  # 默认选高中
        group_combo.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(control_frame, text="开始抽签", command=self.run_draw).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="重置系统", command=self.reset_system).pack(side=tk.LEFT)
        ttk.Button(control_frame, text="导出结果", command=self.export_results).pack(side=tk.LEFT, padx=5)  # 添加导出按钮

        # 地图区域
        self.canvas = tk.Canvas(left_frame, width=600, height=600, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 右侧面板
        right_frame = tk.Frame(main_frame, width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10)

        # 任务表格
        self.tree = ttk.Treeview(right_frame, 
                               columns=("任务", "工程点", "区域"), 
                               show="headings",
                               height=12,
                               selectmode="browse")
        self.tree.column("任务", width=120, anchor=tk.W)
        self.tree.column("工程点", width=80, anchor=tk.CENTER)
        self.tree.column("区域", width=80, anchor=tk.CENTER)
        self.tree.heading("任务", text="任务名称")
        self.tree.heading("工程点", text="工程点")
        self.tree.heading("区域", text="区域")
        self.tree.pack(fill=tk.X, pady=(0,10))

        # 详细要求
        self.requirement_text = tk.Text(right_frame, 
                                      wrap=tk.WORD,
                                      font=("宋体", 12),
                                      height=25,
                                      bg="#F8F9FA",
                                      state="disabled")  # 设置为不可编辑
        self.requirement_text.pack(fill=tk.BOTH, expand=True)

    def draw_base_map(self):
        """绘制基础地图"""
        # 绘制工程点
        for pid, (x,y) in self.project_positions.items():
            self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                                  fill="#4CAF50", width=2)
            self.canvas.create_text(x, y, text=f"工程{pid}", 
                                  fill="white", font=("微软雅黑", 12, "bold"))
            
            # 绘制四个区域
            for zone in range(1,5):
                zx = x + ((zone-1)%2)*50 - 25
                zy = y + ((zone-1)//2)*50 - 25
                self.canvas.create_rectangle(zx-20, zy-20, zx+20, zy+20,
                                           outline="#BDBDBD", width=1)
                self.canvas.create_text(zx, zy, text=str(zone), 
                                      fill="#757575", font=("Arial", 10))

    def run_draw(self):
        """执行抽签流程"""
        self.group = self.group_var.get()
        if not self.group:
            messagebox.showwarning("提示", "请先选择组别")
            return
        
        self.generate_draw()
        self.update_display()

    def generate_draw(self):
        """生成抽签结果"""
        projects = list(range(1, 10))
        self.results.clear()
        self.canvas.delete("marker")

        # ==== 任务1: 物料回收 ====
        task1_project = random.choice(projects)
        projects.remove(task1_project)
        task1_zone = random.randint(1,4)
        self.results["物料回收"] = {
            "工程点": task1_project,
            "区域": task1_zone,
            "坐标": self.get_zone_coord(task1_project, task1_zone),
            "要求": [
                "📦 物料回收任务",
                f"📍 工程点：{task1_project}",
                f"🗺️ 区域：{task1_zone}",
                "📝 要求：将易拉罐摆放在指定区域的最近交叉线"
            ]
        }

        # ==== 任务2: 建设服务区 ====
        task2_project = random.choice(projects)
        projects.remove(task2_project)
        task2_zones = random.sample(range(1, 5), 3)  # 选择3个不同区域
        self.results["建设服务区"] = {
            "工程点": task2_project,
            "区域": task2_zones,
            "坐标": [self.get_zone_coord(task2_project, zone) for zone in task2_zones],
            "要求": [
                "🏗️ 建设服务区任务",
                f"📍 工程点：{task2_project}",
                f"🗺️ 区域：{', '.join(map(str, task2_zones))}",
                "📝 要求：在指定的三个区域分别平放1个纸杯，形成'品'字形"
            ]
        }

        # ==== 任务3: 搭建桥梁 ====
        task3_project = random.choice(projects)
        projects.remove(task3_project)
        colors = ["#FF0000", "#87CEFA", "#00FF00"]  # 红、蓝、绿的十六进制颜色代码
        color_order = ""
        if self.group in ["初中", "高中"]:
            random.shuffle(colors)
            # 将颜色代码转换为中文名称，并添加方向说明
            color_names = {"#FF0000": "红", "#87CEFA": "蓝", "#00FF00": "绿"}
            color_labels = [color_names[color] for color in colors]
            color_order = f"🔢 叠放顺序（从下到上）：{' → '.join(reversed(color_labels))}"
        self.results["搭建桥梁"] = {
            "工程点": task3_project,
            "坐标": self.project_positions[task3_project],
            "要求": [
                "🌉 搭建桥梁任务",
                f"📍 工程点：{task3_project}",
                "📌 固定摆放位置：",
                "🔵 1号位置 - 蓝色",
                "🔴 2-3中间线 - 红色",
                "🟢 4号位置 - 绿色",
                color_order if color_order else "🎓 小学组无顺序要求"
            ],
            "颜色顺序": colors  # 添加颜色顺序
        }

        # ==== 任务4: 建设加油站 ====
        task4_project = random.choice(projects)
        projects.remove(task4_project)
        cup_zone, ball_zone = random.sample(range(1,5), 2)
        self.results["建设加油站"] = {
            "工程点": task4_project,
            "纸杯区域": cup_zone,
            "泡沫球区域": ball_zone,
            "坐标": (
                self.get_zone_coord(task4_project, cup_zone),
                self.get_zone_coord(task4_project, ball_zone)
            ),
            "要求": [
                "⛽ 建设加油站任务",
                f"📍 工程点：{task4_project}",
                f"🥤 纸杯区域：{cup_zone}",
                f"🎈 泡沫球区域：{ball_zone}",
                "📝 要求：将泡沫球放置在倒扣纸杯上"
            ]
        }

    def get_zone_coord(self, project, zone):
        """获取区域坐标"""
        base_x, base_y = self.project_positions[project]
        offset_x = ((zone-1)%2)*50 - 25
        offset_y = ((zone-1)//2)*50 - 25
        return (base_x + offset_x, base_y + offset_y)

    def update_display(self):
        """更新界面显示"""
        # 清空旧数据
        self.canvas.delete("marker")
        self.tree.delete(*self.tree.get_children())
        self.requirement_text.config(state="normal")
        self.requirement_text.delete(1.0, tk.END)

        # 颜色配置
        colors = {
            "物料回收": "#2196F3",
            "建设服务区": "#8BC34A",
            "搭建桥梁": "#FF9800",
            "建设加油站": "#E91E63"
        }

        # 更新显示
        for task, info in self.results.items():
            # 更新表格
            self.tree.insert("", tk.END, values=(task, info["工程点"], info.get("区域", "N/A")))

            # 绘制地图标记
            if task == "物料回收":
                x, y = info["坐标"]
                self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=colors[task], tags="marker")
                self.canvas.create_text(x, y, text="回收", fill="white", font=("微软雅黑", 8), tags="marker")
            elif task == "建设服务区":
                x, y = self.project_positions[info["工程点"]]
                self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=colors[task], tags="marker")
                self.canvas.create_text(x, y, text="服务区", fill="white", font=("微软雅黑", 10), tags="marker")
                for i, (x, y) in enumerate(info["坐标"]):
                    self.canvas.create_oval(x-17, y-17, x+17, y+17, fill=colors[task], tags="marker")
                    self.canvas.create_text(x, y, text=f"纸杯{i+1}", fill="black", font=("宋体", 8), tags="marker")
            elif task == "搭建桥梁":
                x, y = self.project_positions[info["工程点"]]
                self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=colors[task], tags="marker")
                self.canvas.create_text(x, y, text="桥梁", fill="white", font=("微软雅黑", 10), tags="marker")
                # 绘制颜色顺序的方块
                color_order = info.get("颜色顺序", [])
                if color_order:
                    color_x = x + 50  # 方块的起始x坐标
                    color_y = y - 70  # 方块的起始y坐标
                    color_names = {"#FF0000": "红", "#87CEFA": "蓝", "#00FF00": "绿"}
                    for color in color_order:
                        color_y += 30  # 每个方块的间距
                        self.canvas.create_rectangle(color_x, color_y, color_x+20, color_y+20, fill=color, outline="black", tags="marker")
                        self.canvas.create_text(color_x+10, color_y+11, text=color_names[color], fill="black", font=("宋体", 8), tags="marker")
            elif task == "建设加油站":
                x1, y1 = info["坐标"][0]
                x2, y2 = info["坐标"][1]
                self.canvas.create_oval(x1-15, y1-15, x1+15, y1+15, fill=colors[task], tags="marker")
                self.canvas.create_text(x1, y1, text="纸杯", fill="white", font=("宋体", 8), tags="marker")
                self.canvas.create_oval(x2-17, y2-17, x2+17, y2+17, fill="#FFD54F", tags="marker")
                self.canvas.create_text(x2, y2, text="泡沫球", fill="black", font=("宋体", 8), tags="marker")

            # 更新详细要求
            req_text = "\n".join(info["要求"]) + "\n\n"
            self.requirement_text.insert(tk.END, req_text)

        # 设置文本区域为只读
        self.requirement_text.config(state="disabled")

    def reset_system(self):
        """重置系统"""
        self.results.clear()
        self.canvas.delete("marker")
        self.tree.delete(*self.tree.get_children())
        self.requirement_text.config(state="normal")
        self.requirement_text.delete(1.0, tk.END)
        self.requirement_text.config(state="disabled")

    def export_results(self):
        """导出抽签结果到桌面"""
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders")
        desktop_path = winreg.QueryValueEx(key, "Desktop")[0]
        winreg.CloseKey(key)

        file_path = os.path.join(desktop_path, "抽签结果.txt")  # 桌面文件路径
        with open(file_path, "w", encoding="utf-8") as file:
            for task, info in self.results.items():
                file.write(f"任务名称：{task}\n")
                file.write(f"工程点：{info['工程点']}\n")
                file.write(f"区域：{info.get('区域', 'N/A')}\n")
                file.write("要求：\n")
                for req in info["要求"]:
                    file.write(f"    {req}\n")
                file.write("\n")
        messagebox.showinfo("导出成功", f"抽签结果已导出到桌面文件：{file_path}")
        os.startfile(file_path)  # 打开文件

if __name__ == "__main__":
    root = tk.Tk()
    app = RoadCompetitionDrawSystem(root)
    root.mainloop()