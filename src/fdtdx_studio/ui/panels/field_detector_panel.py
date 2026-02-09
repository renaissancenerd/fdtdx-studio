from nicegui import ui
from fdtdx_studio.ui.panels.detector_panel import DetectorConfigurationPanel
class FieldDetectorPanel(DetectorConfigurationPanel):
  '''UI for the field_detector_panel'''
  def __init__(self, view, controller):
    super().__init__(view, controller)
    self.keep_all_components = False # bool
    self.plot_dpi = None #int
    self.button = None
    self.num_time_steps_recorded = None 
    self.reduce_volume = None
    self.components = ['Ex', 'Ey', 'Ez', 'Hx', 'Hy', 'Hz']
    # UI component selection state
    self.component_enabled = {c: True for c in self.components}
    self._component_buttons = {}
    self.plot = None
    
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
        self.plot = ui.checkbox('Plot')
        self.reduce_volume = ui.checkbox('Reduce volume')
        
        ui.label('Plot dpi').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().style('padding-top: 0px').classes('w-full'):
          self.plot_dpi = ui.number('',).classes('w-3/4')

        
        ui.label('Field Components').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;')
        with ui.row().classes('gap-2'):
          def sync_button(c):
            btn = self._component_buttons.get(c)
            if not btn:
              return
            if self.component_enabled.get(c, False):
              btn.props(remove='outline')
              btn.props('unelevated color=primary')
            else:
              btn.props(remove='unelevated color=primary')
              btn.props('outline')

          for comp in self.components:
            def on_click(c=comp):
              self.component_enabled[c] = not self.component_enabled[c]
              sync_button(c)

            btn = ui.button(comp, on_click=lambda c=comp: on_click(c))
            self._component_buttons[comp] = btn
            sync_button(comp)
            
            
            
        self.button = ui.button('Apply', on_click= self.on_save_clicked)
  
  def set_plot_dpi(self, plot_dpi):
      # keep the UI component and set its value
      if hasattr(self, 'plot_dpi') and self.plot_dpi is not None:
        try:
          self.plot_dpi.value = plot_dpi
        except Exception:
          self.plot_dpi = plot_dpi
      else:
        self.plot_dpi = plot_dpi
  
  def set_keep_all_components(self, keep_all_components):
      self.keep_all_components = keep_all_components

  def get_parameters(self):
    parameters = super().get_parameters()
    #parameters['keep_all_components'] = self.keep_all_components.value
    parameters['plot_dpi'] = self.plot_dpi.value if getattr(self, 'plot_dpi', None) is not None and hasattr(self.plot_dpi, 'value') else (self.plot_dpi if self.plot_dpi is not None else None)
    parameters["num_time_steps_recorded"] = self.num_time_steps_recorded.value if getattr(self, 'num_time_steps_recorded', None) is not None and hasattr(self.num_time_steps_recorded, 'value') else (self.num_time_steps_recorded if self.num_time_steps_recorded is not None else None)
    parameters["reduce_volume"] = self.reduce_volume.value if getattr(self, 'reduce_volume', None) is not None and hasattr(self.reduce_volume, 'value') else (self.reduce_volume if self.reduce_volume is not None else None)
    parameters["plot"] = self.plot.value if getattr(self, 'plot', None) is not None and hasattr(self.plot, 'value') else (self.plot if self.plot is not None else None)
    # include selected components
    parameters['components'] = tuple(
      c for c, enabled in self.component_enabled.items() if enabled
    )
    
    return parameters
  
  def update_values(self, parameters):
      

      # First update common parameters
      super().update_values(parameters)

      
      #self.keep_all_components.value = parameters.get('keep_all_components', False)
      # restore numeric/value fields without replacing UI components
      if getattr(self, 'plot_dpi', None) is not None and hasattr(self.plot_dpi, 'value'):
        self.plot_dpi.value = parameters.get('plot_dpi', 0)
      else:
        self.plot_dpi = parameters.get('plot_dpi', 0)

      if getattr(self, 'plot', None) is not None and hasattr(self.plot, 'value'):
        self.plot.value = bool(parameters.get('plot', False))
      else:
        self.plot = parameters.get('plot', False)

      if getattr(self, 'reduce_volume', None) is not None and hasattr(self.reduce_volume, 'value'):
        self.reduce_volume.value = bool(parameters.get('reduce_volume', False))
      else:
        self.reduce_volume = parameters.get('reduce_volume', False)
      
      # restore component selection if provided
      comps = parameters.get('components')
      if comps is not None:
        # normalize to set for quick lookup
        comps_set = set(comps)
        for c in self.components:
          self.component_enabled[c] = c in comps_set
          # sync button visuals
          btn = self._component_buttons.get(c)
          if btn:
            if self.component_enabled[c]:
              btn.props(remove='outline')
              btn.props('unelevated color=primary')
            else:
              btn.props(remove='unelevated color=primary')
              btn.props('outline')

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
    
    self.controller.saveFieldDetectorParams(parameters)
    super().on_save_clicked()
