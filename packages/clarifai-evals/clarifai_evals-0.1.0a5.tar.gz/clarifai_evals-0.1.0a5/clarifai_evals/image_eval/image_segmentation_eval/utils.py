from collections import defaultdict
from io import BytesIO
from typing import DefaultDict, Dict, List, Tuple, Union

import cv2
import numpy as np
from clarifai_grpc.grpc.api import resources_pb2 as res_pb
from numpy.typing import NDArray
from PIL import Image


def bytes_to_image(bytes_img) -> Image.Image:
  img = Image.open(BytesIO(bytes_img))
  return img


def process_polygon_proto_data(
    annot_proto: Union[res_pb.Output, res_pb.Input],
    inp_dict: Dict[str, Tuple[int, int]]) -> Dict[str, List[DefaultDict[str, List[NDArray]]]]:
  """ Convert and de-normalize Clarifai input/output proto has polygon to dict of {concept: list of polygon sets}

  Args:
    proto (Union[res_pb.Output, res_pb.Input])

  Returns:
    Dict[str, List[DefaultDict[str, List[NDArray]]]]: A dictionary with input id as index to partition the masks by group.

  """
  # Create a common dictionary with input id as index to partition the annotations by group.
  annotations = {keys: [] for keys in inp_dict.keys()}
  for ann in annot_proto:
    inp_annotations = defaultdict(list)
    img_width = inp_dict[ann.input_id][0]
    img_height = inp_dict[ann.input_id][1]

    for reg in ann.data.regions:
      mask = np.zeros((img_height, img_width), dtype=np.uint8)
      # skip region without concept from app base workflow
      if not reg.data.concepts:
        continue
      pols = []

      #Scale the polygon points to the image size
      for point in reg.region_info.polygon.points:
        pol_y = point.col * img_height
        pol_x = point.row * img_width
        pols.append((pol_x, pol_y))
        pts = np.array([pols], dtype=np.int32)

        # Fill the polygon on the mask
        cv2.fillPoly(mask, pts, 1)
        concept = reg.data.concepts[0].name
        inp_annotations[concept].append(mask)

    # Append the annotations to the dictionary
    if inp_annotations:
      annotations[ann.input_id].append(inp_annotations)

  return annotations


def process_mask_proto_data(
    proto: Union[res_pb.Output, res_pb.Input]) -> Dict[str, List[DefaultDict[str, List[NDArray]]]]:
  """ Convert Clarifai input/output proto has mask to dict of {concept: list of masks}
      Args:
        proto (Union[res_pb.Output, res_pb.Input])
      Returns:
        Dict[str, List[DefaultDict[str, List[NDArray]]]]: A dictionary with input id as index to partition the mask by group.
  """
  annotations = {}

  # Iterate over the proto to extract the masks
  # output consists of masks with the image bytes data and the concept name.
  for reg in proto:
    annotations[reg.input.id] = []
    ann = defaultdict(list)
    for label in reg.data.regions:
      concept = label.data.concepts[0].name
      mask = label.region_info.mask.image.base64
      mask = np.asarray(bytes_to_image(mask)) > 0
      mask = mask.astype(dtype="uint8")
      ann[concept].append(mask)
    annotations[reg.input.id].append(ann)

  return annotations


def combine_masks(masks):
  """Utility function to combine a list of masks."""
  combined_mask = np.zeros_like(masks[0], dtype=np.uint8)
  for mask in masks:
    combined_mask = np.logical_or(combined_mask, mask)
  return combined_mask


def process_segmentation_proto(inputs_list: List[res_pb.Input],
                               gt_proto: Union[res_pb.Output, res_pb.Input],
                               pred_proto: Union[res_pb.Output, res_pb.Input]) -> Tuple:

  # Process the proto data to mask formats
  # Process the predictions proto to masked predictions format
  predictions_mask = process_mask_proto_data(pred_proto)

  input_dict = {
      i.id: (i.data.image.image_info.width, i.data.image.image_info.height)
      for i in inputs_list
  }

  #process the ground truth (polygon format) to mask for each inputs
  ground_truth_mask = process_polygon_proto_data(gt_proto, input_dict)

  return ground_truth_mask, predictions_mask
