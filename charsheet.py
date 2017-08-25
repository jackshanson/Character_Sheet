#!/usr/bin/python
'''
CHARSHEET.PY V0.0
Attempting to make new thing that will make it easier to analyse the stats, 
inventory, health, ANYTHING, etc, for your DnD character
'''


import os, sys
import itertools, numpy as np
import kivy
import cPickle as Pickle
from kivy.config import Config
Config.set('graphics', 'width', '1500')
Config.set('graphics', 'height', '1000')
#from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)
import datetime
current_date = datetime.datetime.now()
from random import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.graphics import *
from kivy.clock import Clock, mainthread
from kivy.uix.togglebutton import ToggleButton

stat_names = ['STR','DEX','CON','INT','WIS','CHA']
skills=['Acrobatics','Animal Handling','Arcana','Athletics','Deception',      
        'History','Insight','Intimidation','Investigation','Medicine','Nature',
        'Perception','Performance','Persuasion','Religion','Sleight of Hand',
        'Stealth','Survival']
money = ['CP','SP','EP','GP','PP']
skill_parents = [1,4,3,0,5,3,4,5,3,4,3,4,5,5,3,1,1,4]
modifiers = {1:-5,2:-4,3:-4,4:-3,5:-3,6:-2,7:-2,8:-1,9:-1,10:0,11:0,12:1,13:1,
            14:2,15:2,16:3,17:3,18:4,19:4,20:5,21:5,22:6,23:6,24:7,25:7,26:8,
            27:8,28:9,29:9,30:10}

class Character():
    def __init__(self):
        self.name = 'Herb'
        self.race = 'Treefolk'
        self.alignment = 'Chaotic Good'
        self._class = 'Archer Bard'
        self.age = [150]
        self.speed = [25]
        self.height = [[7],[2]]
        self.weight = [150]
        self.stats = [7,17,13,13,12,14]
        self.saving_throw_proficiencies = [0,2,0,2,0,0]
        self.skill_bonuses = [0 for i in skill_parents]
        self.skill_bonuses[skills.index('Nature')] = 1
        self.inventory = [['lute',1],['hammer',1],['rations',2],['tinker''s tools',1],['arrow',30]]
        self.weapons = [['oathbow',5,'1D8+DEX+PROF','Extra 3d6 piercing against sworn enemy'],['handaxe',5,'1D6','']]
        self.languages = ['English','Sylvan','Danish']
        self.money = [0,0,0,59,0]
        self.armour_class = [16]
        self.current_hitpoints = [29]
        self.max_hitpoints = [29]
        self.level = [3]
        self.experience = [0]
        self.money = [0,0,0,59,0]
        self.notes = ['Attack rolls with weapons other than the oathbow have disadvantage while my sworn enemy lives.']
        self.cantrips_spells = [['Druid Craft - Cantrip','30ft','1min'],
                                ['Minor Illusion - Cantrip','30ft','1min'],
                                ['Magic Hand - Cantrip','30ft','1min'],
                                ["Tasha's Hideous Laughter - Lvl 1",'30ft','1min'],
                                ['Comprehend Languages - Lvl 1','30ft','60min']]
        self.passive_perception = [10 + modifiers[self.stats[stat_names.index('WIS')]]]
        self.initiative = [modifiers[self.stats[stat_names.index('DEX')]]]
        print("".join(self.name.split()))
        try:
            with open('Character_Data/'+"".join(self.name.split())+'_features_and_traits.txt','r') as f:
                self.features_and_traits = f.read().splitlines()
            self.features_and_traits = "\n".join(self.features_and_traits)
        except:
            self.features_and_traits = ''


class DrawWidget(Widget):
    def __init__(self, **kwargs):
        super(DrawWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1)  # set the colour to red
            self.rect_charstats = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))   
            self.rect_stats = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))  
            self.rect_skills = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))   
            #self.rect_skills_mod = Rectangle(pos=self.center,
            #                      size=(1,
            #                            self.height))  
            #self.rect_skills_mod2 = Rectangle(pos=self.center,
            #                      size=(1,
            #                            self.height))  
            self.rect_inventory = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))  
            self.rect_inventory_shift = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))  
            self.rect_money = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height)) 
            self.rect_death_saving_throws = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))   
            self.rect_saving_throws = Rectangle(pos=self.center,
                                  size=(1,
                                        self.height))   


        self.bind(pos=self.update_rect,
                  size=self.update_rect)

    def update_rect(self, *args):
        offset_from_bottom = self.size[1]*0.025
        self.rect_charstats.pos = [self.size[0]*0.025,self.size[1]*0.825]
        self.rect_charstats.size = [self.size[0]*0.95,self.size[1]/1000.]
        self.rect_stats.pos = [self.size[0]*0.175,offset_from_bottom]
        self.rect_stats.size = [self.size[1]/1000.,self.size[1]*0.825 - offset_from_bottom*2]
        self.rect_skills.pos = [self.size[0]*0.335,offset_from_bottom]
        self.rect_skills.size = [self.size[1]/1000.,self.size[1]*0.7 - offset_from_bottom*2]
        #self.rect_skills_mod.pos = [self.size[0]*0.335,self.size[1]*0.675]
        #self.rect_skills_mod.size = [self.size[0],self.size[1]/1000.]
        #self.rect_skills_mod2.pos = [self.size[0]*0.535,self.size[1]*0.675]
        #self.rect_skills_mod2.size = [self.size[1]/1000.,self.size[1]*0.15]
        self.rect_inventory.pos = [self.size[0]*0.51,offset_from_bottom]
        self.rect_inventory.size = [self.size[1]/1000.,self.size[1]*0.4 - offset_from_bottom]
        self.rect_inventory_shift.pos = [self.size[0]*0.81,offset_from_bottom]
        self.rect_inventory_shift.size = [self.size[1]/1000.,self.size[1]*0.825 - offset_from_bottom*2]
        self.rect_money.pos = [self.size[0]*(0.51+0.025),self.size[1]*0.135]
        self.rect_money.size = [self.size[0]*0.25,self.size[1]/1000.]
        self.rect_death_saving_throws.pos = [self.size[0]*(0.55),self.size[1]*0.7]
        self.rect_death_saving_throws.size = [self.size[1]/1000.,self.size[1]*0.1]
        self.rect_saving_throws.pos = [self.size[0]*0.025,self.size[1]*0.47]
        self.rect_saving_throws.size = [self.size[0]*0.125,self.size[1]/1000.]
        


