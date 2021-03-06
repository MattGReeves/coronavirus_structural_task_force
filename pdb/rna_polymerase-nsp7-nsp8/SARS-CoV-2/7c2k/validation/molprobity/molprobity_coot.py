# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = []
data['omega'] = [('A', ' 505 ', 'PRO', None, (147.02, 113.64600000000002, 149.44900000000007)), ('B', ' 183 ', 'PRO', None, (119.93900000000004, 113.85400000000001, 150.13200000000006)), ('D', ' 183 ', 'PRO', None, (97.372, 116.503, 177.33800000000005))]
data['rota'] = []
data['cbeta'] = []
data['probe'] = [(' A 312  ASN HD21', ' A 464  CYS  H  ', -0.798, (139.226, 127.256, 118.854)), (' D 147  PHE  HB3', ' D 154  TRP  HB2', -0.772, (93.655, 127.669, 164.052)), (' A 758  LEU HD23', ' A 759  SER  H  ', -0.764, (143.043, 141.338, 139.64)), (' D 162  ALA  HB2', ' D 183  PRO  HD2', -0.762, (97.417, 114.055, 176.593)), (' A 170  ASP  OD2', ' A 173  ARG  NH2', -0.692, (115.008, 124.38, 123.816)), (' A  60  ASP  HB3', ' A  66  ILE HD11', -0.652, (107.734, 124.474, 96.483)), (' A 279  ARG  NH2', ' A 318  SER  OG ', -0.647, (140.843, 114.759, 121.558)), (' A  12  CYS  SG ', ' A  13  GLY  N  ', -0.636, (111.282, 129.774, 83.14)), (' A 576  LEU HD11', ' A 686  THR HG22', -0.622, (152.46, 131.893, 139.104)), (' A 358  ASP  H  ', ' A 534  ASN HD21', -0.616, (159.331, 109.788, 133.262)), (' A 242  MET  HE1', ' A 466  ILE HG22', -0.608, (141.942, 128.238, 112.994)), (' A 416  ASN  HA ', ' A 850  THR HG23', -0.605, (130.334, 141.227, 169.253)), (' A  24  THR HG22', ' A  25  GLY  H  ', -0.6, (110.25, 145.436, 88.751)), (' D 136  ASN  O  ', ' D 140  ASN  ND2', -0.599, (92.91, 130.275, 178.233)), (' A 239  SER  HA ', ' A 242  MET  HE2', -0.589, (140.08, 128.727, 111.528)), (' A 614  LEU  HB2', ' A 802  GLU  HB3', -0.588, (134.837, 156.56, 132.823)), (' A  54  CYS  SG ', ' A  74  ARG  NH2', -0.587, (117.928, 142.844, 87.052)), (' F   5    G  N2 ', ' G  -5    C  O2 ', -0.587, (164.476, 140.992, 160.664)), (' A 225  THR HG22', ' A 226  THR  H  ', -0.587, (148.094, 125.14, 85.505)), (' A 746  TYR  CZ ', ' A 750  ARG  HD2', -0.578, (152.365, 148.622, 124.592)), (' A 755  MET  HG2', ' A 764  VAL HG22', -0.577, (141.325, 148.684, 128.812)), (' A 180  GLU  OE2', ' A 183  ARG  NH1', -0.571, (126.144, 115.01, 108.4)), (' A 116  ARG  HG3', ' A 119  LEU HD11', -0.571, (122.876, 131.936, 93.786)), (' A  57  GLN  HG2', ' A  65  LEU HD12', -0.57, (109.127, 132.802, 97.468)), (' A 540  THR HG23', ' A 665  GLU  HG3', -0.568, (143.466, 119.532, 141.037)), (' A 119  LEU  O  ', ' A 120  THR HG23', -0.568, (119.794, 127.903, 99.673)), (" F   5    G  H2'", ' F   6    U  C6 ', -0.568, (166.142, 142.123, 165.724)), (' D  83  VAL  O  ', ' D  84  THR HG22', -0.567, (127.163, 128.494, 176.372)), (' A  10  ARG  NH2', ' A  10  ARG  O  ', -0.564, (115.967, 132.209, 81.324)), (' B 180  LEU HD13', ' B 184  LEU HD21', -0.563, (115.744, 109.153, 151.624)), (' A 258  ASP  HB2', ' A 263  LYS  HD2', -0.557, (124.677, 103.782, 110.089)), (' A 726  ARG  NH1', ' A 744  GLU  OE2', -0.553, (150.713, 150.486, 109.803)), (' D 132  ILE HG21', ' D 138  TYR  HB2', -0.55, (93.229, 123.789, 174.789)), (' A 601  MET  O  ', ' A 605  VAL HG23', -0.54, (146.246, 154.573, 136.059)), (' A 356  ASN  ND2', ' A 535  VAL  H  ', -0.539, (154.569, 112.488, 132.661)), (' A 109  ASP  N  ', ' A 109  ASP  OD1', -0.538, (120.356, 147.92, 75.101)), (' A  18  ARG  NH1', ' A  60  ASP  O  ', -0.537, (103.55, 126.526, 94.329)), (' D 142  CYS  SG ', ' D 156  ILE HD11', -0.532, (89.99, 125.842, 168.208)), (' A 470  LEU  HA ', ' A 473  VAL HG12', -0.527, (148.489, 134.036, 118.448)), (' A 573  GLN  O  ', ' A 577  LYS  HG2', -0.527, (158.175, 135.759, 142.145)), (' A 356  ASN  HB3', ' A 534  ASN HD22', -0.525, (157.729, 109.798, 133.352)), (' A 388  LEU HD23', ' A 397  SER  HB2', -0.523, (131.607, 110.356, 141.298)), (' D 135  TYR  CZ ', ' D 174  MET  HA ', -0.522, (86.066, 123.91, 180.375)), (" G   1    A  H2'", ' G   2    G  H8 ', -0.517, (141.082, 143.488, 155.867)), (' A 468  GLN  HA ', ' A 731  LEU HD22', -0.516, (143.759, 136.977, 113.861)), (' A 631  ARG  HG2', ' A 663  LEU HD13', -0.513, (143.264, 125.892, 132.054)), (' B 112  ASP  N  ', ' B 112  ASP  OD1', -0.511, (148.835, 98.309, 125.125)), (' A 466  ILE  O  ', ' A 470  LEU  HG ', -0.507, (145.763, 131.953, 114.86)), (' A 238  TYR  O  ', ' A 242  MET  HG3', -0.507, (137.768, 127.597, 110.918)), (' A 341  VAL HG21', ' B 103  LEU HD21', -0.506, (146.217, 98.252, 139.271)), (' D 109  ASN  HB3', ' D 114  CYS  HB2', -0.506, (100.966, 128.823, 173.179)), (' A 468  GLN  NE2', ' A 705  ASN  OD1', -0.504, (138.614, 138.973, 116.528)), (' C  66  VAL HG11', ' C  69  ASN HD22', -0.499, (115.558, 127.934, 182.129)), (' D 122  LEU  H  ', ' D 122  LEU HD23', -0.497, (105.142, 129.803, 155.548)), (' A 388  LEU HD22', ' A 672  SER  HB3', -0.493, (132.587, 110.731, 144.671)), (' A 575  LEU HD13', ' A 641  LYS  HG3', -0.491, (158.291, 136.258, 132.426)), (' D  80  ARG  NH1', " F -18    A  H4'", -0.49, (137.75, 128.918, 169.42)), (" F   5    G  H2'", ' F   6    U  H6 ', -0.488, (166.905, 142.104, 166.022)), (' C  14  LEU HD22', ' C  36  HIS  CG ', -0.484, (120.704, 131.335, 159.09)), (' D 105  ASN HD22', ' D 150  ALA  H  ', -0.483, (100.449, 133.233, 168.028)), (' D 155  GLU  O  ', ' D 157  GLN  NE2', -0.482, (91.118, 123.413, 160.323)), (' A 758  LEU HD23', ' A 759  SER  N  ', -0.481, (143.093, 140.928, 139.256)), (' A  76  THR  OG1', ' A  77  PHE  N  ', -0.478, (131.116, 142.994, 81.411)), (' A 356  ASN HD21', ' A 535  VAL  H  ', -0.476, (153.991, 111.973, 132.807)), (' A 698  GLN  NE2', ' A 789  GLN  OE1', -0.475, (138.471, 135.966, 124.048)), (' B 132  ILE HG21', ' B 138  TYR  HB2', -0.475, (116.637, 108.264, 144.215)), (' A 123  THR HG22', ' A 125  ALA  H  ', -0.475, (127.704, 133.207, 103.824)), (' A 615  MET  HB2', ' A 766  PHE  HE1', -0.474, (134.962, 152.948, 128.395)), (' D 151  SER  O  ', ' D 151  SER  OG ', -0.472, (98.347, 138.014, 163.633)), (' A 502  ALA  HB1', ' A 562  ILE  HB ', -0.47, (151.866, 119.428, 150.562)), (' A 462  THR  OG1', ' A 791  ASN  ND2', -0.47, (132.91, 127.951, 125.144)), (' A 499  ASP  OD2', ' A 513  ARG  NH1', -0.468, (155.198, 127.245, 160.585)), (' B  98  LEU HD11', ' B 103  LEU HD22', -0.467, (143.948, 97.797, 140.915)), (" F   4    C  H2'", ' F   4    C  O2 ', -0.466, (159.584, 140.735, 168.071)), (" F   0    G  H2'", ' F   1    U  H6 ', -0.465, (150.38, 147.768, 157.209)), (' D 114  CYS  HA ', ' D 131  VAL  O  ', -0.465, (100.515, 124.333, 173.71)), (' A  17  ALA  HB1', ' A  58  GLU  HG3', -0.463, (110.39, 127.882, 91.727)), (' A 711  ASP  HB3', ' A 714  LYS  HD2', -0.462, (131.332, 151.701, 106.062)), (' F   4    C  C6 ', " F   4    C H5''", -0.462, (158.571, 144.421, 168.523)), (' A 531  THR HG21', ' A 567  THR HG21', -0.461, (157.217, 119.223, 140.189)), (' A 136  GLU  HG2', ' A 793  PHE  HZ ', -0.46, (121.833, 141.078, 125.539)), (' A 520  SER  OG ', ' A 521  TYR  N  ', -0.459, (168.432, 119.172, 149.902)), (' C  32  CYS  SG ', ' C  58  VAL HG11', -0.458, (115.0, 125.481, 162.303)), (' A 123  THR HG23', ' A 210  GLN  O  ', -0.458, (126.829, 131.772, 101.615)), (' A 312  ASN  O  ', ' A 315  VAL HG12', -0.457, (140.515, 122.721, 119.224)), (' D  64  ASP  O  ', ' D  68  THR HG23', -0.456, (150.362, 144.097, 179.465)), (' A 358  ASP  OD1', ' A 533  ARG  NH1', -0.454, (164.074, 110.44, 132.23)), (' A 572  HIS  O  ', ' A 576  LEU  HG ', -0.453, (155.543, 133.333, 138.997)), (' D 113  GLY  HA3', ' D 133  PRO  HG2', -0.453, (101.771, 124.448, 177.92)), (' A 854  LEU HD22', ' D  72  LYS  HG2', -0.452, (142.466, 140.192, 175.009)), (' A 583  ARG  NH2', ' A 590  GLY  O  ', -0.45, (153.154, 147.175, 144.778)), (' A 268  TRP  CD1', ' A 322  PRO  HD3', -0.45, (134.238, 107.045, 121.88)), (' A 634  ALA  HA ', ' A 693  VAL HG11', -0.449, (147.954, 134.202, 128.916)), (' B 154  TRP  HB3', ' B 188  ALA  HB1', -0.448, (124.757, 97.292, 143.159)), (' A 417  LYS  HD2', ' D  90  MET  HG3', -0.447, (122.814, 140.85, 171.967)), (' A 836  ARG  NH2', ' A 840  ALA  HB2', -0.446, (134.217, 143.676, 156.273)), (' D  80  ARG HH12', " F -18    A  H4'", -0.446, (137.638, 128.684, 169.154)), (" G   1    A  H2'", ' G   2    G  C8 ', -0.445, (141.533, 143.352, 155.425)), (' C  60  LEU HD12', ' D 106  ILE HG22', -0.445, (107.136, 130.814, 170.026)), (' D 173  SER  O  ', ' D 177  SER  OG ', -0.443, (86.233, 120.967, 179.747)), (' A 208  ASP  N  ', ' A 208  ASP  OD1', -0.442, (131.721, 135.201, 101.191)), (' A 715  ILE  O  ', ' A 721  ARG  NH2', -0.441, (138.332, 156.236, 104.487)), (' C  70  LYS  HA ', ' C  70  LYS  HD3', -0.441, (116.433, 133.688, 180.078)), (' A 899  MET  HE3', ' A 906  MET  SD ', -0.439, (147.509, 145.303, 182.03)), (' A 848  VAL HG13', ' D  80  ARG  HE ', -0.439, (136.782, 132.891, 171.863)), (' A  66  ILE HG22', ' A  67  ASP  N  ', -0.438, (112.023, 127.714, 100.329)), (' G   4  F86  C8 ', ' G   4  F86  N2 ', -0.438, (142.295, 138.054, 144.23)), (' A 101  PHE  CD2', ' A 114  ILE HG12', -0.437, (126.87, 133.908, 83.889)), (' B 102  ALA  O  ', ' B 106  ILE HG23', -0.434, (140.147, 93.337, 135.429)), (' D 105  ASN  ND2', ' D 150  ALA  H  ', -0.434, (100.025, 132.994, 168.236)), (' A 303  ASP  N  ', ' A 303  ASP  OD1', -0.433, (156.172, 125.342, 117.568)), (' A 333  ILE HD13', ' A 361  LEU  HG ', -0.432, (156.47, 99.151, 135.844)), (' D 120  ILE HD11', ' D 149  TYR  HE2', -0.432, (103.373, 128.837, 166.269)), (' A 164  ASP  HB3', ' A 167  GLU  O  ', -0.431, (120.323, 132.615, 129.482)), (' A 531  THR HG22', ' A 536  ILE HD12', -0.43, (156.38, 116.582, 138.879)), (' D 159  VAL HG13', ' D 186  VAL HG12', -0.43, (93.165, 119.136, 170.334)), (' A 123  THR HG21', ' A 208  ASP  HA ', -0.429, (127.984, 134.269, 102.002)), (' A 153  ASP  OD1', ' A 154  ASP  N  ', -0.428, (108.604, 130.381, 116.217)), (' D 113  GLY  O  ', ' D 115  VAL HG23', -0.427, (103.878, 124.338, 174.872)), (' C  53  VAL HG13', ' D 106  ILE HD11', -0.424, (105.155, 132.699, 164.939)), (' D 109  ASN  HA ', ' D 109  ASN HD22', -0.422, (100.712, 130.522, 175.444)), (" F   3    U  H2'", " F   4    C  O4'", -0.422, (156.801, 142.584, 169.461)), (' A 305  ARG  NH2', ' A 470  LEU HD13', -0.421, (150.344, 132.728, 114.209)), (' C   2  LYS  O  ', ' C   6  VAL HG13', -0.421, (113.312, 144.036, 162.552)), (" F   0    G  H2'", ' F   1    U  C6 ', -0.42, (150.234, 147.452, 157.608)), (' A 906  MET  HB3', ' A 906  MET  HE2', -0.419, (148.759, 148.914, 182.292)), (' A  35  PHE  HZ ', ' A  50  LYS  HB2', -0.418, (126.035, 141.981, 99.191)), (' B 139  LYS  HB3', ' B 139  LYS  HE2', -0.418, (110.711, 107.874, 139.685)), (' A  10  ARG  HA ', ' A  10  ARG  HD2', -0.417, (113.953, 132.759, 79.686)), (' A  91  LYS  HB3', ' A  91  LYS  HE2', -0.416, (130.191, 121.95, 83.236)), (' A 166  VAL HG13', ' A 458  TYR  CZ ', -0.416, (125.111, 129.4, 134.792)), (' A 136  GLU  HG2', ' A 793  PHE  CZ ', -0.413, (122.191, 140.671, 125.647)), (' A 837  ILE HG21', ' A 866  ALA  HB2', -0.412, (135.425, 151.868, 157.584)), (' B 132  ILE HD11', ' B 142  CYS  SG ', -0.412, (119.983, 104.865, 142.953)), (' A  35  PHE  CZ ', ' A  50  LYS  HB2', -0.411, (126.305, 141.79, 99.483)), (' A 846  ASP  OD1', ' A 848  VAL HG22', -0.41, (137.866, 134.148, 169.061)), (' A 162  TRP  HA ', ' A 168  ASN HD22', -0.409, (116.863, 131.446, 126.295)), (' C   3  MET  HE1', ' C  48  ALA  HB2', -0.409, (112.587, 141.163, 156.483)), (' A 202  VAL HG13', ' A 231  VAL HG13', -0.408, (145.899, 128.27, 93.923)), (' D 181  ALA  C  ', ' D 183  PRO  HD3', -0.408, (96.934, 114.938, 179.025)), (' A 445  ASP  N  ', ' A 445  ASP  OD1', -0.408, (123.2, 124.522, 152.879)), (' C  14  LEU  HA ', ' C  14  LEU HD12', -0.407, (119.611, 129.363, 163.448)), (' A 816  HIS  O  ', ' A 830  PRO  HA ', -0.406, (138.268, 155.177, 146.011)), (' A 414  ASN  HB2', ' A 844  VAL HG23', -0.406, (131.596, 136.991, 165.801)), (' A  98  LYS  O  ', ' A 116  ARG  HA ', -0.405, (122.856, 129.222, 89.3)), (' A 381  HIS  ND1', ' B  94  MET  HE1', -0.405, (145.189, 107.167, 148.383)), (' C  53  VAL HG13', ' D 106  ILE  CD1', -0.403, (105.508, 132.679, 165.074)), (' A 149  TYR  HE2', ' A 212  LEU HD13', -0.402, (120.033, 129.243, 107.325)), (' C   1  SER  OG ', ' C   2  LYS  N  ', -0.401, (114.076, 149.447, 161.336)), (' A 530  TYR  CD1', ' A 536  ILE HD11', -0.401, (157.614, 114.097, 138.824))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
