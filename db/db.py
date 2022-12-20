import sqlite3 
from aiogram import types
from datetime import datetime as dt

con = sqlite3.connect("db/database.sqlite3")
cur = con.cursor()

CATEGORIES = {"такси": 1,
              "продукты": 2,
              "развлечения": 3,
              "бензин": 4,
              "услуги": 5,}

def get_categories() -> list[str]:
    answ = list()
    for category in CATEGORIES:
        answ.append(f"•{category.capitalize()}")
    return answ

def add_expence(expense: types.Message) -> str:
    message = _parse_expense(expense.text)
    if message:
        cur.execute(f"""INSERT INTO expenses (category_id, user_id, time, amount)
                        VALUES ({CATEGORIES[message[1]]}, {expense.from_id}, DATETIME(), {message[0]})""")
        con.commit()
        return "Трата успешно добавлена!"
    return "В вашем запросе ошибка"
    
def _parse_expense(expense: str) -> tuple[float, int]:
    expense = expense.split()
    if len(expense) < 2 or len(expense) > 2:
        return False 
    elif not expense[0].isnumeric() or expense[1].lower() not in CATEGORIES:
        return False 
    else:
        return expense[0], expense[1].lower()
    
def expenses_today(from_id: int) -> str:
    date = f"%{dt.now().month}-{dt.now().day} %"
    res = [0 for i in range(len(CATEGORIES))]
    for i in range(1, len(CATEGORIES) + 1):
        expenses = cur.execute(f'''SELECT * FROM expenses 
                                   WHERE time LIKE "{date}" and category_id = {i}''').fetchall()
        for expense in expenses:
            res[i - 1] += expense[-1]
    for i, cat in enumerate(CATEGORIES):
        res[i] = f"{cat.capitalize()}: {res[i]}"        
    
    return "\n".join(res)
        
def last_expenses(from_id: int) -> str:
    RCATEGORIES = dict((v, k) for k, v in CATEGORIES.items())
    expenses = cur.execute(f'''SELECT id, category_id, amount FROM expenses
                               WHERE user_id = {from_id} ORDER BY id DESC LIMIT 5''').fetchall()
    res = [f"{RCATEGORIES[expense[1]].capitalize()}: {expense[2]}\nУдалить: /del{expense[0]}\n" for expense in expenses]
    return "\n".join(res)

def delete_expense(message: types.Message) -> str:
    id = message.text[4:]
    try:
        from_id = cur.execute(f'''SELECT user_id FROM expenses 
                                  WHERE id = {id}''').fetchall()[0][0]
    except:
        return "Вы ошиблись в запросе"
    
    if from_id == message.from_id:
        cur.execute(f'''DELETE FROM expenses WHERE id = {id}''')
        con.commit()
        return "Трата удалена"
    return "Вы не имеете права удалять чужие траты"

def month_expenses(from_id: int) -> str:
    res = [0 for i in range(len(CATEGORIES))]
    expenses = cur.execute(f'''SELECT category_id, amount FROM expenses
                               WHERE user_id = {from_id} AND time LIKE "%-{dt.now().month}-%"
                               ORDER BY category_id DESC''').fetchall()

    for expense in expenses:
        res[expense[0] - 1] += expense[1]
    
    for i, cat in enumerate(CATEGORIES):
        res[i] = f"{cat.capitalize()}: {res[i]}"
    
    return "Ваша статистика за месяц:\n\n" + "\n".join(res)
    
        