#!/usr/bin/env python

import pygtk 
pygtk.require('2.0')
import gtk
import cairo
import signal
import sys
import time
import scrape

class GoalWindow:
        def __init__(self):
           self.win = gtk.Window(gtk.WINDOW_TOPLEVEL) 
           self.opacity = 1 
           self.win.set_title("Goal Score!!!!!")
           self.win.set_icon_from_file("icon.jpg");
           self.win.set_size_request(300,130)
           self.win.move(500,500)
           self.color = gtk.gdk.color_parse("#230011")
           self.win.modify_bg(gtk.STATE_NORMAL, self.color)
           self.win.connect("destroy",gtk.main_quit)
           self.win.set_opacity(self.opacity)


        def add_icon_image(self,hbox,country):
            try:
                 #  image = gtk.Image() 
                 #  image.set_from_file("flag/spain.png");
                   # a button to contain the image
                   imagebutton = gtk.Button()
                   imagebutton.set_size_request(width = 100,height = 100)
                   pixbuf = gtk.gdk.pixbuf_new_from_file("flag/"+country+".png")
                   pixbuf = pixbuf.scale_simple(100,100,gtk.gdk.INTERP_BILINEAR)
                   image = gtk.image_new_from_pixbuf(pixbuf)
                   imagebutton.add(image)
                   hbox.pack_start(imagebutton,False,False,0)

            except Exception, e:
                    print e.message
                    sys.exit(1)

#contains box for team flag, name and score
        def horizontal_gameteam_box(self, teamA, teamB, teamAscore = "-",teamBscore = "-", decider = "FT"):
            hbox = gtk.HBox()
            hbox.show() 
            self.win.add(hbox)
            hbox.pack_start(self.team_container(teamA),False,False,0)
            hbox.pack_start(self.score_box(teamAscore,teamBscore,decider))
            hbox.pack_start(self.team_container(teamB),False,False,0)
            return hbox

        def score_box(self, teamAscore, teamBscore,gamedecider):
            hbox = gtk.HBox()
            hbox.show()
            self.win.add(hbox)
            scorebuttonA = gtk.Button()
            scorebuttonA.set_size_request(width = 50,height = 100)
            scorebuttonA.set_label(str(teamAscore))
            hbox.pack_start(scorebuttonA,False,False,0)
            scorebuttonB = gtk.Button()
            scorebuttonB.set_size_request(width = 50, height = 100)
            scorebuttonB.set_label(str(teamBscore))
            hbox.pack_start(scorebuttonB,False,False,0)
            vbox = gtk.VBox()
            vbox.show()
            self.win.add(vbox)
            vbox.pack_start(hbox,False,False,0)
            scorebase = gtk.Label()
            scorebase.modify_fg(gtk.STATE_NORMAL,gtk.gdk.Color(65535,65535,65535) )
            scorebase.set_markup("<b>"+gamedecider+"</b>")
            vbox.pack_start(scorebase,False,False,0)
            return vbox

 

        def team_container(self,countryname):
            vcountrybox = gtk.VBox()
            vcountrybox.show()
            self.win.add(vcountrybox)
            self.add_icon_image(vcountrybox,countryname.lower().replace(" ",""))
            countrytext = gtk.Label()
            countrytext.modify_fg(gtk.STATE_NORMAL,gtk.gdk.Color(65535,65535,65535) )
            countrytext.set_markup("<b>"+countryname.upper()+"</b>")
            #countrytext.set_sensitive(False)#enable or disable button
            vcountrybox.pack_start(countrytext,False,False,0)
            return vcountrybox

        def vertical_box(self,box):
            vbox = gtk.VBox(homogeneous = True)#homogeneous give all child equal space allocations
            vbox.pack_start(box,False)
            self.win.add(vbox)

        def make_opaque(self,widget,event):
            self.opacity = 1
            self.win.set_opacity(self.opacity)

        def make_transparent(self,widget,event):
            if event.detail != gtk.gdk.NOTIFY_NONLINEAR:
                return
            self.opacity = 0.5
            self.win.set_opacity(self.opacity)

        def dimness(self):
            self.win.connect("enter_notify_event",self.make_opaque)
            self.win.connect("leave_notify_event",self.make_transparent)

        def error_window(self, errormessage, errortitle = "Error"):
            errorwin = gtk.MessageDialog(self.win,gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, errormessage)
            errorwin.set_title(errortitle)
            errorwin.run()
            errorwin.destroy()


        def main(self): 
            self.vertical_box(self.horizontal_gameteam_box("Spain","south korea"))
            self.dimness()
            self.win.set_app_paintable(True)
            self.win.show_all()
            self.error_window("errordetectedint he photo")

            gtk.main()
            return 0

if __name__ == "__main__":
    window = GoalWindow()
    signal.signal(signal.SIGINT, signal.SIG_DFL)#keyboard ctrl+c interrupt
    window.main()



