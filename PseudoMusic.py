# Goals:
# Translate pitch readings into pseudo-music text and then translate that pseudo-text into an output of music on a blank Staff paper. 
    # Steps 
    # Figure out how to use a made up file format, read it, and then create a "music-text" 
    # How could I use JSON and format a piece of music Staff paper with a Treble cleff and time signature on it? 
# If inputted pitch is B4 or higher, rotate image by 180 degrees 


import pygame
import sys
import Note

def generate_sheet_music(music_file, output_file):

    # pygame setup
    pygame.init()
    background = pygame.image.load("staff_paper.png")



    ASSET_DIR = "MusicImages/"
    LINE_Y_OFFSET = 109.75 # Space in the Y-axiz between two lines of music
    NUM_LINES = 8 # Total lines of music 
    WHOLE_STEP_DIST = 4.075 # pixel measurement between a whole step (moving by one position/ledger line)
    NOTE_SPACE = 36 # amount of space before placing next note

    #Time Signature init (Common Time)
    time_sig_image = pygame.image.load(ASSET_DIR + "key_sig.png")
    time_sig_image = pygame.transform.scale(time_sig_image, (25, 25)) # Resize
    time_sig_position_x = 80
    time_sig_position_y = 26

    # Bar Line init (measure divides)
    bar_line_image = pygame.image.load(ASSET_DIR + "bar_line.png")
    bar_line_image = pygame.transform.scale(bar_line_image, (3, 35)) # Resize
    MEASURE_SPACE = 149 # space before placing next bar line
    MEASURES_PER_LINE = 4 
    bar_line_position_x = 240
    bar_line_position_y = 21.25

    #Quarter Note init
    quarter_note_image = pygame.image.load(ASSET_DIR + "Quarter.png")
    quarter_note_image = pygame.transform.scale(quarter_note_image, (31.5, 31.5))
    #set position for note
    quarter_note_position_x = 105
    quarter_note_position_y = 31.5

    # Half Note init
    half_note_image = pygame.image.load(ASSET_DIR + "Half.png")
    half_note_image = pygame.transform.scale(half_note_image, (40, 40))
    #set position for note
    half_note_position_x = 105
    half_note_position_y = 27

    # Whole Note init 
    whole_note_image = pygame.image.load(ASSET_DIR + "Whole.png")
    whole_note_image = pygame.transform.scale(whole_note_image, (10, 10))
    whole_note_position_x = 105
    whole_note_position_y = 55

    # Quarter Rest init
    rest_image = pygame.image.load(ASSET_DIR + "Quarter_Rest.png")
    rest_image = pygame.transform.scale(rest_image, (50, 20))
    rest_position_x = 105
    rest_position_y = 30

    # init screen and background
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
        # Set up page with Time Sigs and Bar Lines
        for i in range(NUM_LINES):
            for j in range(MEASURES_PER_LINE):
                screen.blit(bar_line_image, (bar_line_position_x + j*MEASURE_SPACE, bar_line_position_y + i*LINE_Y_OFFSET))
        screen.blit(bar_line_image, (bar_line_position_x + j*MEASURE_SPACE, bar_line_position_y + i*LINE_Y_OFFSET))
        for i in range(NUM_LINES):
            screen.blit(time_sig_image, (time_sig_position_x, time_sig_position_y + i*LINE_Y_OFFSET))


        ASSET_DIR = "temp/"
        clef, time_signature, tempo, measures = Note.read_music_file_with_measures(ASSET_DIR + music_file)

        for i in range(len(measures)):
            line_num = i // MEASURES_PER_LINE
            measure_num = i % MEASURES_PER_LINE
            for j in range(len(measures[i])):
                note = measures[i][j]
                position_x=0
                position_y=0
                image=None

                if note.duration == 1:
                    image = quarter_note_image
                    position_x = quarter_note_position_x
                    position_y = quarter_note_position_y
                    rotation_offset_y = 25
                elif note.duration == 2:
                    image = half_note_image
                    position_x = half_note_position_x
                    position_y = half_note_position_y
                    rotation_offset_y = 22
                elif note.duration == 4:
                    image = whole_note_image
                    position_x = whole_note_position_x
                    position_y = whole_note_position_y
                    rotation_offset_y = 0
                else:
                    print("Invalid Duration!")
                    exit(-1)

                dist = note.half_steps_from_d3()
                if dist >= 5:
                    image = pygame.transform.rotate(image, 180)
                    position_y += rotation_offset_y  

                position_x += measure_num * MEASURE_SPACE + j * NOTE_SPACE
                position_y += line_num * LINE_Y_OFFSET - dist * WHOLE_STEP_DIST

                screen.blit(image, (position_x, position_y))
        pygame.image.save(screen, output_file, ".png")

        # Updates the display
        pygame.display.flip()
        running = False

    #Quit pygame
    pygame.quit()
    sys.exit()
