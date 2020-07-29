import PySimpleGUI as gui

layout = [[gui.Text('Document to open')],
          [gui.In(), gui.FileBrowse()],
          [gui.Open(), gui.Cancel()]]

window = gui.Window('Window that stays open', layout)

while True:
    event, values = window.read()

    fname = values[0]
    gui.popup('The filename you chose was', fname)

    if event == gui.WIN_CLOSED or event == 'Exit':
        break

window.close()