import param
import panel as pn
from panel.custom import ReactComponent

class MaterialComponent(ReactComponent):
    """Base class for Material UI components"""

    _importmap = {
        "imports": {
            "@mui/material/": "https://esm.sh/@mui/material@5.14.20/",
            "@emotion/react/": "https://esm.sh/@emotion/react@11.11.1/",
            "@emotion/styled/": "https://esm.sh/@emotion/styled@11.11.0/"
        }
    }


class Stepper(MaterialComponent):
    """Material UI Stepper component with enhanced features"""
    
    active_step = param.Integer(default=0, bounds=(0, None))
    steps = param.List(default=["Step 1", "Step 2", "Step 3"])
    orientation = param.Selector(objects=["horizontal", "vertical"], default="horizontal")
    alternative_label = param.Boolean(default=True)
    
    optional_steps = param.List(default=[], doc="Indices of optional steps")
    error_steps = param.List(default=[], doc="Indices of steps with errors")
    completed_steps = param.List(default=[], doc="Indices of completed steps")
    linear = param.Boolean(default=True, doc="If false, allows clicking directly on steps")
    connector_type = param.Selector(default="normal", objects=["normal", "dashed", "dots", "none"])
    dark_theme = param.Boolean(default=False, doc="Use dark theme for stepper background") # Keep for potential sx overrides
    
    _esm = """
    import StepperMUI from '@mui/material/Stepper';
    import Step from '@mui/material/Step';
    import StepLabel from '@mui/material/StepLabel';
    import StepConnector from '@mui/material/StepConnector';
    import StepButton from '@mui/material/StepButton';
    import Box from '@mui/material/Box';
    import Typography from '@mui/material/Typography';
    // Removed ThemeProvider, createTheme, CssBaseline imports

    export function render({ model }) {
      const [activeStep] = model.useState("active_step");
      const [steps] = model.useState("steps");
      const [orientation] = model.useState("orientation");
      const [alternativeLabel] = model.useState("alternative_label");
      const [optionalSteps] = model.useState("optional_steps");
      const [errorSteps] = model.useState("error_steps");
      const [completedSteps] = model.useState("completed_steps");
      const [linear] = model.useState("linear");
      const [connectorType] = model.useState("connector_type");
      const [darkTheme] = model.useState("dark_theme"); // Still available if needed for specific sx

      // Removed muiTheme creation

      const handleStepClick = (stepIndex) => {
        if (!linear) {
          model.set("active_step", stepIndex);
        }
      };

      const connectorElement = connectorType !== 'none' ? (
        <StepConnector 
          sx={{
            // Minimal sx, rely on MUI defaults based on Step state for colors
            '& .MuiStepConnector-line': {
              borderTopStyle: connectorType === 'dashed' ? 'dashed' : 
                              connectorType === 'dots' ? 'dotted' : 'solid',
            },
          }} 
        />
      ) : null;

      const containerStyle = {
        width: '100%',
        padding: '8px', // Keep some padding for the container
        // backgroundColor is now handled by the global theme (light/dark)
      };

      if (!steps || !Array.isArray(steps) || steps.length === 0) {
        return (
            <Box sx={{ ...containerStyle, border: '1px solid red', padding: '10px' }}>
              Stepper Error: No steps provided.
            </Box>
        );
      }

      return (
        // Removed ThemeProvider and CssBaseline wrapper
        <Box sx={containerStyle}>
          <StepperMUI
            activeStep={activeStep}
            orientation={orientation}
            alternativeLabel={alternativeLabel}
            connector={connectorElement}
          >
            {steps.map((label, index) => {
              const isStepOptional = optionalSteps.includes(index);
              const isStepError = errorSteps.includes(index);
              
              // Determine if the step is completed
              // A step is completed if explicitly in completed_steps OR if it's a previous step in a linear flow and not an error
              let isStepCompleted = completedSteps.includes(index);
              if (linear && index < activeStep && !isStepError) {
                isStepCompleted = true;
              }
              
              const isStepActive = index === activeStep;

              const stepLabelProps = {
                optional: isStepOptional ? (
                  <Typography variant="caption">Optional</Typography>
                ) : null,
                error: isStepError,
                // Let MUI handle icon and label styling based on theme and props (active, completed, error)
              };
              
              const stepComponentProps = {
                key: label + index, // Unique key
                completed: isStepCompleted && !isStepError, // Pass completed state to Step
                active: isStepActive, // Pass active state (MUI uses this for styling)
                // disabled: linear && index > activeStep && !isStepCompleted && !isStepActive, // Basic disabled logic
              };

              if (linear) {
                return (
                  <Step {...stepComponentProps} >
                    <StepLabel {...stepLabelProps}>{label}</StepLabel>
                  </Step>
                );
              } else { // Non-linear
                return (
                  <Step {...stepComponentProps} >
                    <StepButton onClick={() => handleStepClick(index)} /* disabled={stepComponentProps.disabled} */ >
                      <StepLabel {...stepLabelProps}>{label}</StepLabel>
                    </StepButton>
                  </Step>
                );
              }
            })}
          </StepperMUI>
        </Box>
      );
    }
    """
