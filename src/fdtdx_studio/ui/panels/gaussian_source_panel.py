from nicegui import ui
from fdtdx_studio.ui.panels.source_panel import SourcePanel

class GaussianSourcePanel(SourcePanel):
  '''Generates UI Configuration of Parameters specific to the Gaussian Plane Source'''

  def __init__(self, view, controller):
        '''
        Initialize GaussianSourcePanel instance.
        
        :param self: Description
        :param view: Reference to the View instance
        :param controller: Reference to the Controller instance
        '''
        
        super().__init__(view, controller)

        # Polarization Vector Widgets (Tuples with 3 instances) Standard None
        self.fixed_E_polarization_vector_1 = None
        self.fixed_E_polarization_vector_2 = None
        self.fixed_E_polarization_vector_3 = None

        self.fixed_H_polarization_vector_1 = None
        self.fixed_H_polarization_vector_2 = None
        self.fixed_H_polarization_vector_3 = None

        # Normalize_by_energy boolean, standard true
        self.normalize_by_energy = None

        #float
        self.radius = None
        # float default 1/3
        self.std = None
        self.button = None

  def render_into(self, panel):
      '''
      Build the UI elements for the Gaussian Source Panel into the panel.
      :param panel: The UI panel to render into
      '''

      super().render_into(panel)
      with panel:
            ui.label('Fixed E Polarization Vector').style('font-size: 14px; padding-bottom: 0px; font-weight: bold;').tooltip("Placeholder")
            with ui.row().style('padding-top: 0px').classes('justify-center'):
                  self.fixed_E_polarization_vector_1 = ui.number('1', validation=self._validate_float).classes('flex-1').props('dense')
                  self.fixed_E_polarization_vector_2 = ui.number('2', validation=self._validate_float).classes('flex-1').props('dense')
                  self.fixed_E_polarization_vector_3 = ui.number('3', validation=self._validate_float).classes('flex-1').props('dense')
      
            # Fixed H Polarization Vector 
            ui.label('Fixed H Polarization Vector').style('font-size: 14px; padding-bottom: 0px; font-weight: bold;').tooltip("Placeholder")
            with ui.row().style('padding-top: 0px').classes('justify-center'):
                  self.fixed_H_polarization_vector_1 = ui.number('1', validation=self._validate_float).classes('flex-1').props('dense')
                  self.fixed_H_polarization_vector_2 = ui.number('2', validation=self._validate_float).classes('flex-1').props('dense')
                  self.fixed_H_polarization_vector_3 = ui.number('3', validation=self._validate_float).classes('flex-1').props('dense')

            # Normalize by energy (boolean)
            ui.label('Normalize by energy').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("If enabled, normalize polarization by energy.")
            with ui.row().style('padding-top: 0px').classes('justify-center'):
                  self.normalize_by_energy = ui.switch(value=True)

            # Radius (float)
            ui.label('Radius').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("Radius of the Gaussian source.")
            with ui.row().style('padding-top: 0px').classes('justify-center'):
                  self.radius = ui.number('', validation=self._validate_float).classes('flex-1').props('dense')

            # Standard deviation (float)
            ui.label('Standard deviation (std)').style('font-size: 14px; padding-bottom: 0px; font-weight: bold; margin-top: 12px;').tooltip("Standard deviation of the Gaussian profile.")
            with ui.row().style('padding-top: 0px').classes('justify-center'):
                  self.std = ui.number('', validation=self._validate_float).classes('flex-1').props('dense')
            
            self.button = ui.button('Apply', on_click= self.on_save_clicked)

  def get_parameters(self):
      '''
      Retrieves the current Gaussian Plane Source parameters from the UI elements.
      :return: Dictionary of gaussian plane source parameters.
      '''
      parameters = super().get_parameters()
      parameters['fixed_E_polarization_vector'] = (self.fixed_E_polarization_vector_1.value,
                                               self.fixed_E_polarization_vector_2.value,
                                               self.fixed_E_polarization_vector_3.value)
      parameters['fixed_H_polarization_vector'] = (self.fixed_H_polarization_vector_1.value,
                                               self.fixed_H_polarization_vector_2.value,
                                               self.fixed_H_polarization_vector_3.value)
      parameters['normalize_by_energy'] = self.normalize_by_energy.value
      parameters['radius'] = self.radius.value
      parameters['std'] = self.std.value
      return parameters
  
  def update_values(self, parameters):
      '''
      Updates the UI elements with the provided parameters.
      :param parameters: Dictionary of gaussian plane source parameters to update the UI with.
      '''

      # First update common parameters
      super().update_values(parameters)
      
      # Update Gaussian Source specific parameters
      # Update Fixed E Polarization Vector
      self.fixed_E_polarization_vector_1.value = parameters.get('fixed_E_polarization_vector', (0,0,0))[0]
      self.fixed_E_polarization_vector_2.value = parameters.get('fixed_E_polarization_vector', (0,0,0))[1]
      self.fixed_E_polarization_vector_3.value = parameters.get('fixed_E_polarization_vector', (0,0,0))[2]

      # Update Fixed H Polarization Vector
      self.fixed_H_polarization_vector_1.value = parameters.get('fixed_H_polarization_vector', (0,0,0))[0]
      self.fixed_H_polarization_vector_2.value = parameters.get('fixed_H_polarization_vector', (0,0,0))[1]
      self.fixed_H_polarization_vector_3.value = parameters.get('fixed_H_polarization_vector', (0,0,0))[2]

      # Update Normalize by energy
      self.normalize_by_energy.value = parameters.get('normalize_by_energy', True)
      # Update Radius and Std
      self.radius.value = parameters.get('radius', 0.0)
      # Default std to 1/3 if not provided
      self.std.value = parameters.get('std', 1/3)

  
  def on_save_clicked(self):
      '''
      Handle save button click event.
      '''
      parameters = self.get_parameters()
      self.controller.saveGaussianPlaneSourceParams(parameters)
      super().on_save_clicked()

  def apply_disable(self):
    self.button.disable()

  def apply_enable(self):
    self.button.enable()

                  
  def _validate_float(self, value):
      """Validation function to check if input is a float."""
      try:
          float(value)
          return None
      except (ValueError, TypeError):
          return 'Input must be a float number like 0.0'
  