#WORK IN PROGRESS!#
#To do:#
#no code for cities# 

class Army:
    """
    Armies 'live' in two places:
    owner.armies[]: a list, armies have to be removed or added to that list
    Tile.army: an object, hast to be set to None when removed
    Also, Tile ownership has to be set accordingly in Tile.owner     
    """
    def __init__(self,Tile,owner,MAO,units,ignore6=False,unit_type='warrior'): #MAO is the instance of our MyApp we are running (MAO=MyAppObject) and is used to call the RenderTile method
        """

        """
        if units<=0: 
            print "Can't create army: units <= 0!"
            return
        if ignore6==False and Tile.value==6: 
            print "Can't create army: Impassable Terrain!"
            return
        if Tile.owner!=owner and Tile.owner!=None:
            print "Can't create army: tile belongs to another player!"
            return
        self.unit_type=unit_type
        self.units=units
        self.owner=owner
        self.tile=Tile  
        self.MP = 1
        self.MAO=MAO
        
        self.create()      
        
        
    def create(self):        
        """
        If army already exists on Tile, just add units to it
        If Tile is empty create a new army and change self.tile.army, self.owner.armies, self.tile.owner accordingly        
        """       
        try:
            self.tile.army.units=self.tile.army.units+self.units           
        except:
            self.tile.army=self
            self.owner.armies.append(self)
            self.tile.owner = self.owner
        
        self.MAO.tile_renderer(self.tile)           
    
    def move(self,destTile,units='all'):
        """
        add documentation
        """
        #self.tile will later be the same as desTile, so to preserve self.Tile for rendering make temporary copy
        tmp_Tile=self.tile
        
        if units<=0:
            print "Can't move army: units to be moved <= 0."
            return
        
        if destTile.value==6: 
            print "Can't move army: Impassable Terrain!"
            return
        
        if units=='all' or units>=self.units:
            newArmy=False 
            units=self.units
        else:
            #Army will be splitted, so original army still exists, with fewer units, and a new army has to be created on the destination Tile     
            newArmy=True
        
        if destTile.owner!= self.owner and destTile.owner!=None:
            self.battle(destTile,units)
            return     
        
        if destTile.city != None and destTile.owner != self.owner:
            print "Can't move army: City combat not yet implemented!"
           
        else:
            try:
                #if there is already an own army on the destination Tile, units are transferred. If all units are transferred the original army will later be destroyed
                destTile.army.units=destTile.army.units+units 
                self.units=self.units-units
            except:
                if newArmy==False:
                    destTile.army=self 
                    destTile.owner=self.owner 
                    self.tile.army = None 
                    self.tile.owner = None 
                    self.tile = destTile
                if newArmy==True:
                    Army(Tile=destTile,owner=self.owner,MAO=self.MAO,units=units)
                    self.units=self.units-units              
                 
        if self.units<=0:
            self.destroy()
        
        self.MAO.tile_renderer(tmp_Tile)
        self.MAO.tile_renderer(destTile)
            
    def destroy(self):
        #print "Army destroyed on Tile %s %s" %(self.tile.x,self.tile.y)
        self.owner.armies.remove(self.tile.army)               
        self.tile.army=None
        self.tile.owner = None
        self.MAO.tile_renderer(self.tile)

    def battle(self,destTile,units):
        """
        add documentation
        """
        tmp_tile=self.tile
        tmp_destTile=destTile

        print "Battle for tile %s %s !"%(destTile.x,destTile.y)

        attackerUnits = units
        defenderUnits = destTile.army.units
        attacker = self.owner.color
        defender = destTile.owner.color
        
        defenderArmor = destTile.value

        print attacker + " has " + str(attackerUnits) + " units against " + defender + "\'s " + str(defenderUnits) + " units"
        print defender + " fights on " + str(defenderArmor)

        if attackerUnits < defenderUnits + defenderArmor:
            # if attacker has less units than defender+TV he looses all his attacking units
            self.units=self.units-attackerUnits
        else:
            # if attacker has equal or more units than defender he looses units
            # equal to the amount of defending units+TV
            self.units=self.units-(defenderUnits+defenderArmor)
        
        #defender looses units equal to the attacking units minus defenderArmor
        #<=0 check necessary, or (attackerUnits - defenderArmor) below will evalute to a positive number, increasing the defenders units
        if attackerUnits-defenderArmor<=0: pass
        else: destTile.army.units=destTile.army.units-(attackerUnits - defenderArmor)

        #if one of the armies has less or equal to zero units, destroy it
        if self.units <=0 and destTile.army.units<=0:
            print "Mutual Destruction! Both players loose all their units!"
            self.destroy()
            destTile.army.destroy()        
        elif self.units <=0:
            print "%s defends [%s,%s] succesfully against %s's %s units and has %s units left!"%(defender,destTile.x, destTile.y,attacker, attackerUnits, destTile.army.units)            
            self.destroy()
        elif destTile.army.units<=0: 
            print "%s attacks succesfully with %s against %s's %s units and moves with %s units onto %s %s!"%(attacker,attackerUnits,defender, defenderUnits,attackerUnits-(defenderUnits+defenderArmor),destTile.x, destTile.y)
            destTile.army.destroy()
            self.move(destTile,attackerUnits-(defenderUnits+defenderArmor))
        else:
            print "Impasse! %s has %s units left, %s has %s units left!"%(attacker,self.units,defender,destTile.army.units)
        
        self.MAO.tile_renderer(tmp_tile)
        self.MAO.tile_renderer(tmp_destTile)
