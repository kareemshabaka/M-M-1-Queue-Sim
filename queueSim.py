import math
import pygame
import numpy as np
import pandas as pd

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode([1000, 1000])

class Simulation:
    def __init__(self,tellers,customers):
        self.queueLength = 0
        self.tellers = tellers
        self.numTellers = len(self.tellers)
        self.customers = customers
        self.nextArrival = 0
        self.beingServed = [None]*self.numTellers
        self.totalCustomers = 0
        self.customersT1 = 0
        self.customersT2 = 0
        
    def serve(self,customerID):
        tellerID=-1
        for teller in self.tellers:
            tellerID+=1
            if teller.state == 0:
                self.beingServed[tellerID]=customerID
                return True, tellerID
        return False, tellerID
        
    def arrival(self):
        self.queueLength+=1
        newCustomer = Customer(self.queueLength)
        self.customers.append(newCustomer)
        self.nextArrival = simtime + (-np.log(1-(np.random.uniform(low=0.0,high=1.0))) * 3)*3


    def departure(self,tellerID):
        finishedCustomer = self.beingServed[tellerID]
        self.customers.remove(finishedCustomer)
        self.beingServed[tellerID]=None
        del finishedCustomer
        
    def move(self):
        for customer in self.customers:
            if customer.queueLocation != 0:
                customer.queueLocation-=1


    def draw(self,display):
        
        pygame.draw.rect(display,(0,0,0),(540,150,15,600))
        pygame.draw.rect(display,(0,0,0),(540,150,200,15))

        pygame.draw.rect(display,(0,0,0),(640,250,15,500))

    def UI(self,display):
        pass

class Teller():
    def __init__(self, multiplier,tellerID):
        self.state = 0
        self.multiplier = multiplier
        self.delay = 0
        self.finishService = 0
        self.tellerID = tellerID
        

    def tellerDepartureTime(self):                               
        self.delay = (-np.log(1-(np.random.uniform(low=0.0,high=1.0)))*self.multiplier)
        print(self.delay)
        self.finishService = simtime + self.delay
        self.state=1

    def draw(self,display):
        if self.state == 1:
            pygame.draw.rect(display,(252,10,10),(800,200+100*self.tellerID,50,50))
        else:
            pygame.draw.rect(display,(26, 219, 4),(800,200+100*self.tellerID,50,50))


class Customer():
    def __init__(self, location):
        #self.pacience = 0
        self.queueLocation = location
        self.isServed = 0
        self.startTime = simtime
    
    def draw(self,display):
        pygame.draw.rect(display,(13,46,242),(572,180+60*self.queueLocation,50,50))
     

def main():
    running = True

    teller1 = Teller(1.5,0)
    teller2 = Teller(1.3,1)

    global simtime
    simtime = 0
    sim = Simulation([teller1,teller2], [])

    while running:
        clock.tick(10)
        if sim.nextArrival <= simtime: #new customers arrive
            sim.arrival()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        
        sim.draw(screen)

        if (simtime%1==0):
            sim.move()
            for customer in sim.customers:
                
                if customer.queueLocation == 0 and customer.isServed==0:
                    result,id = sim.serve(customer)
                    if result==True:
                        customer.isServed=1
                        sim.tellers[id].tellerDepartureTime()
                        sim.queueLength-=1
            for teller in sim.tellers:
                if teller.finishService <= simtime and teller.state==1:
                    sim.departure(teller.tellerID)
                    teller.state=0

        for customer in sim.customers:
            customer.draw(screen)

        for teller in sim.tellers:
            teller.draw(screen)

        pygame.display.update()

    
        #print(len(sim.customers))
        simtime+=1        


    
    pygame.quit()
main()