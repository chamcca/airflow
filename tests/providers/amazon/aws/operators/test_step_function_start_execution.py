#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

import unittest
from unittest import mock
from unittest.mock import MagicMock

from airflow.providers.amazon.aws.operators.step_function_start_execution \
    import StepFunctionStartExecutionOperator

TASK_ID = 'step_function_start_execution_task'
STATE_MACHINE_ARN = 'arn:aws:states:us-east-1:000000000000:stateMachine:pseudo-state-machine'
NAME = 'NAME'
INPUT = '{}'
AWS_CONN_ID = 'aws_non_default'
REGION_NAME = 'us-west-2'


class TestStepFunctionStartExecutionOperator(unittest.TestCase):

    def setUp(self):
        self.mock_context = MagicMock()

    def test_init(self):
        # Given / When
        operator = StepFunctionStartExecutionOperator(
            task_id=TASK_ID,
            state_machine_arn=STATE_MACHINE_ARN,
            name=NAME,
            input=INPUT,
            aws_conn_id=AWS_CONN_ID,
            region_name=REGION_NAME
        )

        # Then
        self.assertEqual(TASK_ID, operator.task_id)
        self.assertEqual(STATE_MACHINE_ARN, operator.state_machine_arn)
        self.assertEqual(NAME, operator.name)
        self.assertEqual(INPUT, operator.input)
        self.assertEqual(AWS_CONN_ID, operator.aws_conn_id)
        self.assertEqual(REGION_NAME, operator.region_name)

    @mock.patch('airflow.providers.amazon.aws.operators.step_function_start_execution.StepFunctionHook')
    def test_execute(self, mock_hook):
        # Given
        hook_response = 'arn:aws:states:us-east-1:123456789012:execution:'\
                        'pseudo-state-machine:020f5b16-b1a1-4149-946f-92dd32d97934'

        hook_instance = mock_hook.return_value
        hook_instance.start_execution.return_value = hook_response

        operator = StepFunctionStartExecutionOperator(
            task_id=TASK_ID,
            state_machine_arn=STATE_MACHINE_ARN,
            name=NAME,
            input=INPUT,
            aws_conn_id=AWS_CONN_ID,
            region_name=REGION_NAME
        )

        # When
        result = operator.execute(self.mock_context)

        # Then
        self.assertEqual(hook_response, result)
