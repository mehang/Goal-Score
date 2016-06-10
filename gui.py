#!/usr/bin/env python

import pygtk 
pygtk.require('2.0')
import gtk
import cairo
import signal
import sys
import time
import threading
import scrape
import os

class GoalWindow:
        def __init__(self):
           self.win = gtk.Window(gtk.WINDOW_TOPLEVEL) 
           self.vbox = gtk.VBox(homogeneous = False)#homogeneous give all child equal space allocations

           self.separator = gtk.VSeparator()

           self.maincontainer = gtk.VBox(homogeneous=False)

           self.scrolledwindow = gtk.ScrolledWindow()
           self.scrolledwindow.set_border_width(1)
           self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
           self.scrolledwindow.add_with_viewport(self.vbox)

           self.toolbar = gtk.Toolbar()
           self.toolbar.set_style(gtk.TOOLBAR_ICONS)
           self.addteam = gtk.ToolButton(gtk.STOCK_PREFERENCES)
           self.addteam.set_tooltip_text("Modify your favourite team list")
           self.toolbar.insert(self.addteam,0)
           self.addteam.connect("clicked",self.modify_fav_team)

           self.win.add(self.maincontainer)
           self.maincontainer.pack_start(self.toolbar,False,True,0)
           self.maincontainer.pack_start(self.leagueselectionmenu(),False,True,0)
           self.maincontainer.pack_start(self.scrolledwindow,True,True,0)

           self.myteamlist = [] #list of favourite team to display
           self.teamname = ""  #team name in entry box

           self.euroteam = ["Brazil","albania","austria","begium","croatia",
                            "czech republic","england","france","germany",
                            "hungary","iceland","italy","northern ireland",
                            "poland","portugal","republic of ireland","romania",
                            "russia","slovakia","spain","sweden",
                            "switzerland","turkey","ukraine","wales"]

           self.teamstodisplay = []

           self.counter = 1

           gtk.timeout_add(60000,self.main)


        def initialize_window(self):
            self.opacity = 1 
            self.win.set_title("Goal Score!!!!!")
            self.win.set_icon_from_file("icon.jpg");
            self.win.set_size_request(300,200)
            self.win.move(500,500)
            #self.win.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
            self.color = gtk.gdk.color_parse("#032941")
            self.win.modify_bg(gtk.STATE_NORMAL, self.color)
            self.win.connect("destroy",self.close_window)
            self.win.set_opacity(self.opacity)
            self.read_from_file()

        def close_window(self,widget):#close the main window function
            #with open("team list","wb")as f:
            #    pickle.dump(self.myteamlist,f)#pickle writes in human unreadable form
            with open("team list","w+") as f: #w+ creates file if it doesnot exist
                for team in self.myteamlist:
                    f.write(team + "\n")
            gtk.main_quit()

        def read_from_file(self):
            #with open("team list","rb") as f:
            #    self.myteamlist = pickle.load(f)
            with open("team list","a+") as f:
                self.myteamlist = [team.rstrip("\n") for team in f]

        def modify_fav_team(self,widget):
            settings = gtk.Dialog(title = "Settings")
            entry = gtk.Entry()
            entry.set_max_length(50)
            #entry.set_text("Enter your team name")
            entry.set_tooltip_text("Enter your teamname to add or remove from list")
            entry.show()
            settings.vbox.pack_start(entry)
            addbutton = gtk.ToolButton(gtk.STOCK_ADD)
            addbutton.set_tooltip_text("Add to the favourite team list")
            addbutton.connect("clicked",self.add_team,entry)
            addbutton.show()
            deletebutton = gtk.ToolButton(gtk.STOCK_CLEAR)
            deletebutton.set_tooltip_text("Delete from the favourite team list")
            deletebutton.connect("clicked",self.remove_team,entry)
            deletebutton.show()
            buttoncontainer = gtk.HBox()
            buttoncontainer.pack_start(addbutton,False,True,1)
            buttoncontainer.pack_start(deletebutton,False,True,1)
            buttoncontainer.show()
            settings.vbox.pack_start(buttoncontainer)
            settings.run()
            settings.destroy()

        def add_team(self,widget,entry):
            self.teamname = entry.get_text()
            if self.teamname:
                if self.teamname == "Enter your team name":
                    self.error_window("Please enter a team name to add","Team List Modification Error")
                elif self.teamname in self.myteamlist:
                    self.error_window("Team already added", "Team List Modification Error")
                else:
                    self.myteamlist.append(self.teamname)
                    print self.myteamlist

        def remove_team(self,widget,entry):
            self.teamname = entry.get_text()
            if self.teamname:
                if self.teamname == "Enter your team name":
                    self.error_window("Please enter a team name to remove","Team List Modification Error")
                    if self.teamname in self.myteamlist:
                        self.myteamlist.remove(self.teamname)
                    else:
                        self.error_window("No team in the list", "Team List Modification Error")
                        print self.myteamlist

        def add_icon_image(self,hbox,country):
            try:
                 #  image = gtk.Image() 
                 #  image.set_from_file("flag/spain.png");
                 # a button to contain the image
                 imagebutton = gtk.Button()
                 imagebutton.set_size_request(width = 100,height = 50)
                 if os.path.isfile("flag/uefa euro/"+country+".png"):
                     pixbuf = gtk.gdk.pixbuf_new_from_file("flag/uefa euro/"+country+".png")
                 else:
                     pixbuf = gtk.gdk.pixbuf_new_from_file("flag/uefa euro/uefa.jpg")
                 pixbuf = pixbuf.scale_simple(50,50,gtk.gdk.INTERP_BILINEAR)
                 image = gtk.image_new_from_pixbuf(pixbuf)
                 imagebutton.add(image)
                 hbox.pack_start(imagebutton,False,False,0)

            except Exception, e:
                self.error_window(e.message,"Loading Error")
                sys.exit(1)

