# Mini-Net: Garantindo Segurança ao UDP

(5 minutos - projeto rodando)
https://drive.google.com/file/d/1fGijDnzSfNaASa3gkNd_6aMf0YUcxg0G/view?usp=sharing

(14 minutos - detalhes) https://drive.google.com/file/d/1dHdpKZEPVb419h43o10e8SF8MjsNtexp/view?usp=sharing

**Matéria:** Redes de Computadores\
**Professor:** Marciano

## 📌 Descrição do Projeto

O projeto **Mini-Net** tem como objetivo simular uma rede com:

- 1 Servidor
- 2 Roteadores
- 1 Cliente

A comunicação é feita utilizando UDP com mecanismos adicionais para
garantir maior segurança e controle na transmissão.

Arquivos principais do projeto:

- `servidor.py`
- `roteador.py`
- `roteador2.py`
- `cliente.py`
- `color.py`
- `protocol.py`
- `run_dev.py`

### ▶️ Como Executar o Projeto

Existem **duas formas** de executar o sistema:

### ✅ Opção 1 --- Executar via VS Code (Recomendado)

### Execute a Task configurada

Pressione:

    Ctrl + Shift + P

Digite:

    Task: Run Task

Selecione:

    # Iniciar Servidor + 2 Roteadores + Cliente

Isso iniciará automaticamente:

- Servidor
- Roteador 1
- Roteador 2
- Cliente

---

### ✅ Opção 2 --- Executar Manualmente pelo Terminal

Abra **4 terminais diferentes** dentro da pasta do projeto.

### 🖥 Terminal 1 --- Servidor

```bash
python servidor.py
```

---

### 🌐 Terminal 2 --- Roteador 1

```bash
python roteador.py
```

---

### 🌐 Terminal 3 --- Roteador 2

```bash
python roteador2.py
```

---

### 💻 Terminal 4 --- Cliente

```bash
python cliente.py
```

---

### ⚠️ Observações Importantes

- Certifique-se de que todas as portas configuradas nos arquivos estão
  livres.
- Execute os arquivos na ordem:
  1.  Servidor
  2.  Roteadores
  3.  Cliente
- Caso utilize Linux ou Mac, pode ser necessário usar:

```bash
python3 nome_do_arquivo.py
```
