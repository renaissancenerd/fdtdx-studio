from nicegui import ui
from fdtdx_studio.ui.panels.object_config_panel import ObjectConfigPanel

class MaterialObjectConfigPanel(ObjectConfigPanel):
  """Creates the material object configuration panel UI visible on the right drawer.
  
  Inherits from ObjectConfigPanel to provide specific controls for material objects.
  """

  def __init__(self, view, controller):
      """Initializes the MaterialObjectConfigPanel with references to the main view and controller."""
      super().__init__(view, controller)
      self.material = None

  def render_into(self, panel):
      """Renders the material object configuration panel into the specified parent UI component."""
      super().render_into(panel)
      # Additional UI elements specific to material objects can be added here
      
      with panel:
        with ui.dropdown_button('Material').classes('w-full') as self.material_show:
          for obj in self.controller.model.material.material_list:
            ui.item(text=obj[0], on_click= lambda material=obj: self.choose_material(material))
          

        with ui.button('Apply').classes('w-full') as self.apply_button:
          self.apply_button.on_click(lambda: (self.controller.saveParams(self.get_parameters()), ui.timer(0, lambda: self.controller.ui_update(), once=True)))

  def get_parameters(self):
     """Retrieves the parameters from the material object configuration panel."""
     parameters = super().get_parameters()
     parameters['material'] = self.material
     
     return parameters
  
  def apply_enable(self):
    self.apply_button.enable()

  def apply_disable(self):
    self.apply_button.disable()
  
  def choose_material(self, obj):
    self.material = obj[1]
    self.material_show.close()
    self.material_show.text = obj[0]
  
  def update_values(self, parameters):
      """Updates the UI elements with the provided parameters."""
      super().update_values(parameters)
      # TODO: Update material-specific UI elements if needed
      self.material_show.text = self.controller.model.material.get_name_from_material(self.material)