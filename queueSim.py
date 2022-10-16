import math
import pygame
import numpy as np
import pandas as pd
from numpy.random import default_rng

clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode([1000, 1000])

pygame.freetype.init()

titleFont = pygame.font.SysFont("arial", 40)
bodyFont = pygame.font.SysFont("arial", 30)
class Simulation:
    def __init__(self,tellers,customers,multiplier=40):
        self.queueLength = 0
        self.tellers = tellers
        self.numTellers = len(self.tellers)
        self.customers = customers
        self.nextArrival = 0
        self.beingServed = [None]*self.numTellers
        self.multiplier=multiplier
        self.totalCustomers = 0
        self.customersPerTeller=[0]*self.numTellers
        
        self.buttons = []

        self.arrivalTime = titleFont.render("Arrival Time: {}".format(str(self.multiplier)), True, (0, 0, 0))
        self.increaseTellers = titleFont.render("Number of Tellers", True, (0, 0, 0))
        self.tellerTime = titleFont.render("Teller Processing Time ", True, (0, 0, 0))
    def serve(self,customerID):
        tellerID=-1
        for teller in self.tellers:
            tellerID+=1
            if teller.state == 0:
                self.beingServed[tellerID]=customerID
                customerID.assignedTeller=tellerID
                self.customersPerTeller[tellerID]+=1
                self.totalCustomers+=1
                return True, tellerID
        return False, tellerID
        
    def arrival(self):
        if self.multiplier<=0:
            self.multiplier==0.1   
        self.queueLength+=1
        newCustomer = Customer(self.queueLength)
        self.customers.append(newCustomer)
        self.nextArrival = simtime + (-np.log(1-(np.random.uniform(low=0.0,high=1.0)))/self.multiplier*60*60)
        print(self.nextArrival)


    def departure(self,tellerID):
        finishedCustomer = self.beingServed[tellerID]
        self.customers.remove(finishedCustomer)
        self.beingServed[tellerID]=None
        del finishedCustomer
        
    def move(self):
        for customer in self.customers:
            if customer.queueLocation != 1:
                customer.queueLocation-=1


    def draw(self,display):
        
        pygame.draw.rect(display,(0,0,0),(540,150,15,600))
        pygame.draw.rect(display,(0,0,0),(540,150,200,15))

        pygame.draw.rect(display,(0,0,0),(640,250,15,500))

    def UI(self,display):
        self.tCustomers = titleFont.render("Total Customers:", True, (0, 0, 0))
        display.blit(self.tCustomers,(20, 100))
        self.tCustomersAnswer = titleFont.render(str(self.totalCustomers), True, (0, 0, 0))
        display.blit(self.tCustomersAnswer,(400 , 100 ))

        self.teller1 = titleFont.render("Customers to Teller 1:", True, (0, 0, 0))
        display.blit(self.teller1,(20, 160 ))
        self.t1Answer = titleFont.render(str(self.customersPerTeller[0]), True, (0, 0, 0))
        display.blit(self.t1Answer,(400, 160))

        self.teller2 = titleFont.render("Customers to Teller 2:", True, (0, 0, 0))
        display.blit(self.teller2,(20, 220 ))
        self.t2Answer = titleFont.render(str(self.customersPerTeller[1]), True, (0, 0, 0))
        display.blit(self.t2Answer,(400 , 220 ))

        self.qL = titleFont.render("Queue Length: {0}".format(str(self.queueLength)), True, (0,0,0))
        display.blit(self.qL,(520,100))

        self.arrivalTime = titleFont.render("Arrivals per hour: {}".format(str(self.multiplier)), True, (0, 0, 0))
        display.blit(self.arrivalTime,(60, 400 ))
        display.blit(self.increaseTellers,(60 , 460 ))
        display.blit(self.tellerTime,(60, 520 ))

        self.timePassed = titleFont.render("Time: {0}s".format(str(simtime)), True, (0,0,0))
        display.blit(self.timePassed,(800,5))
        


