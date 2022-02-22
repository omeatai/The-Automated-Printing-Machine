# The entry point of your application
from assets.art import logo
from data.data import FORMAT,resources

class Printer(): 
    def __init__(self):
        self.ink = resources['ink']
        self.paper = resources['paper']
        self.profit = resources['profit']

    def show_status(self):
        return f"paper: {self.paper}pc\nink: {self.ink}ml\nprofit: ${self.profit}"
        
class Logistics(Printer):      
    def __init__(self):
        super().__init__() 
        self.c_ink = FORMAT['coloured']['materials']['ink']
        self.c_paper = FORMAT['coloured']['materials']['paper']
        self.c_price = FORMAT['coloured']['price']
        self.g_ink = FORMAT['greyscale']['materials']['ink']
        self.g_paper = FORMAT['greyscale']['materials']['paper']
        self.g_price = FORMAT['greyscale']['price']
        
    def paper_is_enough(self,nums):
        if nums > self.paper:
            print('Sorry there is not enough paper.')
            print('Try Again...')
            return False
        return True
    
    def ink_is_enough(self,nums,type):
        ink_ml = 0
        if type == 'coloured':
            ink_ml = self.c_ink
        elif type == 'grayscale':
            ink_ml = self.g_ink        
        if nums * ink_ml > self.ink:
            print('Sorry there is not enough ink.')
            print('Try Again...')  
            return False    
        return True 
    
    def update_units(self,tcost,nums,type):
        self.profit = resources['profit'] + tcost
        self.paper = resources['paper'] - nums
        ink_ml = 0
        if type == 'coloured':
            ink_ml = self.c_ink
        elif type == 'grayscale':
            ink_ml = self.g_ink 
        t_ink = nums*ink_ml  
        self.ink = resources['ink'] - t_ink  

class Charge(Logistics):
    def __init__(self):
        super().__init__() 
        self.penny = 0.01
        self.nickel = 0.05
        self.dime = 0.10
        self.quarter = 0.25  
    
    def get_cost(self,nums,type):
        price = 0
        if type == 'coloured':
            price = self.c_price
        elif type == 'grayscale':
            price = self.g_price
        tprice = price * nums 
        print(f"Your price is ${tprice:.2f}.") 
        return tprice   
    
    def reply(self,tcost,nums,type):
        print("Here is your Project. Thank you for using our services.")            
        self.update_units(tcost,nums,type)
        print('Printing Report...')
        print(self.show_status()) 
        print("\nPrint Again: ")     
    
    def receive_coins(self,tcost,nums,type): 
        try:
            quarters = int(input("Enter the quantity of Quarters to pay (1 Quarter = $0.25): ") or 0)
            dimes = int(input("Enter the quantity of Dimes to pay (1 Dime = $0.10): ") or 0)
            nickels = int(input("Enter the quantity of Nickels to pay (1 Nickel = $0.05): ") or 0)
            pennys = int(input("Enter the quantity of Pennys to pay (1 Penny = $0.01): ") or 0)
        except ValueError:
            print("Enter only number values with no spaces...Try Again!")   
            return True 
        else:    
            tpaid = (quarters*self.quarter) + (dimes*self.dime) + (nickels*self.nickel) + (pennys*self.penny)
            print(f"You entered a total of: ${tpaid:.2f} out of ${tcost}.")
            if tpaid < tcost:
                print("Sorry that's not enough coins. Coins refunded.") 
                print("Try Again...")           
            elif tpaid ==  tcost:
                self.reply(tcost,nums,type)       
            else:
                print(f"Here is ${tpaid - tcost} in change.")
                self.reply(tcost,nums,type) 
            return True   
class Processing(Charge):
    def __init__(self):
        super().__init__()  
    
    def process(self,type):
        try:
            nums = int(input("How many pages would you like to print?: ") or 1) 
        except ValueError:
            print("Enter only number values with no spaces...Try Again!")   
            return True 
        else:    
            if not self.paper_is_enough(nums):
                return True
            if not self.ink_is_enough(nums,type):
                return True
            tcost = self.get_cost(nums,type)
            if not self.receive_coins(tcost,nums,type):
                return False
            return True

class Power(Processing):
    def __init__(self):
        super().__init__()
        
    def start(self):  
        print(logo)  
        ON = True
        while ON:
            mode = input("What format would you like? (c = coloured or g = grayscale): ")
            if (mode.lower() == 'off'):
                ON = False
                print('Switching Off...')
                break
            elif (mode.lower() == 'report'):
                print('Printing Report...') 
                print(self.show_status())                
            elif (mode.lower() == 'c'):
                if not self.process('coloured'):
                    ON = False
                    break  
            elif (mode.lower() == 'g'):
                if not self.process('grayscale'):
                    ON = False
                    break    
            else:
                print("Enter only 'c' = coloured or 'g' = grayscale...Try again!")     
                
power_ON = Power()
power_ON.start()