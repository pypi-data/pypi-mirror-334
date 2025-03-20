import warnings

class InferenceWarning(UserWarning):
    """
    InferenceWarning is a user-defined warning class that extends the built-in UserWarning class.
    It overrides the __str__ method and provides a custom_showwarning static method.
    """

    def __str__(self):
        """
        Override the __str__ method to return the first argument passed to the warning.
        """
        return str(self.args[0])
    
    @staticmethod
    def custom_showwarning(message, category, *args, **kwargs):
        """
        DESCRIPTION:
            Customizes the display of warnings. If the warning is an instance of InferenceWarning, 
            it prints the warning's class name and message. Otherwise, it defers to the default 
            showwarning method from the warnings module.

        PARAMETERS:
            message: 
                Required Argument.
                Specifies the warning message to be displayed.
                Types: str

            category:
                Required Argument. 
                Specifies the category of the warning, which determines if the custom formatting 
                should be applied or if it should fall back to the default warning display.
                Types: Warning class
        
        RETURNS:
            None
                
        RAISES:
            None            
        """
        # Check if the warning is an instance of InferenceWarning
        if issubclass(category, InferenceWarning):
            # If it is, print the warning's class name and message
            print(f'[{category.__name__}] {message}')
        else:
            # If it's not, call the original showwarning method from the warnings module
            original_showwarning(message, category, *args, **kwargs)