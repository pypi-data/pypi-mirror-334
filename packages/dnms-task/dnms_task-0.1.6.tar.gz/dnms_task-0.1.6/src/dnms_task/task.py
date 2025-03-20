""" DNMS (Delayed Non-Match-To-Sample) task """
import logging
from typing import Any

import numpy as np
from pydantic import NonNegativeFloat

import iblrig.misc
from iblrig.base_choice_world import BiasedChoiceWorldSession, BiasedChoiceWorldTrialData
from iblrig.hardware import SOFTCODE
from pybpodapi.protocol import StateMachine

REWARD_AMOUNTS_UL = (1.5, 3) 
log = logging.getLogger(__name__)

class DNMSTrialData(BiasedChoiceWorldTrialData):
    delay: NonNegativeFloat
    contrast_set: NonNegativeFloat
    omit_feedback: bool
    choice_delay: NonNegativeFloat

class Session(BiasedChoiceWorldSession):
    """
    DNMS Choice World is the ChoiceWorld task engaging working memory processes. It contains several epochs:
    1. Precue presentation: a visual stimulus is shown on the screen
    2. Delay: a gray screen is shown
    3. Cue presentation: 2 visual stimuli are shown, one of them identical to the precue and another the mirror image of the precue
    4. Closed loop: the mouse has to choose between the two stimuli. Possible outcomes are correct choice, error, or no-go.
    5. Feedback: the mouse gets a reward if it chooses the correct stimulus, i.e. the one that mismatches the precue
    6. ITI: the mouse waits for the next trial
    It differs from BaseChoiceWorld in that it implements additional epochs and shows 2 visual stimuli on the screen during choice epoch.
    """
    protocol_name = '_iblrig_tasks_DNMSChoiceWorld'
    TrialDataModel = DNMSTrialData

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw_next_trial_info(self, **kwargs):
        self.trials_table.at[self.trial_num, 'stim_phase'] = self.task_params.STIM_PHASE #if turned off, the phase will be random
        self.trials_table.at[self.trial_num, 'stim_angle'] = self.task_params.STIM_ANGLE_SET[self.trial_num]
        self.trials_table.at[self.trial_num, 'contrast_set'] = self.task_params.CONTRAST_SET[0] #if turned off, the contrast will be random
        super().draw_next_trial_info(
            pleft=0.5,
            contrast=self.trials_table.at[self.trial_num, 'contrast_set'],
            stim_angle = self.trials_table.at[self.trial_num, 'stim_angle'],
            stim_phase=self.trials_table.at[self.trial_num, 'stim_phase'],
            delay = self.trials_table.at[self.trial_num, 'delay']
        )

    def next_trial(self):
        super().next_trial()
        # then there is a probability of omitting feedback regardless of the choice
        self.trials_table.at[self.trial_num, 'omit_feedback'] = np.random.random() < self.task_params.OMIT_FEEDBACK_PROBABILITY

        # setting the delay for the choice
        choice_delay_strategy = 'fixed'
        if choice_delay_strategy == 'binary':  # this is a choice with probabilities 1/3 2/3
            self.trials_table.at[self.trial_num, 'choice_delay'] = np.random.choice([1.5, 3.0], p=[2 / 3, 1 / 3])
        elif choice_delay_strategy == 'uniform':  # uniform probability draw between 1.5s and 3s
            self.trials_table.at[self.trial_num, 'choice_delay'] = np.random.random() * 1.5 + 1.5
        elif choice_delay_strategy == 'binned':  # 5 valures from 0 to 2.5 secs The "Charline Way"
            self.trials_table.at[self.trial_num, 'choice_delay'] = np.random.choice(np.linspace(0, 2.5, 3))
        elif choice_delay_strategy == 'fixed' : # fixed delay
            self.trials_table.at[self.trial_num, 'choice_delay'] = self.task_params.CHOICE_DELAY

        if self.task_params.VARIABLE_REWARDS == True: #doesnt work yet, fixed reward is defined via task_params
            reward_amount = np.random.choice(REWARD_AMOUNTS_UL, p=[0.8, 0.2]) #reward is a draw within an uniform distribution between 3 and 1.5
            self.trials_table.at[self.trial_num, 'reward_amount'] = reward_amount
        else: 
            self.trials_table.at[self.trial_num, 'reward_amount'] = self.task_params.REWARD_AMOUNT_UL
        
        # setting the delay for the delay epoch
        if self.task_params.VARIABLE_DELAY == True:
            self.trials_table.at[self.trial_num, 'delay'] = self.task_params.VARIABLE_DELAY_SET[self.trial_num]
        else: 
            self.trials_table.at[self.trial_num, 'delay'] = self.task_params.FIXED_DELAY

        self.draw_next_trial_info(pleft=0.5)

    @property
    def omit_feedback(self):
        return self.trials_table.at[self.trial_num, 'omit_feedback']

    @property
    def choice_to_feedback_delay(self):
        return self.trials_table.at[self.trial_num, 'choice_delay']
    
    @property
    def delay(self):
        return self.trials_table.at[self.trial_num, 'delay']
    
    def show_trial_log(self, extra_info: dict[str, Any] | None = None, log_level: int = logging.INFO):
        # construct info dict
        trial_info = self.trials_table.iloc[self.trial_num]
        info_dict = {
            'Stim. Angle': trial_info.stim_angle,
            'Variable WM Delay': self.task_params.VARIABLE_DELAY,
            'WM Delay': trial_info.delay
        }

        # update info dict with extra_info dict
        if isinstance(extra_info, dict):
            info_dict.update(extra_info)

        # call parent method
        super().show_trial_log(extra_info=info_dict, log_level=log_level)

    def get_state_machine_trial(self, i):
        sma = StateMachine(self.bpod)

        if i == 0:  # First trial exception start camera
            session_delay_start = self.task_params.get('SESSION_DELAY_START', 0)
            log.info('First trial initializing, will move to next trial only if:')
            log.info('1. camera is detected')
            log.info(f'2. {session_delay_start} sec have elapsed')
            sma.add_state(
                state_name='trial_start',
                state_timer=0,
                state_change_conditions={'Port1In': 'delay_initiation'},
                output_actions=[('SoftCode', SOFTCODE.TRIGGER_CAMERA), ('BNC1', 255)],
            )  # start camera
            sma.add_state(
                state_name='delay_initiation',
                state_timer=session_delay_start,
                output_actions=[],
                state_change_conditions={'Tup': 'reset_rotary_encoder'},
            )
        else:
            sma.add_state(
                state_name='trial_start',
                state_timer=0,  # ~100µs hardware irreducible delay
                state_change_conditions={'Tup': 'reset_rotary_encoder'},
                output_actions=[self.bpod.actions.stop_sound, ('BNC1', 255)],
            )  # stop all sounds

        sma.add_state(
            state_name='reset_rotary_encoder',
            state_timer=0,
            output_actions=[self.bpod.actions.rotary_encoder_reset],
            state_change_conditions={'Tup': 'quiescent_period'},
        )

        sma.add_state(  # '>back' | '>reset_timer'
            state_name='quiescent_period',
            state_timer=self.quiescent_period,
            output_actions=[],
            state_change_conditions={
                'Tup': 'precue_on',
                self.movement_left: 'reset_rotary_encoder',
                self.movement_right: 'reset_rotary_encoder',
            },
        )

        # PRECUE EPOCH
        sma.add_state(
            state_name='precue_on',
            state_timer=self.task_params.PRECUE_PRESENTATION_TIME,
            output_actions=[self.bpod.actions.bonsai_show_center, self.bpod.actions.play_tone, ('BNC1', 255)], #show_center instead of show_stim; for now nothing appears
            state_change_conditions={'Tup': 'interactive_delay', 'BNC1High': 'interactive_delay', 'BNC1Low': 'interactive_delay'},
        )

        sma.add_state(
            state_name='interactive_delay',
            state_timer=self.task_params.INTERACTIVE_DELAY,
            output_actions=[],
            state_change_conditions={'Tup': 'precue_off'},
        )

        sma.add_state(
            state_name='precue_off',
            state_timer=0, #0 instead of 0.1, to try out
            output_actions=[self.bpod.actions.bonsai_hide_stim],
            state_change_conditions={'Tup': 'reset2_rotary_encoder', 'BNC2High': 'reset2_rotary_encoder'},
        )

        sma.add_state(
            state_name='reset2_rotary_encoder',
            state_timer=0.05,
            output_actions=[self.bpod.actions.rotary_encoder_reset],
            state_change_conditions={'Tup': 'delay_on'},
        )

        # DELAY EPOCH
        sma.add_state(
            state_name='delay_on',
            state_timer=self.delay, 
            output_actions=[],
            state_change_conditions={'Tup': 'reset3_rotary_encoder', 'BNC2High': 'reset3_rotary_encoder'},
        )

        sma.add_state(
            state_name='reset3_rotary_encoder',
            state_timer=0,
            output_actions=[self.bpod.actions.rotary_encoder_reset],
            state_change_conditions={'Tup': 'stim_on'},
        )

        # CUE EPOCH
        sma.add_state(
            state_name='stim_on',
            state_timer=self.task_params.CUE_PRESENTATION_TIME,
            output_actions=[self.bpod.actions.bonsai_show_stim],
            state_change_conditions={'Tup': 'interactive_delay2', 'BNC1High': 'interactive_delay2', 'BNC1Low': 'interactive_delay2'},
        )

        sma.add_state(
            state_name='interactive_delay2',
            state_timer=self.task_params.INTERACTIVE_DELAY,
            output_actions=[],
            state_change_conditions={'Tup': 'play_tone3'},
        )

        sma.add_state(
            state_name='play_tone3',
            state_timer=0.1,
            output_actions=[self.bpod.actions.play_tone, ('BNC1', 255)],
            state_change_conditions={'Tup': 'reset4_rotary_encoder', 'BNC2High': 'reset4_rotary_encoder'},
        )

        sma.add_state(
            state_name='reset4_rotary_encoder',
            state_timer=0.05,
            output_actions=[self.bpod.actions.rotary_encoder_reset],
            state_change_conditions={'Tup': 'closed_loop'},
        )

        if self.omit_feedback:
            sma.add_state(
                state_name='closed_loop',
                state_timer=self.task_params.RESPONSE_WINDOW,
                output_actions=[self.bpod.actions.bonsai_closed_loop],
                state_change_conditions={'Tup': 'omit_no_go', self.event_error: 'omit_error', self.event_reward: 'omit_correct'},
            )
        else:
            sma.add_state(
                state_name='closed_loop',
                state_timer=self.task_params.RESPONSE_WINDOW,
                output_actions=[self.bpod.actions.bonsai_closed_loop],
                state_change_conditions={
                    'Tup': 'delay_no_go',
                    self.event_error: 'delay_error',
                    self.event_reward: 'delay_reward',
                },
            )

        # here we create 3 separates states to disambiguate the choice of the mouse
        # in the output data - apart from the name they are exactly the same state
        for state_name in ['omit_error', 'omit_correct', 'omit_no_go']:
            sma.add_state(
                state_name=state_name,
                state_timer=(
                    self.task_params.FEEDBACK_NOGO_DELAY_SECS
                    + self.task_params.FEEDBACK_ERROR_DELAY_SECS
                    + self.task_params.FEEDBACK_CORRECT_DELAY_SECS
                )
                / 3,
                output_actions=[],
                state_change_conditions={'Tup': 'hide_stim'},
            )

        sma.add_state(
            state_name='delay_no_go',
            state_timer=self.choice_to_feedback_delay,
            state_change_conditions={'Tup': 'no_go'},
            output_actions=[],
        )

        sma.add_state(
            state_name='no_go',
            state_timer=self.task_params.FEEDBACK_NOGO_DELAY_SECS,
            output_actions=[self.bpod.actions.bonsai_hide_stim, self.bpod.actions.play_noise],
            state_change_conditions={'Tup': 'exit_state'},
        )

        sma.add_state(
            state_name='delay_error',
            state_timer=self.choice_to_feedback_delay,
            state_change_conditions={'Tup': 'freeze_error'},
            output_actions=[],
        )

        sma.add_state(
            state_name='freeze_error',
            state_timer=0,
            output_actions=[self.bpod.actions.bonsai_freeze_stim],
            state_change_conditions={'Tup': 'error'},
        )

        sma.add_state(
            state_name='error',
            state_timer=self.task_params.FEEDBACK_ERROR_DELAY_SECS,
            output_actions=[self.bpod.actions.play_noise],
            state_change_conditions={'Tup': 'hide_stim'},
        )

        sma.add_state(
            state_name='delay_reward',
            state_timer=self.choice_to_feedback_delay,
            state_change_conditions={'Tup': 'freeze_reward'},
            output_actions=[],
        )

        sma.add_state(
            state_name='freeze_reward',
            state_timer=0,
            output_actions=[self.bpod.actions.bonsai_freeze_stim],
            state_change_conditions={'Tup': 'reward'},
        )

        sma.add_state(
            state_name='reward',
            state_timer=self.reward_time,
            output_actions=[('Valve1', 255)],
            state_change_conditions={'Tup': 'correct'},
        )

        sma.add_state(
            state_name='correct',
            state_timer=self.task_params.FEEDBACK_CORRECT_DELAY_SECS,
            output_actions=[],
            state_change_conditions={'Tup': 'hide_stim'},
        )

        sma.add_state(
            state_name='hide_stim',
            state_timer=0.1,
            output_actions=[self.bpod.actions.bonsai_hide_stim],
            state_change_conditions={'Tup': 'exit_state', 'BNC1High': 'exit_state', 'BNC1Low': 'exit_state'},
        )

        sma.add_state(
            state_name='exit_state', state_timer=0.5, output_actions=[('BNC1', 255)], state_change_conditions={'Tup': 'exit'}
        )
        return sma


