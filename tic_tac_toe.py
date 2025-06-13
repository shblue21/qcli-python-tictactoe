import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
LINE_WIDTH = 5
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

class TicTacToe:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Tic-Tac-Toe")
        self.clock = pygame.time.Clock()
        
        # Game state
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        
        # Font for displaying messages
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
    def draw_grid(self):
        """Draw the tic-tac-toe grid"""
        self.screen.fill(WHITE)
        
        # Draw vertical lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(
                self.screen, 
                BLACK, 
                (i * CELL_SIZE, 0), 
                (i * CELL_SIZE, WINDOW_SIZE), 
                LINE_WIDTH
            )
        
        # Draw horizontal lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(
                self.screen, 
                BLACK, 
                (0, i * CELL_SIZE), 
                (WINDOW_SIZE, i * CELL_SIZE), 
                LINE_WIDTH
            )
    
    def draw_figures(self):
        """Draw X's and O's on the board"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == 'X':
                    self.draw_cross(row, col)
                elif self.board[row][col] == 'O':
                    self.draw_circle(row, col)
    
    def draw_cross(self, row, col):
        """Draw an X in the specified cell"""
        start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
        end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
        pygame.draw.line(self.screen, RED, start_desc, end_desc, CROSS_WIDTH)
        
        start_asc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
        end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
        pygame.draw.line(self.screen, RED, start_asc, end_asc, CROSS_WIDTH)
    
    def draw_circle(self, row, col):
        """Draw an O in the specified cell"""
        center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(self.screen, BLUE, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
    
    def mark_square(self, row, col, player):
        """Mark a square with the current player's symbol"""
        if self.board[row][col] == '':
            self.board[row][col] = player
            return True
        return False
    
    def is_board_full(self):
        """Check if the board is full"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] == '':
                    return False
        return True
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows
        for row in range(GRID_SIZE):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] != ''):
                return self.board[row][0]
        
        # Check columns
        for col in range(GRID_SIZE):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] != ''):
                return self.board[0][col]
        
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != ''):
            return self.board[0][0]
        
        if (self.board[2][0] == self.board[1][1] == self.board[0][2] != ''):
            return self.board[2][0]
        
        return None
    
    def get_cell_from_mouse(self, pos):
        """Convert mouse position to board cell coordinates"""
        x, y = pos
        row = y // CELL_SIZE
        col = x // CELL_SIZE
        return row, col
    
    def draw_game_over_screen(self):
        """Draw the game over screen with winner or tie message"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
        overlay.set_alpha(128)
        overlay.fill(GRAY)
        self.screen.blit(overlay, (0, 0))
        
        # Display winner or tie message
        if self.winner:
            text = self.font.render(f"Player {self.winner} Wins!", True, BLACK)
        else:
            text = self.font.render("It's a Tie!", True, BLACK)
        
        text_rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Display restart instruction
        restart_text = self.small_font.render("Press R to restart or Q to quit", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 + 50))
        self.screen.blit(restart_text, restart_rect)
    
    def draw_current_player(self):
        """Display current player at the top of the window"""
        if not self.game_over:
            player_text = self.small_font.render(f"Current Player: {self.current_player}", True, BLACK)
            # Position text at top-left corner with some padding
            self.screen.blit(player_text, (10, 10))
    
    def restart_game(self):
        """Reset the game to initial state"""
        self.board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.game_over:
                        self.restart_game()
                    elif event.key == pygame.K_q:
                        running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        row, col = self.get_cell_from_mouse(mouse_pos)
                        
                        # Make sure the click is within the board
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            if self.mark_square(row, col, self.current_player):
                                # Check for winner
                                self.winner = self.check_winner()
                                if self.winner or self.is_board_full():
                                    self.game_over = True
                                else:
                                    # Switch players
                                    self.current_player = 'O' if self.current_player == 'X' else 'X'
            
            # Draw everything
            self.draw_grid()
            self.draw_figures()
            self.draw_current_player()
            
            if self.game_over:
                self.draw_game_over_screen()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