class Teller():
    def __init__(self, multiplier,tellerID):
        self.state = 0
        self.multiplier = multiplier
        self.delay = 0
        self.finishService = 0
        self.tellerID = tellerID
        

    def tellerDepartureTime(self):
        if self.multiplier<=0:
            self.multiplier==0             

        rg = default_rng()
        rg.poisson(5)              
        self.delay = (-np.log(1-(np.random.uniform(low=0.0,high=1.0)))*self.multiplier)*45
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
        self.assignedTeller=-1
        self.startTime = simtime
        self.ready = 0
        self.inPosition = 0
        self.x = 572
        self.y = 750
    
    def draw(self,display):
        self.object = pygame.draw.rect(display,(13,46,242),(self.x,self.y,50,50))

    
    def update(self,sim,teller=-1):
        if teller==-1:
            if self.y >= 130+self.queueLocation*70:
                self.y -=20
            elif self.y<=210:
                self.ready = 1
        elif teller==0:
            if self.x <= 700:
                self.x+=20
            else:
                if self.isServed==1:
                    sim.tellers[self.assignedTeller].tellerDepartureTime()
                    sim.queueLength-=1
                    sim.move()
                    self.isServed+=1
        elif teller==1:
            if self.x<=650:
                self.x+=20
            elif self.y<=320:
                self.y+=20
            elif self.x<=700:
                self.x+=20
            else:
                if self.isServed==1:
                    sim.tellers[self.assignedTeller].tellerDepartureTime()
                    sim.queueLength-=1
                    sim.move()
                    self.isServed+=1
            

class Button():
    def __init__(self,text,pos,use):
        self.x,self.y=pos        
        self.use=use
        self.text = titleFont.render(text, 1, pygame.Color("red"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill("white")
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def draw(self):
        screen.blit(self.surface, (self.x, self.y))

def main():
    running = True

    teller1 = Teller(1.5,0)
    teller2 = Teller(1.3,1)

    global simtime
    simtime = 0
    sim = Simulation([teller1,teller2], [])

    arrivalm = Button("-",(35, 400),"decreaseAT")
    arrivalp = Button("+",(sim.arrivalTime.get_size()[0]+170, 400),"increaseAT")
    
    ntellerm = Button("-",(35, 460),"decreaseTeller")
    ntellerp = Button("+",(sim.increaseTellers.get_size()[0]+70, 460),"increaseTeller")

    tellertimem = Button("-",(35, 520),"decreaseTT")
    tellertimep = Button("+",(sim.tellerTime.get_size()[0]+70, 520),"increaseTT")

    sim.buttons = [arrivalm,arrivalp,ntellerm,ntellerp,tellertimem,tellertimep]

    while running:
        clock.tick(60)       
        if sim.nextArrival <= simtime: #new customers arrive
           sim.arrival()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                #print(x,y)
                for button in sim.buttons:
                    if button.rect.collidepoint(x, y):
                        #button.click()
                        if button.use == "decreaseAT":
                            sim.multiplier-=0.5
                        if button.use == "increaseAT":
                            sim.multiplier+=0.5
                        if button.use == "decreaseTT":
                            for teller in sim.tellers:
                                teller.multiplier-=0.3
                        if button.use == "increaseTT":
                            for teller in sim.tellers:
                                teller.multiplier+=0.3
        screen.fill((255, 255, 255))
        
        sim.draw(screen)
    
        sim.UI(screen)

        for button in sim.buttons:
            button.draw()
        if (simtime%1==0):
            for customer in sim.customers:
                if customer.queueLocation == 1 and customer.isServed==0 and customer.ready==1:
                    result,id = sim.serve(customer)
                    if result==True:
                        customer.isServed=1
            for teller in sim.tellers:
                if teller.finishService <= simtime and teller.state==1:
                    teller.state=0
                    sim.departure(teller.tellerID)
            
            
        for customer in sim.customers:
            customer.update(sim,customer.assignedTeller)
            customer.draw(screen)

        for teller in sim.tellers:
            teller.draw(screen)

        pygame.display.update()
        simtime+=1        
    pygame.quit()
main()