import streamlit as st
import music21 as m21
from MelodyConverter import preprocess
from MelodyGenerator import MelodyGenerator, SEQUENCE_LENGTH
# import StringIO
#from pydub import AudioSegment

@st.cache(allow_output_mutation=True)
def load_model(model):
    mg = MelodyGenerator(model_path=model)

    return mg

model_path = "E:/G_project/model_final.h5"
mg = load_model(model_path)

header = st.container()
workstation = st.container()

with header:
    st.title("Music Generation Model")
    st.text("")

with workstation:
    with st.form(key = "form1"):

        melody_path = st.text_input("Enter your MIDI file path :")
        default_save_path = melody_path.split('\\')[:-1]
        s = str()
        for i in default_save_path:
            s += str(i) + '\\'
        save_path = st.text_input("Where do you want to save the generated melody?",s)
        submit = st.form_submit_button("Done")
        if melody_path != '':
            try:

                encoded_song = preprocess(melody_path, save_path)
                st.write("Your file successfully loaded")

            except:
                st.write("Your paths are not correct!")

        else:
            st.write("Please enter your file path")

    x = st.slider("Determine the seed length", min_value= 10, max_value= 100, value= 10, step= 10)
    num_of_symbols = st.slider("Determine the number of symbols to be generated", min_value=200, max_value=10000, value=200, step=100)
    temp = st.slider("How much percent do you want your generated melody to be unpredictable?",min_value=10, max_value= 90, value= 70, step= 10)
    temp = temp/100
    st.write(temp)
    st.markdown("Applying this algorithm multiple times could generate different melodies, how many times do you want to run the algorithm on the same seed ?")
    num_of_melodies = st.selectbox("", options=[1,2,3,4,5])

    predict_button = st.button("Predict")
    if predict_button == True:


        s = encoded_song.split(' ')[:x]
        seed = ''
        for i in s:
            seed += str(i) + " "
        st.markdown("Here it's the music time-series representation of your seed ")
        st.write(seed)
        st.markdown("Please Wait MuseScore to open ...")
        for i in range(num_of_melodies):
            melody = mg.generate_melody(seed, num_of_symbols, SEQUENCE_LENGTH, temp)
            full_file_name = save_path + "\\" + "generated_melody_" + str(i) + ".mid"

            stream = mg.save_melody(melody, file_name = full_file_name)
            stream.show()


#
