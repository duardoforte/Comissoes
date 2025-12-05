#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# JSON com os dados de vendas
dados_json = '''
{
  "vendas": [
    { "vendedor": "João Silva", "valor": 1200.50 },
    { "vendedor": "João Silva", "valor": 950.75 },
    { "vendedor": "João Silva", "valor": 1800.00 },
    { "vendedor": "João Silva", "valor": 1400.30 },
    { "vendedor": "João Silva", "valor": 1100.90 },
    { "vendedor": "João Silva", "valor": 1550.00 },
    { "vendedor": "João Silva", "valor": 1700.80 },
    { "vendedor": "João Silva", "valor": 250.30 },
    { "vendedor": "João Silva", "valor": 480.75 },
    { "vendedor": "João Silva", "valor": 320.40 },
    { "vendedor": "Maria Souza", "valor": 2100.40 },
    { "vendedor": "Maria Souza", "valor": 1350.60 },
    { "vendedor": "Maria Souza", "valor": 950.20 },
    { "vendedor": "Maria Souza", "valor": 1600.75 },
    { "vendedor": "Maria Souza", "valor": 1750.00 },
    { "vendedor": "Maria Souza", "valor": 1450.90 },
    { "vendedor": "Maria Souza", "valor": 400.50 },
    { "vendedor": "Maria Souza", "valor": 180.20 },
    { "vendedor": "Maria Souza", "valor": 90.75 },
    { "vendedor": "Carlos Oliveira", "valor": 800.50 },
    { "vendedor": "Carlos Oliveira", "valor": 1200.00 },
    { "vendedor": "Carlos Oliveira", "valor": 1950.30 },
    { "vendedor": "Carlos Oliveira", "valor": 1750.80 },
    { "vendedor": "Carlos Oliveira", "valor": 1300.60 },
    { "vendedor": "Carlos Oliveira", "valor": 300.40 },
    { "vendedor": "Carlos Oliveira", "valor": 500.00 },
    { "vendedor": "Carlos Oliveira", "valor": 125.75 },
    { "vendedor": "Ana Lima", "valor": 1000.00 },
    { "vendedor": "Ana Lima", "valor": 1100.50 },
    { "vendedor": "Ana Lima", "valor": 1250.75 },
    { "vendedor": "Ana Lima", "valor": 1400.20 },
    { "vendedor": "Ana Lima", "valor": 1550.90 },
    { "vendedor": "Ana Lima", "valor": 1650.00 },
    { "vendedor": "Ana Lima", "valor": 75.30 },
    { "vendedor": "Ana Lima", "valor": 420.90 },
    { "vendedor": "Ana Lima", "valor": 315.40 }
  ]
}
'''

def calcular_comissao(valor):
    """Calcula a comissão baseada no valor da venda."""
    if valor < 100:
        return 0
    elif valor < 500:
        return valor * 0.01
    else:
        return valor * 0.05

def processar_vendas(dados_json):
    """Processa as vendas e calcula comissões por vendedor."""
    dados = json.loads(dados_json)
    vendas = dados['vendas']
    
    vendedores = {}
    
    for venda in vendas:
        vendedor = venda['vendedor']
        valor = venda['valor']
        comissao = calcular_comissao(valor)
        
        if vendedor not in vendedores:
            vendedores[vendedor] = {
                'total_vendas': 0,
                'total_comissao': 0,
                'quantidade_vendas': 0
            }
        
        vendedores[vendedor]['total_vendas'] += valor
        vendedores[vendedor]['total_comissao'] += comissao
        vendedores[vendedor]['quantidade_vendas'] += 1
    
    return vendedores

