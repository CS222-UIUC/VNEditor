from src.utils import DBManager

db = DBManager.DbManager("./test.db")
db.create_table_if_not_exist("memory")
db.close()