#contains box for team flag, name and score
        def horizontal_gameteam_box(self, teamA, teamB, teamAscore = "?",teamBscore = "?", decider = "?"):
            hbox = gtk.HBox()
            hbox.show() 
            hbox.pack_start(self.team_container(teamA),False,False,0)
            hbox.pack_start(self.score_box(teamAscore,teamBscore,decider),False,False,0)
            hbox.pack_end(self.team_container(teamB),False,False,0)
            return hbox

        def score_box(self, teamAscore, teamBscore,gamedecider):
            hbox = gtk.HBox()
            hbox.show()
            scorebuttonA = gtk.Button()
            scorebuttonA.set_size_request(width = 50,height = 50)
            scorebuttonA.set_label(str(teamAscore))
            hbox.pack_start(scorebuttonA,False,False,0)
            scorebuttonB = gtk.Button()
            scorebuttonB.set_size_request(width = 50, height = 50)
            scorebuttonB.set_label(str(teamBscore))
            hbox.pack_start(scorebuttonB,False,False,0)
            hbox.pack_start(scorebuttonB,False,False,0)
            hbox.pack_start(scorebuttonB,False,False,0)
            hbox.pack_start(scorebuttonB,False,False,0)
            hbox.pack_end(scorebuttonB,False,False,0)
            vbox = gtk.VBox()
            vbox.show()
            vbox.pack_start(hbox,False,False,0)
            scorebase = gtk.Label()
            scorebase.modify_fg(gtk.STATE_NORMAL,gtk.gdk.Color(65535,65535,65535) )
            scorebase.set_markup("<b>"+gamedecider+"</b>")
            vbox.pack_start(scorebase,False,False,0)
            return vbox

 

        def team_container(self,countryname):
            vcountrybox = gtk.VBox()
            vcountrybox.show()
            self.add_icon_image(vcountrybox,countryname.lower().replace(" ",""))
            countrytext = gtk.Label()
            countrytext.modify_fg(gtk.STATE_NORMAL,gtk.gdk.Color(65535,65535,65535) )
            countrytext.set_markup("<b>"+countryname.upper()+"</b>")
            #countrytext.set_sensitive(False)#enable or disable button
            vcountrybox.pack_start(countrytext,False,False,0)
            return vcountrybox

        def leagueselectionmenu(self):
            menu = gtk.combo_box_new_text()
            menu.set_size_request(width = 200,height = 40)
            menu.append_text("Select a league:")
            menu.append_text("My Team")
            menu.append_text("UEFA Euro")
            menu.append_text("FIFA World Cup")
            menu.append_text("COPA America")
            menu.append_text("English Premier League")
            menu.append_text("La Liga")
            menu.append_text("Bundesliga")
            menu.append_text("Serie A")
            menu.append_text("Ligue 1")
            menu.connect("changed",self.league)
            menu.set_active(0)  #tells which is to be shown first
            return menu

        def league(self,menu): 
            leaguename = menu.get_model()
            #print self.euroteam
            dictionary = {1 : self.myteamlist[:],2 : self.euroteam[:]}
            index = menu.get_active()
            if not dictionary[index]:
                self.error_window("Please add team name","Empty Team List")
                return
            self.teamstodisplay = dictionary[index][:]
            print self.teamstodisplay
            if index:
                print "league selected:", leaguename[index][0] 
            return

        def vertical_box(self,box):
            self.vbox.pack_start(box,False)
            self.vbox.pack_start(self.separator,False,True,1)
            self.vbox.show()
            self.scrolledwindow.add_with_viewport(self.vbox)

        def make_opaque(self,widget,event):
            self.opacity = 1
            self.win.set_opacity(self.opacity)

        def make_transparent(self,widget,event):
            
            if event.detail != gtk.gdk.NOTIFY_NONLINEAR_VIRTUAL and event.detail != gtk.gdk.NOTIFY_NONLINEAR :
                return
            self.opacity = 0.5
            self.win.set_opacity(self.opacity)

        def dimness(self):
            self.win.connect("enter_notify_event",self.make_opaque)
            self.win.connect("leave_notify_event",self.make_transparent)
            self.win.connect("focus_out_event",self.make_transparent)

        def error_window(self, errormessage, errortitle = "Error"):
            errorwin = gtk.MessageDialog(self.win,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, errormessage)
            errorwin.set_title(errortitle)
            errorwin.run()
            errorwin.destroy()


        def main(self, searchFor=["england"]): 
            self.initialize_window()

            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))


            print self.counter
            for i in self.myteamlist:
                obj = scrape.main(i)
                self.vertical_box(self.horizontal_gameteam_box(teamA = obj.homeTeam, teamB = obj.awayTeam, teamAscore = obj.homeScore,teamBscore = obj.awayScore, decider = obj.time))
           
            self.dimness()
            self.win.set_app_paintable(True)
            self.win.show_all()
            self.counter=self.counter+1
            print self.counter

            gtk.main()
            return 0

if __name__ == "__main__":
    window = GoalWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)#keyboard ctrl+c interrupt
    teams = ["Brazil","FC Inter"]
    window.main(teams) 


