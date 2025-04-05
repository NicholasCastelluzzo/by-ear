# Class to create note objects
import re

class NOTE:
    VALID_PITCHES = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#''R']
    VALID_OCTAVES = list(range(0,8)) # Can make from 3 to 5 for test purposes  
    VALID_DURATIONS = [0.5, 1, 2, 4]
    
    # initialization of arguments 
    def __init__(self, pitch, octave, duration):
        if pitch not in self.VALID_PITCHES:
            raise ValueError(f"Invalid pitch '{pitch}'. Must be one of {self.VALID_PITCHES}")
        if octave not in self.VALID_OCTAVES:
            raise ValueError(f"Invalid octave '{octave}'. Must be between 0 and 8.")
        if duration not in self.VALID_DURATIONS:
            raise ValueError(f"Invalid duration '{duration}'. Must be one of {self.VALID_DURATIONS}")
        
        self.pitch = pitch
        self.octave = octave
        self.duration = duration

    def __repr__(self):
        return f"Note(pitch='{self.pitch}', octave={self.octave}, duration={self.duration})"
    
    # Number of half steps from the lowest possible/ default position note - D3
    def half_steps_from_d3(self):
        p_d = ord(self.pitch[0]) - ord('D')
        o_d = self.octave - 3
        dist = p_d + o_d * 7
        return dist

# Parses through the header line. Cleff, Time Sig, and Tempo Marking 
def parse_header_line(line):
    parts = line.strip().split()
    if len(parts) != 3 or not parts[2].startswith("Q="):
        raise ValueError("Header line must be in format: 'T 4/4 Q=109'")
    
    clef = parts[0]
    time_signature = parts[1]
    tempo = int(parts[2][2:])  # Get value after 'Q='
    return clef, time_signature, tempo

# For inserting semicolons if by some chance the input file makes a mistake in formatting
def fix_missing_semicolons(measure_str):
    # Add semicolons between notes that are missing them
    return re.sub(r'(\d)([A-GR][#b]?\d:)', r'\1;\2', measure_str)

# Parses through measures. A measure's end is desginated by "|"
def parse_measure(measure_str):
    notes = []
    measure_str = fix_missing_semicolons(measure_str)  # auto-fix formatting issues
    for token in measure_str.strip().split(';'):
        if not token:
            continue
        try:
            pitch_octave, duration_str = token.split(':')
            match = re.match(r'^([A-GR][#b]?)(\d)$', pitch_octave)
            if not match:
                raise ValueError(f"Invalid pitch-octave format: '{pitch_octave}'")
            pitch = match.group(1)
            octave = int(match.group(2))
            duration = float(duration_str)
            notes.append(NOTE(pitch, octave, duration))
        except Exception as e:
            raise ValueError(f"Error parsing token '{token}': {e}")
    return notes


# Reads formatted music file w/ measure structure
# I got the full note sequence and the detector for reading all lines of .music files from ChatGPT
def read_music_file_with_measures(filename) -> tuple[str, str, str, list[list[NOTE]]]:
    import os
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File '{filename}' not found. Make sure it's in the correct folder.")

    with open(filename, 'r') as file:
        # Remove empty lines and comments
        lines = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

    if len(lines) < 2:
        raise ValueError("File must contain at least a header and a note line")

    # Header line is still the first
    clef, time_signature, tempo = parse_header_line(lines[0])

    # Remaining lines may span multiple lines of notes
    note_lines = lines[1:]

    # Join all the note lines together using '|' to preserve measure separation
    full_note_sequence = '|'.join(note_lines)

    # Now split the full sequence into measures
    measure_strs = full_note_sequence.split('|')
    measures = [parse_measure(m_str) for m_str in measure_strs]

    return clef, time_signature, tempo, measures
    