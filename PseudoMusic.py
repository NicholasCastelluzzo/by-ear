# Goals:
# Translate pitch readings into pseudo-music text and then translate that pseudo-text into an output of music on a blank Staff paper. 
    # Steps 
    # Figure out how to use a made up file format, read it, and then create a "music-text" 
    # How could I use JSON and format a piece of music Staff paper with a Treble cleff and time signature on it? 


# If inputted pitch is B4 or higher, rotate image by 180 degrees 

# Example file showing a basic pygame "game loop"
import pygame
import sys

# pygame setup
pygame.init()
background = pygame.image.load("staff_paper.png")

#WHOLE_STEP_DIST_X =
#WHOLE_STEP_DIST_Y =


LINE_Y_OFFSET = 109.7 # Space in the Y-axiz between two lines of music
NUM_LINES = 8 # Total lines of music 

time_sig_image = pygame.image.load("key_sig.png")
time_sig_image = pygame.transform.scale(time_sig_image, (25, 25))
time_sig_position_x = 80
time_sig_position_y = 26

bar_line_image = pygame.image.load("bar_line.png")
bar_line_image = pygame.transform.scale(bar_line_image, (5, 35))
MEASURE_SPACE = 149 # space before placing next bar line
MEASURES_PER_LINE = 4 
bar_line_position_x = 240
bar_line_position_y = 26


# Test for inserting image onto background
quarter_note_image = pygame.image.load("Quarter.png")
# Resize if needed
quarter_note_image = pygame.transform.scale(quarter_note_image, (31, 31))
#set position for note
NOTE_SPACE = 36 # amount of space before placing next note
# NUM_NOTES = 
note_position_x = 110
note_position_y = 20

screen_width, screen_height = background.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("By Ear")


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the background
    screen.blit(background, (0, 0))
    # Insert Notes
    screen.blit(quarter_note_image, (note_position_x, note_position_y))
    screen.blit(quarter_note_image, (note_position_x, note_position_y))
    #for i in range(16):
        #screen.blit(quarter_note_image, (note_position_x + i*NOTE_SPACE, note_position_y))
        #screen.blit(quarter_note_image, (note_position_x + 540, note_position_y))

    for i in range(NUM_LINES):
        for j in range(MEASURES_PER_LINE):
            screen.blit(bar_line_image, (bar_line_position_x + j*MEASURE_SPACE, note_position_y + i*LINE_Y_OFFSET))
    
    
    for i in range(NUM_LINES):
        screen.blit(time_sig_image, (time_sig_position_x, time_sig_position_y + i*LINE_Y_OFFSET))

    # Updates the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()


