from nicegui import ui
import fdtdx

class new_pop_up():
  """Superclass for creating new pop-up dialogs for adding simulation components."""

  def __init__(self, controller):
    self.controller = controller
    self.material = self.controller.model.material
    self.input_material = fdtdx.Material()
    self.input_color = '#FF0000'
    self.input_name = None
    self.input_length = None
    self.input_width = None
    self.input_height = None
          

  def build_common_ui(self):
    """Builds the common UI components for the superclass popup."""

    self.input_color = '#FF0000'
    self.input_name = ui.input('Name', value='New Object',on_change= lambda e: self.validate_name(e.value))
    self.name_error = ui.label().style('color: red; font-size: 13px')
    self.name_error.set_visibility(False)

    # Color selection dropdown
    with ui.dropdown_button('Color: Red').classes('w-full') as self.color_show:
      ui.item('Red', on_click=lambda: self.pick_color('#FF0000', 'Red'))
      ui.item('Green', on_click=lambda: self.pick_color('#00FF00', 'Green'))
      ui.item('Blue', on_click=lambda: self.pick_color('#0000FF', 'Blue'))
      ui.item('Orange', on_click=lambda: self.pick_color('#FFA500', 'Orange'))
      ui.item('Purple', on_click=lambda: self.pick_color('#800080', 'Purple'))
      ui.item('Cyan', on_click=lambda: self.pick_color('#00FFFF', 'Cyan'))
      ui.item('Pink', on_click=lambda: self.pick_color('#FFC0CB', 'Pink'))
      ui.item('Yellow', on_click=lambda: self.pick_color('#FFFF00', 'Yellow'))
      ui.item('Gray', on_click=lambda: self.pick_color('#808080', 'Gray'))
      ui.item('Black', on_click=lambda: self.pick_color('#000000', 'Black'))
    
    # Dimension inputs
    ui.label('Unit in m')
    self.input_width = ui.number('x', value=0.000003, step = 0.000001)
    self.input_length = ui.number('y', value=0.000003, step = 0.000001)
    self.input_height = ui.number('z', value=0.000003, step = 0.000001)
    

  def add_button(self, function, label='Save'):
    """Adds a button to the popup with the given function and label."""
    # Callback verzögert ausführen und aktuelle Werte verwenden
    self.save = ui.button('Save',
      on_click=  function
    ).classes('w-full').style('margin-top: 8px;').on_click(lambda: self.controller.ui_update()) 

  def validate_name(self, name:str):
    '''Validates the name to guarantee name is not already in use'''
    if hasattr(self,'save'):
      if self.controller.model.name_is_object_X(name):
        self.name_error.set_text("Objects cannot be named Object_X")
        self.name_error.set_visibility(True)
        self.save.disable()
      else:
        if name != self.controller.model.namecheck(name):
          self.name_error.set_text("This Name is already in use")
          self.name_error.set_visibility(True)
          self.save.disable()
        else:
          self.name_error.set_visibility(False)
          self.save.enable()


  def build_dialog(self):
    """Builds the dialog UI for the popup."""
    with ui.dialog() as self.new_pop_up, ui.card():
      with ui.column():
        self.build_common_ui()
  
  #helper methods for the popup
  def pick_color(self, color, name):
    self.input_color = color
    self.color_show.close()
    self.color_show.text = name

  def choose_material(self, material):
    self.input_material = material

  def open_new_popup(self):
    self.new_pop_up.open()  
  
  def close_self(self):
    # reset popup values
    self.color_show.text = 'Color: Red'
    self.input_color = '#FF0000'
    self.input_length.value = 1
    self.input_width.value = 1
    self.input_height.value = 1
    self.new_pop_up.close()
    ui.timer( 0,lambda: self.controller.ui_update(), once=True)
  