class SistemaComissoes:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Comissões de Vendas")
        self.root.geometry("1000x650")
        self.root.configure(bg='#f0f0f0')
        
        # Processar dados
        self.vendedores = processar_vendas(dados_json)
        
        # Criar interface
        self.criar_interface()
        
    def criar_interface(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='#2c3e50', height=120)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="📊 RELATÓRIO DE COMISSÕES DE VENDAS",
            font=('Arial', 18, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title.pack(pady=20)
        
        # Data atual
        data_label = tk.Label(
            header_frame,
            text=f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}",
            font=('Arial', 10),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        data_label.pack()
        
        # Frame para cards de resumo
        cards_frame = tk.Frame(main_frame, bg='#f0f0f0')
        cards_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Calcular totais
        total_vendas = sum(v['total_vendas'] for v in self.vendedores.values())
        total_comissoes = sum(v['total_comissao'] for v in self.vendedores.values())
        total_vendas_qtd = sum(v['quantidade_vendas'] for v in self.vendedores.values())
        
        # Cards de resumo
        self.criar_card(cards_frame, "Total de Vendas", f"R$ {total_vendas:,.2f}", "#27ae60", 0)
        self.criar_card(cards_frame, "Total de Comissões", f"R$ {total_comissoes:,.2f}", "#e74c3c", 1)
        self.criar_card(cards_frame, "Quantidade de Vendas", str(total_vendas_qtd), "#3498db", 2)
        self.criar_card(cards_frame, "Vendedores", str(len(self.vendedores)), "#9b59b6", 3)
        
        # Frame para tabela
        table_frame = tk.Frame(main_frame, bg='white', relief=tk.RAISED, borderwidth=1)
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Criar Treeview
        columns = ('Vendedor', 'Qtd Vendas', 'Total Vendas', 'Total Comissão', '% Comissão')
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Definir cabeçalhos
        self.tree.heading('Vendedor', text='Vendedor')
        self.tree.heading('Qtd Vendas', text='Qtd. Vendas')
        self.tree.heading('Total Vendas', text='Total em Vendas')
        self.tree.heading('Total Comissão', text='Total de Comissão')
        self.tree.heading('% Comissão', text='% Comissão')
        
        # Definir larguras
        self.tree.column('Vendedor', width=200, anchor='w')
        self.tree.column('Qtd Vendas', width=100, anchor='center')
        self.tree.column('Total Vendas', width=150, anchor='e')
        self.tree.column('Total Comissão', width=150, anchor='e')
        self.tree.column('% Comissão', width=100, anchor='center')
        
        # Estilo da tabela
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', 
                       background='white',
                       foreground='black',
                       rowheight=30,
                       fieldbackground='white',
                       font=('Arial', 10))
        style.configure('Treeview.Heading',
                       background='#34495e',
                       foreground='white',
                       font=('Arial', 11, 'bold'))
        style.map('Treeview', background=[('selected', '#3498db')])
        
        # Adicionar dados
        for vendedor in sorted(self.vendedores.keys()):
            dados = self.vendedores[vendedor]
            percentual = (dados['total_comissao'] / dados['total_vendas'] * 100) if dados['total_vendas'] > 0 else 0
            
            self.tree.insert('', tk.END, values=(
                vendedor,
                dados['quantidade_vendas'],
                f"R$ {dados['total_vendas']:,.2f}",
                f"R$ {dados['total_comissao']:,.2f}",
                f"{percentual:.2f}%"
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Rodapé com botões
        footer_frame = tk.Frame(main_frame, bg='#f0f0f0')
        footer_frame.pack(fill=tk.X, pady=(20, 0))
        
        # Botão de regras
        btn_regras = tk.Button(
            footer_frame,
            text="📋 Ver Regras de Comissão",
            command=self.mostrar_regras,
            bg='#3498db',
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn_regras.pack(side=tk.LEFT)
        
        # Botão de sair
        btn_sair = tk.Button(
            footer_frame,
            text="❌ Sair",
            command=self.root.quit,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 11, 'bold'),
            cursor='hand2',
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        btn_sair.pack(side=tk.RIGHT)
        
    def criar_card(self, parent, titulo, valor, cor, coluna):
        """Cria um card de resumo."""
        card = tk.Frame(parent, bg=cor, relief=tk.RAISED, borderwidth=2)
        card.grid(row=0, column=coluna, padx=10, pady=5, sticky='ew')
        parent.grid_columnconfigure(coluna, weight=1)
        
        titulo_label = tk.Label(
            card,
            text=titulo,
            font=('Arial', 10, 'bold'),
            bg=cor,
            fg='white'
        )
        titulo_label.pack(pady=(10, 5))
        
        valor_label = tk.Label(
            card,
            text=valor,
            font=('Arial', 16, 'bold'),
            bg=cor,
            fg='white'
        )
        valor_label.pack(pady=(0, 10))
        
    def mostrar_regras(self):
        """Mostra as regras de comissão."""
        regras = """
        REGRAS DE COMISSÃO:
        
        ✓ Vendas abaixo de R$ 100,00:
          → Sem comissão (0%)
        
        ✓ Vendas entre R$ 100,00 e R$ 499,99:
          → Comissão de 1%
        
        ✓ Vendas a partir de R$ 500,00:
          → Comissão de 5%
        """
        messagebox.showinfo("Regras de Comissão", regras)

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaComissoes(root)
    root.mainloop()