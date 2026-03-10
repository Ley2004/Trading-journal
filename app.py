import streamlit as st
import auth
import main

st.title("Journal de Trading")

# session utilisateur
if "user" not in st.session_state:
    st.session_state.user = None

menu = st.sidebar.selectbox("Menu", ["Connexion", "Créer un compte", "Journal"])

# -------------------------
# CRÉER UN COMPTE
# -------------------------
if menu == "Créer un compte":
    st.subheader("Créer un compte")

    new_username = st.text_input("Nom d'utilisateur")
    new_password = st.text_input("Mot de passe", type="password")

    if st.button("Créer le compte"):
        success, message = auth.register_user(new_username, new_password)

        if success:
            st.success(message)
        else:
            st.error(message)

# -------------------------
# CONNEXION
# -------------------------
elif menu == "Connexion":
    st.subheader("Connexion")

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        user = auth.login_user(username, password)

        if user is not None:
            st.session_state.user = user
            st.success(f"Bienvenue {user['username']}")
        else:
            st.error("Identifiants incorrects")

# -------------------------
# JOURNAL
# -------------------------
elif menu == "Journal":
    if st.session_state.user is None:
        st.warning("Connecte-toi d'abord.")
    else:
        user = st.session_state.user

        st.subheader(f"Journal de {user['username']}")

        pair = st.text_input("Pair", value="XAUUSD")
        lot = st.number_input("Lot", min_value=0.01, value=0.09)
        entry = st.number_input("Prix d'entrée", value=0.0)
        exit_price = st.number_input("Prix de sortie", value=0.0)
        note = st.text_input("Note")

        if st.button("Ajouter trade"):
            main.add_trade_for_user(
                user_id=user["id"],
                pair=pair,
                lot=lot,
                entry=entry,
                exit_price=exit_price,
                note=note
            )
            st.success("Trade ajouté !")

        user_trades = main.get_user_trades(user["id"])
        st.subheader("Historique des trades")
        st.dataframe(user_trades)