"""Huvudfönster för SensorySafe."""

import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from . import data


class SensorySafeWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title("SensorySafe")
        self.set_default_size(500, 700)

        self.places = data.load_places()
        self.filter_max = {"ljud": 10, "ljus": 10, "traengsel": 10}

        # Huvudlayout
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(box)

        # Headerbar
        header = Adw.HeaderBar()
        box.append(header)

        add_btn = Gtk.Button(icon_name="list-add-symbolic")
        add_btn.set_tooltip_text("Lägg till plats")
        add_btn.connect("clicked", self._on_add_clicked)
        header.pack_start(add_btn)

        filter_btn = Gtk.Button(icon_name="funnel-symbolic")
        filter_btn.set_tooltip_text("Filtrera platser")
        filter_btn.connect("clicked", self._on_filter_clicked)
        header.pack_end(filter_btn)

        # Inforad
        info = Gtk.Label(label="Tryck + för att lägga till en plats. Betyg 1-10 (10 = mest belastande).")
        info.set_wrap(True)
        info.set_margin_start(12)
        info.set_margin_end(12)
        info.set_margin_top(6)
        info.set_margin_bottom(6)
        info.add_css_class("dim-label")
        box.append(info)

        # Scrollbar med platslista
        scroll = Gtk.ScrolledWindow(vexpand=True)
        box.append(scroll)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.listbox.add_css_class("boxed-list")
        self.listbox.set_margin_start(12)
        self.listbox.set_margin_end(12)
        self.listbox.set_margin_top(6)
        self.listbox.set_margin_bottom(12)
        scroll.set_child(self.listbox)

        self._populate_list()

    def _populate_list(self):
        """Fyller listan med platser."""
        # Rensa listan
        while True:
            row = self.listbox.get_row_at_index(0)
            if row is None:
                break
            self.listbox.remove(row)

        for i, place in enumerate(self.places):
            # Filtrera
            if (place["ljud"] > self.filter_max["ljud"] or
                place["ljus"] > self.filter_max["ljus"] or
                place["traengsel"] > self.filter_max["traengsel"]):
                continue

            row = self._create_place_row(place, i)
            self.listbox.append(row)

    def _create_place_row(self, place, index):
        """Skapar en rad för en plats."""
        row = Adw.ActionRow()
        row.set_title(place["namn"])

        overall = data.get_overall_rating(place)
        icon = data.get_sensory_icon(overall)
        subtitle = (
            f"{icon} Snitt: {overall}/10  |  "
            f"Ljud: {place['ljud']}  Ljus: {place['ljus']}  "
            f"Trängsel: {place['traengsel']}"
        )
        row.set_subtitle(subtitle)

        # Varningsikoner
        warnings = []
        if place["ljud"] >= 7:
            warnings.append("Högt ljud!")
        if place["ljus"] >= 7:
            warnings.append("Starkt ljus!")
        if place["traengsel"] >= 7:
            warnings.append("Mycket trångt!")

        if warnings:
            warn_label = Gtk.Label(label=" | ".join(warnings))
            warn_label.add_css_class("error")
            row.add_suffix(warn_label)

        # Detaljknapp
        detail_btn = Gtk.Button(icon_name="go-next-symbolic")
        detail_btn.set_valign(Gtk.Align.CENTER)
        detail_btn.add_css_class("flat")
        detail_btn.connect("clicked", self._on_detail_clicked, index)
        row.add_suffix(detail_btn)

        row.set_activatable_widget(detail_btn)
        return row

    def _on_detail_clicked(self, _btn, index):
        """Visar detaljer för en plats."""
        place = self.places[index]
        dialog = Adw.Dialog()
        dialog.set_title(place["namn"])
        dialog.set_content_width(400)
        dialog.set_content_height(450)

        toolbar_view = Adw.ToolbarView()
        dialog.set_child(toolbar_view)

        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)

        # Ta bort-knapp
        del_btn = Gtk.Button(icon_name="user-trash-symbolic")
        del_btn.add_css_class("destructive-action")
        del_btn.set_tooltip_text("Ta bort plats")
        del_btn.connect("clicked", self._on_delete_place, index, dialog)
        header.pack_end(del_btn)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        toolbar_view.set_content(box)

        # Beskrivning
        desc = Gtk.Label(label=place["beskrivning"])
        desc.set_wrap(True)
        desc.set_xalign(0)
        box.append(desc)

        # Sensoriska nivåer
        for key, label in [("ljud", "Ljud"), ("ljus", "Ljus"), ("traengsel", "Trängsel")]:
            val = place[key]
            level_text = data.get_sensory_level(val)
            icon = data.get_sensory_icon(val)

            level_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            level_box.append(Gtk.Label(label=f"{icon} {label}: {val}/10 ({level_text})"))

            bar = Gtk.LevelBar()
            bar.set_min_value(0)
            bar.set_max_value(10)
            bar.set_value(val)
            bar.set_hexpand(True)
            level_box.append(bar)

            box.append(level_box)

        # Varningar
        warnings = []
        if place["ljud"] >= 7:
            warnings.append("Högt ljud - ta med hörselskydd")
        if place["ljus"] >= 7:
            warnings.append("Starkt ljus - ta med solglasögon")
        if place["traengsel"] >= 7:
            warnings.append("Mycket trångt - besök vid lugnare tider")

        if warnings:
            warn_group = Adw.PreferencesGroup(title="Varningar")
            for w in warnings:
                warn_row = Adw.ActionRow(title=w, icon_name="dialog-warning-symbolic")
                warn_group.add(warn_row)
            box.append(warn_group)

        # Kommentar
        if place.get("kommentar"):
            comment_group = Adw.PreferencesGroup(title="Kommentar")
            comment_label = Gtk.Label(label=place["kommentar"])
            comment_label.set_wrap(True)
            comment_label.set_xalign(0)
            comment_label.set_margin_start(12)
            comment_label.set_margin_end(12)
            comment_label.set_margin_top(8)
            comment_label.set_margin_bottom(8)
            comment_group.add(comment_label)
            box.append(comment_group)

        dialog.present(self)

    def _on_delete_place(self, _btn, index, dialog):
        """Tar bort en plats."""
        del self.places[index]
        data.save_places(self.places)
        self._populate_list()
        dialog.close()

    def _on_add_clicked(self, _btn):
        """Öppnar dialog för att lägga till en ny plats."""
        dialog = Adw.Dialog()
        dialog.set_title("Lägg till plats")
        dialog.set_content_width(400)
        dialog.set_content_height(550)

        toolbar_view = Adw.ToolbarView()
        dialog.set_child(toolbar_view)

        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)

        save_btn = Gtk.Button(label="Spara")
        save_btn.add_css_class("suggested-action")
        header.pack_end(save_btn)

        scroll = Gtk.ScrolledWindow(vexpand=True)
        toolbar_view.set_content(scroll)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        scroll.set_child(box)

        # Namn
        name_group = Adw.PreferencesGroup(title="Platsinfo")
        name_entry = Adw.EntryRow(title="Namn")
        name_group.add(name_entry)
        desc_entry = Adw.EntryRow(title="Beskrivning")
        name_group.add(desc_entry)
        comment_entry = Adw.EntryRow(title="Kommentar / tips")
        name_group.add(comment_entry)
        box.append(name_group)

        # Sensoriska betyg
        sensor_group = Adw.PreferencesGroup(title="Sensorisk betygsättning (1-10)")
        scales = {}
        for key, label in [("ljud", "Ljud"), ("ljus", "Ljus"), ("traengsel", "Trängsel")]:
            scale_row = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            scale_row.set_margin_top(8)

            scale_label = Gtk.Label(label=label, xalign=0)
            scale_row.append(scale_label)

            scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 10, 1)
            scale.set_draw_value(True)
            scale.set_value(5)
            scale.set_hexpand(True)
            for i in range(1, 11):
                scale.add_mark(i, Gtk.PositionType.BOTTOM, str(i) if i % 5 == 0 else None)
            scale_row.append(scale)
            scales[key] = scale

            sensor_group.add(scale_row)

        box.append(sensor_group)

        def on_save(_btn):
            name = name_entry.get_text().strip()
            if not name:
                name_entry.add_css_class("error")
                return

            place = {
                "namn": name,
                "beskrivning": desc_entry.get_text().strip(),
                "ljud": int(scales["ljud"].get_value()),
                "ljus": int(scales["ljus"].get_value()),
                "traengsel": int(scales["traengsel"].get_value()),
                "kommentar": comment_entry.get_text().strip(),
            }
            self.places.append(place)
            data.save_places(self.places)
            self._populate_list()
            dialog.close()

        save_btn.connect("clicked", on_save)
        dialog.present(self)

    def _on_filter_clicked(self, _btn):
        """Öppnar filterdialog."""
        dialog = Adw.Dialog()
        dialog.set_title("Filtrera platser")
        dialog.set_content_width(380)
        dialog.set_content_height(400)

        toolbar_view = Adw.ToolbarView()
        dialog.set_child(toolbar_view)

        header = Adw.HeaderBar()
        toolbar_view.add_top_bar(header)

        reset_btn = Gtk.Button(label="Återställ")
        header.pack_end(reset_btn)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        toolbar_view.set_content(box)

        info = Gtk.Label(label="Visa bara platser med max denna nivå:")
        info.set_wrap(True)
        info.set_xalign(0)
        box.append(info)

        scales = {}
        for key, label in [("ljud", "Max ljud"), ("ljus", "Max ljus"), ("traengsel", "Max trängsel")]:
            scale_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            scale_box.set_margin_top(8)
            scale_box.append(Gtk.Label(label=label, xalign=0))

            scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 10, 1)
            scale.set_draw_value(True)
            scale.set_value(self.filter_max[key])
            scale.set_hexpand(True)
            scale.connect("value-changed", self._on_filter_changed, key)
            scale_box.append(scale)
            scales[key] = scale

            box.append(scale_box)

        def on_reset(_btn):
            for key, scale in scales.items():
                scale.set_value(10)
                self.filter_max[key] = 10
            self._populate_list()

        reset_btn.connect("clicked", on_reset)
        dialog.present(self)

    def _on_filter_changed(self, scale, key):
        """Uppdaterar filter och listan."""
        self.filter_max[key] = int(scale.get_value())
        self._populate_list()
