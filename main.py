import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

file = "trade.csv"


def load_data():
    if not os.path.exists(file):
        df = pd.DataFrame(columns=["user_id", "Date", "Pair", "Lot", "Entry", "Exit", "Profit", "Note"])
        df.to_csv(file, index=False)
    else:
        df = pd.read_csv(file)

        # Au cas où ton ancien CSV n'a pas encore la colonne user_id
        if "user_id" not in df.columns:
            df["user_id"] = None

    return df


def add_trade_for_user(user_id, pair, lot, entry, exit_price, note):
    df = load_data()

    profit = (exit_price - entry) * lot * 100
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nouveau_trade = {
        "user_id": user_id,
        "Date": date,
        "Pair": pair,
        "Lot": lot,
        "Entry": entry,
        "Exit": exit_price,
        "Profit": profit,
        "Note": note
    }

    nouveau_trade_df = pd.DataFrame([nouveau_trade])

    if df.empty:
        df = nouveau_trade_df
    else:
        df = pd.concat([df, nouveau_trade_df], ignore_index=True)

    df.to_csv(file, index=False)
    return df


def get_user_trades(user_id):
    df = load_data()
    df = df.dropna(subset=["Profit"])
    return df[df["user_id"] == user_id]


def get_stats(user_id=None):
    df = load_data()
    df = df.dropna(subset=["Profit"])

    if user_id is not None:
        df = df[df["user_id"] == user_id]

    total_profit = df["Profit"].sum() if not df.empty else 0
    win_rate = (df["Profit"] > 0).mean() * 100 if not df.empty else 0
    profit_moyen = df["Profit"].mean() if not df.empty else 0
    cumulative_profit = df["Profit"].cumsum() if not df.empty else pd.Series(dtype=float)

    return df, total_profit, win_rate, profit_moyen, cumulative_profit


def terminal_app():
    # utilisateur test pour le terminal
    user_id = 1

    while True:
        pair = input("Pair (ex: XAUUSD): ")

        while True:
            lot = float(input("Lot: "))
            if lot <= 10:
                break
            print("Lot trop grand. Réessaie.")

        entry = float(input("Prix d'entrée: "))
        exit_price = float(input("Prix de sortie: "))
        note = input("Note (optionnel): ")

        df = add_trade_for_user(user_id, pair, lot, entry, exit_price, note)

        print("Trade ajouté !")
        continuer = input("Ajouter un autre trade ? (oui/non): ")
        if continuer.lower() != "oui":
            break

    df, total_profit, win_rate, profit_moyen, cumulative_profit = get_stats(user_id)

    print(df)
    print("Total profit :", total_profit)
    print("Win rate :", win_rate)
    print("Profit moyen :", profit_moyen)

    if not cumulative_profit.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(range(1, len(cumulative_profit) + 1), cumulative_profit, marker="o")
        plt.title("Profit cumulatif")
        plt.xlabel("Nombre de trades")
        plt.ylabel("Profit cumulatif")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    terminal_app()