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
           self.opacity = 1 
           self.win.set_title("Goal Score!!!!!")
           self.win.set_icon_from_file("icon.jpg");
           self.win.set_size_request(300,200)
           self.win.move(500,500)
           #self.win.set_gravity(gtk.gdk.GRAVITY_SOUTH_WEST)
           self.color = gtk.gdk.color_parse("#032941")
           self.win.modify_bg(gtk.STATE_NORMAL, self.color)
           self.win.connect("destroy",gtk.main_quit)
           self.win.set_opacity(self.opacity)
           self.vbox = gtk.VBox(homogeneous = False)#homogeneous give all child equal space allocations

           self.separator = gtk.VSeparator()

           self.maincontainer = gtk.VBox(homogeneous=False)

           self.scrolledwindow = gtk.ScrolledWindow()
           self.scrolledwindow.set_border_width(1)
           self.scrolledwindow.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_ALWAYS)
           self.scrolledwindow.add_with_viewport(self.vbox)
           self.win.add(self.maincontainer)
           self.maincontainer.pack_start(self.leagueselectionmenu(),False,True,0)
           self.maincontainer.pack_start(self.scrolledwindow,True,True,0)


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

#button.set_tooltip_text("jalksjfl")

        def leagueselectionmenu(self):
            menu = gtk.combo_box_new_text()
            menu.set_size_request(width = 200,height = 40)
            menu.append_text("Select a league:")
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
            index = menu.get_active()
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


        def main(self, searchFor): 

            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))
            self.vertical_box(self.horizontal_gameteam_box(teamA = "korea", teamB = "japan", teamAscore = "2",teamBscore = "3", decider = "FT"))


           # for i in searchFor:
           #     obj = scrape.main(i)
           #     self.vertical_box(self.horizontal_gameteam_box(teamA = obj.homeTeam, teamB = obj.awayTeam, teamAscore = obj.homeScore,teamBscore = obj.awayScore, decider = obj.time))
           
            self.dimness()
            self.win.set_app_paintable(True)
            self.win.show_all()

            gtk.main()
            return 0

if __name__ == "__main__":
    window = GoalWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)#keyboard ctrl+c interrupt
    teams = ["Brazil","Ecuador","Haiti","Colombia","Peru"]
    window.main(teams) 


