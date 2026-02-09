from nicegui import ui
from fdtdx_studio.ui.panels.source_panel import SourcePanel

class ModeSourcePanel(SourcePanel):
  ''' Panel for configuring mode source parameters'''
  def __init__(self, view, controller):
    '''
    Initialize ModeSourcePanel instance.
    
    :param view: Reference to the View instance
    :param controller: Reference to the Controller instance
    '''
    super().__init__(view, controller)
    
    self.button = None
    #filter_pol widget Optional[Literal['te', 'tm']] default None
    self.filter_pol = None

    #mode_index widget int default 0
    self.mode_index = None

  def render_into(self, panel):
      '''
      Build the UI elements for the Mode Source Panel into the panel.
      
      :param panel: The UI panel to render into
      '''
      super().render_into(panel)
      with panel:
        ui.label('Filter Pol').style('font-size: 14px; padding-bottom: 0px; font-weight: bold;').tooltip("Which value to filter with")
        # Note: UI elements no longer call `update_button_state` on change (deprecated).
        self.filter_pol = ui.select(options=['te', 'tm', None], value = None).classes('w-3/4')
        ui.label('Mode Index').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("Mode index to be used")
        self.mode_index = ui.number('', value=0, validation=self._validate_float).classes('flex-1').props('dense')

        self.button = ui.button('Apply', on_click= self.on_save_clicked)
  
  
  def get_parameters(self):
    '''
    Get parameters specific to Mode Source Panel
    Returns: dict
    '''
    parameters = super().get_parameters()
    parameters['filter_pol'] = self.filter_pol.value
    parameters['mode_index'] = self.mode_index.value

    return parameters
  
  def apply_disable(self):
    self.button.disable()

  def apply_enable(self):
    self.button.enable()

  def on_save_clicked(self):
    '''
    Handle save button click event.
    '''
    parameters = self.get_parameters()
    self.controller.saveModePlaneSourceParams(parameters)
    super().on_save_clicked()

  def update_values(self, parameters):
    """
    Update the panel's UI elements with the provided parameters.
    
    :param parameters: Dictionary of parameters to update the UI with
    """

    super().update_values(parameters)
    self.filter_pol.value = parameters.get('filter_pol', None)
    self.mode_index.value = parameters.get('mode_index', 0)