class CharsheetApp(App):
    def build(self):
        self.parent = RelativeLayout()
        #print "Size of thing:"
        #print(dir(App))
        self.drawing = DrawWidget()
        self.parent.add_widget(self.drawing)
        self.character = Character()       
        self.My_Clock = Clock

        self.draw_file_toolbar()
        self.draw_character_info()
        self.draw_death_saving_throws()
        self.draw_stats()
        self.draw_skills()
        self.draw_saving_throws()
        self.add_bonuses()
        self.draw_features()
        self.draw_weapons()
        self.draw_inventory()
        self.draw_money()
        self.draw_cantrips()
        self.draw_notes()
        l = Label(text=current_date.strftime("%d/%m/%Y"), size_hint=(0.15, 0.05),pos_hint={'x': 0.85, 'y': 0.95})
        self.parent.add_widget(l)
        #self.hitpoints = 
        return self.parent
    
    def draw_money(self):
        self.label_input('money_label','[b]MONEY[/b]',(0.15, 0.15),{'x': 0.46, 'y': 0.04},0,0)    
        for I,i in enumerate(money):
            self.label_input('money_'+i+'_label',i,(0.15, 0.15),{'x': 0.5+I*0.05, 'y': 0.04},0,0)    
            self.text_input('money_'+i+'_text',str(self.character.money[I]),(0.035, 0.04),{'x': 0.564+I*0.05, 'y': 0.06},0,0,background_colour=(1,1,1,1),foreground_colour=(0,0,0,1))
        self.button_input('confirm_money_button','Confirm money change',(0.25, 0.05),{'x': 0.55, 'y': 0},0,0,function=self.change_money)
        
    def change_money(self,object):
        for I,i in enumerate(money):
            self.character.money[I] = getattr(self,'money_'+i+'_text').text
        print self.character.money          

    def draw_file_toolbar(self):
        self.file_dropdown = DropDown()
        functions =     [['New',self.clear_all_fields],
                         ['Save',self.save_current_char],
                         ['Load',self.load_prev_char]]
        for button in functions:
            btn = Button(text='%r' % button[0], size_hint_y=None, height=30)
            btn.bind(on_release= button[1])
            self.file_dropdown.add_widget(btn)

        # create a big main button
        self.file_dropdownbutton = Button(text='File', size_hint=(0.1, 0.05),pos_hint={'x': 0, 'y': 0.95})
        self.file_dropdownbutton.bind(on_release=self.file_dropdown.open)
        #dropdown.bind(on_select=lambda instance, x: setattr(dropdownbutton, 'text', x))
        self.file_dropdown.bind(on_select=lambda instance, x: setattr(self.file_dropdownbutton, 'text', x))
        #parent.add_widget(self.painter)
        #add button to App
        self.parent.add_widget(self.file_dropdownbutton)

    def draw_cantrips(self):
        self.label_input('cantrip_label','[b]CANTRIPS + SPELLS[/b]',(0.2, 0.1),{'x': 0.8, 'y': 0.75},0,0)
        text = [[j if isinstance(j,str) else str(j) for j in i ]for i in self.character.cantrips_spells]
        text = '\n'.join([', '.join(i) for i in text])
        self.text_input('cantrip_spell_text',text,(0.16,0.25),{'x': 0.82, 'y': 0.53},0,0)
        self.button_input('cantrip_spells_button','Update cantrips/spells', (0.16, 0.045),{'x': 0.82, 'y': 0.5},0,0,function=self.change_cantrips)

    def change_cantrips(self,obj):
        text = self.cantrip_spell_text.text.split('\n')
        text = [i.split(',') for i in text]
        self.character.cantrips_spells = text

    def draw_notes(self):
        self.label_input('note_label','[b]PERSONAL NOTES[/b]',(0.2, 0.1),{'x': 0.8, 'y': 0.425},0,0)
        text = self.character.notes[0]
        self.text_input('note_text',text,(0.16,0.4),{'x': 0.82, 'y': 0.045},0,0)
        self.button_input('note_button','Update notes', (0.16, 0.045),{'x': 0.82, 'y': 0.0},0,0,function=self.change_notes)

    def change_notes(self,obj):
        self.character.notes = self.note_text.text
    
    def draw_character_info(self):
        x_axis_point = 0
        y_axis_point = 0.9     
        self.label_input('info_label','[b]CHARACTER INFO[/b]',(0.15, 0.05),{'x': 0.4, 'y': 0.95},x_axis_point,y_axis_point)
        x_axis_point = self.label_input('name_label','Name:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('name_text',self.character.name,(0.1,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)  
        x_axis_point = self.label_input('race_label','Race:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)   
        x_axis_point = self.text_input('race_text',self.character.race,(0.075,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)  
        x_axis_point = self.label_input('alignment_label','Alignment:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('alignment_text',self.character.alignment,(0.075,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.label_input('class_label','Class:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('class_text',self.character._class,(0.075,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        #---------------------------------LEVEL---------------------------
        x_axis_point = self.label_input('level_label','Level:\nExperience:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('level_text',str(self.character.level[0])+'\n'+str(self.character.experience[0]),(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('level_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.level,self.level_text,-1, *args))
        x_axis_point = self.button_input('experience_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.experience,self.level_text,-50, *args))
        self.button_input('level_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.level,self.level_text,1, *args))
        x_axis_point = self.button_input('experience_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.experience,self.level_text,50, *args))
        #--------------------------------Height/Weight--------------------------
        x_axis_point = self.label_input('height_weight_label','Height:\nWeight:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('height_weight_text',str(self.character.height[0][0])+'ft '+str(self.character.height[1][0])+'in\n'+str(self.character.weight[0])+'lbs',(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('height_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.height[1],self.height_weight_text,-1, *args))
        x_axis_point = self.button_input('weight_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.weight,self.height_weight_text,-10, *args))
        self.button_input('height_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.height[1],self.height_weight_text,1, *args))
        x_axis_point = self.button_input('weight_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.weight,self.height_weight_text,10, *args))
        #-------------------------------------NEW LINE--------------------------
        x_axis_point = 0
        y_axis_point = 0.85
        #----------------------------------------HP-----------------------------
        x_axis_point = self.label_input('hitpoints_label','Hitpoints:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('hitpoints_text',str(self.character.current_hitpoints[0])+'/'+str(self.character.max_hitpoints[0]),(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('HP_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_hitpoints(1, *args))
        x_axis_point = self.button_input('HP_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_hitpoints(-1, *args))   
        self.button_input('max_HP_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_max_hitpoints(1, *args))
        x_axis_point = self.button_input('max_HP_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_max_hitpoints(-1, *args))   
        #----------------------------------------AC-----------------------------
        x_axis_point = self.label_input('AC_label','Armour Class:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('armour_class_text',str(self.character.armour_class[0]),(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('AC_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.armour_class,self.armour_class_text,1, *args))
        x_axis_point = self.button_input('AC_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.armour_class,self.armour_class_text,-1, *args))   
        #-------------------------------INITITIATVE-----------------------------
        x_axis_point = self.label_input('initiative_label','Initiative:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        preface = '+' if self.character.initiative[0] > 0 else ''
        x_axis_point = self.text_input('initiative_text',preface+str(self.character.initiative[0]),(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('initiative_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.initiative,self.initiative_text,1,posneg=True, *args))
        x_axis_point = self.button_input('initiative_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.initiative,self.initiative_text,-1,posneg=True, *args))
        #------------------------------PASSIVE PERCEPTION-----------------------
        x_axis_point = self.label_input('PP_label','Passive\nPerception:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('PP_text',str(self.character.passive_perception[0]),(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('speed_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.passive_perception,self.PP_text,1, *args))
        x_axis_point = self.button_input('speed_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.passive_perception,self.PP_text,-1, *args))
        #------------------------------------SPEED------------------------------
        x_axis_point = self.label_input('speed_label','Speed:',(0.075, 0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        x_axis_point = self.text_input('speed_text',str(self.character.speed[0]),(0.05,0.05),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point)
        self.button_input('speed_increase_button','^',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point+0.025},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.speed,self.speed_text,5, *args))
        x_axis_point = self.button_input('speed_decrease_button','v',(0.025, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.change_stat(self.character.speed,self.speed_text,-5, *args))
        #-----------------------------------CONFIRM----------------------------#
        x_axis_point += 0.025
        x_axis_point = self.button_input('confirm_character_changes_button','Confirm info changes?',(0.175, 0.025),{'x': x_axis_point, 'y': y_axis_point},x_axis_point,y_axis_point,function=lambda *args: self.confirm_character_changes(self))

    def change_stat(self,stat,text_obj,modifier,obj,posneg=False):
        stat[0] += modifier
        preface = '+' if stat[0] > 0 and posneg else ''
        if text_obj is self.level_text:
            text_obj.text = str(self.character.level[0])+'\n'+str(self.character.experience[0])
        elif text_obj is self.height_weight_text:
            if self.character.height[1][0] == 12:
                self.character.height[1][0] = 0
                self.character.height[0][0] += 1
            elif self.character.height[1][0] == -1:
                self.character.height[1][0] = 11
                self.character.height[0][0] -= 1                
            text_obj.text = str(self.character.height[0][0])+'ft '+str(self.character.height[1][0])+'in\n'+str(self.character.weight[0])+'lbs'
        else:
            text_obj.text = preface + str(stat[0])
        
    def confirm_character_changes(self,object):
        self.character.name = self.name_text.text
        self.character.race = self.race_text.text
        self.character.alignment = self.alignment_text.text
        self.character._class = self.class_text.text
        tmp_hitpoints = self.hitpoints_text.text.split('/')
        try:
            self.character.current_hitpoints = [int(tmp_hitpoints[0])]
            self.character.max_hitpoints = [int(tmp_hitpoints[1])]
            self.character.armour_class = [int(self.armour_class_text.text)]
            self.character.initiative = [int(self.initiative_text.text)]
            self.character.speed = [int(self.speed_text.text)]
        except:
            pass

    def text_input(self,attr_name,input_text,size_hint,pos_hint,x,y,background_colour=(1,1,1,1),foreground_colour=(0,0,0,1)):
        #x_axis_point += l.size_hint[0] 
        text = TextInput(text=input_text,size_hint=size_hint,pos_hint=pos_hint,background_color=background_colour,foreground_color=foreground_colour)
        text_obj = setattr(self, attr_name, text)
        self.parent.add_widget(text)
        x += text.size_hint[0] 
        return x

    def label_input(self,attr_name,input_text,size_hint,pos_hint,x,y):
        #x_axis_point += l.size_hint[0] 
        l = Label(text=input_text, size_hint=size_hint,pos_hint=pos_hint,markup=True)
        text_obj = setattr(self, attr_name, l)
        self.parent.add_widget(l)
        x += l.size_hint[0] 
        return x

    def button_input(self,attr_name,input_text,size_hint,pos_hint,x,y,function=None,background_colour=(1,1,1,1),foreground_colour=(0,0,0,1)):
        #x_axis_point += l.size_hint[0] 
        button = Button(text=input_text, size_hint=size_hint,pos_hint=pos_hint)
        if function is not None:           
            button.bind(on_release=function)
        button_obj = setattr(self, attr_name, button)
        self.parent.add_widget(button)
        x += button.size_hint[0] 
        return x

    def draw_stats(self):
        self.label_input('stats_label','[b]STATS[/b]',(0.15, 0.1),{'x': 0, 'y': 0.75},0,0)
        self.stat_text = []
        self.mod_text = []
        self.label_input('stat_level_label','LVL',(0.08, 0.1),{'x': 0.05, 'y': 0.725},0,0)
        self.label_input('stat_mod_label','mod',(0.1175, 0.1),{'x': 0.07, 'y': 0.725},0,0)
        for I,i in enumerate(stat_names):
            self.label_input('stat_'+i+'_label',i,(0.05, 0.1),{'x': 0, 'y': 0.7-I*0.05},0,0)
            self.stat_text.append(TextInput(text=str(self.character.stats[I]),size_hint=(0.03,0.03),pos_hint={'x': 0.08, 'y': 0.735-I*0.05},foreground_color=(1,1,1,1),background_color=(0,0,0,1)))
            self.parent.add_widget(self.stat_text[-1])
            preface = '+' if modifiers[self.character.stats[I]] > 0 else ''
            self.mod_text.append(TextInput(text=preface + str(modifiers[self.character.stats[I]]),size_hint=(0.03,0.03),pos_hint={'x': 0.1175, 'y': 0.735-I*0.05},foreground_color=(1,1,1,1),background_color=(0,0,0,1)))
            self.parent.add_widget(self.mod_text[-1])    
        self.button_input("update_stats_btn",'Update Stats',(0.15, 0.05),{'x': 0, 'y': 0},0,0,function=self.update_stats)

    def draw_saving_throws(self):
        self.label_input('saving_throw_label','[b]SAVING THROWS[/b]',(0.15, 0.1),{'x': 0, 'y': 0.4},0,0)
        self.sav_throw_text = []
        self.sav_throw_mod_text = []
        self.label_input('sav_throw_level_label','mod',(0.05, 0.1),{'x': 0.1, 'y': 0.375},0,0)
        self.label_input('sav_throw_mod_label','prof.',(0.05, 0.1),{'x': 0.063, 'y': 0.375},0,0)
        for I,i in enumerate(stat_names):
            self.label_input('saving_throw_'+i+'_label',i,(0.05, 0.1),{'x': 0, 'y': 0.35-I*0.05},0,0)
            preface = '+' if modifiers[self.character.stats[I]] > 0 else ''
            self.sav_throw_text.append(TextInput(text=preface + str(modifiers[self.character.stats[I]]),size_hint=(0.05,0.05),pos_hint={'x': 0.1175, 'y': 0.365-I*0.05},foreground_color=(1,1,1,1),background_color=(0,0,0,1)))
            self.parent.add_widget(self.sav_throw_text[-1])
            self.sav_throw_mod_text.append(TextInput(text=str(self.character.saving_throw_proficiencies[I]),size_hint=(0.03,0.05),pos_hint={'x': 0.08, 'y': 0.365-I*0.05},foreground_color=(1,1,1,1),background_color=(0,0,0,1)))
            self.parent.add_widget(self.sav_throw_mod_text[-1])    
        

    def update_stats(self,obj):
        print('Updating stats, BIIIIIITCH')
        for i in range(len(self.character.stats)):
            self.character.stats[i] = int(self.stat_text[i].text)
            self.stat_text[i].text = str(self.character.stats[i])
            preface = '+' if modifiers[self.character.stats[i]] > 0 else ''
            self.mod_text[i].text = preface + str(modifiers[self.character.stats[i]])
            self.character.saving_throw_proficiencies[i] = int(self.sav_throw_mod_text[i].text)
        for i in range(len(skills)):
            if self.character.skill_bonuses[i]!=0:
                plusminus = '+' if self.character.skill_bonuses[i] >= 0 else ''
                self.skills_mod_text[i].text = str(self.mod_text[skill_parents[i]].text)+'('+plusminus+str(self.character.skill_bonuses[i])+')'
            else:
                self.skills_mod_text[i].text = str(self.mod_text[skill_parents[i]].text)
        preface = '+' if modifiers[self.character.stats[stat_names.index('DEX')]] >= 0 else '-'
        self.initiative_text.text = preface + str(modifiers[self.character.stats[stat_names.index('DEX')]])
        print('Done')

    def draw_skills(self):
        l = Label(text='[b]SKILLS[/b]', size_hint=(0.15, 0.1),pos_hint={'x': 0.2, 'y': 0.75}, markup=True) 
        self.parent.add_widget(l)
        self.skills_mod_text = []
        for I,i in enumerate(skills):
            l = Label(text=i, size_hint=(0.1, 0.1),pos_hint={'x': 0.17, 'y': 0.71-I/float(25)},halign="right",valign='middle')
            self.parent.add_widget(l)
            plusminus = '+' if str(self.character.skill_bonuses[I]) >= 0 else '-'
            string=self.mod_text[skill_parents[I]].text if self.character.skill_bonuses[I]==0 else str(self.mod_text[skill_parents[I]].text)+'('+plusminus+str(abs(self.character.skill_bonuses[I]))+')'
            self.skills_mod_text.append(TextInput(text=string,size_hint=(0.04,0.1),pos_hint={'x': 0.29, 'y': 0.683-I/float(25)},foreground_color=(1,1,1,1),background_color=(0,0,0,1)))
            self.parent.add_widget(self.skills_mod_text[-1])
            #self.skills_mod_text.append(TextInput(text=str(modifiers[self.character.stats[I]]),size_hint=(0.05,0.05),pos_hint={'x': 0.225, 'y': 0.63-I/float(9)}))
            #self.parent.add_widget(self.skills_mod_text[-1])

    def draw_weapons(self):        
        #size_hint=(0.2, 0.1),pos_hint={'x': 0.3, 'y': 0.35}
        l = Label(text='[b]WEAPONS[/b]', size_hint=(0.15, 0.1),pos_hint={'x': 0.475, 'y': 0.35}, markup=True) 
        self.parent.add_widget(l)
        self.weapon_select_dropdown = DropDown()
        weapons = self.character.weapons
        for button in weapons:
            btn = Button(text=button[0], size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.weapon_select_dropdown.select(btn.text))
            self.weapon_select_dropdown.add_widget(btn)
        self.weapon_button = Button(text='SELECT WEAPON', size_hint=(0.2, 0.045),pos_hint={'x': 0.6, 'y': 0.375})
        self.weapon_button.bind(on_release=self.weapon_select_dropdown.open)
        self.weapon_select_dropdown.bind(on_select = lambda instance,weapon: self.disp_weapon_stats(weapon,instance))
        self.parent.add_widget(self.weapon_button)
        l = Label(text='Name:', size_hint=(0.15, 0.1),pos_hint={'x': 0.475, 'y': 0.3}, markup=True) 
        self.parent.add_widget(l)
        self.name_weapon_text = TextInput(text='',size_hint=(0.2,0.05),pos_hint={'x': 0.6, 'y': 0.315},foreground_color=(1,1,1,1),background_color=(0,0,0,1))
        self.parent.add_widget(self.name_weapon_text)
        l = Label(text='Roll Bonus:', size_hint=(0.15, 0.1),pos_hint={'x': 0.475, 'y': 0.25}, markup=True) 
        self.parent.add_widget(l)
        self.weapon_roll_bonus = TextInput(text='',size_hint=(0.2,0.05),pos_hint={'x': 0.6, 'y': 0.265},foreground_color=(1,1,1,1),background_color=(0,0,0,1))
        self.parent.add_widget(self.weapon_roll_bonus)
        l = Label(text='Damage', size_hint=(0.15, 0.1),pos_hint={'x': 0.475, 'y': 0.2}, markup=True) 
        self.parent.add_widget(l)
        self.weapon_damage = TextInput(text='',size_hint=(0.2,0.05),pos_hint={'x': 0.6, 'y': 0.215},foreground_color=(1,1,1,1),background_color=(0,0,0,1))
        self.parent.add_widget(self.weapon_damage)
        self.label_input('weapon_effects_label','Effects:',(0.15, 0.1),{'x': 0.475, 'y': 0.15},0,0)
        self.text_input('weapon_effects_text','',(0.2,0.05),{'x': 0.6, 'y': 0.165},0,0,background_colour=(0,0,0,1),foreground_colour=(1,1,1,1))
        self.button_input("new_weapon_button",'Add or remove weapon',(0.2,0.04),{'x': 0.6, 'y': 0.14},0,0,function=lambda *args: self.add_new_weapon(self))
   
    def add_new_weapon(self,obj):
        weapon_name = self.name_weapon_text.text
        weapon_damage = self.weapon_damage.text
        weapon_roll_bonus = self.weapon_roll_bonus.text
        weapon_effects = self.weapon_effects_text.text
        weapon_names = [i[0] for i in self.character.weapons]
        try:  #remove old weapon
            ind = weapon_names.index(weapon_name)
            del self.character.weapons[ind]
        except:
            self.character.weapons.append([weapon_name,weapon_damage,weapon_roll_bonus,weapon_effects])
        self.parent.remove_widget(self.weapon_select_dropdown)
        self.parent.remove_widget(self.weapon_button)
        self.weapon_select_dropdown = DropDown()
        weapons = self.character.weapons
        for button in weapons:
            btn = Button(text=button[0], size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.weapon_select_dropdown.select(btn.text))
            self.weapon_select_dropdown.add_widget(btn)
        self.weapon_button = Button(text='SELECT WEAPON', size_hint=(0.2, 0.045),pos_hint={'x': 0.6, 'y': 0.375})
        self.weapon_button.bind(on_release=self.weapon_select_dropdown.open)
        self.weapon_select_dropdown.bind(on_select = lambda instance,weapon: self.disp_weapon_stats(weapon,instance))
        self.parent.add_widget(self.weapon_button)
        

    def draw_death_saving_throws(self):
        self.label_input('saving_throw_label','[b]DEATH SAVING THROWS[/b]', (0.15, 0.1),{'x': 0.63, 'y': 0.75},0,0) 
        self.label_input('success_saving_throw_label','[b]Successes:[/b]', (0.15, 0.1),{'x': 0.55, 'y': 0.715},0,0) 
        self.label_input('fail_saving_throw_label','[b]Fails:[/b]', (0.15, 0.1),{'x': 0.55, 'y': 0.68},0,0) 
        self.saving_throw_boxes = []
        for j in [self.success_saving_throw_label.pos_hint['y']+0.04,self.fail_saving_throw_label.pos_hint['y']+0.04]:
            for i in range(3):
                checkbox = ToggleButton(text=str(i+1),size_hint=(0.02,0.02),pos_hint={'x': 0.66+0.05*i, 'y': j},color=[1,1,1,1])
                self.saving_throw_boxes.append(checkbox)
                self.parent.add_widget(self.saving_throw_boxes[-1])

    def change_name(self,obj):
        self.character.name = self.name_text.text

    def change_race(self,obj):
        self.character.race = self.race_text.text

    def save_features_and_traits(self,obj):
        with open('Character_Data/'+"".join(self.character.name.split())+'_features_and_traits.txt','w') as f:
            f.write(self.features_and_traits_text.text)

    def draw_features(self):
        l = Label(text='[b]CHARACTER FEATURES[/b]', size_hint=(0.1, 0.1),pos_hint={'x': 0.35, 'y': 0.6}, markup=True) 
        self.parent.add_widget(l)
        self.features_and_traits_text = TextInput(text=self.character.features_and_traits,size_hint=(0.45,0.2),pos_hint={'x': 0.35, 'y': 0.42})
        self.parent.add_widget(self.features_and_traits_text)
        self.save_new_features_and_traits = Button(text='Update features and traits', size_hint=(0.2, 0.05),pos_hint={'x': 0.6, 'y': 0.625})
        self.save_new_features_and_traits.bind(on_release=lambda *args: self.save_features_and_traits(*args))
        self.parent.add_widget(self.save_new_features_and_traits)

    def draw_inventory(self):
        l = Label(text='[b]INVENTORY[/b]', size_hint=(0.15, 0.1),pos_hint={'x': 0.35, 'y': 0.35}, markup=True) 
        self.parent.add_widget(l)
        text = '\n'.join([i[0] + '\t'+str(i[1]) for i in self.character.inventory])
        self.inventory_text = TextInput(text=text,size_hint=(0.15,0.18),pos_hint={'x': 0.35, 'y': 0.2})
        self.parent.add_widget(self.inventory_text)
        l = Label(text='[b]Adjust inventory[/b]', size_hint=(0.15, 0.1),pos_hint={'x': 0.35, 'y': 0.135}, markup=True) 
        self.parent.add_widget(l)
        l = Label(text='[b]Item[/b]', size_hint=(0.2, 0.1),pos_hint={'x': 0.27, 'y': 0.095}, markup=True) 
        self.parent.add_widget(l)
        self.new_item = TextInput(text='',size_hint=(0.1,0.05),pos_hint={'x': 0.4, 'y': 0.12})
        self.parent.add_widget(self.new_item)
        l = Label(text='[b]Amount[/b]', size_hint=(0.2, 0.1),pos_hint={'x': 0.27, 'y': 0.045}, markup=True) 
        self.parent.add_widget(l)
        self.new_item_amount = TextInput(text=str(0),size_hint=(0.1,0.05),pos_hint={'x': 0.4, 'y': 0.06})
        self.parent.add_widget(self.new_item_amount)
        self.inv_change_button = Button(text='Confirm', size_hint=(0.15, 0.05),pos_hint={'x': 0.35, 'y': 0})
        self.inv_change_button.bind(on_release=lambda *args: self.change_inventory(*args))
        self.parent.add_widget(self.inv_change_button)

    def change_inventory(self,object):
        item = str(self.new_item.text.lower())
        amount = int(self.new_item_amount.text)
        current_inventory = self.character.inventory
        items = [i[0] for i in current_inventory]
        if item not in items and amount > 0: #add new item
            current_inventory.append([item,amount])
            self.rewrite_inventory(self)
        elif item not in items and amount < 0: #can't remove items I don't have
            self.inventory_text.text = 'ITEM NOT FOUND'
            self.My_Clock.schedule_once(self.rewrite_inventory, 1)
        elif item in items and (current_inventory[items.index(item)][1] + amount) >= 0: # add/subtract to existing item
            current_inventory[items.index(item)][1] += amount
            if current_inventory[items.index(item)][1] == 0:
                del current_inventory[items.index(item)]
            self.rewrite_inventory(self)
        elif item in items and (current_inventory[items.index(item)][1] + amount) < 0: #don't have enough to do this!
            self.inventory_text.text = 'NOT ENOUGH'
            #time.sleep(1)
            self.My_Clock.schedule_once(self.rewrite_inventory, 1)

    def rewrite_inventory(self,obj):
        text = '\n'.join([i[0] + '\t'+str(i[1]) for i in self.character.inventory])
        self.inventory_text.text = text
        return

    def disp_weapon_stats(self,weapon,object):
        #        self.weapons = [['oathbow',5,'1D8+DEX+PROF',True],['handaxe',5,'1D6',False]]
        weapon_index = [i[0] for i in self.character.weapons].index(weapon)
        self.name_weapon_text.text = str(self.character.weapons[weapon_index][0])
        self.weapon_roll_bonus.text = str(self.character.weapons[weapon_index][1])
        self.weapon_damage.text = self.character.weapons[weapon_index][2]
        self.weapon_effects_text.text = self.character.weapons[weapon_index][3]
        setattr(self.weapon_button, 'text', weapon)

    def add_bonuses(self):
        l = Label(text='[b]SKILL BONUSES[/b]', size_hint=(0.15, 0.1),pos_hint={'x': 0.35, 'y': 0.75}, markup=True) 
        self.parent.add_widget(l)
        self.bonus_selector_dropdown = DropDown()
        functions = skills
        for button in functions:
            btn = Button(text=button, size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.bonus_selector_dropdown.select(btn.text))
            self.bonus_selector_dropdown.add_widget(btn)
        self.dropdownskillbonusbutton = Button(text='SELECT SKILL', size_hint=(0.15, 0.05),pos_hint={'x': 0.35, 'y': 0.73})
        self.dropdownskillbonusbutton.bind(on_release=self.bonus_selector_dropdown.open)
        self.bonus_selector_dropdown.bind(on_select=lambda instance, x: setattr(self.dropdownskillbonusbutton, 'text', x))
        self.parent.add_widget(self.dropdownskillbonusbutton)
        self.bonus_increase_button = Button(text='Up', size_hint=(0.075, 0.05),pos_hint={'x': 0.35, 'y': 0.68})
        self.bonus_decrease_button = Button(text='Down', size_hint=(0.075, 0.05),pos_hint={'x': 0.425, 'y': 0.68})
        self.bonus_increase_button.bind(on_release=lambda *args: self.change_bonuses(1, *args))
        self.bonus_decrease_button.bind(on_release=lambda *args: self.change_bonuses(-1, *args))
        self.parent.add_widget(self.bonus_increase_button)
        self.parent.add_widget(self.bonus_decrease_button)

    def change_hitpoints(self,modifier,obj):
        self.character.current_hitpoints[0] += modifier
        self.character.current_hitpoints[0] = 0 if self.character.current_hitpoints[0] < 0 else self.character.current_hitpoints[0]
        self.character.current_hitpoints[0] = self.character.max_hitpoints[0] if self.character.current_hitpoints[0] > self.character.max_hitpoints[0] else self.character.current_hitpoints[0]
        self.hitpoints_text.text = str(self.character.current_hitpoints[0])+'/'+str(self.character.max_hitpoints[0])

    def change_max_hitpoints(self,modifier,obj):
        self.character.max_hitpoints[0] += modifier
        self.character.max_hitpoints[0] = 0 if self.character.max_hitpoints[0] < 0 else self.character.max_hitpoints[0]
        self.character.current_hitpoints[0] = self.character.max_hitpoints[0] if self.character.current_hitpoints[0] > self.character.max_hitpoints[0] else self.character.current_hitpoints[0]
        self.hitpoints_text.text = str(self.character.current_hitpoints[0])+'/'+str(self.character.max_hitpoints[0])

    def change_bonuses(self,modifier,obj):
        selection = skills.index(self.dropdownskillbonusbutton.text)
        self.character.skill_bonuses[selection] += modifier
        self.update_stats(0)        
        

    def clear_all_fields(self,obj):
        print('Clearing')
        for i in dir(self):
            z = getattr(self, i, 1)
            if isinstance(z, list):
                for j in z:
                    if isinstance(j, kivy.uix.textinput.TextInput):
                        j.text = ''
            else:
                if isinstance(z, kivy.uix.textinput.TextInput):
                    z.text = ''        
        self.parent.remove_widget(self.weapon_select_dropdown)
        self.parent.remove_widget(self.weapon_button)
        self.weapon_select_dropdown = DropDown()
        self.weapon_button = Button(text='SELECT WEAPON', size_hint=(0.2, 0.045),pos_hint={'x': 0.6, 'y': 0.375})
        self.weapon_button.bind(on_release=self.weapon_select_dropdown.open)
        self.weapon_select_dropdown.bind(on_select = lambda instance,weapon: self.disp_weapon_stats(weapon,instance))
        self.parent.add_widget(self.weapon_button)
        
    def refresh(self):
        for i in range(len(self.character.stats)):
            self.stat_text[i].text = str(self.character.stats[i])
            preface = '+' if modifiers[self.character.stats[i]] > 0 else ''
            self.mod_text[i].text = preface + str(modifiers[self.character.stats[i]])
            self.sav_throw_text[i].text = preface + str(modifiers[self.character.stats[i]])
            self.sav_throw_mod_text[i].text = str(self.character.saving_throw_proficiencies[i])
        for i in range(len(skills)):
            if self.character.skill_bonuses[i]!=0:
                plusminus = '+' if self.character.skill_bonuses[i] >= 0 else '-'
                self.skills_mod_text[i].text = str(self.mod_text[skill_parents[i]].text)+'('+plusminus+str(abs(self.character.skill_bonuses[i]))+')'
            else:
                self.skills_mod_text[i].text = str(self.mod_text[skill_parents[i]].text)
        self.rewrite_inventory(self)
        self.features_and_traits_text.text = self.character.features_and_traits        
        self.name_text.text = self.character.name 
        self.race_text.text = self.character.race 
        self.alignment_text.text = self.character.alignment
        self.class_text.text = self.character._class 
        tmp_hitpoints = str(self.character.current_hitpoints[0]) + '/' + str(self.character.max_hitpoints[0])
        self.hitpoints_text.text = tmp_hitpoints
        self.armour_class_text.text = str(self.character.armour_class[0])
        self.initiative_text.text = str(self.character.initiative[0])
        self.PP_text.text = str(self.character.passive_perception[0])
        self.level_text.text = str(self.character.level[0])+'\n'+str(self.character.experience[0])
        self.height_weight_text.text = str(self.character.height[0][0])+'ft '+str(self.character.height[1][0])+'in\n'+str(self.character.weight[0])+'lbs'
        self.speed_text.text = str(self.character.speed[0])
        for I,i in enumerate(money):
            getattr(self,'money_'+i+'_text').text = str(self.character.money[I])        
        self.parent.remove_widget(self.weapon_select_dropdown)
        self.parent.remove_widget(self.weapon_button)
        self.weapon_select_dropdown = DropDown()
        weapons = self.character.weapons
        for button in weapons:
            btn = Button(text=button[0], size_hint_y=None, height=30)
            btn.bind(on_release=lambda btn: self.weapon_select_dropdown.select(btn.text))
            self.weapon_select_dropdown.add_widget(btn)
        self.weapon_button = Button(text='SELECT WEAPON', size_hint=(0.2, 0.045),pos_hint={'x': 0.6, 'y': 0.375})
        self.weapon_button.bind(on_release=self.weapon_select_dropdown.open)
        self.weapon_select_dropdown.bind(on_select = lambda instance,weapon: self.disp_weapon_stats(weapon,instance))
        self.parent.add_widget(self.weapon_button)
        text = [[j if isinstance(j,str) else str(j) for j in i ]for i in self.character.cantrips_spells]
        text = '\n'.join([', '.join(i) for i in text])
        self.cantrip_spell_text.text = text
        self.note_text.text = self.character.notes[0]

    def load_prev_char(self,obj):
        print('Loading')
        try:
            with open('Character_Data/'+"".join(self.character.name.split())+'_character_sheet.p','r') as f:
                self.character = Pickle.load(f)
        except:
            content = Button(text='Cannot find file:\n Character_Data/'+"".join(self.character.name.split())+'_character_sheet.p\nClick to dismiss')
            popup = Popup(title='File not found',content=content,auto_dismiss=False)
            # bind the on_press event of the button to the dismiss function
            content.bind(on_press=popup.dismiss)
            popup.open()
        self.refresh()
        

    def save_current_char(self,obj):
        print('Saving')
        with open('Character_Data/'+"".join(self.character.name.split())+'_character_sheet.p','w') as f:
            Pickle.dump(self.character,f)

if __name__ == '__main__':
    CharsheetApp().run()



