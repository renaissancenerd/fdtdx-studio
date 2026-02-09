from nicegui import ui


class DetectorDialog:
    """Dialog owner that wraps a BaseDetectorPopup-derived class.

    Usage:
      dialog = DetectorDialog(controller, FieldDetectorPopup)
      dialog.open()

    The dialog creates the UI dialog and instantiates the popup class
    inside the dialog. The popup receives a reference to the owning
    dialog via `popup._dialog_owner` so it can close the dialog only
    at the approved point (`_call_add`).
    """

    def __init__(self, controller, popup_cls):
        self.controller = controller
        self.dialog = None
        self.popup = None

        # Build the dialog and instantiate the popup inside it.
        with ui.dialog() as dlg, ui.card():
            # instantiate popup (UI-only) and render its contents inside
            # the dialog. `build_dialog_inside` expects a parent context
            # manager (the dialog object) and will create the UI there.
            self.popup = popup_cls(controller)
            self.popup.build_dialog_inside(dlg)

        # Keep a reference to the dialog element and expose it to popup
        self.dialog = dlg
        self.popup._dialog_owner = self.dialog

    def open(self):
        if self.dialog is not None:
            self.dialog.open()
