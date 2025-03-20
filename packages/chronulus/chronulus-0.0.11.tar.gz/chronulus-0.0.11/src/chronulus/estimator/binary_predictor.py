# MIT License
#
# Copyright (c) 2024 Chronulus AI Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import base64
import json
import gzip
import pickle
import time
from datetime import datetime
from typing import Tuple, List, Type, Optional, Union

import requests
from chronulus_core.types.response import QueuePredictionResponse, PredictionBatchGetByIdResponse, EstimatorGetResponse
from chronulus_core.types.requests import EstimatorCreationRequest
from chronulus_core.types.inputs import InputModelInfo, create_model_from_schema

from ..environment import BaseEnv, Env
from ..io import get_object_size_mb
from ..prediction import BinaryPrediction, BinaryPair, BinaryPredictionSet, BetaParams
from ..session import Session
from .base import Estimator, BaseModelSubclass


class BinaryPredictor(Estimator):
    """
   A prediction agent that estimates the probability binary events / outcomes.

   This class handles the creation, queuing, and retrieval of binary event predictions and explanatory notes.

   Parameters
   ----------
   session : Session
       Active session instance for API communication.
   input_type : Type[BaseModelSubclass]
       Pydantic model class that defines the expected input data structure.

   Attributes
   ----------
   estimator_name : str
       Name identifier for the estimator. Set to "BinaryPredictor".
   estimator_version : str
       Version string for the estimator. Set to "1".
   prediction_version : str
       Version string for the prediction. Set to "1".
   estimator_id : str or None
       Unique identifier assigned by the API after creation.

   """

    estimator_name = "BinaryPredictor"
    estimator_version = "1"
    prediction_version = "1"

    def __init__(self, session: Session, input_type: Type[BaseModelSubclass], estimator_id: Optional[str] = None, verbose: bool = True):
        super().__init__(session, input_type)
        self.verbose = verbose
        self.estimator_id = estimator_id
        if self.estimator_id is None:
            self.create()

    def create(self):
        """
        Initialize the agent instance with the API.

        Creates a agent instance on the API side with the specified input schema.
        The schema is serialized before transmission.

        Raises
        ------
        ValueError
            If the API fails to create the estimator or returns an invalid response.
        """

        request_data = EstimatorCreationRequest(
            estimator_name=self.estimator_name,
            session_id=self.session.session_id,
            input_model_info=InputModelInfo(
                validation_schema=self.input_type.model_json_schema(mode="validation"),
                serialization_schema=self.input_type.model_json_schema(mode="serialization"),
            )
        )

        resp = requests.post(
            url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/create",
            headers=self.session.headers,
            json=request_data.model_dump()
        )
        if resp.status_code == 200:
            response_json = resp.json()
            if 'estimator_id' in response_json:
                self.estimator_id = response_json['estimator_id']
                if self.verbose:
                    print(f"Estimator created with estimator_id: {response_json['estimator_id']}")
            else:
                if self.verbose:
                    print(resp.status_code)
                    print(resp.text)
                raise ValueError("There was an error creating the estimator. Please try again.")
        else:
            raise ConnectionError(f"There was an error creating the estimator. Status code: {resp.status_code}. Response: {resp.text}")

    def queue(
            self,
            item: BaseModelSubclass,
            num_experts: int = 2,
            note_length: Tuple[int, int] = (3, 5),
    ):
        """
        Queue a prediction request for processing.

        Parameters
        ----------
        item : BaseModelSubclass
            The input data conforming to the specified input_type schema.
        num_experts : int, optional
            Number of experts to consult for the prediction request. (minimum = 2, default=2)
        note_length : tuple[int, int], optional
            Desired length range (number of sentences) for explanatory notes (min, max), by default (3, 5).

        Returns
        -------
        QueuePredictionResponse
            Response object containing the request status and ID.

        Raises
        ------
        TypeError
            If the provided item doesn't match the expected input_type.
        """

        if not isinstance(item, self.input_type):
            try:
                assert item.model_json_schema(mode='validation') == self.input_type.model_json_schema(mode='validation')
                assert item.model_json_schema(mode='serialization') == self.input_type.model_json_schema(mode='serialization')

            except Exception as e:
                raise TypeError(f"Expect item to be an instance of {self.input_type}, but item has type {type(item)}")

        data = dict(
            estimator_id=self.estimator_id,
            item_data=item.model_dump(),
            num_experts=num_experts,
            note_length=note_length,
        )

        max_size_mb = 35
        data_mb = get_object_size_mb(data)
        if 3.0 < data_mb < max_size_mb :

            get_url_resp = requests.get(
                url=f'{self.session.env.API_URI}/uploads/get-upload-url',
                headers=self.session.headers
            )

            get_url_resp_json = get_url_resp.json()

            # Compress the JSON string
            compressed_data = gzip.compress(json.dumps(data).encode('utf-8'))

            upload_headers = {'Content-Type': 'application/json', 'Content-Encoding': 'gzip'}

            upload_response = requests.put(
                get_url_resp_json.get('url'),
                data=compressed_data,
                headers=upload_headers
            )

            resp = requests.post(
                url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/queue-predict",
                headers=self.session.headers,
                json=dict(upload_id=get_url_resp_json.get('upload_id','')),
            )

        elif data_mb >= max_size_mb:
            return QueuePredictionResponse(
                success=False,
                request_id='',
                message=f'Queuing failed. Input size ({data_mb:5.2f} MB) exceeds {max_size_mb} MB.',
            )
        else:

            resp = requests.post(
                url=f"{self.session.env.API_URI}/estimators/{self.get_route_prefix()}/queue-predict",
                headers=self.session.headers,
                json=data,
            )

        if resp.status_code == 200:
            return QueuePredictionResponse(**resp.json())
        else:
            return QueuePredictionResponse(
                success=False,
                request_id='',
                message=f'Queuing failed with status code {resp.status_code}: {resp.text}',
            )

    def get_request_predictions(self, request_id: str, try_every: int = 3, max_tries: int = 20) -> Union[BinaryPredictionSet, dict, None]:
        """
        Retrieve predictions for a queued request.

        Parameters
        ----------
        request_id : str
            The ID of the queued prediction request.
        try_every : int, optional
            Seconds to wait between retry attempts, by default 3.
        max_tries : int, optional
            Maximum number of retry attempts, by default 20.

        Returns
        -------
        Union[BinaryPredictionSet, dict, None]
            A BinaryPredictionSet containing predictions and explanations from each expert

        Raises
        ------
        Exception
            If the maximum retry limit is exceeded or if an API error occurs.
        """
        return self.get_request_predictions_static(request_id=request_id, try_every=try_every, max_tries=max_tries, env=self.session.env, verbose=self.verbose)


    @staticmethod
    def get_request_predictions_static(request_id: str, try_every: int = 3, max_tries: int = 20, env: Optional[dict] = None, verbose: bool = True) -> Union[BinaryPredictionSet, dict, None]:
        """
        Retrieve predictions for a queued request.

        Parameters
        ----------
        request_id : str
            The ID of the queued prediction request.
        try_every : int, optional
            Seconds to wait between retry attempts, by default 3.
        max_tries : int, optional
            Maximum number of retry attempts, by default 20.

        Returns
        -------
        Union[BinaryPredictionSet, dict, None]
            A BinaryPredictionSet containing predictions and explanations from each expert

        Raises
        ------
        Exception
            If the maximum retry limit is exceeded or if an API error occurs.
        """

        prediction_version = BinaryPredictor.prediction_version
        if isinstance(env, Env):
            base = BaseEnv(**env.model_dump())
        else:
            env = env if env and isinstance(env, dict) else {}
            base = BaseEnv(**env)

        retries = 0

        while retries < max_tries:

            resp = requests.post(
                url=f"{base.env.API_URI}/predictions/{prediction_version}/check-by-request-id",
                headers=base.headers,
                json=dict(request_id=request_id),
            )

            if resp.status_code != 200:
                if verbose:
                    print(resp)
                raise Exception(f"An error occurred. Status code: {resp.status_code}. Response: {resp.text}")

            else:
                response_json = resp.json()

                if response_json['status'] == 'ERROR':
                    return response_json

                if response_json['status'] == 'SUCCESS':
                    if verbose:
                        print(f'{response_json["status"]} - {response_json["message"]} - Fetching predictions.')
                    prediction_ids = response_json.get('prediction_ids', [])
                    return BinaryPredictor.get_predictions_static(prediction_ids, base.env)

                if response_json['status'] in ['PENDING', 'NOT_FOUND', 'QUEUING']:
                    if verbose:
                        print(f'{response_json["status"]} - {response_json["message"]} - Checking again in {try_every} seconds...')
                    time.sleep(try_every)

                retries += 1

        if retries >= max_tries:
            raise Exception(f"Retry limit exceeded max_tries of {max_tries}")

    @staticmethod
    def get_predictions_static(prediction_ids: List[str], env: Optional[dict] = None, verbose: bool = True) -> Optional[BinaryPredictionSet]:
        """
        Static method to retrieve a batch of predictions with prediction_ids.

        Parameters
        ----------
        prediction_ids : List[str]
            A list of prediction ids
        env : dict, optional
            Environment configuration dictionary. If None, default environment will be used.
        verbose : bool, optional
            Print feedback to stdout if True. Default: True

        Returns
        -------
        BinaryPredictionSet or None
            A BinaryPredictionSet containing predictions and explanations from each expert,
            None if the predictions couldn't be retrieved.
        """
        prediction_version = BinaryPredictor.prediction_version
        if isinstance(env, Env):
            base = BaseEnv(**env.model_dump())
        else:
            env = env if env and isinstance(env, dict) else {}
            base = BaseEnv(**env)

        resp = requests.post(
            url=f"{base.env.API_URI}/predictions/{prediction_version}/get-by-prediction-id-batch",
            headers=base.headers,
            json=dict(prediction_ids=prediction_ids),
        )

        if resp.status_code == 200:
            response_json = resp.json()
            pred_response = PredictionBatchGetByIdResponse(**response_json)
            if pred_response.success:
                estimator_responses = pred_response.responses

                prediction = BinaryPredictionSet(
                    predictions=[BinaryPrediction(_id=pid, opinion_set=BinaryPair(**r)) for pid, r in zip(prediction_ids, estimator_responses)],
                    beta_params=BetaParams(**pred_response.meta.get('beta_params')),
                )
                return prediction
            else:
                if verbose:
                    print(f"The prediction could not be retrieved for batch of predictions ids")
                    print(pred_response.message)

        else:
            if verbose:
                print(f"The prediction could not be retrieved for batch of predictions ids")
                print(resp.status_code)
                print(resp.text)

    @staticmethod
    def load_from_saved_estimator(estimator_id: str, env: Optional[dict] = None, verbose: bool = True):

        # get estimator from estimator id
        env = env if env and isinstance(env, dict) else {}
        base = BaseEnv(**env)

        resp = requests.post(
            url=f"{base.env.API_URI}/estimators/{BinaryPredictor.estimator_version}/from-estimator-id",
            headers=base.headers,
            json=dict(estimator_id=estimator_id)
        )

        if resp.status_code != 200:
            raise ValueError(f"Failed to load estimator with status code: {resp.status_code}, {resp.text}")

        try:
            estimator_response = EstimatorGetResponse(**resp.json())
            if estimator_response.success:
                session = Session(**estimator_response.session.model_dump(), env=base.env.model_dump(), verbose=verbose)
                input_type = create_model_from_schema(estimator_response.input_model_info.validation_schema)
                estimator = BinaryPredictor(
                    session=session,
                    input_type=input_type,
                    estimator_id=estimator_response.estimator_id,
                    verbose=verbose
                )

                if verbose:
                    print(f"Estimator retrieved with estimator_id: {estimator_response.estimator_id}")

                return estimator

            else:
                raise ValueError(estimator_response.message)

        except Exception as e:
            raise ValueError(f"Failed to parse estimator response: {resp.text}")

