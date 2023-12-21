# qqt

This project is a PyQt5-based application framework aimed at simplifying threading and callback mechanisms. It streamlines the integration of QML with Python by providing key functionalities.
<br/><br/>
It facilitates data exchange in JSON format between the QML interface and Python backend using dedicated methods and wrappers.

## Overview

The core of this framework revolves around the following components:

### `call_qml`
- **Functionality:** Facilitates communication between Python and QML.
- **Usage:** `call_qml(name, args)`
- **Description:** This method serves as a bridge, allowing seamless invocation of QML functions from Python code. It enables passing arguments to QML functions, enhancing interactivity and data exchange between the two environments. It ensures correct flow of execution using `qqtThreadEscape.escape_thread`.

### `qcallback`
- **Functionality:** Registration mechanism for callbacks.
- **Usage:** `@qcallback`
- **Description:** This function decorator simplifies the registration of callbacks within the framework. By using `@qcallback` above a function definition, it becomes accessible for invocation through various system events or user interactions, providing a structured approach to handle callbacks.

### `qqtThreadWrapper`
- **Functionality:** Managing and orchestrating multiple threads.
- **Usage:** `@qqtThreadWrapper.future`
- **Description:** This class provides a robust mechanism for handling multiple threads within the application. It manages thread creation, execution, and termination. The `@future` decorator simplifies the creation and management of threads, enabling the execution of functions concurrently, enhancing the application's efficiency.

Certainly! To install this framework, follow these steps:

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Krabbens/qqt.git
   ```

2. **Install Dependencies**
   ```bash
   pip install PyQt5 colorama
   ```

### Usage

   ```python
    # Import necessary libraries and modules
    from qqt import qqtApp, qcallback, call_qml, qqtDebug
    from qqt import qqtThreadWrapper as TW
    from time import sleep
    
    # Define a class 'Program' inheriting from 'qqtApp'
    class Program(qqtApp):
        def __init__(self):
            super().__init__()  # Initialize the parent class
        
        # Define a callback function 'on_button_clicked' using a decorator
        @qcallback
        def on_button_clicked(self, button_id):
            qqtDebug()(button_id)  # Debug print the button_id
        
        # Method to set a parameter in QML (Qt Modeling Language)
        def set_parameter_in_qml(self, parameter):
            ### Resource intensive operations here ###
            call_qml("set_parameter", parameter)  # Call QML function with parameter
        
        # Method using qqtThreadWrapper for executing 'set_parameter_in_qml' asynchronously
        @TW.future(target=set_parameter_in_qml)
        def set_parameter_in_qml_thread(self, parameter):
            pass  # Placeholder, actual implementation happens through decorator
        
    # Check if the script is being run as the main program
    if __name__ == "__main__":
        # Instantiate the Program class
        app = Program()
        app.run()  # Run the application
   ```

### Contributing

While these components offer a foundation for communication, they may evolve and benefit from further refinement or adaptation based on your specific project requirements. There's always room for improvement and expansion, and your contributions, feedback, and enhancements are genuinely appreciated.

### License

[MIT](https://github.com/Krabbens/qqt/blob/main/LICENSE)
