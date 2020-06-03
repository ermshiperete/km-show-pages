#!/usr/bin/python3

import gi
import logging
import magic
import os.path
import subprocess
import webbrowser
import urllib.parse

import webbrowser
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

class BrowserView(Gtk.Window):

  def __init__(self, pageUrl, kbName, autoClose):
    self.accelerators = None
    self.pageUrl = pageUrl
    self.kbName = kbName
    self.autoClose = autoClose
    windowTitle = kbName + " (" + os.path.basename(self.pageUrl) + ")"
    Gtk.Window.__init__(self, title=kbName)

    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

    s = Gtk.ScrolledWindow()
    self.webview = WebKit2.WebView()
    self.webview.connect("decide-policy", self.doc_policy)
    self.webview.connect("load-failed", self.on_load_failed)
    self.webview.connect("load-changed", self.on_load_changed)
    self.webview.load_uri(pageUrl)
    s.add(self.webview)
    vbox.pack_start(s, True, True, 0)

    hbox = Gtk.Box(spacing=12)
    vbox.pack_start(hbox, False, False, 6)

    text = Gtk.Label("Page displayed correctly?")
    hbox.pack_start(text, True, True, 12)

    button = Gtk.Button.new_with_mnemonic("_No")
    button.connect("clicked", self.on_no_clicked)
    hbox.pack_start(button, False, False, 12)

    button = Gtk.Button.new_with_mnemonic("_Yes")
    button.connect("clicked", self.on_yes_clicked)
    hbox.pack_end(button, False, False, 12)

    self.add(vbox)

  def doc_policy(self, web_view, decision, decision_type):
    logging.info("Checking policy")
    logging.debug("received policy decision request of type: {0}".format(decision_type.value_name))
    if decision_type == WebKit2.PolicyDecisionType.NAVIGATION_ACTION or decision_type == WebKit2.PolicyDecisionType.NEW_WINDOW_ACTION:
      nav_action = decision.get_navigation_action()
      request = nav_action.get_request()
      uri = request.get_uri()
      logging.debug("nav request is for uri %s", uri)
    return False

  def on_no_clicked(self, button):
    self.addErrorKeyboard()
    self.close()

  def on_yes_clicked(self, button):
    self.close()

  def on_load_failed(self, web_view, load_event, failing_uri, error):
    logging.info("load failed: " + error.message)
    if self.autoClose:
      self.addErrorKeyboard()

  def on_load_changed(self, web_view, load_event):
    if load_event == WebKit2.LoadEvent.FINISHED:
      if self.autoClose:
        self.close()

  def checkEncoding(self):
    url = urllib.parse.urlparse(self.pageUrl)
    blob = open(url.path, 'rb').read()
    m = magic.open(magic.MAGIC_MIME_ENCODING)
    m.load()
    encoding = m.buffer(blob)
    logging.debug("file encoding: %s", encoding)
    if encoding != "utf-8" and encoding != "us-ascii":
      return f' [{encoding}]'
    return ''

  def addErrorKeyboard(self):
    encoding = self.checkEncoding()
    print(f"\t- [ ] {self.kbName} ({os.path.basename(self.pageUrl)}{encoding})")
