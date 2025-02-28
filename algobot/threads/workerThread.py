import traceback

from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.
    """
    restore = pyqtSignal()
    started = pyqtSignal()
    finished = pyqtSignal(object)
    error = pyqtSignal(str)


class Worker(QRunnable):
    """
    Worker thread inherited from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """
    def __init__(self, fn, logger=None, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.logger = logger
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """
        try:
            self.signals.started.emit()
            result = self.fn(*self.args, **self.kwargs)
            self.signals.finished.emit(result)
        except Exception as e:
            error_message = traceback.format_exc()
            if self.logger:
                self.logger.critical(error_message)
            else:
                print(error_message)
            self.signals.error.emit(str(e))
        finally:
            self.signals.restore.emit()
