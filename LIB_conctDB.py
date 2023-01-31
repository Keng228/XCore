import mysql.connector
from mysql.connector import connect, Error
import discord


#Работа с базой данных
class BDconect:
    def __init__(self):
        self.__host_name = "161.97.78.70"
        self.__user_name = "u11291_CvGCz7PpzF"
        self.__user_password = "8sBK32eWGxRyelX!Wel==5Pm"
        self.__db_name = "s11291_Warn"

    @property
    def host_name(self):
        return self.__host_name
    
    @host_name.setter
    def host_name(self, host_name):
        self.__host_name = host_name
    
    @property
    def user_name(self):
        return self.__user_name
    
    @user_name.setter
    def user_name(self, user_name):
        self.__user_name = user_name
    
    @property
    def user_password(self):
        return self.__user_password
    
    @user_password.setter
    def user_password(self, user_password):
        self.__user_password = user_password
    
    @property
    def db_name(self):
        return self.__db_name
    
    @db_name.setter
    def db_name(self, db_name):
        self.__db_name = db_name

class BDcomand:
    def __init__(self):
        self.__command = None
        self.__table = None
        self.__columns = list()
        self.__condition = list()
        self.__data = list()
        self.__addition = None
    
    @property
    def command(self):
        return self.__command
    
    @command.setter
    def command(self, command):
        self.__command = command
    
    @property
    def table(self):
        return self.__table
    
    @table.setter
    def table(self, table):
        self.__table = table
    
    @property
    def columns(self):
        return self.__columns
    
    @columns.setter
    def columns(self, columns):
        self.__columns = columns
    
    @property
    def condition(self):
        return self.__condition
    
    @condition.setter
    def condition(self, condition):
        self.__condition = condition
        
    @property
    def data(self):
        return self.__data
    
    @data.setter
    def data(self, data):
        self.__data = data
        
    @property
    def addition(self):
        return self.__addition
    
    @addition.setter
    def addition(self, addition):
        self.__addition = addition
        
    def clear(self):
        self.addition = None
        self.columns.clear()
        self.command = None
        self.condition.clear()
        self.data.clear()
        self.table = None

