from nicegui import ui
from fdtdx_studio.ui.panels.detector_panel import DetectorConfigurationPanel

class ModeOverlapDetectorPanel(DetectorConfigurationPanel):
  '''UI for the mode overlap detector'''
  def __init__(self, view, controller):
    super().__init__(view, controller)
    self.direction = None #['-','+']
    self.plot_dpi = None #int
    self.filter_pol = None # Literal["h", "v"] | None
    self.mode_index = None # int
    self.wave_phase_shift = None
    self.wave_period = None
    self.wave_length = None
    self.wave_frequency = None
    self.wave_button = None
    self.wave_value = None
    self.wave = 'Frequency'  # Default wave type
    self.button = None
    
  def render_into(self, panel):
    super().render_into(panel)
    super().render_specific_parameters(panel)
    with panel:
      with ui.column().classes('w-full gap-2 p-2'):

        self.direction = ui.select(['+', '-'], label='Direction', value = '+').classes('w-3/4')

        ui.label('Plot dpi').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.plot_dpi = ui.number('').classes('w-3/4')

        ui.label('Filter polarization').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.filter_pol = ui.select(['h', 'v'], clearable=True, label='Filter pol').classes('w-3/4')

        ui.label('Node index').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.mode_index = ui.number(value=0, min=0, step=1).classes('w-3/4')

       # Wave Character
        ui.label('Wave Character').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("Wave character parameters.")
        with ui.dropdown_button('Frequency').classes('w-full') as self.wave_button:
          ui.item('Wavelength', on_click=lambda: self.set_wave('Wavelength'))
          ui.item('Period', on_click=lambda: self.set_wave('Period'))
          ui.item('Frequency', on_click=lambda: self.set_wave('Frequency'))
        self.wave_value = ui.number('Frequency Value', value=1.0)
        self.wave_phase_shift = ui.number('Phase Shift', value=0.0)

        self.button = ui.button('Apply', on_click= self.on_save_clicked)

  def set_fixed_propagation_axis(self, fixed_propagation_axis):
      self.fixed_propagation_axis = fixed_propagation_axis
  
  def set_plot_dpi(self, plot_dpi):
      self.plot_dpi = plot_dpi
      
  def set_keep_all_components(self, keep_all_components):
      self.keep_all_components = keep_all_components
      
  def get_parameters(self):
    parameters = super().get_parameters()
    parameters['direction'] = self.direction.value
    parameters['plot_dpi'] = self.plot_dpi.value
    parameters['filter_pol'] = self.filter_pol.value
    parameters['mode_index'] = self.mode_index.value
    # Wave Character parameters
    parameters['wave_characters'] = {
            'phase_shift': self.wave_phase_shift.value,
        }
    match self.wave:
      case 'Frequency':
        parameters['wave_characters']['frequency'] = self.wave_value.value 
      case 'Period':
        parameters['wave_characters']['period'] = self.wave_value.value
      case 'Wavelength':
        parameters['wave_characters']['wavelength'] = self.wave_value.value

    return parameters
  
  def update_values(self, parameters):

      # First update common parameters
      super().update_values(parameters)

      self.direction.value = parameters.get('direction', '+')
      self.plot_dpi.value = parameters.get('plot_dpi', 100)
      self.filter_pol.value = parameters.get('filter_pol', None)
      self.mode_index.value = parameters.get('mode_index', 0)
      if 'wave_character' in parameters:
          wave_char = parameters['wave_character']
          if wave_char.phase_shift is not None:
              self.set_wave_phase_shift(wave_char.phase_shift)
          if wave_char.period is not None:
              self.set_wave('Period')
              self.wave_value.value = wave_char.period
          elif wave_char.wavelength is not None:
              self.set_wave('Wavelength') 
              self.wave_value.value = wave_char.wavelength
          elif wave_char.frequency is not None:
              self.set_wave('Frequency')
              self.wave_value.value = wave_char.frequency
              
  def apply_disable(self):
    self.button.disable()

  def apply_enable(self):
    self.button.enable() 

  def on_save_clicked(self):
    parameters = self.get_parameters()
    self.controller.saveModeOverlapDetectorParams(parameters)
    super().on_save_clicked()
    
  def set_wave(self, wave):
    """Sets the Wave Type and updates the button display."""
    self.wave_value.label = f'{wave} Value'
    self.wave_button.close()
    self.wave = wave
    self.wave_button.text = f'{wave}'
    
  # Wave Character Setters

  def set_wave_phase_shift(self, shift):
        """Update wave phase shift."""
        if self.wave_phase_shift:
          self.wave_phase_shift.value = shift

  def set_wave_period(self, period):
        """Update wave period."""
        if self.wave_period:
          self.wave_period.value = period

  def set_wave_length(self, length):
        """Update wave length."""
        if self.wave_length:
          self.wave_length.value = length

  def set_wave_frequency(self, frequency):
        """Update wave frequency."""
        if self.wave_frequency:
          self.wave_frequency.value = frequency
    