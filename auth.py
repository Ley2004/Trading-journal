import pandas as pd
import os
from pandas.errors import EmptyDataError
users_file = "users.csv"

#crée users.csv s’il n’existe pas puis le lit
def load_users():
    columns = ["id", "username", "password"]

    if not os.path.exists(users_file):
        df = pd.DataFrame(columns=columns)
        df.to_csv(users_file, index=False)
        return df

    # si le fichier existe mais est vide
    if os.path.getsize(users_file) == 0:
        df = pd.DataFrame(columns=columns)
        df.to_csv(users_file, index=False)
        return df

    try:
        df = pd.read_csv(users_file)
    except EmptyDataError:
        df = pd.DataFrame(columns=columns)
        df.to_csv(users_file, index=False)
    # forcer username et password en texte
    df["username"] = df["username"].astype(str).str.strip()
    df["password"] = df["password"].astype(str).str.strip()
    return df


def save_users(df):
    df.to_csv(users_file, index=False)


def user_exists(username):
    df = load_users()
    return username in df["username"].values


def register_user(username, password):
    df = load_users()

    username = username.strip()
    password = password.strip()

    if username == "" or password == "":
        return False, "Nom d'utilisateur ou mot de passe vide."

    if user_exists(username):
        return False, "Ce nom d'utilisateur existe déjà."

    if df.empty:
        new_id = 1
    else:
        new_id = int(df["id"].max()) + 1

    new_user = {
        "id": new_id,
        "username": username,
        "password": password
    }

    new_user_df = pd.DataFrame([new_user])

    if df.empty:
        df = new_user_df
    else:
        df = pd.concat([df, new_user_df], ignore_index=True)

    save_users(df)
    return True, "Compte créé avec succès."


def login_user(username, password):
    df = load_users()

    username = username.strip()
    password = password.strip()

    user = df[(df["username"] == username) & (df["password"] == password)]

    if user.empty:
        return None

    return user.iloc[0].to_dict()