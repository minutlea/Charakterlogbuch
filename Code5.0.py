import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import binascii
import pandas as pd
from github_contents import GithubContents
import urllib

# Set constants
DATA_FILE = "MyLoginTable.csv"
DATA_COLUMNS = ['username', 'name', 'password']
CHAR_COLUMNS = [
    "username",
    "name",
    "age",
    "gender",
    "race",
    "body_type",
    "eye_color",
    "hair_color",
    "skin_color",
    "skin_condition",
    "characteristics",
    "perks",
    "flaws",
    "special_traits",
    "image"
    ]

def login_page():
    """ Login an existing user. """
    st.title("Login")
    with st.form(key='login_form'):
        st.session_state['username'] = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            authenticate(st.session_state.username, password)

def register_page():
    """ Register a new user. """
    st.title("Register")
    with st.form(key='register_form'):
        new_username = st.text_input("New Username")
        new_name = st.text_input("Name")
        new_password = st.text_input("New Password", type="password")
        if st.form_submit_button("Register"):
            hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt()) # Hash the password
            hashed_password_hex = binascii.hexlify(hashed_password).decode() # Convert hash to hexadecimal string
            
            # Check if the username already exists
            if new_username in st.session_state.df_users['username'].values:
                st.error("Username already exists. Please choose a different one.")
                return
            else:
                new_user = pd.DataFrame([[new_username, new_name, hashed_password_hex]], columns=DATA_COLUMNS)
                st.session_state.df_users = pd.concat([st.session_state.df_users, new_user], ignore_index=True)
                
                # Writes the updated dataframe to GitHub data repository
                st.session_state.github.write_df(DATA_FILE, st.session_state.df_users, "added new user")
                st.success("Registration successful! You can now log in.")

def authenticate(username, password):
    """ 
    Initialize the authentication status.

    Parameters:
    username (str): The username to authenticate.
    password (str): The password to authenticate.    
    """
    login_df = st.session_state.df_users
    login_df['username'] = login_df['username'].astype(str)

    if username in login_df['username'].values:
        stored_hashed_password = login_df.loc[login_df['username'] == username, 'password'].values[0]
        stored_hashed_password_bytes = binascii.unhexlify(stored_hashed_password) # convert hex to bytes
        
        # Check the input password
        if bcrypt.checkpw(password.encode('utf8'), stored_hashed_password_bytes): 
            st.session_state['authentication'] = True
            st.success('Login successful')
            st.rerun()
        else:
            st.error('Incorrect password')
    else:
        st.error('Username not found')

def init_github():
    """Initialize the GithubContents object."""
    if 'github' not in st.session_state:
        st.session_state.github = GithubContents(
            st.secrets["github"]["owner"],
            st.secrets["github"]["repo"],
            st.secrets["github"]["token"])
        print("github initialized")
    
def init_credentials():
    """Initialize or load the dataframe."""
    if 'df_users' in st.session_state:
        pass

    if st.session_state.github.file_exists(DATA_FILE):
        st.session_state.df_users = st.session_state.github.read_df(DATA_FILE)
    else:
        st.session_state.df_users = pd.DataFrame(columns=DATA_COLUMNS)

def init_character_data():
    """Initialize or load the character dataframe."""

    char_file = f"MyCharacterTable_{st.session_state.username}.csv"
    if 'df_characters' in st.session_state:
        pass

    if st.session_state.github.file_exists(char_file):
        st.session_state.df_characters = st.session_state.github.read_df(char_file)
    else:
        st.session_state.df_characters = pd.DataFrame(columns=CHAR_COLUMNS)


# Funktion zum Konvertieren von Bildern in Base64
def image_to_base64(image):
    buffered = BytesIO()
    img = Image.open(image)
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

# Funktion zum Konvertieren von Base64 in Bilder
def base64_to_image(base64_str):
    return Image.open(BytesIO(base64.b64decode(base64_str)))

