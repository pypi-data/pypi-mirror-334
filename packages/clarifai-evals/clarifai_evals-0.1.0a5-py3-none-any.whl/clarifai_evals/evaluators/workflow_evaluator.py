import time
import requests
import zipfile
import io

from dataclasses import dataclass, field
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc, service_pb2
from clarifai_grpc.grpc.api.resources_pb2 import (
    UserAppIDSet, DatasetVersionExport, InputBatch, Input, Dataset, DatasetInput, WorkflowNode, 
    DatasetVersion, Concept, WorkflowVersionEvaluation, EvaluationMetricValue
)
from clarifai_grpc.grpc.api.status import status_code_pb2
from clarifai_grpc.grpc.api.status.status_pb2 import Status
import logging
from uuid import uuid4
from clarifai_evals.text_eval.text_classification_eval.classification_evaluator import TextClassificationEvaluator
# from clarifai_evals.image_eval.image_detection_eval.detection_evaluator import ImageDetectionEvaluator

logging.basicConfig(level=logging.INFO)

@dataclass
class WorkflowVersionEvaluationParams():
    user_id: str
    app_id: str
    gt_dataset_id: str
    workflow_id: str
    workflow_version_id: str
    workflow_version_evaluation_id: str
    gt_dataset_version_id: str
    pat: str = field(repr=False)
    pred_dataset_id: str | None = None
    pred_dataset_version_id: str | None = None
    target_node_id: str | None = None
    task_type: str | None = None


