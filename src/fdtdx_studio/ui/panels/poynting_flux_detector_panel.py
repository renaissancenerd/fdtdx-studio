from nicegui import ui
from fdtdx_studio.ui.panels.detector_panel import DetectorConfigurationPanel

#Version 1.1
class PoyntingFluxDetectorPanel(DetectorConfigurationPanel):
  '''UI for the poynting flux detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller)
    self.direction = None #Literal['-','+']
    self.fixed_propagation_axis = None # int
    self.keep_all_components = False # bool
    self.plot_dpi = None #int
    self.button = None

  def render_into(self, panel):
    super().render_into(panel)
    super().render_specific_parameters(panel)
    with panel:
      with ui.column().classes('w-full gap-2 p-2'):

        ui.select(['+', '-'], label='Direction', value = '+').classes('w-3/4')

        ui.label('Fixed propagation axis').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.fixed_propagation_axis = ui.number('').classes('w-3/4')

        ui.label('Keep all components').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("If enabled, keeps all components")
        with ui.row().style('padding-top: 0px'):
            self.keep_all_components = ui.switch(value=False)

        ui.label('Plot dpi').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.polt_dpi = ui.number('').classes('w-3/4')

        self.button = ui.button('Apply', on_click= self.on_save_clicked)

  def set_fixed_propagation_axis(self, fixed_propagation_axis):
      self.fixed_propagation_axis = fixed_propagation_axis

  def set_keep_all_components(self, keep_all_components):
      self.keep_all_components = keep_all_components
  
  def set_plot_dpi(self, plot_dpi):
      self.plot_dpi = plot_dpi
    

  def get_parameters(self):
    parameters = super().get_parameters()
    parameters['direction'] = self.direction.value if self.direction else None
    parameters['fixed_propagation_axis'] = self.fixed_propagation_axis.value if self.fixed_propagation_axis else None
    parameters['keep_all_components'] = self.keep_all_components.value
    parameters['plot_dpi'] = self.plot_dpi.value if self.plot_dpi else None

    return parameters
  
  def update_values(self, parameters):

      # First update common parameters
      super().update_values(parameters)
      if 'direction' in parameters:
          self.set_direction(parameters['direction'])
      self.fixed_propagation_axis.value = parameters.get('fixed_propagation_axis', 0)
      self.keep_all_components.value = parameters.get('keep_all_components', False)
      if 'plot_dpi' in parameters:
        self.set_plot_dpi(parameters.get('plot_dpi', 0))
  
  def apply_disable(self):
    self.button.disable()

  def apply_enable(self):
    self.button.enable()

  def on_save_clicked(self):
    parameters = self.get_parameters()
    self.controller.savePoyntingFluxDetectorParams(parameters)
    super().on_save_clicked()

  def set_direction(self, direction):
        """Update direction dropdown."""
        if self.direction:
          self.direction.set_text(direction)