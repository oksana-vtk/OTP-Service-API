import mysql.connector
from dotenv import load_dotenv
import os


# завантаження змінних з .env
load_dotenv()


# Підключення до бази даних
def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME_OTP")
    )


# 1. Вставляємо дані в таблицю users
# для API: input_tel_number()
def insert_into_users(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = "INSERT INTO users(user_tel_number, otp_code) VALUES (%s, %s)"
    mycursor.execute(sql, val)
    mydb.commit()

    mycursor.close()
    mydb.close()


# 2. Перевірка, чи існує otp_code в таблиці users
# для API: validate_otp_code()
def select_all_codes_for_user(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT otp_code " \
          " FROM users " \
          " WHERE user_tel_number = %s"

    mycursor.execute(sql, val)
    all_otp_codes_for_user = mycursor.fetchall()

    mycursor.close()
    mydb.close()

    for i in range(len(all_otp_codes_for_user)):
        a = all_otp_codes_for_user[i]
        (all_otp_codes_for_user[i],) = a  # unpack tuple

    return all_otp_codes_for_user


# 3. Пошук останнього згенерованого, але невикористаного otp кода для заданого користувача
# для API: validate_otp_code()
def find_last_generated_code(user_tel_number):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT otp_code " \
          " FROM users " \
          " WHERE user_tel_number = %s AND " \
          "       created_at = (SELECT created_at FROM users " \
          "                     WHERE user_tel_number = %s " \
          "                     ORDER BY created_at DESC " \
          "                     LIMIT 1) "
    val = (user_tel_number[0], user_tel_number[0])
    mycursor.execute(sql, val)

    otp_code = mycursor.fetchone() #type = tuple

    mycursor.close()
    mydb.close()

    a = otp_code
    (otp_code,) = a #unpack tuple

    return otp_code


# 3. Пошук останньої дати created_at для конкретного користувача
# для API: validate_otp_code()
def find_last_created_at(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT created_at " \
          " FROM users " \
          " WHERE user_tel_number = %s " \
          " ORDER BY created_at DESC " \
          " LIMIT 1 "

    mycursor.execute(sql, val)

    last_created_at = mycursor.fetchone() #type = tuple

    mycursor.close()
    mydb.close()

    a = last_created_at
    (last_created_at,) = a #unpack tuple

    return last_created_at


# 4. Перевірка, чи код вже було використано користувачем
# для API: validate_otp_code():
def check_already_validated_code(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = " SELECT otp_code " \
          " FROM users " \
          " WHERE user_tel_number = %s AND " \
          "       otp_code = %s AND " \
          "       validated = TRUE"

    mycursor.execute(sql, val)

    otp_code = mycursor.fetchone()  #type = tuple

    mycursor.close()
    mydb.close()

    if otp_code is None:
        pass
    else:
        a = otp_code
        (otp_code,) = a  #unpack tuple

    return otp_code


# 5. Пошук останнього згенерованого, але невикористаного otp кода для заданого користувача
# для API: validate_otp_code():
def find_last_unvalidated_code(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = f" SELECT otp_code " \
          f" FROM users " \
          f" WHERE user_tel_number = {val[0]} AND " \
          f"       validated = FALSE AND "\
          f"       created_at = (SELECT created_at FROM users " \
          f"                     WHERE user_tel_number = {val[0]} " \
          f"                     ORDER BY created_at DESC " \
          f"                     LIMIT 1) "

    mycursor.execute(sql)

    otp_code = mycursor.fetchone()  #type = tuple

    mycursor.close()
    mydb.close()

    if otp_code is None:
        pass
    else:
        a = otp_code
        (otp_code,) = a  #unpack tuple

    return otp_code


# 6. Зміна значення validated з FALSE на TRUE
# для API: validate_otp_code()
def change_validated_status(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = f"UPDATE users " \
          f"SET validated = TRUE, validated_at = current_timestamp() " \
          f"WHERE user_tel_number = {val[0]} AND otp_code = {val[1]}"

    mycursor.execute(sql)
    mydb.commit()

    mycursor.close()
    mydb.close()

    return val


# 7. Підрахунок кількості вже згенерованих кодів для конкретного користувача за останні 2 години
# для API: generate_otp_code():
def count_last_generated_codes(val):

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = f" SELECT COUNT(otp_code) " \
          f" FROM users " \
          f" WHERE user_tel_number = %s AND TIMESTAMPDIFF(HOUR, created_at, current_timestamp()) <= %s "

    mycursor.execute(sql, val)

    count_codes = mycursor.fetchone()  #type = tuple

    mycursor.close()
    mydb.close()

    a = count_codes
    (count_codes,) = a  #unpack tuple

    return count_codes


# 8. Всі унікальні номери телефонів
# для API: generate_otp_code():
def unique_tel_numbers():

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = f" SELECT DISTINCT user_tel_number " \
          f" FROM users " \

    mycursor.execute(sql)

    unique_tel = mycursor.fetchall()  #type = tuple

    for i in range(len(unique_tel)):
        a = unique_tel[i]
        (unique_tel[i],) = a  # unpack tuple

    mycursor.close()
    mydb.close()

    return unique_tel


# Для тестування
# для API: test():
def show_db():

    mydb = connect_to_db()
    mycursor = mydb.cursor()

    sql = f" SHOW  DATABASES"

    mycursor.execute(sql)

    count_codes = mycursor.fetchall()  #type = tuple

    mycursor.close()
    mydb.close()

    #a = count_codes
    #(count_codes,) = a  #unpack tuple

    print(count_codes)

    return count_codes


