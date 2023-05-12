#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from common_flexbe_states.subscriber_state import Ros2SubscriberState
from common_flexbe_states.trigger_service_state import TriggerServiceState
from flexbe_states.check_condition_state import CheckConditionState
from flexbe_states.flexible_calculation_state import FlexibleCalculationState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]
from ariac_msgs.msg import CompetitionState
from ariac_tutorials.robot_commander import RobotCommander, GoalRejectedException
from rclpy.executors import MultiThreadedExecutor
# [/MANUAL_IMPORT]


'''
Created on Fri May 05 2023
@author: Runaround Robotics LLC
'''
class AriacBehaviorSM(Behavior):
	'''
	ARIAC CCS Behavior
	'''


	def __init__(self, node):
		super(AriacBehaviorSM, self).__init__()
		self.name = 'Ariac Behavior'

		# parameters of this behavior

		# references to used behaviors
		OperatableStateMachine.initialize_ros(node)
		ConcurrencyContainer.initialize_ros(node)
		PriorityContainer.initialize_ros(node)
		Logger.initialize(node)
		CheckConditionState.initialize_ros(node)
		FlexibleCalculationState.initialize_ros(node)
		Ros2SubscriberState.initialize_ros(node)
		TriggerServiceState.initialize_ros(node)
		WaitState.initialize_ros(node)

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		# self._commander = RobotCommander()
		# self._executor = MultiThreadedExecutor()

		# self._executor.add_node(self._commander)
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:387 y:434, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		Logger.loginfo('MANUAL_CREATE')
		# [/MANUAL_CREATE]

		# x:281 y:354, x:130 y:365
		_sm_waituntilready_0 = OperatableStateMachine(outcomes=['finished', 'failed'])

		with _sm_waituntilready_0:
			# x:90 y:103
			OperatableStateMachine.add('ReadState',
										Ros2SubscriberState(topic='/ariac/competition_state', msg_type=CompetitionState, blocking=True, clear=False),
										transitions={'received': 'CheckState', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'competition_state'})

			# x:307 y:138
			OperatableStateMachine.add('CheckState',
										CheckConditionState(predicate=lambda x: x.competition_state == CompetitionState.READY),
										transitions={'true': 'finished', 'false': 'ReadState'},
										autonomy={'true': Autonomy.Off, 'false': Autonomy.Off},
										remapping={'input_value': 'competition_state'})



		with _state_machine:
			# x:187 y:97
			OperatableStateMachine.add('WaitUntilReady',
										_sm_waituntilready_0,
										transitions={'finished': 'Wait', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:463 y:224
			OperatableStateMachine.add('InitRobots',
										FlexibleCalculationState(calculation=self._init_robots, input_keys=[]),
										transitions={'done': 'CompleteOrders'},
										autonomy={'done': Autonomy.Off},
										remapping={'output_value': 'output_value'})

			# x:430 y:97
			OperatableStateMachine.add('Wait',
										WaitState(wait_time=600),
										transitions={'done': 'InitRobots'},
										autonomy={'done': Autonomy.Off})

			# x:559 y:314
			OperatableStateMachine.add('CompleteOrders',
										TriggerServiceState(service_topic='/competitor/complete_orders'),
										transitions={'done': 'finished', 'failed': 'failed'},
										autonomy={'done': Autonomy.Off, 'failed': Autonomy.Off})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	# Move robots to home position
	def _init_robots(self):
		# self._commander.get_logger().info("Moving the robots to the home position")
		# self._commander.move_floor_robot(RobotCommander.floor_robot_home_, 2)
		# self._commander.move_ceiling_robot(RobotCommander.ceiling_robot_home_, 4)
		# self._commander.get_logger().info("Waiting for both robots to finish moving..")
	
		# try:
		#	while not self._commander.finished_executing():
		#		self._executor.spin_once()
		# except GoalRejectedException as e:
		#	print(e)
		pass
	# [/MANUAL_FUNC]
