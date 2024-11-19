import tkinter as tk
from tkinter import ttk, messagebox

class CPUSimulator:
    def __init__(self):
        self.registers = {"A": 0, "B": 0}
        self.memory = [0] * 10
        self.instruction_pointer = 0
        self.instructions = []
        self.history = []
    
    def load_program(self, program):
        self.instructions = program
        self.instruction_pointer = 0
        self.history = []

    def execute_next_instruction(self):
        if self.instruction_pointer >= len(self.instructions):
            return "Fim do programa."
        
        instruction = self.instructions[self.instruction_pointer]
        parts = instruction.split()
        cmd = parts[0].upper()
        
        try:
            if cmd == "LOAD":
                reg, value = parts[1], int(parts[2])
                self.registers[reg] = value
            elif cmd == "STORE":
                reg, addr = parts[1], int(parts[2])
                self.memory[addr] = self.registers[reg]
            elif cmd == "ADD":
                reg1, reg2 = parts[1], parts[2]
                self.registers[reg1] += self.registers[reg2]
            elif cmd == "SUB":
                reg1, reg2 = parts[1], parts[2]
                self.registers[reg1] -= self.registers[reg2]
            elif cmd == "HALT":
                self.history.append("Programa finalizado.")
                return "Programa finalizado."
            else:
                return f"Instrução desconhecida: {cmd}"
        except (IndexError, ValueError) as e:
            return f"Erro na instrução: {instruction}. Detalhes: {e}"
        
        self.history.append(instruction)
        self.instruction_pointer += 1
        return f"Instrução '{instruction}' executada com sucesso."
    
    def get_status(self):
        return {
            "Registers": self.registers.copy(),
            "Memory": self.memory.copy(),
            "Instruction Pointer": self.instruction_pointer,
            "History": self.history[:],
        }

class CPUGUI:
    def __init__(self, root):
        self.cpu = CPUSimulator()
        self.root = root
        self.root.title("Simulador Interativo de CPU")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        self.create_program_tab()
        self.create_status_tab()
        self.create_history_tab()

    def create_program_tab(self):
        self.program_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.program_tab, text="Programa")

        ttk.Label(self.program_tab, text="Digite as instruções do programa:").pack(pady=5)
        self.program_entry = tk.Text(self.program_tab, height=10, width=60)
        self.program_entry.pack(padx=10, pady=5)

        control_frame = ttk.Frame(self.program_tab)
        control_frame.pack(pady=10)
        ttk.Button(control_frame, text="Carregar Programa", command=self.load_program).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Executar Próxima Instrução", command=self.execute_instruction).pack(side=tk.LEFT, padx=5)

    def create_status_tab(self):
        self.status_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.status_tab, text="Status da CPU")

        ttk.Label(self.status_tab, text="Registradores").pack(pady=5)
        self.registers_table = ttk.Treeview(self.status_tab, columns=("Register", "Value"), show="headings", height=2)
        self.registers_table.heading("Register", text="Registrador")
        self.registers_table.heading("Value", text="Valor")
        self.registers_table.pack(pady=5)

        for reg in self.cpu.registers:
            self.registers_table.insert("", "end", values=(reg, self.cpu.registers[reg]))

        ttk.Label(self.status_tab, text="Memória").pack(pady=5)
        self.memory_table = ttk.Treeview(self.status_tab, columns=("Address", "Value"), show="headings", height=10)
        self.memory_table.heading("Address", text="Endereço")
        self.memory_table.heading("Value", text="Valor")
        self.memory_table.pack(pady=5)

        for i in range(10):
            self.memory_table.insert("", "end", values=(i, self.cpu.memory[i]))

    def create_history_tab(self):
        self.history_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.history_tab, text="Histórico")

        ttk.Label(self.history_tab, text="Instruções Executadas").pack(pady=5)
        self.history_text = tk.Text(self.history_tab, height=15, width=60, state=tk.DISABLED)
        self.history_text.pack(padx=10, pady=5)

    def update_status(self):
        status = self.cpu.get_status()

        for i, (reg, value) in enumerate(status["Registers"].items()):
            self.registers_table.item(self.registers_table.get_children()[i], values=(reg, value))

        for i, value in enumerate(status["Memory"]):
            self.memory_table.item(self.memory_table.get_children()[i], values=(i, value))

        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.insert(tk.END, "\n".join(status["History"]))
        self.history_text.config(state=tk.DISABLED)

    def load_program(self):
        program = self.program_entry.get("1.0", tk.END).strip().split("\n")
        self.cpu.load_program(program)
        self.update_status()
        messagebox.showinfo("Info", "Programa carregado com sucesso!")

    def execute_instruction(self):
        result = self.cpu.execute_next_instruction()
        self.update_status()
        messagebox.showinfo("Execução", result)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUGUI(root)
    root.mainloop()