# Funktion zum Erstellen eines neuen Charakters
def create_character():
    st.title("Neuen Charakter erstellen")
    st.subheader("Charaktereigenschaften")

    # Eingabefelder für Charaktereigenschaften
    name = st.text_input("Name")
    age = st.number_input("Alter", min_value=0, max_value=200, value=0)
    gender = st.selectbox("Geschlecht", ["Männlich", "Weiblich", "Andere"])
    race = st.selectbox("Rasse", ["Mensch", "Elf", "Zwerg", "Ork", "Goblin", "Tiefling", "Halbelf", "Drachengeborener", "Halbork", "Andere"])
    body_type = st.text_input("Körperbau", "Körperbau hier eingeben...")
    eye_color = st.color_picker("Augenfarbe", "#FFFFFF")  # Standardfarbe ist weiß
    hair_color = st.color_picker("Haarfarbe", "#FFFFFF")  # Standardfarbe ist weiß
    skin_color = st.color_picker("Hautfarbe", "#FFFFFF")  # Standardfarbe ist weiß
    skin_condition = st.text_input("Hautzustand", "Hautzustand hier eingeben...")
    characteristics = st.text_area("Charakteristika", "Charakteristika hier eingeben...")
    perks = st.text_area("Vorteile", "Vorteile hier eingeben...")
    flaws = st.text_area("Fehler", "Fehler hier eingeben...")
    special_traits = st.text_area("Besondere Merkmale", "Besondere Merkmale hier eingeben...")
    #character_image = st.file_uploader("Charakterbild hochladen", type=["jpg", "jpeg", "png"])
    character_image = st.text_input("Bild-URL", "Bild-URL hier eingeben...")


    if st.button("Charakter erstellen"):
        # Charakterdaten in Session State speichern
        character_data = {
            "username": st.session_state.username, 
            "name": name,
            "age": age,
            "gender": gender,
            "race": race,
            "body_type": body_type,
            "eye_color": eye_color,
            "hair_color": hair_color,
            "skin_color": skin_color,
            "skin_condition": skin_condition,
            "characteristics": characteristics,
            "perks": perks,
            "flaws": flaws,
            "special_traits": special_traits,
            "image": None
        }

        # Bild hochladen
        if character_image:
            character_data["image"] = character_image

        save_character_data(character_data)
        st.dataframe(st.session_state.df_characters)

# Funktion zum Bearbeiten eines vorhandenen Charakters
def edit_character():
    st.title("Charakter bearbeiten")
    characters = st.session_state.df_characters['name'].unique().tolist()
    selected_character = st.selectbox("Zu bearbeitenden Charakter auswählen", characters)

    st.subheader("Charaktereigenschaften bearbeiten")
    changed_data = st.data_editor(st.session_state.df_characters.loc[st.session_state.df_characters['name'] == selected_character])
    st.session_state.df_characters.loc[st.session_state.df_characters['name'] == selected_character] = changed_data
    if st.button("Änderungen speichern"):
        st.session_state.github.write_df(f"MyCharacterTable_{st.session_state.username}.csv", st.session_state.df_characters, "changed character")
        st.success("Character data saved successfully.")


# Funktion zum Laden der erstellten Charaktere
def load_characters():
    st.title("Charaktere laden")
    if st.session_state.df_characters is not None and not st.session_state.df_characters.empty:
        for _, character in st.session_state.df_characters.iterrows():
            st.write(f"Name: {character['name']}")
            if character['image'] and not pd.isna(character['image']) and is_valid_url(character['image']):
                st.image(character['image'])
            else:
                st.write(" -> Kein Bild für diesen Charakter verfügbar.")
    else:
        st.write("Noch keine Charaktere erstellt.")

def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

# Funktion zum Speichern der Charakterdaten
def save_character_data(character_data):
    new_entry = pd.DataFrame([character_data], columns=CHAR_COLUMNS)
    st.session_state.df_characters = pd.concat([st.session_state.df_characters, new_entry], ignore_index=True)
    st.session_state.github.write_df(f"MyCharacterTable_{st.session_state.username}.csv", st.session_state.df_characters, "added new character")
    st.success("Character data saved successfully.")


def main():
    init_github() # Initialize the GithubContents object
    init_credentials() # Loads the credentials from the Github data repository

    if 'authentication' not in st.session_state:
        st.session_state['authentication'] = False

    if not st.session_state['authentication']:
        st.image("logo.jpeg", width=200)
        st.title("Charakter-Logbuch")
        options = st.sidebar.selectbox("Select a page", ["Login", "Register"])
        if options == "Login":
            login_page()
        elif options == "Register":
            register_page()

    else:
        init_character_data()
        st.sidebar.title("Optionen")
        option = st.sidebar.selectbox("Option auswählen", ("Neuen Charakter erstellen", "Charakter bearbeiten", "Charaktere laden", "Abmelden"))

        if option == "Neuen Charakter erstellen":
            create_character()
        elif option == "Charakter bearbeiten":
            edit_character()
        elif option == "Charaktere laden":
            load_characters()
        elif option == "Abmelden":
            st.session_state['authentication'] = False
            st.rerun()


if __name__ == "__main__":
    main()
