import asyncio
import os
import telegram
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

class TelegramBotPanel(tk.Tk):
    def __init__(self, bot, loop):
        super().__init__()
        self.iconbitmap('icone.ico')
        self.bot = bot
        self.loop = loop
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.title("Painel de Controle do Bot Telegram")
        self.geometry("650x850")
        self.configure(bg="#121212")

        # Desativar a opção de maximizar
        self.resizable(False, False)

        # Fontes
        self.title_font = tkfont.Font(family="Segoe UI", size=26, weight="bold")
        self.button_font = tkfont.Font(family="Segoe UI", size=10)
        self.entry_font = tkfont.Font(family="Segoe UI", size=11)

        # Centralizar a janela
        self.center_window(610, 850)

        # Título
        self.label_title = tk.Label(self, text="Painel Telegram V6", font=self.title_font, bg="#121212",
                                    fg="#4CAF50")
        self.label_title.pack(pady=20)

        # Frame para os controles
        self.frame_controls = ttk.Frame(self, padding="20")
        self.frame_controls.pack(fill=tk.BOTH, padx=20, pady=10)

        # Configurar fundo do frame
        style = ttk.Style()
        style.configure("TFrame", background="#1E1E1E")
        self.frame_controls.configure(style="TFrame")

        # Entrada de mensagem
        self.label_msg = tk.Label(self.frame_controls, text="Mensagem:", font=self.entry_font, bg="#121212",
                                  fg="#4CAF50")
        self.label_msg.grid(row=0, column=0, pady=5, sticky=tk.W)
        self.entry_msg = ttk.Entry(self.frame_controls, font=self.entry_font, foreground="#333333")
        self.entry_msg.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.EW)
        self.entry_msg.insert(0, "Digite a mensagem aqui...")  # Placeholder

        # Botões com ícones
        self.create_buttons_with_icons()

        # Entrada para agendamento de mensagens
        self.label_schedule = tk.Label(self.frame_controls, text="Agendar Mensagem para (HH:MM):", font=self.entry_font,
                                       bg="#121212", fg="#4CAF50")
        self.label_schedule.grid(row=2, column=0, pady=5, sticky=tk.W)
        self.entry_time = ttk.Entry(self.frame_controls, font=self.entry_font, foreground="#333333")
        self.entry_time.grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.EW)
        self.entry_time.insert(0, "HH:MM")  # Placeholder

        # Adicionar uma barra de progresso
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate')
        self.progress_bar.pack(pady=10)

        # Lista de mensagens recebidas
        self.text_log = tk.Text(self, height=10, font=self.entry_font, bg="#1E1E1E", fg="#E0E0E0", bd=0, padx=10,
                                pady=10)
        self.text_log.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        self.text_log.configure(state='disabled')

        # Campo para Chat ID
        self.label_chat_id = tk.Label(self.frame_controls, text="Chat ID:", font=self.entry_font, bg="#121212",
                                      fg="#4CAF50")
        self.label_chat_id.grid(row=4, column=0, pady=5, sticky=tk.W)
        self.entry_chat_id = ttk.Entry(self.frame_controls, font=self.entry_font, foreground="#333333")
        self.entry_chat_id.grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)
        self.entry_chat_id.insert(0, '-1002222609076')  # Valor padrão

        # Rodapé
        self.footer = tk.Label(self, text="Desenvolvido por Guilherme Augusto", font=self.entry_font, bg="#121212",
                               fg="#4CAF50", pady=10)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X)

    def center_window(self, width, height):
        # Obtém as dimensões da tela
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcula as coordenadas para centralizar a janela
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Define a geometria da janela
        self.geometry(f"{width}x{height}+{x}+{y}")

    def create_buttons_with_icons(self):
        button_data = [
            ("Enviar Mensagem", "send_icon.png", self.on_send_message),
            ("Exibir Última Mensagem", "view_icon.png", self.on_show_last_message),
            ("Agendar Mensagem", "schedule_icon.png", self.on_schedule_message),
            ("Enviar Foto", "photo_icon.png", self.on_send_photo),
            ("Enviar Documento", "document_icon.png", self.on_send_document),
            ("Exibir Chat ID", "chat_id_icon.png", self.on_display_chat_id)
        ]

        style = ttk.Style()
        style.configure("TButton",
                        background="#333333",
                        foreground="#000000",  # Texto preto
                        borderwidth=1,
                        relief=tk.RAISED,
                        font=self.button_font)
        style.map("TButton",
                  background=[("active", "#555555")],
                  foreground=[("active", "#000000")])  # Texto preto quando o botão está ativo

        for i, (text, icon, command) in enumerate(button_data):
            icon_path = os.path.join(os.path.dirname(__file__), icon)
            if not os.path.isfile(icon_path):
                print(f"Ícone não encontrado: {icon_path}")
                continue

            img = Image.open(icon_path)
            img = img.resize((24, 24), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            button = ttk.Button(self.frame_controls, text=text, image=photo, compound=tk.LEFT, command=command)
            button.image = photo

            # Ajustar a posição dos botões na grade
            if text == "Exibir Chat ID":
                button.grid(row=5, column=2, pady=10, padx=5, sticky=tk.EW)
            elif text == "Enviar Mensagem":
                button.grid(row=1, column=2, pady=10, padx=5, sticky=tk.EW)
            elif text == "Exibir Última Mensagem":
                button.grid(row=6, column=0, pady=10, padx=5, sticky=tk.EW)
            elif text == "Agendar Mensagem":
                button.grid(row=3, column=2, pady=10, padx=5, sticky=tk.EW)
            elif text == "Enviar Foto":
                button.grid(row=6, column=1, pady=10, padx=5, sticky=tk.EW)
            elif text == "Enviar Documento":
                button.grid(row=6, column=2, pady=10, padx=5, sticky=tk.EW)


    def on_send_message(self):
        message = self.entry_msg.get()
        self.progress_bar.start()  # Inicia a barra de progresso
        asyncio.create_task(self.send_message(message))

    def on_show_last_message(self):
        self.progress_bar.start()  # Inicia a barra de progresso
        asyncio.create_task(self.show_last_message())

    def on_schedule_message(self):
        message = self.entry_msg.get()
        schedule_time = self.entry_time.get()
        self.progress_bar.start()  # Inicia a barra de progresso
        asyncio.create_task(self.schedule_message(message, schedule_time))

    def on_send_photo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.gif")])
        if file_path:
            self.progress_bar.start()  # Inicia a barra de progresso
            asyncio.create_task(self.send_photo(file_path))

    def on_send_document(self):
        file_path = filedialog.askopenfilename(filetypes=[("Document files", "*.pdf *.docx *.xlsx")])
        if file_path:
            self.progress_bar.start()  # Inicia a barra de progresso
            asyncio.create_task(self.send_document(file_path))

    def on_display_chat_id(self):
        chat_id = self.entry_chat_id.get()
        messagebox.showinfo("Chat ID", f"O Chat ID atual é: {chat_id}")

    async def send_message(self, message):
        try:
            chat_id = self.entry_chat_id.get()
            await self.bot.send_message(chat_id=chat_id, text=message)
            self.append_log(f"Mensagem enviada: {message}")
        except Exception as e:
            self.append_log(f"Erro ao enviar mensagem: {e}")
        finally:
            self.progress_bar.stop()  # Para a barra de progresso

    async def show_last_message(self):
        try:
            chat_id = self.entry_chat_id.get()
            last_message = await self.get_last_message(chat_id)
            self.append_log(f"Última mensagem: {last_message}")
        except Exception as e:
            self.append_log(f"Erro ao exibir última mensagem: {e}")
        finally:
            self.progress_bar.stop()  # Para a barra de progresso

    async def schedule_message(self, message, schedule_time):
        try:
            hour, minute = map(int, schedule_time.split(":"))
            now = datetime.now()
            scheduled_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

            if scheduled_time < now:
                scheduled_time = scheduled_time.replace(day=now.day + 1)

            await asyncio.sleep((scheduled_time - now).total_seconds())
            await self.send_message(message)
        except Exception as e:
            self.append_log(f"Erro ao agendar mensagem: {e}")
        finally:
            self.progress_bar.stop()  # Para a barra de progresso

    async def send_photo(self, file_path):
        try:
            chat_id = self.entry_chat_id.get()
            with open(file_path, 'rb') as photo:
                await self.bot.send_photo(chat_id=chat_id, photo=photo)
            self.append_log(f"Foto enviada: {file_path}")
        except Exception as e:
            self.append_log(f"Erro ao enviar foto: {e}")
        finally:
            self.progress_bar.stop()  # Para a barra de progresso

    async def send_document(self, file_path):
        try:
            chat_id = self.entry_chat_id.get()
            with open(file_path, 'rb') as document:
                await self.bot.send_document(chat_id=chat_id, document=document)
            self.append_log(f"Documento enviado: {file_path}")
        except Exception as e:
            self.append_log(f"Erro ao enviar documento: {e}")
        finally:
            self.progress_bar.stop()  # Para a barra de progresso

    async def get_last_message(self, chat_id):
        updates = await self.bot.get_updates()
        for update in reversed(updates):
            if update.message and update.message.chat.id == int(chat_id):
                return update.message.text
        return "Nenhuma mensagem encontrada."

    def append_log(self, text):
        self.text_log.configure(state='normal')
        self.text_log.insert(tk.END, f"{text}\n")
        self.text_log.configure(state='disabled')
        self.text_log.see(tk.END)


async def main():
    bot_token = 'SEU-TOKEN-ID'
    bot = telegram.Bot(token=bot_token)
    loop = asyncio.get_running_loop()

    # Criar a aplicação Tkinter
    app = TelegramBotPanel(bot, loop)

    # Atualizar a interface Tkinter periodicamente
    while True:
        app.update()
        await asyncio.sleep(0.1)

if __name__ == '__main__':
    asyncio.run(main())


