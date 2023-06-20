from psychopy import visual, core, gui
import random
import pandas as pd
import gdown

# Define the experiment parameters
experiment_info = {'Participant ID': '', 'Condition': ''}
dlg = gui.DlgFromDict(dictionary=experiment_info, title='Movie-fMRI Task')
if not dlg.OK:
    core.quit()

# Path to the Excel file containing questions and choices
questions_file = 'path_to_questions_file.xlsx'

# Load the questions and choices from the Excel file
questions_data = pd.read_excel(questions_file)

# Define the durations in seconds
cue_duration = 2.0  # Duration of the cue display
question_duration = 4.0  # Duration of the question display
iti_duration = 2.0  # Duration of the inter-trial interval

# Google Drive file IDs for movie and question folders
movie_folder_ids = {
    'Video01': 'google_drive_file_id1',
    'Video02': 'google_drive_file_id2',
    # Add file IDs for Video03 to Video14 folders
}

question_folder_ids = {
    'movie01': 'google_drive_file_id1',
    'movie02': 'google_drive_file_id2',
    # Add file IDs for movie03 to movie14 folders
}

# Function to download files from Google Drive
def download_file_from_drive(file_id, destination):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url, destination, quiet=False)

# Create the PsychoPy window
win = visual.Window(size=(800, 600), fullscr=False)

# Create the visual stimuli
cue_text = visual.TextStim(win, text='', height=0.1)
movie_stimulus = visual.MovieStim3(win, filename='', size=(800, 600), flipVert=False, flipHoriz=False)
question_text = visual.TextStim(win, text='', height=0.1)
image_stimulus = visual.ImageStim(win, image='', size=500)

# Load the question data for the current movie
def load_question_data(movie_index):
    return questions_data.iloc[movie_index]

# Main experiment loop
for movie_index in range(len(questions_data)):
    # Load the question data for the current movie
    question_data = load_question_data(movie_index)

    # Randomly select a cognitive domain
    cognitive_domain = random.choice([
        'Color', 'Motion-Direction', 'Face', 'Object', 'Body',
        'Scene', 'Auditory', 'Emotion', 'Semantics', 'Action',
        'Social interaction', 'Spatial/Relational', 'Language'
    ])

    # Set the cue text based on the current cognitive domain
    cue_text.text = cognitive_domain

    # Download the movie from Google Drive
    movie_folder_id = movie_folder_ids[f'Video{movie_index+1:02d}']
    movie_filename = 'Video.mp4'
    movie_path = f'movie{movie_index+1:02d}/{movie_filename}'
    download_file_from_drive(movie_folder_id, movie_path)

    # Download the question file from Google Drive
    question_folder_id = question_folder_ids[f'movie{movie_index+1:02d}']
    question_filename = f'movie{movie_index+1:02d}/{cognitive_domain}_Questions.txt'
    question_path = f'movie{movie_index+1:02d}/{cognitive_domain}_Questions.txt'
    download_file_from_drive(question_folder_id, question_path)
    with open(question_path, 'r') as f:
        question_text.text = f.read()

    # Start the trial
    cue_text.draw()
    win.flip()
    core.wait(cue_duration)

    movie_stimulus.loadMovie(movie_path)
    movie_stimulus.play()
    win.flip()
    core.wait(movie_stimulus.duration)

    movie_stimulus.stop()

    if cognitive_domain in ['Color', 'Motion-Direction', 'Face', 'Object', 'Body']:
        # Load the image choices for the current question
        choices_folder_id = movie_folder_ids[f'Video{movie_index+1:02d}']
        choices_folder_path = f'movie{movie_index+1:02d}'
        download_file_from_drive(choices_folder_id, choices_folder_path)
        
        choice1_image = f'{choices_folder_path}/{cognitive_domain}_Choice1.jpg'
        choice2_image = f'{choices_folder_path}/{cognitive_domain}_Choice2.jpg'

        # Display image choices
        image_stimulus.setImage(choice1_image)
        image_stimulus.draw()
        win.flip()
        core.wait(question_duration)

        image_stimulus.setImage(choice2_image)
        image_stimulus.draw()
        win.flip()
        core.wait(iti_duration)

    else:
        # Display text choices
        choice1_text = question_data[f'{cognitive_domain} - Choice 1']
        choice2_text = question_data[f'{cognitive_domain} - Choice 2']

        # Randomize the correct choice between 'a' and 'b'
        correct_choice = random.choice(['a', 'b'])

        if correct_choice == 'a':
            correct_choice_text = choice1_text
            incorrect_choice_text = choice2_text
        else:
            correct_choice_text = choice2_text
            incorrect_choice_text = choice1_text

        choice1_text_stimulus = visual.TextStim(win, text=choice1_text, height=0.1)
        choice2_text_stimulus = visual.TextStim(win, text=choice2_text, height=0.1)

        # Display the choices without indicating correctness
        choice1_text_stimulus.draw()
        win.flip()
        core.wait(question_duration)

        choice2_text_stimulus.draw()
        win.flip()
        core.wait(iti_duration)

# Clean up
win.close()
core.quit()
