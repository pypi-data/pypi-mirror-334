# Delayed Non-Match-To-Sample task

Delayed Non-Match-To-Sample task is a working memory-dependent variation of a standard IBL Rig decision-making task.

## Description

This package implements a classic working memory-dependent task (Delayed Non-Match-To-Sample task, or DNMS) on the IBL Rig. Its structure inherits from BaseChoiceWorld, notably the BiasedChoiceWorld Session, and has certain functions of the NeuromodulatorChoiceWorld Session. 
DNMS task contains 5 epochs: precue presentation, delay, cue presentation, choice, and outcome.
    1. Precue presentation: a visual stimulus is shown on the screen;
    2. Delay: a gray screen is shown;
    3. Cue presentation: 2 visual stimuli are shown, one of them identical to the precue and another the mirror image of the precue;
    4. Closed loop: the mouse has to choose between the two stimuli. Possible outcomes are correct choice, error, or no-go;
    5. Feedback: the mouse gets a reward if it chooses the correct stimulus, i.e. the one that mismatches the precue;
    6. ITI: the mouse waits for the next trial.

## License

[MIT](https://choosealicense.com/licenses/mit/)