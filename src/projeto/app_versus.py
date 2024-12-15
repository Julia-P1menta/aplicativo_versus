import toga
from toga.style import Pack
from toga.style.pack import COLUMN
from spellchecker import SpellChecker  # Biblioteca para correção ortográfica


class PoemaApp(toga.App):
    def startup(self):
        # Janela principal
        self.main_window = toga.MainWindow(title=self.name)

        # Lista salva dos poemas
        self.poemas = []
        self.poemas_list = toga.Selection(items=self.poemas, on_select=self.on_poemas_select)

        # Botão para criar novo
        add_button = toga.Button('Criar Novo Poema', on_press=self.add_poema, style=Pack(padding=10))
        main_box = toga.Box(children=[self.poemas_list, add_button], style=Pack(direction=COLUMN, padding=10))

        # Janela principal
        self.main_window.content = main_box
        self.main_window.show()

    def add_poema(self, widget):
        # Janela para criação do poema
        edit_window = toga.Window(title="Novo Poema")

        # Campo de texto para o título
        title_input = toga.TextInput(placeholder='Título do Poema', style=Pack(flex=1, padding=10))

        # Campo de texto maior para o poema
        dialog = toga.MultilineTextInput(placeholder='Escreva seu Poema', style=Pack(flex=1, padding=10))

        # Botão de corrigir
        correct_button = toga.Button('Corrigir', on_press=lambda x: self.correct_text(dialog), style=Pack(padding=10))

        # Botão de salvar
        save_button = toga.Button('Salvar', on_press=lambda x: self.save_poema(title_input.value, dialog.value, edit_window), style=Pack(padding=10))

        # Botão de cancelar
        cancel_button = toga.Button('Cancelar', on_press=lambda x: edit_window.close(), style=Pack(padding=10))

        # Dois botões na mesma janela
        edit_box = toga.Box(children=[title_input, dialog, correct_button, save_button, cancel_button],
                            style=Pack(direction=COLUMN, padding=10, alignment='center'))

        edit_window.content = edit_box
        edit_window.show()

    def correct_text(self, dialog):
        # Corrige o texto do poema
        spell = SpellChecker(language='pt')  # Define o idioma para português
        words = dialog.value.split()
        corrected_words = [spell.correction(word) if word in spell else word for word in words]
        corrected_text = ' '.join(corrected_words)
        dialog.value = corrected_text
        self.main_window.info_dialog("Correção", "Erros corrigidos automaticamente!")

    def save_poema(self, title, text, edit_window):
        # Salva o poema na lista
        if title.strip() == "" or text.strip() == "":
            self.main_window.info_dialog("ATENÇÃO", "O título e o poema não podem ser vazios!")
            return

        # Atualiza a lista com o novo poema
        self.poemas.append(f"{title}: {text}")
        self.poemas_list.items = [poema.split(': ')[0] for poema in self.poemas]  # Mostra apenas os títulos

        edit_window.close()
        self.return_to_main()

    def return_to_main(self):
        # Retorna para a janela principal
        add_button = toga.Button('Criar Novo Poema', on_press=self.add_poema, style=Pack(padding=10))
        main_box = toga.Box(children=[self.poemas_list, add_button], style=Pack(direction=COLUMN, padding=10))
        self.main_window.content = main_box  # Atualiza o conteúdo da janela principal

    def on_poemas_select(self, widget):
        # Exibe o poema selecionado
        selected_poema = widget.value
        if selected_poema:
            poema_completo = next(poema for poema in self.poemas if poema.startswith(selected_poema))
            titulo, conteudo = poema_completo.split(': ', 1)
            self.main_window.info_dialog(titulo, conteudo)


def main():
    return PoemaApp('Versos', 'org.beeware.poemasnotes')


if __name__ == "__main__":
    main().main_loop()
