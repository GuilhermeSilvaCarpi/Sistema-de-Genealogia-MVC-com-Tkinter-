from view import View
from model import Model
from controller import Controller

if __name__ == '__main__':
    model = Model()
    view = View(model)
    controller = Controller(model, view)
    
    view.mainloop()
    
    model.fechar_conexao()
