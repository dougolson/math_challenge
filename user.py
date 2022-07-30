import sqlite3

class User:
    def __init__(self, id: int, user_name: str) -> None:
        self.id = id
        self.user_name = user_name
    
    def display_user(self) ->None:
        print(f"{self.id} - {self.user_name}")
    
    def print_user_info(self) ->None:
        print("User")
        print(f"  id        : {self.id}")
        print(f"  user_name : {self.user_name}")

def get_users()->list[User]:
    query = '''
    SELECT id, user_name from users
    '''
    with (sqlite3.connect('math_challenge.db')) as con:
        cur = con.cursor()
        cur.execute(query)
        data = cur.fetchall()
        result = [User(*x) for x in data]
        return result
    

if __name__ == '__main__':
    users = get_users()
    for user in users:
        user.print_user_info()