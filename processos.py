import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProcessSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Escalonador de Processos com Prioridade")
        self.process_list = []
        self.quantum = tk.IntVar(value=2)
        self.setup_ui()
    
    def setup_ui(self):
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack()
        
        ttk.Label(frame, text="ID do Processo:").grid(row=0, column=0, padx=5, pady=5)
        self.process_id_entry = ttk.Entry(frame, width=10)
        self.process_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Tempo de Execução:").grid(row=0, column=2, padx=5, pady=5)
        self.burst_time_entry = ttk.Entry(frame, width=10)
        self.burst_time_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame, text="Prioridade (1-Maior):").grid(row=0, column=4, padx=5, pady=5)
        self.priority_entry = ttk.Entry(frame, width=10)
        self.priority_entry.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(frame, text="Adicionar Processo", command=self.add_process).grid(row=0, column=6, padx=5, pady=5)
        
        ttk.Label(frame, text="Quantum:").grid(row=1, column=0, padx=5, pady=5)
        self.quantum_entry = ttk.Entry(frame, textvariable=self.quantum, width=10)
        self.quantum_entry.grid(row=1, column=1, padx=5, pady=5)
        
        self.process_table = ttk.Treeview(frame, columns=("ID", "Tempo de Execução", "Prioridade"), show="headings")
        self.process_table.heading("ID", text="ID")
        self.process_table.heading("Tempo de Execução", text="Tempo de Execução")
        self.process_table.heading("Prioridade", text="Prioridade")
        self.process_table.grid(row=2, column=0, columnspan=7, padx=5, pady=5)
        
        ttk.Button(frame, text="Executar Escalonamento", command=self.run_scheduler).grid(row=3, column=0, columnspan=5, pady=10)
        ttk.Button(frame, text="Resetar", command=self.reset).grid(row=3, column=5, columnspan=2, padx=5, pady=10)
        
        self.result_label = tk.Label(frame, text="", fg="blue", font=("Arial", 10, "bold"))
        self.result_label.grid(row=4, column=0, columnspan=7, pady=5)
    
    def reset(self):
        self.process_list.clear()
        for item in self.process_table.get_children():
            self.process_table.delete(item)
        self.result_label.config(text="")
        self.process_id_entry.delete(0, tk.END)
        self.burst_time_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
        self.quantum.set(2)
    
    def add_process(self):
        process_id = self.process_id_entry.get()
        burst_time = self.burst_time_entry.get()
        priority = self.priority_entry.get()
        
        if not process_id or not burst_time.isdigit() or not priority.isdigit():
            messagebox.showerror("Erro", "Dados do processo inválidos!")
            return
        
        self.process_list.append({"id": process_id, "burst_time": int(burst_time), "priority": int(priority)})
        self.process_table.insert("", "end", values=(process_id, burst_time, priority))
        self.process_id_entry.delete(0, tk.END)
        self.burst_time_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
    
    def run_scheduler(self):
        if not self.process_list:
            messagebox.showwarning("Aviso", "Nenhum processo adicionado!")
            return
        
        quantum = self.quantum.get()
        if quantum <= 0:
            messagebox.showerror("Erro", "Quantum deve ser maior que 0!")
            return
        
        processes = sorted(self.process_list, key=lambda x: x["priority"])
        execution_order = []
        time = 0
        
        while processes:
            process = processes.pop(0)
            if process["burst_time"] > quantum:
                time += quantum
                process["burst_time"] -= quantum
                processes.append(process)
                processes.sort(key=lambda x: x["priority"])
                execution_order.append(f"{process['id']} ({quantum}s)")
            else:
                time += process["burst_time"]
                execution_order.append(f"{process['id']} ({process['burst_time']}s)")
        
        result_text = f"Ordem de Execução: {' -> '.join(execution_order)} | Tempo Total: {time}s"
        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessSchedulerApp(root)
    root.mainloop()
