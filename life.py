import time
import tkinter as tk
from tkinter import messagebox
from functools import partial

import shapes_and_seeds as ss

class LifeGame:
# An instance of LifeGame contains all the parts necessary for our simulation:
# A GUI to contain the simulation output and its controls     
# An array of game Cells, each containing its address, state, and a function to determine its neighbor count
    def __init__(self, rows, cols):
        self.gui = self.LifeGUI(self)
        self.rows = rows
        self.cols = cols
        self.board = [[self.Cell(self, r, c) for c in range(cols)] for r in range(rows)]
        self.turn = 0
        self.simulation_on = False
        self.seed = None # record this so that users can click 'Reset'
        
        self.game_speed = .5 # tick length in seconds
        self.CYCLE_SPEED = 50 # ms between checking for updated
        self.after_id = None # for repeating the game loop
        self.last_turn_timestamp = time.time()

        self.pending_insert = False # When the user selects an item to insert, flag this as True and store the item seed in pending_insert_seed
        self.pending_insert_seed = None
    
    def game_loop(self):
        # print('game_loop')
        if self.simulation_on: # and self.turn < 25:
            now = time.time()
            if (now - self.last_turn_timestamp) >= self.game_speed:
                self.last_turn_timestamp =  time.time()

                self.turn +=1
                self.gui.lbl_turn.config(text=f'Tick: {self.turn}')
                # self.gui.print_board(show_neighbors=False)
                
                self.advance_simulation()
                self.gui.root.update_idletasks()
                
            self.after_id = self.gui.root.after(self.CYCLE_SPEED, self.game_loop) #try again in (at least) X ms
            
    class Cell:
        def __init__(self, parent, row, col):
            self.parent = parent
            self.row = row
            self.col = col
            self.alive = False
            self.alive_next_turn = False
            self.alive_prev_turn = False
            
            self.button = tk.Button(master=parent.gui.frame_board, text=' ', width=1, height=1, command=self.click_event)
            self.button.grid(row=row, column=col)     

        def click_event(self):
            if self.parent.pending_insert: # Try to place the object

                try:
                    self.parent.parse_seed_val(self.parent.pending_insert_seed, offset_r=self.row, offset_c=self.col)
                    self.parent.pending_insert = False
                    self.parent.pending_insert_seed = None
                    self.parent.gui.lbl_pending_insert.config(text='')
                except IndexError:
                    messagebox.showerror(title='Out of Range', message='Not enough room to place object!')        
            
            else:
                self.toggle_cell_value()

        def toggle_cell_value(self):
            self.alive = not self.alive
            bg = '#000000' if self.alive  else '#FFFFFF'
            self.button.config(bg=bg)

        def get_neighbor_count(self):
            r = self.row
            c = self.col
            neighbors = [(r-1, c-1), (r-1, c), (r-1, c+1), (r, c-1), (r, c+1), (r+1, c-1), (r+1, c), (r+1, c+1)]

            count = 0
            for n in neighbors:
                if n[0]>=0 and n[0]<self.parent.rows and n[1]>=0 and n[1]<self.parent.cols and self.parent.board[n[0]][n[1]].alive: count += 1
            return count
  
    def advance_simulation(self):
    # Loops through board and determine which cells should survive/be generated and store result in alive_next_turn, 
    # then render any changes to the board and finally set .alive to .alive_next_turn's value
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.board[r][c]
                neighbors = cell.get_neighbor_count()
                if neighbors < 2 or neighbors > 3: cell.alive_next_turn = False # underpopulation / overpopulation
                elif cell.alive: cell.alive_next_turn = True # goldilocks zone
                elif neighbors == 3: cell.alive_next_turn = True # dead cells become alive IFF they have 3 neighbors

        for r in range(self.rows):
            for c in range(self.cols): 
                cell = self.board[r][c] 
                cell.alive_prev_turn = cell.alive # used for sparse rendering
                self.board[r][c].alive = self.board[r][c].alive_next_turn     

        self.gui.render_board(sparse=True)

    def restart_simulation(self): # Reload the seed (if any)
        self.simulation_on = False
        self.turn = 0
        self.clear_board()
        self.gui.btn_start_pause.config(text='Start')
        self.gui.lbl_turn.config(text='Tick: 0')
        
        self.pending_insert = False
        self.pending_insert_seed = None
        self.gui.lbl_pending_insert.config(text='')

        if self.seed is not None:
            self.parse_seed_val(self.seed)

    def clear_simulation(self):
        self.seed = None
        self.restart_simulation()
        
    class LifeGUI:
        def __init__(self, parent):
            self.parent = parent 
            self.root = tk.Tk()
            self.root.title('Life')
            self.root.config(menu=self.create_menu_bar())    
            self.frame_board = tk.Frame(master=self.root) # contains the cell buttons that make up the game
            
            self.controls_frame = tk.Frame(master=self.root) # Start/Stop/Continue/Reset/New
            self.lbl_turn = tk.Label(master = self.controls_frame, text='Tick: 0', font='Arial 16 bold')
            self.btn_start_pause = tk.Button(master=self.controls_frame, text='Start', font='Arial 18 bold', command=self.parent.start_pause_simulation) # Start/resume the simulation
            self.btn_reset = tk.Button(master=self.controls_frame, text='Reset', font='Arial 18 bold', command=self.parent.restart_simulation) # Start/resume the simulation
            self.btn_clear = tk.Button(master=self.controls_frame, text='Clear', font='Arial 18 bold', command=self.parent.clear_simulation) # Start/resume the simulation
            self.speed_val = tk.IntVar()
            self.speed_val.set(3)
            self.lbl_pending_insert = tk.Label(master = self.controls_frame, text='', font='Arial 16 italic')
            
            lbl_slider_speed = tk.Label(master=self.controls_frame, text='Speed', font= 'Arial 14 bold')
            self.slider_speed = tk.Scale(master=self.controls_frame, from_=5, to=1,var=self.speed_val, command=self.parent.adjust_game_speed)

            self.lbl_turn.grid(row=0, column=0, padx=10)
            self.btn_start_pause.grid(row=0, column=1, padx=10)
            self.btn_reset.grid(row=0, column=2, padx=10)
            self.btn_clear.grid(row=0, column=3, padx=10)
            lbl_slider_speed.grid(row=0, column=4, padx=(10,0))
            self.slider_speed.grid(row=0, column=5, padx=(0,10))
            self.lbl_pending_insert.grid(row=1, column=1, columnspan=6, padx=10)

            self.controls_frame.grid(row=0, column=0, padx=30, pady=30)        
            self.frame_board.grid(row=1, column=0, padx=30, pady=(0,30))

            self.add_key_binds()

        def add_key_binds(self):
            self.root.bind('<Control-Q>', self.quit_game)
            self.root.bind('<Control-q>', self.quit_game)
        
        def quit_game(self, event=None):
            print('Goodbye.')
            self.root.quit()
                
        def create_menu_bar(self):
            menubar = tk.Menu(self.root)
            file_menu = tk.Menu(menubar, tearoff=0)
            
            open_menu = tk.Menu(file_menu, tearoff=0)
            file_menu.add_cascade(label='Open Seed', menu=open_menu)

            for i in ss.dict_seeds.keys():
                open_menu.add_command(label=i, command=partial(self.parent.seed_game, i))
            
            insert_menu = tk.Menu(file_menu, tearoff=0)
            file_menu.add_cascade(label='Insert', menu=insert_menu)

            for i in ss.dict_entities.keys():
                insert_menu.add_command(label=i, command=partial(self.parent.add_pending_insert, i))

            file_menu.add_command(label='Exit', command=self.root.quit, accelerator='Ctrl+Q')
            menubar.add_cascade(label='File', menu=file_menu)
            return menubar
        
        def render_board(self, sparse=False): # If sparse, only update cells that have changed state this tick
            for r in range(self.parent.rows):
                for c in range(self.parent.cols):  
                    if not sparse or (sparse and self.parent.board[r][c].alive != self.parent.board[r][c].alive_prev_turn):
                        bg = '#000000' if self.parent.board[r][c].alive else '#FFFFFF'
                        self.parent.board[r][c].button.config(bg=bg)            
        
        def print_board(self, show_neighbors=True):
            out = f'Tick: {self.parent.turn}\n'
            for r in range(self.parent.rows):
                for c in range(self.parent.cols):
                    if show_neighbors:
                        out += ' . ' if not self.parent.board[r][c].alive else f' {self.parent.board[r][c].get_neighbor_count()} '
                    else:
                        out += ' .' if not self.parent.board[r][c].alive else f' ■'

                out += '\n'
            print(out)

    def start_pause_simulation(self):
        self.simulation_on = not self.simulation_on
        if self.simulation_on:
            self.game_loop()
            self.gui.btn_start_pause.config(text='Pause')
        else:
            self.gui.btn_start_pause.config(text='Start')

    def adjust_game_speed(self, event):
        speed = self.gui.speed_val.get()
        if speed == 1:   self.game_speed = 2
        elif speed == 2: self.game_speed = 1
        elif speed == 3: self.game_speed = .5
        elif speed == 4: self.game_speed = .25
        elif speed == 5: self.game_speed = .15
            
    def clear_board(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.board[r][c].alive = False
                self.board[r][c].alive_next_turn = False
                self.board[r][c].alive_prev_turn = False

        self.gui.render_board(sparse=False)
                
    def parse_seed_val(self, seed_val, offset_r=0, offset_c=0):
    # TODO preemptively check if we have enough space to plop this down before starting, otherwise we'll end up with a partially drawn object
    
        row_num = -1 # because 0-indexed arrays
        for row in seed_val.splitlines()[1:]: # ignore the first, blank line
            row_num += 1
            col_num = -1 # because 0-indexed arrays
            for col in row:
                col_num += 1
                if int(col) > 0: 
                    self.board[offset_r+row_num][offset_c+col_num].alive = True

        self.gui.render_board(sparse=False)

    def add_pending_insert(self, entity_name):
        self.pending_insert_seed = ss.dict_entities[entity_name]
        self.pending_insert = True # When the user selects an item to insert, flag this as True and store the item seed in pending_insert_seed
        self.gui.lbl_pending_insert.config(text='Click on a cell to place the object, or Esc to cancel')
        
    def seed_game(self, seed_name):
        self.clear_simulation()

        self.seed = ss.dict_seeds[seed_name]
        self.parse_seed_val(self.seed)

if __name__ == '__main__':    
    game_of_life = LifeGame(rows=25, cols=40)
    game_of_life.seed_game('Pulsars')
    
    game_of_life.gui.root.mainloop()