class WorkflowEvaluator:
    def __init__(self, params: WorkflowVersionEvaluationParams):
        self.params = params
        self.channel = ClarifaiChannel.get_grpc_channel()
        self.stub = service_pb2_grpc.V2Stub(self.channel)
        self.metadata = (("authorization", f"Key {self.params.pat}"),)
        self.user_app_id_set = UserAppIDSet(user_id=self.params.user_id, app_id=self.params.app_id)
        self.gt_exported_data = None
        self.pred_exported_data = None

    def tuples_to_dict(self, tuples):
        return {tuple[0]: tuple[1] for tuple in tuples}

    def find_target_node(self):
        logging.info(f"Setting Target Node (unless already)")
        if self.params.target_node_id is not None:
            return

        workflow_version_request = service_pb2.GetWorkflowVersionRequest(
            user_app_id=self.user_app_id_set,
            workflow_id=self.params.workflow_id,
            workflow_version_id=self.params.workflow_version_id
        )
        workflow_version_response = self.stub.GetWorkflowVersion(workflow_version_request, metadata=self.metadata)
        
        if workflow_version_response.status.code != status_code_pb2.SUCCESS:
            raise Exception (f"Failed to fetch workflow: {workflow_version_response.status.description}")
        else:
            workflow_version = workflow_version_response.workflow_version
            nodes = workflow_version.nodes

            if not self.params.target_node_id:
                nodes_with_inputs = set()
                for node in nodes:
                    for input_node in node.node_inputs:
                        nodes_with_inputs.add(input_node.node_id)
            
                last_nodes = [node for node in nodes if node.id not in nodes_with_inputs]
            
                if last_nodes:
                    self.params.target_node_id = last_nodes[0].id
                    self.target_node = last_nodes[0]
                else:
                    raise Exception (f"No terminal node found to be set as a target node")
            else:
                self.target_node = next((node for node in nodes if node.id == self.params.target_node_id), None)
                if not target_node:
                    raise Exception(f"No node found with id: {self.params.target_node_id}")
        logging.info(f"Target Node is set with id: {self.params.target_node_id} and model-version-id: {self.target_node.model.model_version.id}")
    
    def retry_until_success(self, func, should_retry, max_retry_duration=60, retry_interval=2):
        """Retries a function until success or timeout."""
        start_time = time.time()
        while time.time() - start_time < max_retry_duration:
            result = func()
            if should_retry and not should_retry(result):
                return result
            time.sleep(retry_interval)
        raise TimeoutError(f"{func.__name__} timed out after {max_retry_duration} seconds.")
    
    def export_dataset_version(self, dataset_id, dataset_version_id):
        """Requests dataset version export."""
        logging.info(f"Exporting dataset version: {dataset_version_id} for dataset: {dataset_id}")
        request = service_pb2.PutDatasetVersionExportsRequest(
            user_app_id=self.user_app_id_set,
            dataset_id=dataset_id,
            dataset_version_id=dataset_version_id,
            exports=[DatasetVersionExport(format=1)]
        )
        
        def should_retry(response):
            if response.status.code != status_code_pb2.SUCCESS:
                raise Exception(f"Failed: {response.status.description}")
            return response.exports[0].status.code != status_code_pb2.DATASET_VERSION_EXPORT_SUCCESS
        
        response = self.retry_until_success(lambda: self.stub.PutDatasetVersionExports(request, metadata=self.metadata), should_retry)
        return response.exports[0].url
    
    def download_exported_data(self, url):
        """Downloads the exported dataset."""
        logging.info(f"Downloading exported dataset from: {url}")
        return requests.get(url, headers=self.tuples_to_dict(self.metadata)).content
    
    def extract_zip_data(self, exported_data):
        """Extracts files from the exported ZIP archive as a generator."""
        logging.info("Extracting ZIP archive contents.")
        exported_zip = io.BytesIO(exported_data)
        with zipfile.ZipFile(exported_zip, "r") as zip_ref:
            for name in zip_ref.namelist():
                if "inputbatch" in name:
                    logging.info(f"Extracting batch file: {name}")
                    yield name, zip_ref.read(name)

    def create_pred_dataset_version(self):
        logging.info("Creating Dataset Version for Predictions Dataset")
        dataset_version_request = service_pb2.PostDatasetVersionsRequest(
            user_app_id=self.user_app_id_set,
            dataset_id=self.params.pred_dataset_id,
            dataset_versions=[DatasetVersion(description="Version 1 for Evaluation")]
        )
        dataset_version_response = self.stub.PostDatasetVersions(dataset_version_request, metadata=self.metadata)
        
        if dataset_version_response.status.code == status_code_pb2.SUCCESS:
            dataset_version_id = dataset_version_response.dataset_versions[0].id
            self.params.pred_dataset_version_id = dataset_version_id
            logging.info(f"Dataset Version Created Successfully: {dataset_version_id}")
        else:
            raise Exception(f"Failed to create dataset version: {dataset_version_response.status.description}")

    def get_all_region_concepts(self, gt_data_objs, pred_data_objs):
        available_concepts = set()
        for region in regions:
            region_info = region.region_info.bounding_box
            allpreds.append([region_info.top_row, region_info.left_col, region_info.bottom_row, region_info.right_col, region.data.concepts[0].name, region.data.concepts[0].value])
            cpts.add(region.data.concepts[0].name)

        return 

    def get_concepts(self, gt_data_objs, pred_data_objs):
        available_concepts = set()
        for gt_data_obj in gt_data_objs:
            for concept in gt_data_obj.concepts:
                available_concepts.add((concept.id, concept.name))

        for pred_data_obj in pred_data_objs:
            for concept in pred_data_obj.concepts:
                available_concepts.add((concept.id, concept.name))

        return [Concept(id=tup[0], value=1.0, name=tup[1]) for tup in available_concepts]

    def run_eval_template(self):
        logging.info("Running evaluation template")
        logging.info("Getting Ground Truth Dataset Inputs")
        gt_inputs = self.get_inputs(self.gt_exported_data)

        logging.info("Getting Prediction Dataset Inputs")
        pred_inputs = self.get_inputs(self.pred_exported_data)

        gt_data_objs = [inp.data for inp in gt_inputs]
        pred_data_objs = [inp.data for inp in pred_inputs]
        match self.params.task_type:
            case "TextClassification":  # ToDo: Use enums
                available_concepts = self.get_concepts(gt_data_objs, pred_data_objs)
                evaluator = TextClassificationEvaluator(available_labels=available_concepts)
                response = evaluator.evaluate(prediction_batch=pred_data_objs, ground_truth_batch=gt_data_objs)
            # case "ImageDetection":
            #     available_concepts = self.get_concepts(gt_inputs, pred_inputs)
            #     evaluator = ImageDetectionEvaluator(available_labels=cpts)
            #     response = evaluator.evaluate(prediction_batch=pred_data_objs, ground_truth_batch=gt_data_objs, image_dimensions=[dims])

        return response

    def process_gt_and_create_pred_dataset(self):
        logging.info(f"Processing GT dataset to create Predictions Dataset using results")
        self.get_wf_ver_eval_and_update_params()
        if not (self.params.pred_dataset_id and self.params.pred_dataset_version_id):
            self.patch_wf_ver_eval_status(
                status=Status(code=status_code_pb2.EVALUATION_IN_PROGRESS, details="Evaluation Step 1/2: Processing GT and Creating Pred Dataset")
            )
            self.find_target_node()
            self.create_pred_dataset()
            self.export_gt_dataset()
            self.process_gt_dataset()
            self.create_pred_dataset_version()
            self.patch_wf_ver_eval_status(pred_dataset_id=self.params.pred_dataset_id, pred_dataset_version_id=self.params.pred_dataset_version_id)

    def get_wf_ver_eval_and_update_params(self):
        get_wf_ver_eval_request = service_pb2.GetWorkflowVersionEvaluationRequest(
            user_app_id=self.user_app_id_set,
            workflow_id=self.params.workflow_id,
            workflow_version_id=self.params.workflow_version_id,
            workflow_version_evaluation_id=self.params.workflow_version_evaluation_id
        )

        get_wf_ver_eval_response = self.stub.GetWorkflowVersionEvaluation(get_wf_ver_eval_request, metadata=self.metadata)
        if get_wf_ver_eval_response.status.code == status_code_pb2.SUCCESS:
            logging.info(f"Fetched Workflow Version Evaluation successfully!")
        else:
            raise Exception (f"Failed to Get Workflow Version Evaluation with error: {get_wf_ver_eval_response.status}")

        wf_ver_eval = get_wf_ver_eval_response.workflow_version_evaluation
        if not self.params.pred_dataset_id and wf_ver_eval.predictions_dataset_id:
            self.params.pred_dataset_id = wf_ver_eval.predictions_dataset_id
        if not self.params.pred_dataset_version_id and wf_ver_eval.predictions_dataset_version_id:
            self.params.pred_dataset_version_id = wf_ver_eval.predictions_dataset_version_id
    

    def patch_wf_ver_eval_status(self, status=None, eval_results=None, pred_dataset_id=None, pred_dataset_version_id=None):
        if not (status or eval_results or pred_dataset_id or pred_dataset_version_id):
            raise Exception("No valid attribute provided to Patch WorkflowVersionEvaluation")
        wf_ver_eval = WorkflowVersionEvaluation()
        wf_ver_eval.id=self.params.workflow_version_evaluation_id
        if status:
            wf_ver_eval.status.CopyFrom(status)
        if eval_results:
            wf_ver_eval.workflow_evaluation_result.CopyFrom(eval_results['WorkflowEvaluationResult'][0])
        if pred_dataset_id:
            wf_ver_eval.predictions_dataset_id = pred_dataset_id
        if pred_dataset_version_id:
            wf_ver_eval.predictions_dataset_version_id = pred_dataset_version_id
        patch_wf_ver_eval_request = service_pb2.PatchWorkflowVersionEvaluationsRequest(
            user_app_id=self.user_app_id_set,
            workflow_id=self.params.workflow_id,
            workflow_version_id=self.params.workflow_version_id,
            workflow_version_evaluations = [
                wf_ver_eval
            ]
        )
        patch_wf_ver_eval_response = self.stub.PatchWorkflowVersionEvaluations(patch_wf_ver_eval_request, metadata=self.metadata)
        if patch_wf_ver_eval_response.status.code == status_code_pb2.SUCCESS:
            logging.info(f"Workflow Version Evaluation Patched successfully!")
        else:
            raise Exception (f"Failed to Patch Workflow Version Evaluation with error: {patch_wf_ver_eval_response.status}")

    def submit_eval_results(self, eval_results):
        self.patch_wf_ver_eval_status(status=Status(code=status_code_pb2.EVALUATION_SUCCESS, details="Evaluation Completed"),
                                      eval_results=eval_results)
        logging.info(f"Eval Results submitted successfully!")

    def export_datasets_and_run_evaluations(self):
        logging.info(f"Exporting GT and Pred dataset to run evaluations")
        self.get_wf_ver_eval_and_update_params()
        self.patch_wf_ver_eval_status(
                status=Status(code=status_code_pb2.EVALUATION_IN_PROGRESS, details="Evaluation Step 2/2: Exporting GT and Pred Datasets to run evaluations")
            )
        self.export_gt_dataset()
        self.export_pred_dataset()
        eval_results = self.run_eval_template()
        logging.info(f"Evaluation Results returned from Template: {eval_results['WorkflowEvaluationResult'][0]}")
        self.submit_eval_results(eval_results)

    def evaluate_workflow(self):
        """Main evaluation function."""
        logging.info(f"Starting workflow evaluation with params: {self.params}")
        self.process_gt_and_create_pred_dataset()
        self.export_datasets_and_run_evaluations()
        
        logging.info("Workflow evaluation completed.")
    
    def create_pred_dataset(self):
        """Creates a Predictions Dataset if needed."""
        if self.params.pred_dataset_id is None:
            logging.info("Creating Predictions Dataset.")
            pred_dataset_id = str(uuid4())
            create_dataset_request = service_pb2.PostDatasetsRequest(
                user_app_id=self.user_app_id_set,
                datasets=[Dataset(id=pred_dataset_id)]
            )
            
            dataset_response = self.stub.PostDatasets(create_dataset_request, metadata=self.metadata)
            
            if dataset_response.status.code == status_code_pb2.SUCCESS:
                logging.info(f"Dataset '{pred_dataset_id}' created successfully!")
            else:
                raise Exception (f"Failed to create dataset with name {pred_dataset_id} with error: {dataset_response.status}")
            self.params.pred_dataset_id = pred_dataset_id
        else:
            logging.info(f"Using existing Predictions Dataset: {self.params.pred_dataset_id}")
    
    def export_gt_dataset(self):
        """Handles GT dataset export."""
        if not self.gt_exported_data:
            logging.info("Exporting GT Dataset.")
            gt_export_url = self.export_dataset_version(self.params.gt_dataset_id, self.params.gt_dataset_version_id)
            self.gt_exported_data = self.download_exported_data(gt_export_url)
        else:
            logging.info("Skipping GT Dataset Export as it's already exported.")

    def export_pred_dataset(self):
        """Handles GT dataset export."""
        if not self.pred_exported_data:
            logging.info("Exporting Predictions Dataset.")
            pred_export_url = self.export_dataset_version(self.params.pred_dataset_id, self.params.pred_dataset_version_id)
            self.pred_exported_data = self.download_exported_data(pred_export_url)
        else:
            logging.info("Skipping Predictions Dataset Export as it's already exported")

    def get_inputs(self, exported_data):
        inputs = []
        
        for file_name, content in self.extract_zip_data(exported_data):
            input_batch = InputBatch()
            input_batch.ParseFromString(content)
    
            inputs.extend(input_batch.inputs)

        return inputs
    
    def process_gt_dataset(self, batch_size=32):  # batch size = http.MaxWorkflowPredictInputs, i.e. 32 at the moment
        """Processes GT dataset batch by batch."""
        logging.info("Processing GT dataset batches.")
        
        input_data_batch = []
        
        for file_name, content in self.extract_zip_data(self.gt_exported_data):
            input_batch = InputBatch()
            input_batch.ParseFromString(content)
    
            input_data_batch.extend(input_batch.inputs)
    
            while len(input_data_batch) >= batch_size:
                self.process_inputs(input_data_batch[:batch_size])
                input_data_batch = input_data_batch[batch_size:]
    
        if input_data_batch:
            self.process_inputs(input_data_batch)

    def execute_workflow(self, post_workflow_results_request):
        """Requests dataset version export."""
        logging.info(f"Executing Workflow for the inputs batch of length: {len(post_workflow_results_request.inputs)}")
        
        def should_retry(response):
            return response.status.code == status_code_pb2.MODEL_DEPLOYING
        
        response = self.retry_until_success(lambda: self.stub.PostWorkflowResults(post_workflow_results_request, metadata=self.metadata), should_retry)
        return response

    
    def process_inputs(self, input_data_batch):
        """Processes a single input through the workflow."""
        logging.info(f"Processing inputs of length: {len(input_data_batch)}")
        post_workflow_results_request = service_pb2.PostWorkflowResultsRequest(
            user_app_id=self.user_app_id_set,
            workflow_id=self.params.workflow_id,
            version_id=self.params.workflow_version_id,
            inputs=input_data_batch
        )
        workflow_response = self.execute_workflow(post_workflow_results_request)
        if workflow_response.status.code != status_code_pb2.SUCCESS:
            raise Exception(f"Failed processing batch: {workflow_response.status.description}")

        dataset_inputs = []
        for idx, result in enumerate(workflow_response.results):
            input_id = post_workflow_results_request.inputs[idx].id  # Assuming post_workflow_results_request.inputs maintains input order
            target_node_output = next(
                (output for output in result.outputs
                 if output.model.model_version.id == self.target_node.model.model_version.id),
                None
            )
            if not target_node_output:
                raise Exception(f"Input {idx+1} ({input_id}): No output found for target node {self.params.target_node}")
            dataset_inputs.append(
                DatasetInput(
                    input=Input(id=input_id, data=target_node_output.data)  # Include data from target_node_output
                )
            )

        if dataset_inputs:
            add_to_dataset_request = service_pb2.PostDatasetInputsRequest(
                user_app_id=self.user_app_id_set,
                dataset_id=self.params.pred_dataset_id,
                dataset_inputs=dataset_inputs
            )

            dataset_response = self.stub.PostDatasetInputs(add_to_dataset_request, metadata=self.metadata)

            if dataset_response.status.code == status_code_pb2.SUCCESS:
                logging.info(f"Batch: Successfully added {len(dataset_inputs)} inputs to dataset ✅")
            else:
                raise Exception(f"Batch: Failed to add inputs to dataset - {dataset_response.status.description}")
