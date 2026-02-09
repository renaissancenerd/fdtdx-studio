from nicegui import ui
from fdtdx_studio.ui.panels.detector_panel import DetectorConfigurationPanel

class EnergyDetectorPanel(DetectorConfigurationPanel):
  '''UI for the field_detector_panel'''
  def __init__(self, view, controller):
    super().__init__(view, controller)
    #self.keep_all_components = False # bool
    self.plot_dpi = None #int
    self.button = None
    self.num_time_steps_recorded = None 
    self.reduce_volume = None
    
    self.aggregate = None #String
    self.as_slices = None #bool
    self.x_slice = None #float
    self.y_slice = None #float
    self.z_slice = None #float
    
  def render_into(self, panel):
    super().render_into(panel)
    super().render_specific_parameters(panel)
    with panel:
      with ui.column().classes('w-full gap-2 p-2'):
        '''
        ui.label('Keep all components').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("If enabled, keeps all components")
        with ui.row().style('padding-top: 0px'):
            self.keep_all_components = ui.switch(value=False, on_change=lambda e: self.update_button_state())
        '''
        ui.label('Plot dpi').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.plot_dpi = ui.number('',).classes('w-3/4')

          
        ui.label('As slices').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("If enabled, returns energy measurements as 2D slices through the volume.")
        with ui.row().style('padding-top: 0px'):
          # Note: UI elements no longer call `update_button_state` on change (deprecated).
          self.as_slices = ui.switch(value=False)
          
        ui.label('X slice').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px'):
          self.x_slice = ui.number('', validation=self._validate_float).classes('flex-1').props('dense')
        ui.label('Y slice').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px'):
          self.y_slice = ui.number('', validation=self._validate_float).classes('flex-1').props('dense')
        ui.label('Z slice').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px'):
          self.z_slice = ui.number('', validation=self._validate_float).classes('flex-1').props('dense')

        self.button = ui.button('Apply', on_click= self.on_save_clicked)
  
  def set_plot_dpi(self, plot_dpi):
      self.plot_dpi = plot_dpi
  
  def set_keep_all_components(self, keep_all_components):
      self.keep_all_components = keep_all_components

  def get_parameters(self):
    parameters = super().get_parameters()
    #parameters['keep_all_components'] = self.keep_all_components.value
    parameters['plot_dpi'] = self.plot_dpi.value if self.plot_dpi else None
    parameters["num_time_steps_recorded"] = self.num_time_steps_recorded.value if self.num_time_steps_recorded else None # Not in UI implemented, idk if necessary :D
    parameters["reduce_volume"] = self.reduce_volume.value if self.reduce_volume else None # Not in UI implemented, idk if necessary :D
    parameters['as_slices'] = self.as_slices.value
    parameters['x_slice'] = self.x_slice.value
    parameters['y_slice'] = self.y_slice.value
    parameters['z_slice'] = self.z_slice.value
    
    return parameters
  
  def update_values(self, parameters):
      

      # First update common parameters
      super().update_values(parameters)

      
      #self.keep_all_components.value = parameters.get('keep_all_components', False)
      self.plot_dpi.value = parameters.get('plot_dpi', 0)
      
      self.as_slices.value = parameters.get('as_slices', False)
      self.x_slice.value = parameters.get('x_slice', 0.0)
      self.y_slice.value = parameters.get('y_slice', 0.0)
      self.z_slice.value = parameters.get('z_slice', 0.0)

  '''  def update_button_state(self):
    # delegate to base implementation which triggers validation/update of save button
    if self.button is not None:
      self.button.enabled = super().update_button_state()'''

  def apply_disable(self):
    self.button.disable()

  def apply_enable(self):
    self.button.enable()

  def on_save_clicked(self):
    parameters = self.get_parameters()
    self.controller.saveEnergyDetectorParams(parameters)
    super().on_save_clicked()


