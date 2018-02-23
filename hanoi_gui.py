'''
Created on Feb 16, 2018

@author: DanielBadir
'''

import tkinter
import hanoi

_BACKGROUND_COLOR = '#FFFFFF' # White

# TODO:
## 1. Drawing Towers
## 2. Drawing Disks
## 3. Moving from one Tower to another
class HanoiWindow:
    _WIDTH = 500
    _HEIGHT = 500
    
    # TODO -- find some way to ask the user how many Disks he wants
    def __init__(self):
        self._create_window()
        
        self.game = hanoi.Game(3)
        
    def _create_window(self) -> None:
        """Create the main window for the Tower of Hanoi puzzle."""
        self._root_window = tkinter.Tk()
        self._root_window.title('Tower of Hanoi')
        
        hanoi_canvas = tkinter.Canvas(master=self._root_window,
                                      width=self._WIDTH, 
                                      height=self._HEIGHT,
                                      background=_BACKGROUND_COLOR)
        
        hanoi_canvas.create_rectangle(self._WIDTH // 5, self._HEIGHT,
                                      self._WIDTH // 5 - 50, 75, 
                                      fill='black',
                                      tags=('tower 1'))
        
        hanoi_canvas.create_rectangle(self._WIDTH // 2 + 50, self._HEIGHT, 
                                      self._WIDTH // 2, 75, 
                                      fill='black',
                                      tags=('tower 2'))
        
        hanoi_canvas.create_rectangle(self._WIDTH - 50, self._HEIGHT,
                                      self._WIDTH - 100, 75,
                                      fill='black',
                                      tags=('tower 3'))
        
        hanoi_canvas.pack()
        
    def run(self) -> None:
        """Start a session of Tower of Hanoi."""
        self._root_window.mainloop()
        
        

if __name__ == '__main__':
    hanoi_window = HanoiWindow()
    hanoi_window.run()