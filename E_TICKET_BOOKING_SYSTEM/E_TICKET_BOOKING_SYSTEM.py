#Validation
def Get_Booking_ID(Event_id):
    get_Booking_ID_No="SELECT BOOKING_ID_NO FROM BOOKING_TABLE WHERE EVENT_ID=?"
    for i in cur.execute(get_Booking_ID_No,(Event_id,)):
        print("[Booking Successful! Your Booking ID is : ",i[0],"]")


def check_Ticket_Available(Event_id,Ticket_No):
    get_ticket_no_data=Find_Total_Seats(Event_id)
    if(get_ticket_no_data[0]<Ticket_No):
        print("Insufficient amount of tickets!")
        return False
    else:
        return True

def User_choice():
    Start=input("Want to book (Yes/No) : ")
    Start=Start.lower()
    if(Start=="yes"):
        return True
    else:
        return False

def Find_ticket_cost(Event_id):
    global cur
    get_data="SELECT TICKET_PRICE FROM EVENT_TABLE WHERE EVENT_ID_NO=?"
    price=cur.execute(get_data,(Event_id,))
    whole_price=0
    for i in price:
        String_price=str(i)
        i=String_price[1:(len(String_price)-3)]
        whole_price=float(i[2:])
    return whole_price    

def update_Event_Table(Ticket_No, Event_id):
    global cur
    
    # 1. Get the tuple from your function (Example: (50,))
    seat_tuple = Find_Total_Seats(Event_id)
    
    # 2. Get the integer number at index 0 (Example: 50)
    total_seats = seat_tuple[0]
    
    # 3. Do the math
    Current_Seats = total_seats - Ticket_No
    
    # 4. Update the database using a simple tuple at the end
    cur.execute(
        "UPDATE EVENT_TABLE SET TOTAL_SEATS = ? WHERE EVENT_ID_NO = ?", 
        (Current_Seats, Event_id)
    )


def Find_Total_Seats(Event_id):
    global cur
    get_seats="SELECT TOTAL_SEATS FROM EVENT_TABLE WHERE EVENT_ID_NO=?"
    for i in cur.execute(get_seats,(Event_id,)):
        return i


def Delete_row(Event_id):
    global cur
    cur.execute("DELETE FROM EVENT_TABLE WHERE EVENT_ID_NO=?",(Event_id,))

def Welcome_presentation():
    print("*** WELCOME TO THE E-TICKET SYSTEM ***")

def print_Events(j):
    global cur
    get_data="SELECT * FROM EVENT_TABLE WHERE EVENT_ID_NO=?"
    for i in cur.execute(get_data,(j,)):
        print(i)

def Check_Available_movies():
    global cur
    get_dual_data="SELECT TOTAL_SEATS,EVENT_ID_NO FROM EVENT_TABLE"
    cur.execute(get_dual_data)
    all_movies = cur.fetchall()
    for i in all_movies:
        if(i[0]>0):
            print_Events(i[1])
        else:
            Delete_row(i[1])    

import sqlite3

conn=sqlite3.connect("Booking.db")
cur=conn.cursor()
Event_table='''CREATE TABLE IF NOT EXISTS EVENT_TABLE
(EVENT_ID_NO INTEGER PRIMARY KEY AUTOINCREMENT,
EVENT_NAME VARCHAR(255) NOT NULL,
TOTAL_SEATS INTEGER NOT NULL,
TICKET_PRICE VARCHAR(50) NOT NULL)'''

cur.execute(Event_table)

Booking_table='''CREATE TABLE  IF NOT EXISTS BOOKING_TABLE
(BOOKING_ID_NO INTEGER PRIMARY KEY AUTOINCREMENT,
CUSTOMER_NAME VARCHAR(255) NOT NULL,
EVENT_ID INTEGER NOT NULL,
SEATS_BOOKED INTEGER NOT NULL,
TOTAL_COST VARCHAR(50) NOT NULL)'''

cur.execute(Booking_table)

Events='''INSERT INTO EVENT_TABLE
(EVENT_NAME,TOTAL_SEATS,TICKET_PRICE)
VALUES
('PSYCHO_PASS','40','$50.00'),
('PLUTO','25','$25.00'),
('BHOOTNATH','430','$12.00'),
('FARADISE','250','$45.00')'''
#cur.execute(Events)

Welcome_presentation()
#Printing the availibity movie
print("Available Events Today:")
Check_Available_movies()
print("\n")
#Asking the customer for booking
Customer_name=input("Enter your name : ")
booking='''INSERT INTO BOOKING_TABLE
(CUSTOMER_NAME,EVENT_ID,SEATS_BOOKED,TOTAL_COST)
VALUES
(?,?,?,?)'''
will_update=True
while True:
    if(User_choice()==False):
        is_booked=False
        break
    else:
        is_booked=True
    Event_id=int(input("Which Event id you want to book? "))
    Ticket_No=int(input("How many tickets? "))
    if(check_Ticket_Available(Event_id,Ticket_No)==False):
        will_update=False
        break
    Total_cost=Ticket_No*Find_ticket_cost(Event_id)
    print("Total price : $",Total_cost)
    confirm=input("Do you want to confirm booking? (Yes/No) : ")
    confirm=confirm.lower()
    if(confirm=="yes"):
        t=(Customer_name,Event_id,Ticket_No,Total_cost)
        cur.execute(booking,t)
        Get_Booking_ID(Event_id)
        break
    
if(is_booked==True and will_update==True):
    update_Event_Table(Ticket_No,Event_id)


conn.commit()
cur.close()
conn.close()    
