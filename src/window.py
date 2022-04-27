# window.py
#
# Copyright 2022 Andras Molnar
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Pango, Gio, GLib

def apply_css(widget,provider):
    ctx = widget.get_style_context()
    ctx.add_provider(provider,Gtk.STYLE_PROVIDER_PRIORITY_USER)
    child = widget.get_first_child()
    while child:
        apply_css(child,provider)
        child = child.get_next_sibling()



@Gtk.Template(resource_path='/com/github/molnarandris/gtk4_css_shadow/window.ui')
class Gtk4CssShadowWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'Gtk4CssShadowWindow'

    paned = Gtk.Template.Child()
    textview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        provider = Gtk.CssProvider()

        text = self.textview.get_buffer()
        text.create_tag("warning", underline = Pango.Underline.SINGLE)
        text.create_tag("error", underline = Pango.Underline.ERROR)
        text.connect("changed", self.css_text_changed, provider)

        byte = Gio.resources_lookup_data("/css_shadows/gtk.css", 0)
        text.set_text(byte.get_data().decode(),byte.get_size())

        provider.connect("parsing-error", self.show_parsing_errors, text)

        apply_css(self,provider)


    def css_text_changed(self, buffer, provider):
        start_iter = buffer.get_start_iter()
        end_iter = buffer.get_end_iter()
        buffer.remove_all_tags(start_iter,end_iter)
        byte = buffer.get_text(start_iter,end_iter, False).encode("utf-8")
        provider.load_from_data(byte)

    def show_parsing_errors(self, provider,section,error,buffer):
        location = section.get_start_location()
        _ , start_iter = buffer.get_iter_at_line_index(location.lines, location.line_bytes)
        location = section.get_end_location()
        _ , end_iter = buffer.get_iter_at_line_index(location.lines, location.line_bytes)
        # Not sure how to get if it is error or warning.
        tag_name = "error"
        buffer.apply_tag_by_name(tag_name, start_iter, end_iter)

class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'gtk4_css_shadow'
        self.props.version = "0.1.0"
        self.props.authors = ['Andras Molnar']
        self.props.copyright = '(C) 2021 Andras Molnar'
        self.props.logo_icon_name = 'com.github.molnarandris.gtk4_css_shadow'
        self.set_transient_for(parent)
