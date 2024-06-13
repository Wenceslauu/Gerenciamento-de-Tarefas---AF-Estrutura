from BinaryTree import BinaryTree, Task
from Pilha import Pilha
import os
from datetime import datetime


class TaskManager:
    def __init__(self):
        self.bst = BinaryTree()
        self.command_stack = Pilha()

    def add_task(self, description):
        priority = get_priority_input()
        due_date = get_date_input()
        task = Task(description, priority, due_date)
        self.bst.insert(task)
        self.command_stack.push(("add", task))
        print(f"Tarefa '{task}' adicionada.")
        wait_for_key()

    def remove_task(self, description):
        task_to_remove = Task(description, '', datetime.min)
        if self.bst.search(task_to_remove):
            self.bst.delete(task_to_remove)
            self.command_stack.push(("remove", task_to_remove))
            print(f"Tarefa '{description}' removida.")
        else:
            print(f"Tarefa '{description}' não encontrada.")
        wait_for_key()

    def edit_task(self, old_description, new_description, new_priority, new_due_date):
        old_task = Task(old_description, '', datetime.min)
        if self.bst.search(old_task):
            self.bst.delete(old_task)
            new_task = Task(new_description, new_priority, new_due_date)
            self.bst.insert(new_task)
            self.command_stack.push(("edit", old_task, new_task))
            print(f"Tarefa '{old_description}' editada.")
        else:
            print(f"Tarefa '{old_description}' não encontrada.")
        wait_for_key()

    def view_tasks(self, filter_by=None, order_by=None):
        tasks = self.bst.inorder()
        if tasks:
            if filter_by == 'prioridade':
                tasks = [task for task in tasks if task.priority == order_by]
            elif filter_by == 'data':
                tasks.sort(key=lambda x: x.due_date)
            elif filter_by == 'descrição':
                tasks.sort(key=lambda x: x.description)
            print_tasks(tasks)
        else:
            print("Nenhuma tarefa disponível.")
        wait_for_key()

    def view_tasks_alphabetical(self):
        clear_console()
        self.bst.display_alphabetical()
        wait_for_key()

    def undo(self):
        if not self.command_stack.is_empty():
            command = self.command_stack.pop()
            action = command[0]
            if action == "add":
                task = command[1]
                self.bst.delete(task)
                print(f"Adição de tarefa '{task.description}' desfeita.")
            elif action == "remove":
                task = command[1]
                self.bst.insert(task)
                print(f"Remoção de tarefa '{task.description}' desfeita.")
            elif action == "edit":
                old_task, new_task = command[1], command[2]
                self.bst.delete(new_task)
                self.bst.insert(old_task)
                print(f"Edição de tarefa '{new_task.description}' desfeita.")
        else:
            print("Nenhuma ação para desfazer.")
        wait_for_key()


def print_tasks(tasks):
    print("\n" + "="*40)
    print(" TAREFAS ".center(40, "="))
    print("="*40)
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task}")
    print("="*40)


def get_priority_input():
    while True:
        priority = input("Digite a prioridade (alta, média, baixa): ").lower()
        if priority in ['alta', 'média', 'baixa']:
            return priority
        print("Prioridade inválida. Por favor, escolha entre alta, média ou baixa.")


def get_date_input():
    while True:
        due_date_str = input("Digite a data de vencimento (dd/mm/yyyy): ")
        try:
            due_date = datetime.strptime(due_date_str, "%d/%m/%Y")
            return due_date
        except ValueError:
            print("Formato de data inválido. Por favor, siga o formato dd/mm/yyyy.")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_for_key():
    input("Pressione qualquer tecla para continuar...")


def main():
    manager = TaskManager()

    while True:
        clear_console()
        print("=== Gerenciador de Tarefas ===")
        print("1. Adicionar Tarefa")
        print("2. Remover Tarefa")
        print("3. Visualizar Tarefas")
        print("4. Editar Tarefa")
        print("5. Desfazer Última Operação")
        print("6. Visualizar Tarefas em Ordem Alfabética")
        print("7. Sair")
        print("="*30)
        choice = input("Escolha uma opção: ")
        print("="*30 + "\n")

        if choice == "1":
            description = input("Digite a descrição da tarefa: ")
            manager.add_task(description)
        elif choice == "2":
            description = input(
                "Digite a descrição da tarefa a ser removida: ")
            manager.remove_task(description)
        elif choice == "3":
            filter_by = input(
                "Filtrar por (prioridade, data, descrição, ou deixe em branco para nenhum): ").lower()
            if filter_by in ['prioridade', 'data', 'descrição']:
                order_by = input(
                    "Digite o valor para o filtro: ") if filter_by == 'prioridade' else None
                manager.view_tasks(filter_by, order_by)
            else:
                manager.view_tasks()
        elif choice == "4":
            old_description = input(
                "Digite a descrição da tarefa a ser editada: ")
            new_description = input("Digite a nova descrição da tarefa: ")
            new_priority = get_priority_input()
            new_due_date = get_date_input()
            manager.edit_task(old_description, new_description,
                              new_priority, new_due_date)
        elif choice == "5":
            manager.undo()
        elif choice == "6":
            manager.view_tasks_alphabetical()
        elif choice == "7":
            break
        else:
            print("Opção inválida. Tente novamente.")
            wait_for_key()


if __name__ == "__main__":
    main()