class BDwork:
    def __init__(self):
        self.__BDconnect = BDconect()
        self.__BDcommand = BDcomand()
        self.__port = None
        
    @property
    def BDconnect(self):
        return self.__BDconnect
    
    @BDconnect.setter
    def BDconnect(self):
        self.__BDconnect = BDconect()
        
    @property
    def BDcommand(self):
        return self.__BDcommand
    
    @BDcommand.setter
    def BDcommand(self):
        self.__BDcommand = BDcomand()
        
    @property
    def port(self):
        return self.__port
    
    @port.setter
    def port(self, BDconnect: BDconect):
        connection = None
        try:
            connection = connect(
                host=BDconnect.host_name,
                user=BDconnect.user_name,
                passwd=BDconnect.user_password,
                database=BDconnect.db_name
            )
            print("Все данные введены успешно!")
        except Error as e:
            print(f"Произошла ошибка '{e}'")
        
        connection.close()
        self.__port = connection
        
    def open_connect(self):
        self.port.connect()
        
    def connect(self):
        self.port = self.BDconnect
        
    def close_connect(self):
        self.port.close()
        
    def writeUserID(self, UserID):
        self.BDcommand.command = f"""
        SELECT ID
        FROM Users
        WHERE ID = {UserID}"""
        try:
            self.open_connect()
            with self.port.cursor() as cursor:
                cursor.execute(self.BDcommand.command)
                if str(cursor.fetchall()) == "[]":
                    self.BDcommand.command = f"""
                    INSERT INTO Users (ID)
                    VALUES ({UserID})"""
                    with self.port.cursor() as cursor:
                        cursor.execute(self.BDcommand.command)
                        self.port.commit()
        except Error as e:
            print(f"""Произошла ошибка:
            '{e}'
            ```{self.BDcommand.command}```""")
            
        self.close_connect()

    def writeMoney(self, user: discord.User):
        self.writeUserID(UserID=user.id)
        
        self.BDcommand.command = f"""
        SELECT Money
        FROM Money 
        WHERE UserID = {user.id}"""
        try:
            self.open_connect()
            cursor = self.port.cursor() 
            cursor.execute(self.BDcommand.command)
            obj = cursor.fetchall()
            self.close_connect()
        except Error as e:
            print(f"""
            Произошла ошибка:
            '{e}'
            ```{self.BDcommand.command}```""")

        if str(obj) == "[]":
            self.BDcommand.command = f"""
            INSERT INTO Money (UserID, Money)
            VALUES ({user.id}, 0)"""
        else:
            self.BDcommand.command = f"""
            UPDATE Money
            SET Money = Money + 0
            WHERE UserID = '{user.id}'"""
        try:
            self.open_connect()
            with self.port.cursor() as cursor:
                cursor.execute(self.BDcommand.command)
                self.port.commit()
                self.close_connect()
        except Error as e:
            print(f"""Произошла ошибка:
            '{e}'
            ```{self.BDcommand.command}```""")
    
    def bdinsert(self, more: bool = False):
        """Добавить данные в таблицу (more трогать, если нужно сделать несколько записей)"""
        result = None
        self.open_connect()
        try:
            #основная часть
            self.BDcommand.command = f"""INSERT INTO {self.BDcommand.table}"""
            self.BDcommand.command += " ("
            first = False
            count = 0
            for column in self.BDcommand.columns:
                if first == False:  
                    self.BDcommand.command += f"{column}"
                    first = True
                else:
                    self.BDcommand.command += f", {column}"
                count += 1
            first = False
            self.BDcommand.command += """)
            """
            #введение данных
            self.BDcommand.command += f"""VALUES ("""
            if more == True:
                #множественный запрос
                for column in self.BDcommand.columns:
                    if first == False:
                        self.BDcommand.command += "%s"
                        first = True
                    else:
                        self.BDcommand.command += ", %s"
                self.BDcommand.command += ")"
                #реализация запроса
                with self.port.cursor() as cursor:
                    cursor.executemany(self.BDcommand.command, self.BDcommand.data)
                    self.port.commit()
                result = True
            else:
                #единичный запрос
                for data in self.BDcommand.data:
                    if first == False:
                        self.BDcommand.command += f"{data}"
                        first = True
                    else:
                        self.BDcommand.command += f", {data}"
                self.BDcommand.command += ")"
                with self.port.cursor() as cursor:
                    cursor.execute(self.BDcommand.command)
                    self.port.commit()
                result = True
        except Error as e:
            result = str(e) + "!"
        self.close_connect()
        return result
    
    def bdselect(self):
        """Выбрать данные в таблице"""
        result = list()
        self.open_connect()
        try:
            #основная часть
            self.BDcommand.command = "SELECT"
            first = False
            if str(self.BDcommand.columns) == "[]":
                self.BDcommand.command += " *"
            else:
                for column in self.BDcommand.columns:
                    if first == False:  
                        self.BDcommand.command += f"""
                        {column}"""
                        first = True
                    else:
                        self.BDcommand.command += f"""
                        , {column}"""
            #откуда данные
            self.BDcommand.command += f""" FROM {self.BDcommand.table}
            """
            #условие
            if str(self.BDcommand.condition) != "[]":
                self.BDcommand.command += f"WHERE "
                for condit in self.BDcommand.condition:
                    self.BDcommand.command += f"{condit} "
            #допольнительно:
            if self.BDcommand.addition != None:
                self.BDcommand.command += f"""
                {self.BDcommand.addition}"""
            #реализация запроса
            with self.port.cursor() as cursor:
                cursor.execute(self.BDcommand.command)
                for data in cursor.fetchall():
                    result.append(data)
        except Error as e:
            result = str(e) + "!"
        self.close_connect()
        return result
    
    def bddelete(self):
        """Удалить данные из таблицы"""
        result = None
        self.open_connect()
        try:
            #основная часть
            self.BDcommand.command = f"""DELETE FROM {self.BDcommand.table}
            """
            #условие
            if str(self.BDcommand.condition) != "[]":
                self.BDcommand.command += f"WHERE "
                for condit in self.BDcommand.condition:
                    self.BDcommand.command += f"{condit} "
            #реализация запроса
            with self.port.cursor() as cursor:
                cursor.execute(self.BDcommand.command)
                self.port.commit()
            result = True
        except Error as e:
            result = str(e) + "!"
        self.close_connect()
        return result
        
    def bdupdate(self, more: bool = False):
        """Обновить данные в таблице (more трогать если несколько условий)"""
        result = None
        self.open_connect()
        try:
            #основная часть
            self.BDcommand.command = f"UPDATE {self.BDcommand.table}"
            #данные
            self.BDcommand.command += f" SET"
            i = 0
            first = False
            while i < len(self.BDcommand.columns):
                if first == False:
                    self.BDcommand.command += f" {self.BDcommand.columns[i]} {self.BDcommand.data[i]}"
                    first = True
                else:
                    self.BDcommand.command += f", {self.BDcommand.columns[i]} {self.BDcommand.data[i]}"
                i += 1
            #условие
            if str(self.BDcommand.condition) != "[]":
                self.BDcommand.command += f"""
                WHERE """
                for condit in self.BDcommand.condition:
                    self.BDcommand.command += f"{condit} "
            #реализация запроса
            if more == False:
                #одиночное обновление
                with self.port.cursor() as cursor:
                    cursor.execute(self.BDcommand.command)
                    self.port.commit()
            else:
                #множественное
                with self.port.cursor() as cursor:
                    cursor.execute(self.BDcommand.command, multi=True)
                    self.port.commit()
            result = True
        except Error as e:
            result = str(e) + "!"
        self.close_connect()
        return result
        
    def warns(self, user: discord.User):
        #стандартное начало
        Moderation.BDcommand.clear()
        
        Moderation.BDcommand.table = "ListWarns"
        Moderation.BDcommand.columns = ["UserID", "WarnTime", "Grade", "TextProtocol"]
        Moderation.BDcommand.condition.append(f"UserID = {user.id}")
        Moderation.BDcommand.addition = "ORDER BY ID"
        
        result = Moderation.bdselect()
        Moderation.BDcommand.clear()
        arrs = list()
        i = 0
        j = 0
        warns = list()
        Warn = ""
        for warns in result:
            i += 1
            arrs.append(warns)
        return arrs
        
Economy = BDwork()
Economy.connect()
Moderation = BDwork()
Moderation.connect()