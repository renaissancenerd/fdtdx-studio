from nicegui import ui
from fdtdx_studio.ui.panels.detector_panel import DetectorConfigurationPanel

class PhasorDetectorPanel(DetectorConfigurationPanel):
  '''UI for the phasor detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller)
    self.fixed_propagation_axis = None # int | None
    self.direction = None # Literal["+", "-"] | None
    self.plot_dpi = None #int
    self.components = None # Sequence[FieldComponent] | None
    self.filter_pol = None # Literal["h", "v"] | None
    self.wave_character = None # Literal["standing", "forward", "backward"]
    self.button = None
    
  def render_into(self, panel):
    super().render_into(panel)
    super().render_specific_parameters(panel)
    with panel:
      with ui.column().classes('w-full gap-2 p-2'):

        self.direction = ui.select(['+', '-'], label='Direction', value = None, clearable=True, on_change=lambda e: self.update_button_state()).classes('w-3/4')

        ui.label('Fixed propagation axis').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.fixed_propagation_axis = ui.number('', value=None, on_change=lambda e: self.update_button_state()).props('clearable').classes('w-3/4')

        ui.label('Plot dpi').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.plot_dpi = ui.number('', on_change=lambda e: self.update_button_state()).classes('w-3/4')

        ui.label('Components').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.components = ui.select(['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz'], multiple=True, clearable=True, label='Select components', on_change=lambda e: self.update_button_state()).classes('w-3/4')

        ui.label('Filter polarization').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.filter_pol = ui.select(['h', 'v'], clearable=True, label='Filter pol', on_change=lambda e: self.update_button_state()).classes('w-3/4')

        ui.label('Wave character').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.wave_character = ui.select(['standing', 'forward', 'backward'], value='standing', on_change=lambda e: self.update_button_state()).classes('w-3/4')

        self.button = ui.button('Apply', on_click= self.on_save_clicked)

  def set_fixed_propagation_axis(self, fixed_propagation_axis):
      self.fixed_propagation_axis = fixed_propagation_axis
  
  def set_plot_dpi(self, plot_dpi):
      self.plot_dpi = plot_dpi
      
  def get_parameters(self):
    parameters = super().get_parameters()
    parameters['direction'] = self.direction.value
    parameters['fixed_propagation_axis'] = self.fixed_propagation_axis.value
    parameters['plot_dpi'] = self.plot_dpi.value
    parameters['components'] = self.components.value if self.components.value else None
    parameters['filter_pol'] = self.filter_pol.value
    parameters['wave_character'] = self.wave_character.value

    return parameters
  
  def update_values(self, parameters):

      # First update common parameters
      super().update_values(parameters)

      self.direction.value = parameters.get('direction', None)
      self.fixed_propagation_axis.value = parameters.get('fixed_propagation_axis', None)
      self.plot_dpi.value = parameters.get('plot_dpi', 100)
      components = parameters.get('components', None)
      self.components.value = components if components is not None else []
      self.filter_pol.value = parameters.get('filter_pol', None)
      self.wave_character.value = parameters.get('wave_character', 'standing')

  def update_button_state(self):
    # delegate to base implementation which triggers validation/update of save button
    if self.button is not None:
      self.button.enabled = super().update_button_state()
  
  def apply_disable(self):
    self.button.disable()

  def apply_enable(self):
    self.button.enable()

  def on_save_clicked(self):
    parameters = self.get_parameters()
    self.controller.savePhasorDetectorParams(parameters)
    super().on_save_clicked()