class SessionRelatedBlocks(Session):
    """
    In this scenario, the blocks define a poor and a rich side.
    The probability blocks and reward blocks structure is staggered so that we explore all configurations every 4 blocks
    P0 P1 P2 P1 P2 P1 P2 P1 P2
    R0 R1 R1 R2 R2 R1 R1 R2 R2
    """

    # from iblrig_tasks._iblrig_tasks_neuroModulatorChoiceWorld.task import SessionRelatedBlocks
    # sess = SessionRelatedBlocks()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trials_table['omit_feedback'] = np.zeros(self.trials_table.shape[0], dtype=bool)
        self.trials_table['choice_delay'] = np.zeros(self.trials_table.shape[0], dtype=np.float32)
        self.trials_table['probability_left_rich'] = np.zeros(self.trials_table.shape[0], dtype=np.float32)
        self.blocks_table['probability_left_rich'] = np.zeros(self.blocks_table.shape[0], dtype=np.float32)
        self.BLOCK_REWARD_STAGGER = np.random.randint(0, 2)

    def new_block(self):
        super(Session, self).new_block()
        if self.block_num == 0:
            probability_left_rich = 0.5
        elif int((self.block_num + self.BLOCK_REWARD_STAGGER) / 2 % 2):
            probability_left_rich = 0.8
        else:
            probability_left_rich = 0.2
        self.blocks_table.at[self.block_num, 'probability_left_rich'] = probability_left_rich

    def next_trial(self):
        super().next_trial()
        self.trials_table.at[self.trial_num, 'reward_amount'] = self.draw_reward_amount()
        prich = self.blocks_table.loc[self.block_num, 'probability_left_rich']
        self.trials_table.at[self.trial_num, 'probability_left_rich'] = prich

    def draw_reward_amount(self):
        # FIXME check: this has 0.5 probability of being correct !!!
        reward_amounts = (1, 3)  # poor and rich
        plr = self.blocks_table.at[self.block_num, 'probability_left_rich']
        if np.sign(self.position):  # noqa: SIM108
            probas = [plr, (1 - plr)]  # right
        else:
            probas = [(1 - plr), plr]  # left
        return np.random.choice(reward_amounts, p=probas)


if __name__ == '__main__':  # pragma: no cover
    kwargs = iblrig.misc.get_task_arguments(parents=[Session.extra_parser()])
    sess = Session(**kwargs)
    sess.run()
